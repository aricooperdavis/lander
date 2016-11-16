#!/usr/bin/python
#The above is a shebang for executing on Mac/Linux systems (must use chmod +x filname.py and execute using ./filename.py)
#Not even sure if this runs on Mac/Linux systems easily due to issues with outdated pygame libraries

import functions
#I've split functions off into a different script for ease of editing/adding new levels/resolutions etc
import subprocess
#subprocess allows us to open a new window and close the old window when we change the resolution (which enables us to run the game on different computers)
import sys
#we use sys for reading/editing a hidden settings file for saving preferences
import pygame
#pygame gives us easy graphics toys
import level1, level2, level3, level4, level5, level6, level7
#I've split the levels off into different scripts for ease of adding/changing them
import video1, video2, video3, video4, video5

pygame.mixer.pre_init(44100, -16, 2, 2048)
#this sets the system audio settings so that our game plays audio at the right speed
pygame.init()
#this gets pygame ready to start displaying things

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
#defines the colours white and black for white text and to clear the screen of old images

difficulty = 7
#this is set at this screen so that we have have editable difficulty levels in the future
#it is essentially the maximum horizontal/vertical speed that the craft can survive landing at

icon = pygame.image.load("./resources/images/icon.png")
#loads up the application icon from the resources folder
pygame.display.set_icon(icon)
#tells pygame to use the previously loaded application icon as the application icon
screen = pygame.display.set_mode((1280,720))
#sets the screen size to that defined by the resolution that is in the hidden settings file
pygame.display.set_caption("Lander - an educational physics game")
#sets the title of the window to "Lander"
background_image = pygame.image.load("./resources/images/launcher.png")
#loads up a splash-screen background image from the relevant resolution resources folder
screen.fill(BLACK)
#clears the screen
screen.blit(background_image, [0,0])
#displays the background image on the screen

clock = pygame.time.Clock()
#gives us a steady time (for playing music and counting frames per second)
pygame.mixer.music.load("./resources/audio/title_sound.mp3")
#loads up the background music
pygame.mixer.music.play(-1)
#gets the background music playing on loop

large_font = pygame.font.SysFont('Courier New', 100, True, False)
#defines the font for pygame to use for large things, using sizes in the functions file so that it obeys resoultion changes
medium_font = pygame.font.SysFont('Courier New', 33, True, False)
#same as above but for medium fonts
small_font = pygame.font.SysFont('Courier New', 20, True, False)
#same as above but for small fonts

title_text = large_font.render("Lander", True, WHITE)
#renders the title text
subtitle_text = medium_font.render("An educational physics game", True, WHITE)
#renders the subtitle text
effects_text = small_font.render("Toggle Sound Effects [N]", True, WHITE)
#renders option to mute effects
music_text = small_font.render("Toggle Music [M]", True, WHITE)
#renders the text that gives the player the option to mute music
exit_text = small_font.render("Exit [ESC]", True, WHITE)
#renders the text that tells the player how to exit
highscore_text = small_font.render("Highscores [H]", True, WHITE)
#renders the hihgscore text
play_text = medium_font.render("Press [SPACE] to Start", True, WHITE)
#renders the text that tells the player how to start playing

class Buttons(pygame.sprite.Sprite):
    """This code creates a sprites class to allow the showing of mute/resolution/exit buttons"""
    def __init__(self):
        super(Buttons, self).__init__()

        self.image = ""
        self.xy_location = ""
        #creates two empty properties that the buttons use

sprite_list = pygame.sprite.Group()
#initialize a list of sprites that need to be displayed on the screen

audio_on = Buttons()
#makes a button called audio_on
audio_on.image = pygame.image.load("./resources/images/unmuted.png")
#defines the image used for the button
audio_on.xy_location = (7, 7)
#defines where the button will appear
sprite_list.add(audio_on)
#adds the button to the list of sprites to display

audio_off = Buttons()
#makes a button called audio_off
audio_off.image = pygame.image.load("./resources/images/muted.png")
#defines the image used for the button
audio_off.xy_location = (7, 7)
#defines where the button will appear
sprite_list.add(audio_off)
#adds the button to the list of sprites to display

music_on = Buttons()
#makes a button called music_on
music_on.image = pygame.image.load("./resources/images/musicon.png")
#defines the image used
music_on.xy_location = (7, 47)
#defines where the button will appear
sprite_list.add(music_on)

music_off = Buttons()
#makes a button called music_on
music_off.image = pygame.image.load("./resources/images/musicoff.png")
#defines the image used
music_off.xy_location = (7, 47)
#defines where the button will appear
sprite_list.add(music_off)

audio_state = True
music_state = True
#a variable used to define whether the music is on or off by default

done = False
while not done:
    high_score = 0
    level_score = 0
    #enables quitting of the game using esc
    for event in pygame.event.get():
        #checks for events (e.g. clicking things, pressing keys)
        if event.type == pygame.QUIT:
            #checks to see if the x in the corner of the window was pressed
            done = True
            #drops out of the loop if it has been
        elif event.type == pygame.KEYDOWN:
            #checks to see if a keyboard button was pressed
            if event.key == pygame.K_ESCAPE:
                #checks to see if ESC was pressed
                done = True
                #drops out of the loop if it has been
            elif event.key == pygame.K_n:
                #checks to see if the "m" key was pressed
                if audio_state == True:
                    #checks to see if the music is on
                    audio_state = False
                    #changes the audio state variable for future reference
                elif audio_state == False:
                    #checks to see if the music is off
                    audio_state = True
                    #changes the audio state variable for future reference
            elif event.key == pygame.K_m:
                #checks to see if the "n" key was pressed
                if music_state == True:
                    #checks to see if the music is on
                    music_state = False
                    #changes the audio state variable
                    pygame.mixer.music.pause()
                    #pauses the music
                elif music_state == False:
                    #checks to see if music is off
                    music_state = True
                    #changes the audio state variable
                    pygame.mixer.music.unpause()
                    #unpauses the music
            elif event.key == pygame.K_h:
                functions.display_highscores(screen)
            elif event.key == pygame.K_SPACE:
                #checks to see if the space key was pressed
                next_level = video1.play(screen, clock)
                #next_level = level1.play(screen, clock, difficulty, audio_state)
                functions.fix_music(music_state)
                #if it was then call the play function in the level1.py document i.e. the next level (the code here will wait until the level is completed then drop back in)
                #note that the play function gets given the screen, clock, difficulty, audio_state, resource location, and resolution
                #play will return true when the level has been beaten and the player has chosen to progress, or false if exiting out to the main menu
                if next_level == True:
                    next_level, level_score = functions.show_controls(screen)
                    high_score += level_score
                    if next_level == True:
                        next_level, level_score = level1.play(screen, clock, difficulty, audio_state)
                        high_score += level_score
                        if next_level == True:
                            next_level = video2.play(screen, clock)
                            functions.fix_music(music_state)
                            if next_level == True:
                                next_level, level_score = level2.play(screen, clock, difficulty, audio_state)
                                high_score += level_score
                                if next_level == True:
                                    next_level, level_score = level3.play(screen, clock, difficulty, audio_state)
                                    high_score += level_score
                                    if next_level == True:
                                        next_level = video3.play(screen, clock)
                                        functions.fix_music(music_state)
                                        if next_level == True:
                                            next_level, level_score = level4.play(screen, clock, difficulty, audio_state)
                                            high_score += level_score
                                            if next_level == True:
                                                next_level = video4.play(screen, clock)
                                                functions.fix_music(music_state)
                                                if next_level == True:
                                                    next_level, level_score = level5.play(screen, clock, difficulty, audio_state)
                                                    high_score += level_score
                                                    if next_level == True:
                                                        next_level, level_score = level6.play(screen, clock, difficulty, audio_state)
                                                        high_score += level_score
                                                        if next_level == True:
                                                            next_level, level_score = level7.play(screen, clock, difficulty, audio_state)
                                                            high_score += level_score
                                                            if next_level == True:
                                                                functions.register_highscore(screen, high_score)
                                                                #next_level = video5.play(screen, clock)
                                                                #functions.fix_music(music_state)
                                                                #if next_level == True:
                                                                    #functions.register_highscore(screen, high_score)

    if audio_state == True:
        #checks to see if the current audio state is on
        screen.blit(audio_on.image, audio_on.xy_location)
        #prints the audio on button on the screen
    elif audio_state == False:
        #checks to see if the current audio state is off
        screen.blit(audio_off.image, audio_off.xy_location)
        #prints the audio off button on the screen
    if music_state == True:
        screen.blit(music_on.image, music_on.xy_location)
    elif music_state == False:
        screen.blit(music_off.image, music_off.xy_location)

    #print on the screen the text that appears on the title screen
    screen.blit(title_text, [450, 117])
    screen.blit(subtitle_text, [353, 217])
    screen.blit(effects_text, [60, 17])
    screen.blit(music_text, [60, 57])
    screen.blit(exit_text, [1133, 17])
    screen.blit(highscore_text, [1085, 47])
    screen.blit(play_text, [413, 450])

    clock.tick(30)
    #essentially defines the maximum frame rate whilst keeping CPU usage low; frame rate may still be way lower than this
    pygame.display.flip()
    #"flip" the display i.e. take what's been "blit"ed and display it to the user
    screen.fill(BLACK)
    #cover up the last stuff on the screen
    screen.blit(background_image, [0,0])
    #write the background image to the screen for the next pass

pygame.quit()
#quits the game
