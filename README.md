# timelapse_long_videos
a script to use OpenCV in python to take long videos, and shorten them to drop frames so the video plays faster... then combines them all into one video.

you need to install OpenCV first.. I used "pip3 install opencv-python"

## How to configure:

look for the line in the script that say:<br>
<code>time_lapse_video(input_path, output_path, 150)</code><br>
and change the 150 to 300 for mega warp speed, or 50 to just be much faster than normal, or 10 to be faster than normal. this value describes how many frames the script should drop before it keeps a frame when it's creating a new video.
