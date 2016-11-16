# python-lander
An educational physics game based on the BBC Micro game "Lander".

## Download
The game can be downloaded in an easily digestible package **for Windows**. We would highly recommend [downloading the installer](https://mega.nz/#!Itd0UDIA!9AnbarO9LTiYHQrYUUGtG2MspQ3cki-KJiQTNkSQi6E) as it includes everything that you need to run the game without installing python and a load of different modules. This installer, however, may end up being slightly behind the github source code, so you can also compile it for yourself:

## Install from source
Should you wish to install from the github source (the only option if you want to run this on **Linux**) you will need to install Python and a number of modules. We would recommend `Python 2.7` since, although it has been tested on Python 3, some features (such as highscores) are not available in this version at the moment. We think that the easiest way to get python and all of the packages that you'll require is by installing Anaconda (**Python 2.7**) then running `conda install -c cogsci pygame=1.9.2a0` from a command line. The game can then be run by opening a terminal/command line, navigating to the python-lander folder, and starting the launcher using "python play.py".

### Modules
If you are installing from source and **not** using Anaconda, you will need:

1. A number of modules that usually come packaged with Python:
  * `math`
  * `random`
  * `string`
  * `pickle`
  * `sys`
  * `operator`
  * `subprocess`
  
2. One module that is *not* usually packaged with Python:
  * [`pygame`](http://www.pygame.org/hifi.html)

## Things that we're working on
We're working on many things:
* Mac compatibility
* Online highscores
* Links to online educational material
* Disabling cheating (which is currently possible so that we can skip levels during testing)
