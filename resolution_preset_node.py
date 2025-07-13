class WanResolutionPresets:
    def __init__(self):
        self.name = "WanResolutionPresets"
        
        # Updated resolution groups ensuring all dimensions are divisible by 64 (matches WanImageToVideoScaler)
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
                "size": (["1080p", "720p", "540p", "480p"],),
                "aspect_ratio": (["21:9", "16:9", "4:3", "1:1"],),
                "orientation": (["landscape", "portrait"],),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "get_resolution"

    CATEGORY = "utils"

    @staticmethod
    def get_note():
        return """Wan2.1 Video Compatibility:
- All output dimensions divisible by 64
- Matches Wan Image-to-Video Scaler presets
- Ensures compatibility with Wan2.1 text-to-video generation"""

    def get_resolution(self, size, aspect_ratio, orientation):
        # Get the available resolutions for the selected size and aspect ratio
        resolutions = self.resolution_groups[size].get(aspect_ratio, [])
        
        if not resolutions:
            raise ValueError(f"No resolutions available for size {size} and aspect ratio {aspect_ratio}")
        
        # Select landscape or portrait version
        if orientation == "landscape":
            resolution = resolutions[0]  # First item is landscape (width > height)
        else:
            resolution = resolutions[-1]  # Last item is portrait (height > width)
        
        width, height = map(int, resolution.split('x'))
        
        # Final verification (should always pass since we're using the same groups as WanImageToVideoScaler)
        if width % 64 != 0 or height % 64 != 0:
            raise ValueError(f"Resolution {width}x{height} is not divisible by 64")
            
        return (width, height)

NODE_CLASS_MAPPINGS = {
    "WanResolutionPresets": WanResolutionPresets
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WanResolutionPresets": "🟦 Wan Video Resolution Presets (Wan2.1 Optimized)"
}