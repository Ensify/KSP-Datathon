from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# ffmpeg_extract_subclip("full.mp4", start_seconds, end_seconds, targetname="cut.mp4")
ffmpeg_extract_subclip("result2.avi", 4, 158, targetname="result_final.avi")