import os
from moviepy.editor import *

images = ['/data/'+x for x in os.listdir('/data')]
video = ImageSequenceClip(images, fps=25)
video.write_gif('/data/result.gif',fps=10)
