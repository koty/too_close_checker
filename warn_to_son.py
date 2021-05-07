import os
import pychromecast
# https://qiita.com/rukihena/items/8af9b8baed49542c033d

CHROMECAST_NAME = os.environ['CHROMECAST_NAME']
DIRECTION_MP3_URL = os.environ['DIRECTION_MP3_URL']

def warn_to_son():
    chromecasts = pychromecast.get_chromecasts()
    google_home = [c for c in chromecasts[0] if CHROMECAST_NAME in c.device.friendly_name][0]
    google_home.wait()
    google_home.media_controller.play_media(DIRECTION_MP3_URL, 'audio/mp3')
    google_home.media_controller.block_until_active()

