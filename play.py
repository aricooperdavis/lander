import sys
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
from main import launcher
launcher.play()
