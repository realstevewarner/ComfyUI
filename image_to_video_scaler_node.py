import numpy as np
import torch
import re
from PIL import Image, ImageOps

class WanImageToVideoScaler:
    def __init__(self):
        self.name = "WanImageToVideoScaler"
        
        # Updated resolution groups ensuring all dimensions are divisible by 64
        self.resolution_groups = {
            "1080p": {
                "21:9": ["2560x1088", "1088x2560"],
                "16:9": ["1920x1088", "1088x1920"],
                "4:3": ["1456x1088", "1088x1456"],  # Adjusted to be divisible by 64
                "1:1": ["1088x1088"]
            },
            "720p": {
                "21:9": ["1728x704", "704x1728"],   # Adjusted width to be divisible by 64
                "16:9": ["1280x704", "704x1280"],
                "4:3": ["960x704", "704x960"],
                "1:1": ["704x704"]
            },
            "540p": {
                "21:9": ["1280x576", "576x1280"],
                "16:9": ["1024x576", "576x1024"],   # Changed from 960x576 to 1024x576
                "4:3": ["768x576", "576x768"],       # Changed from 704x576 to 768x576
                "1:1": ["576x576"]
            },
            "480p": {
                "21:9": ["1152x512", "512x1152"],   # Changed from 1138x512 to 1152x512
                "16:9": ["896x512", "512x896"],      # Changed from 854x512 to 896x512
                "4:3": ["704x512", "512x704"],       # Changed from 640x512 to 704x512
                "1:1": ["512x512"]
            }
        }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "size": (["1080p", "720p", "540p", "480p"],),
                "aspect_ratio": (["auto", "21:9", "16:9", "4:3", "1:1"],),
                "proportion_fix": (["crop", "stretch", "pad"], {
                    "default": "crop",
                }),
            },
            "hidden": {
                "note": "STRING",
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("resized_image", "width", "height")
    FUNCTION = "resize_image"

    CATEGORY = "image/wantools"

    @staticmethod
    def get_note():
        return """Wan2.1 Video Compatibility:
- All output dimensions guaranteed divisible by 64
- Aspect ratios maintained as closely as possible
- Auto mode will always find a valid resolution"""

    def find_best_resolution(self, img_width, img_height, size, aspect_ratio):
        available_resolutions = []
        if aspect_ratio == "auto":
            for ratio_group in self.resolution_groups[size].values():
                available_resolutions.extend(ratio_group)
        else:
            available_resolutions = self.resolution_groups[size].get(aspect_ratio, [])
        
        if not available_resolutions:
            # If no exact match, find closest valid resolution for the aspect ratio
            target_ratio = {
                "21:9": 21/9,
                "16:9": 16/9,
                "4:3": 4/3,
                "1:1": 1
            }.get(aspect_ratio)
            
            if target_ratio:
                # Generate a valid resolution on the fly
                if img_width > img_height:  # Landscape
                    height = {
                        "1080p": 1088,
                        "720p": 704,
                        "540p": 576,
                        "480p": 512
                    }[size]
                    width = int(height * target_ratio)
                    width = ((width + 63) // 64) * 64  # Round to nearest multiple of 64
                else:  # Portrait
                    width = {
                        "1080p": 1088,
                        "720p": 704,
                        "540p": 576,
                        "480p": 512
                    }[size]
                    height = int(width / target_ratio)
                    height = ((height + 63) // 64) * 64  # Round to nearest multiple of 64
                
                return f"{width}x{height}"
            else:
                raise ValueError(f"No compatible resolutions for {size} {aspect_ratio}")
        
        img_ratio = img_width / img_height
        closest_resolution = None
        smallest_diff = float('inf')
        
        for res in available_resolutions:
            w, h = map(int, res.split('x'))
            ratio_diff = abs((w/h) - img_ratio)
            if ratio_diff < smallest_diff:
                smallest_diff = ratio_diff
                closest_resolution = res
        
        return closest_resolution

    def resize_image(self, image, size, aspect_ratio, proportion_fix, note=None):
        i = 255. * image[0].cpu().numpy()
        pil_img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        
        resolution = self.find_best_resolution(pil_img.width, pil_img.height, size, aspect_ratio)
        width, height = map(int, resolution.split('x'))
        
        # Final verification
        if width % 64 != 0 or height % 64 != 0:
            # If we somehow got here, adjust to nearest divisible by 64
            width = ((width + 63) // 64) * 64
            height = ((height + 63) // 64) * 64
        
        if proportion_fix == "stretch":
            resized = pil_img.resize((width, height), Image.LANCZOS)
        elif proportion_fix == "crop":
            resized = ImageOps.fit(pil_img, (width, height), centering=(0.5, 0.5))
        elif proportion_fix == "pad":
            orig_ratio = pil_img.width / pil_img.height
            target_ratio = width / height
            
            if orig_ratio > target_ratio:
                new_w = width
                new_h = int(width / orig_ratio)
            else:
                new_h = height
                new_w = int(height * orig_ratio)
            
            # Ensure padded dimensions are divisible by 64
            new_w = ((new_w + 63) // 64) * 64
            new_h = ((new_h + 63) // 64) * 64
            
            resized = pil_img.resize((new_w, new_h), Image.LANCZOS)
            padded = Image.new("RGB", (width, height), (0, 0, 0))
            offset = ((width - new_w) // 2, (height - new_h) // 2)
            padded.paste(resized, offset)
            resized = padded

        resized_np = np.asarray(resized).astype(np.float32) / 255.0
        resized_tensor = torch.from_numpy(resized_np).unsqueeze(0)
        
        return (resized_tensor, width, height)


NODE_CLASS_MAPPINGS = {
    "WanImageToVideoScaler": WanImageToVideoScaler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WanImageToVideoScaler": "🟦 Wan Image-to-Video Scaler (Wan2.1 Optimized)"
}