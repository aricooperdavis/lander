if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
from main.launcher import play
play()
