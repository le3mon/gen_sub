from subtitle import *

sub = Subtitle()
sub.video_capture('sample3.mp4')
sub.set_video_option('mp4v', 60)
sub.video_writer('output.mp4')
sub.load_subtitles('sample.json')
sub.edit()