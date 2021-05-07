#!/usr/bin/env python
from is_too_close import is_too_close
from warn_to_son import warn_to_son
#import frame_convert2
import freenect
#import numpy as np

latest_rgb = None
latest_depth = None
has_warned = False
keep_running = True

def process_depth(dev, data, timestamp):
    global has_warned
    global latest_depth
    global keep_running
    # raise freenect.Kill

    if has_warned:
        return
    if latest_rgb is None:
        return
    latest_depth = data

    if not is_too_close(latest_rgb, latest_depth):
        return
    
    warn_to_son()
    #has_warned = True
    #np.save('np_depth.npy', latest_depth)
    #np.save('np_rgb.npy', latest_rgb)
    #keep_running = False

def process_rgb(dev, data, timestamp):
    global latest_rgb
    latest_rgb = data

def body(*args):
    if not keep_running:
        raise freenect.Kill


print('Press ESC in window to stop')
freenect.runloop(depth=process_depth,
                 video=process_rgb,
                 body=body)
