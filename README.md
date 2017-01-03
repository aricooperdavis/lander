# python-lander
An educational physics game based on the BBC Micro game "Lander".

## Download
The game can be downloaded in an easily digestible package **for Windows**. We would highly recommend [downloading the game executable](https://mega.nz/#!8oFQAS6J!btz5GAAcqPAbZmvoGzTROle61vAeZJYnGkT5NoSZL50) as it includes everything that you need to run the game without installing python and a load of different modules. This executable should be considered the tested, functional game, but may end up being slightly behind the github source code, so you can also compile it for yourself for an experimental/development version.

## Install from source
Should you wish to install from the github source (the only option if you want to run this on **Linux** or **Mac OS X**) you will need to install Python and a number of modules. We think that the easiest way to get python and all of the packages that you'll require is by installing Anaconda then running `conda install -c cogsci pygame=1.9.2a0` from a command line. The game can then be run by opening a terminal/command line, navigating to the python-lander folder, and starting the launcher using `python play.py`.

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
We're working on a number of things:
* Mac compatibility (the *code* is now Mac compatible, but finding a `Pygame` library that includes the, now depreciated, `Movie` module is almost impossible)
* Online highscores
* Links to online educational material
* Disabling cheating (which is currently possible so that we can skip levels during testing, but we'll not tell you how!)
* Rewriting the game in [`Processing`](https://processing.org/) for compatibility with other systems and so as not to rely on the heavily outdated `Pygame` module

## Screenshots
![The titlescreen](http://i.imgur.com/81xPhF4.jpg "The titlescreen")

![The controls](http://i.imgur.com/2ijzsWW.jpg "The controls")

![The moon](http://i.imgur.com/AI7M7Gv.png "The moon")

![Io](http://i.imgur.com/hFsNd8u.jpg "Io")

![HD 189733 b](http://i.imgur.com/Na7RsZr.jpg "HD 189733 b")

![The highscores](http://i.imgur.com/eOpysNq.jpg "The highscores")
