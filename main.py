from subtitle import *
import json

sub = Subtitle()
sub.video_capture('sample3.mp4')
sub.set_option('mp4v', 60)
sub.video_writer('output.mp4')
sub.set_subtitles('sample.json')
sub.edit()