# Blind_test_maker

How to change image:
    - Download image and video (Countdown)
    - Check size of video (scale) and extension of video (extension)
    - Think about duration of image (-t arg)
    - Transform into mp4 or avi : ffmpeg -loop 1 -i input.extension_image -c:v libx264 -t 15 -pix_fmt yuv420p -vf scale=1920:1080 output.extension_video
    - Transform duration of video : ffmpeg -i input_video.extension -c copy -t 00:00:5.0 output_video.extension
    - Merge video and image transformed :
        - (echo file 'output_video.extension' & echo file 'output.extension_video' )>list.txt 
        - ffmpeg -safe 0 -f concat -i list.txt -c copy C:\Users\yourprofile\Downloads\test_avi.mp4
You got the video of Countdown and Image for displaying answer