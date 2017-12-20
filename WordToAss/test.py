import os
import subprocess
import json

#运行ffprobe进程，将stdout解码为utf-8&转换为JSON 
ffprobeOutput = subprocess.check_output("ffprobe -v quiet -print_format json -show_streams t.mp4").decode("utf-8")
ffprobeOutput = json.loads(ffprobeOutput)
 
#查找高度和宽度
height = ffprobeOutput ['streams'] [0] ['height'] 
width = ffprobeOutput ['streams'] [0] ['width'] 
print(height, width)
print("\n\n\n")
print(ffprobeOutput)
