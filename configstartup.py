from kivy.config import Config
from kivy.utils import platform

# Default window size and position, also used to set minimum window size
if platform == 'macosx':
    window_width = 175
    window_height = 550
else:
    window_width = 222
    window_height = 600

window_top = 100
window_left = 100

Config.set('kivy', 'exit_on_escape', 0)
Config.set('input', 'mouse', 'mouse,disable_multitouch')
