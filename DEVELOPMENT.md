# Lander Documentation

## Game operation

The following system flow-chart describes the operation of the game on a basic
level; how the different scripts and functions call each other and transfer
data between themselves.

![Flow chart diagram](https://lh3.googleusercontent.com/Brt920IhSKhfOq0ALzMpOdjWwzojpnOxAk6ZETkbvj9oKLR92X5Cm0twrk-qM_8t6-Moiv6MhbvkVqBAk-ACcwVjsmxQN137f6sykkID0ezsnvMF7EHRy-9qc6s7aATYyzP9qsOB77spZ8-_8_P1wInhHZ959kGK9xB4bYSSREITPYfTEkjwOMYOXaZTVC8u19QI4nvlcXN6hHXY_FWvt-f0Ae_CUn-QF69nuuZe9anT24rzzKVcbTw5uqedjXJ2EK0BML6czo6z4ic1E_d5_um3LdpRKE-A1alznFGuU9wd_qxKq5k4RBwVDQ7k_S4c451itgHFdLqFSU4FuiL-9kpt-2q3a113fie0XUnWuxaGYW9j9uXWvN8iucMbkPlIYMEWCEkhqEukA448m_EGkj6cgmkximFANt7fzndqnhUiXZXV2g_yG3aSY8W8wJP6n5b701MIN99OtyCekznl6DZN7UyyxrkGiDVfTVufhN2mBTzyvpDMmWt_h9DYt136va8dL8G9kTNQyLXOnGXZwCGtF5YJ1FyY8hk_HVjbXTfIyK4yqAVToqz0c-Ymhc-fGQP8e5uC=w3201-h1509)

The `play.py` file is only used for enabling PyInstaller to build an executable and is not included in the system flow-chart since it simply calls `launcher.py`.

![Flow chart diagram 2](https://lh6.googleusercontent.com/da7FiC2wBFCRxSYVaON4LQgCd7m0qQYBVwE1m4jovtTTEsctgcg4tuhf9tRSk1RgIY4wZ3MRvzIoMfs=w3201-h1509-rw)

## Adding levels
### Creating resources

First you need to create all of the resources that are required by the level. These are all images, and as such should be stored in the `/resources/images` directory:

- A level background. This should be a `1280x2880` png image file with a unique file name. e.g. `resources/images/moon_long.png`
- A level map. This is the thumbnail in the top right of the display whilst playing, and can simply be the level background (above) rescaled to `128x288`. e.g. `resources/images/moon_map.png`
- A level surface. This should be another `1280x2880` png image file that contains the surface for the planet that you're landing on. It's easiest to make this by taking the level background and removing anything that you don't want the craft to collide with and leaving this as alpha/transparent. e.g. `resources/images/moon_surface.png`

Should you wish to have an introductory video then this should be a `1280x2880` MPEG1 file stored with a unique filename in the `resources/videos` directory. Pygame is very specific about its video files, and the easiest way to ensure that you're meeting its requirements is to take your video and use ffmpeg to convert it to MPEG1. Once ffmpeg has been installed and added to your path this can be done using:

```bash
ffmpeg -i <infile> -vcodec mpeg1video -acodec libmp3lame -intra <outfile.mpg>
```

### Updating code

The code has been designed so that adding levels should be easy; the file `level_template.py` is a copy of `level1.py` with areas of the code that are likely to need updating marked with `#CHANGE_ME` so that they can easily be found (usually using ctrl-f or cmd-f). For example, on line 114 the code that imports the planet surface image looks like:

```python
self.image = pygame.image.load("./resources/images/moon_surface.png").convert_alpha() #CHANGE_ME
      #the image used for the planet surface
```

To make a new level the path to the image file describing the surface of the planet would need to be replaced with the path to the new image, which must be in the `/resources/images` directory.

It should be an easy task to go through this `level_template.py` file  changing where these links point to, and altering values for acceleration due to gravity, air density etc. This file should ultimately be saved in the `/main` directory.

To add a video introduction the same process can be repeated going through the `video_template.py` file; only the filename for the video should need to be changed.

Once these changes have been made it is necessary to update the `launcher.py` script to run these files. Import them at the top with  the other levels/videos, lines 13 and 15 respectively, by using their filename without the `.py` extension. Calling levels is a nested process beginning on line 181.

To add your level simply add another:

```python
if next_level ==  True:
    next_level, level_score = level7.play(screen, clock, difficulty, audio_state)
    high_score += level_score
```

block after the final level, replacing `level7.play()` with the appropriate file name.

To add your video before the level simply add another:

```python
if next_level == True:
    next_level = video6.play(screen, clock)
    functions.fix_music(music_state)
```

block before your level. It should be fairly simple to copy the structure of the file that is already in place, but it is important to ensure that your indentation matches that already present in the file.
