from moviepy.editor import *

video = ImageSequenceClip('/data', fps=20)
video.write_gif('/data/result.gif',fps=20)
