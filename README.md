# ComfyUI-stevewarner
Here are a few quality of life nodes for ComfyUI.  

#Image to Scalar Node:

<img width="471" height="269" alt="Image to Scalar" src="https://github.com/user-attachments/assets/771c5ef9-b901-437f-9eb3-1aab6f9233c8" />

This is designed to be used in the Image 2 Video workflows for Wan2.1.  It simplifies the sizing of your starting image into a resolution and aspect ratio that will work great with Wan2.1.  Just plug in your image, choose a resolution from the Size popup menu, set your aspect ratio and your proportion fix method.  The node will scale your image and ensure it's Wan2.1 ready.  

Size Options:

<img width="512" height="296" alt="Size Options" src="https://github.com/user-attachments/assets/459cdfc6-a940-4819-b86a-a1af6ded49cd" />

The most common video sizes are represented here.  480p, 540p, 720p and 1080p.  

Aspect Ration Options:

<img width="473" height="309" alt="Aspect Options" src="https://github.com/user-attachments/assets/659ff507-acaa-43d1-9fee-848af0ecde63" />

This node uses logic to maintain the aspect ratio of your source image, be it portrait or landscape orientation.  Choosing 9:16 is the same as choosing 16:9.  4:3 is the same as choosing 3:4.  Your source aspect ratio (portrait or landscape) determines which will be used.  

The options for the Aspect Ratio are Auto, 16:9, 4:3 and 1:1.  
• Auto will preserve your source image's original aspect ratio and scale it to the desired Size, rounding to the nearest size divisible by 64 to ensure compatibility with Wan2.1.  This will preserve the source image in its entirety, making sure that the sizing works with Wan2.1.  If you just want to scale your image and hit a general size resolution (e.g. 480p), leave this at auto.
• 16:9, 4:3 and 1:1 will scale your image to the respective format.  If your source image wasn't in in the chosen aspect ratio to begin with, the Proportion Fix options will come into play.  For example, if your source image is 16:9 and you choose a 4:3 aspect ratio, the image will be scaled to 4:3, but how it handles the disproportionate aspect ratio is determined by the Proportion Fix settings.

Proportion Fix Options:

<img width="485" height="296" alt="Proportion Options" src="https://github.com/user-attachments/assets/57f4f21e-60b0-4b3f-82d9-b7d230ee902c" />

Proportion Fix only comes into play when your chosen Aspect Ratio is different than the aspect ratio of the source image.  If you leave Aspect Ratio to Auto, the Proportion Fix options aren't used, as your original image's aspect ratio is maintained and the size is simply adjusted to hit the target resolution while maintaining Wan2.1 safe resolutions.  If your source image and target aspect ratio are different, the options here will come into play.  They are Crop, Stretch and Pad.  

• Crop will cut out pixels to achieve the desired aspect ratio.  Cropping happens from the center.  For example, if you have a 16:9 image and choose 4:3 as your aspect ratio, the image will be scaled down first, and then the width will be cropped from the left and right until the desired 4:3 aspect ratio is attained.
• Pad will add black around the image.  This maintains the source image's aspect ratio but handles discrepancies with black pixels.  This is similar to how forced letterboxing was done for early DVDs.
• Stretch.  This will disproportionately scale the image to meet the desired aspect ratio.  By most accounts, you likely won't use this, as setting the auto aspect ratio is preferable.  But I left it here for those that might want disproportionate scaling.

Usage:

<img width="1331" height="527" alt="Usage" src="https://github.com/user-attachments/assets/75a667e1-1a25-4c58-b26f-fac6c61f31e8" />

This node can be plugged into any image generation workflow.  It outputs the scaled image along with the width and height.  If you want to test it out, simply load an image, connect it to the node, and then run a preview node out of the scaler.  You can then play with the various settings to see how it handles different use cases.

#Resolution Preset Node:

<img width="566" height="240" alt="Resolution Preset" src="https://github.com/user-attachments/assets/d844cb7b-a964-4935-ace3-f8a59e512d1c" />

This node is designed to make it easy to choose a video resolution for your Text 2 Video genreations.  It is intended for Wan2.1 video workflows (although it should work fine in any image or video generation workflow).  Just choose a starting size, the appropriate aspect ratio, and the desired orientation (portrait or landscape).  The node will choose the appropriate size image to work with Wan2.1 video generation, meaning the final resolution will be divisible by 64.  

Usage:

<img width="566" height="240" alt="Resolution Preset" src="https://github.com/user-attachments/assets/d69d9c4d-6806-497f-a759-31fd951db08a" />

Just plug this into your workflow and use the width and height outputs to drive the latent image or video generation.  
