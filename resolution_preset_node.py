class WanResolutionPresets:
    def __init__(self):
        self.name = "WanResolutionPresets"
        
        # Resolution groups from WanImageToVideoScaler
        self.resolution_groups = {
            "1080p": {
                "21:9": ["2560x1080", "1080x2560"],
                "16:9": ["1920x1080", "1080x1920"],
                "4:3": ["1440x1080", "1080x1440"],
                "1:1": ["1080x1080"]
            },
            "720p": {
                "21:9": ["1706x720", "720x1706"],
                "16:9": ["1280x720", "720x1280"],
                "4:3": ["960x720", "720x960"],
                "1:1": ["720x720"]
            },
            "540p": {
                "21:9": ["1280x540", "540x1280"],
                "16:9": ["960x540", "540x960"],
                "4:3": ["720x540", "540x720"],
                "1:1": ["540x540"]
            },
            "480p": {
                "21:9": ["1138x480", "480x1138"],
                "16:9": ["854x480", "480x854"],
                "4:3": ["640x480", "480x640"],
                "1:1": ["480x480"]
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
        return (width, height)

NODE_CLASS_MAPPINGS = {
    "WanResolutionPresets": WanResolutionPresets
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WanResolutionPresets": "🟦 Wan Video Resolution Presets"
}