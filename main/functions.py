import pygame
#we need pygame for fonts
import math
#we need pythons math library for absolute value functions for safe landing calculations
import random
#just used for winds
import string
import pickle
from operator import itemgetter

BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
GREEN  = (  0, 255,   0)
YELLOW = (255, 255,   0)
RED    = (255,   0,   0)
ORANGE = (255, 127,   0)
#RGB colour definitions for text

def safe_landing(player, difficulty):
    if math.fabs(player.velocities[0]) <= difficulty and math.fabs(player.velocities[1]) <= difficulty:
        if player.angle <= 10 and player.angle >= -10:
            return True
        else:
            return "angle"
    else:
        return "speed"

def explosion(screen, player, planet):
    for x in range(0, 5):
        for y in range(0, 5):
            screen.blit(player.explosion_image, (player.rect.topleft[0]-45, player.rect.topleft[1]-30), (x*130, y*130, 130, 130))
            pygame.display.flip()
            screen.blit(planet.bg_image, (0, 0), (0, player.last_altitude, 1280, 720))

def surface_collision(screen, player, difficulty, planet):
    font = pygame.font.SysFont('Courier New', 33, True, False)
    success_text = font.render("Good Landing, Commander!", True, GREEN)
    next_level_text = font.render("Press [SPACE] to try the next level.", True, GREEN)
    crash_text = font.render("You came in too fast, Commander!", True, RED)
    angle_crash_text = font.render("You need to land vertically, Commander!", True, RED)
    instruct_text = font.render("Press [A] to play again.", True, WHITE)
    exit_text = font.render("Press [ESC] to exit.", True, WHITE)

    if safe_landing(player, difficulty) == True:
        #If landing is safe display success messages
        player.landed_sound.play()
        screen.blit(success_text, (420, 100))
        screen.blit(instruct_text, (403, 167))
        screen.blit(exit_text, (447, 217))
        screen.blit(next_level_text, (303, 367))
        #And ensure craft stops moving and stays on surface
        accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
        #Set safe landing check to True
        safe_landing_check = True
        playing = False
    elif safe_landing(player, difficulty) == "speed":
        #If landing is crash, display try again messages
        player.explosion_sound.play()
        explosion(screen, player, planet)
        screen.blit(crash_text, (333, 100))
        screen.blit(instruct_text, (403, 167))
        screen.blit(exit_text, (447, 217))
        #And ensure craft stops moving and stays on surface
        accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
        #Set safe landing check to False
        safe_landing_check = False
        playing = False
    elif safe_landing(player, difficulty) == "angle":
        #If landing is crash, display try again messages
        player.explosion_sound.play()
        explosion(screen, player, planet)
        screen.blit(angle_crash_text, (283, 100))
        screen.blit(instruct_text, (403, 167))
        screen.blit(exit_text, (447, 217))
        #And ensure craft stops moving and stays on surface
        accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
        #Set safe landing check to False
        safe_landing_check = False
        playing = False

    return player, safe_landing_check, playing

def surface_hover(screen, player, difficulty, planet, burn_up=False):
    font = pygame.font.SysFont('Courier New', 33, True, False)
    success_text = font.render("Good Hovering, Commander!", True, GREEN)
    next_level_text = font.render("Press [SPACE] to try the next level.", True, GREEN)
    instruct_text = font.render("Press [A] to play again.", True, WHITE)
    exit_text = font.render("Press [ESC] to exit.", True, WHITE)
    crash_text = font.render("You burned up in the atmosphere, Commander!", True, RED)
    player.hovering_time += 1
    if burn_up == False:
        if player.hovering_time >= 120:
            player.hovering_time = 0
            player.burn_sound.stop()
            player.landed_sound.play()
            screen.blit(success_text, (420, 100))
            screen.blit(instruct_text, (403, 167))
            screen.blit(exit_text, (447, 217))
            screen.blit(next_level_text, (303, 367))
            #And ensure craft stops moving and stays on surface
            accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
            #Set safe landing check to True
            safe_landing_check = True
            playing = False
        else:
            safe_landing_check = True
            playing = True
    else:
        #If landing is crash, display try again messages
        player.hovering_time = 0
        player.burn_sound.stop()
        player.explosion_sound.play()
        screen.blit(crash_text, (200, 100))
        screen.blit(instruct_text, (403, 167))
        screen.blit(exit_text, (447, 217))
        #And ensure craft stops moving and stays on surface
        accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
        #Set safe landing check to False
        safe_landing_check = False
        playing = False

    return player, safe_landing_check, playing

def object_collision(screen, player, difficulty):
    font = pygame.font.SysFont('Courier New', 33, True, False)
    success_text = font.render("Good Landing, Commander!", True, GREEN)
    next_level_text = font.render("Press [SPACE] to try the next level.", True, GREEN)
    crash_text = font.render("You can't land on that, Commander!", True, RED)
    instruct_text = font.render("Press [A] to play again.", True, WHITE)
    exit_text = font.render("Press [ESC] to exit.", True, WHITE)

    if safe_landing(player, difficulty) == True:
        #If landing is safe display success messages
        player.landed_sound.play()
        screen.blit(success_text, (420, 100))
        screen.blit(instruct_text, (403, 167))
        screen.blit(exit_text, (447, 217))
        screen.blit(next_level_text, (303, 367))
        #And ensure craft stops moving and stays on surface
        accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
        #Set safe landing check to True
        safe_landing_check = True
        playing = False
    else:
        #If landing is crash, display try again messages
        player.explosion_sound.play()
        screen.blit(crash_text, (333, 100))
        screen.blit(instruct_text, (403, 167))
        screen.blit(exit_text, (447, 217))
        #And ensure craft stops moving and stays on surface
        accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
        #Set safe landing check to False
        safe_landing_check = False
        playing = False

    return player, safe_landing_check, playing

def drag(density, velocity, dragCoeff, Area):
	# F = force due to drag
	p = density
	v = velocity
	c = dragCoeff
	A = Area
	if v>0:
		F = 0.5*p*(v**2)*c*A
	elif v<0:
		F = -0.5*p*(v**2)*c*A
	else:
		F=0
	return F

def fix_music(music_state):
    if music_state == True:
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 2, 2048)
        pygame.mixer.music.load("../resources/audio/title_sound.mp3")
        pygame.mixer.music.play(-1)
    elif music_state == False:
        pygame.mixer.quit
        pygame.mixer.init(44100, -16, 2, 2048)
        pygame.mixer.music.load("../resources/audio/title_sound.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

def player_planet_motion(player, planet, screen, objects=False):
    player.altitude += player.velocities[1]

    if player.altitude < 0:
        player.rect.center = (player.c_position[0]+int(round(player.velocities[0])), player.c_position[1]+int(round(player.velocities[1])))
        screen.blit(planet.bg_image, [0, 0], (0, 0, 1280, 720))
        if objects != False:
            for i in objects:
                i.rect.topleft = (i.rect.topleft[0]+i.velocity[0], i.rect.topright[1]+i.velocity[1])
                if i.rect.topleft[0] > 0:
                    i.rect.topleft = (i.rect.topleft[0]-1280, i.rect.topleft[1])
            objects.draw(screen)
        screen.blit(planet.map, (1280-148, 20))
        planet.rect.topleft = (0, 0)
        pygame.draw.rect(screen, WHITE, (1280-150, 18, 131, 291), 2)
        pygame.draw.rect(screen, ORANGE, (1280-150, 18, 131, 76), 2)
        player.c_position = player.rect.center
        screen.blit(player.image_mini, (int(round(player.rect.center[0]*0.1, 0)+1280-150), int(round(player.rect.center[1]*0.1, 0)+18)))
    elif player.altitude <= 720*3:
        screen.blit(planet.bg_image, [0, 0], (0, player.altitude, 1280, 720))
        planet.rect.topleft = (0, -player.altitude)
        if objects != False:
            for i in objects:
                i.rect.topleft = (i.rect.topleft[0]+i.velocity[0], -player.altitude+i.velocity[1])
                if i.rect.topleft[0] > 0:
                    i.rect.topleft = (i.rect.topleft[0]-1280, i.rect.topleft[1])
            objects.draw(screen)
        screen.blit(planet.map, (1280-148, 20))
        pygame.draw.rect(screen, WHITE, (1280-150, 18, 131, 291), 2)
        pygame.draw.rect(screen, ORANGE, (1280-150, int(player.altitude/10)+18, 131, 76), 2)
        player.rect.center = (player.c_position[0]+int(round(player.velocities[0])), player.c_position[1])
        player.c_position = player.rect.center
        player.last_altitude = player.altitude
        screen.blit(player.image_mini, (int(round(player.rect.center[0]*0.1, 0)+1280-150), int(round(player.rect.center[1]*0.1, 0)+18+player.altitude*0.1)))
    else:
        player.rect.center = (player.c_position[0]+int(round(player.velocities[0])), player.c_position[1]+int(round(player.velocities[1])))
        screen.blit(planet.bg_image, [0, 0], (0, player.last_altitude, 1280, 720))
        planet.rect.topleft = (0, -player.last_altitude)
        if objects != False:
            for i in objects:
                i.rect.topleft = (i.rect.topleft[0]+i.velocity[0], -player.last_altitude+i.velocity[0])
                if i.rect.topleft[0] > 0:
                    i.rect.topleft = (i.rect.topleft[0]-1280, i.rect.topleft[1])
            objects.draw(screen)
        screen.blit(planet.map, (1280-148, 20))
        pygame.draw.rect(screen, WHITE, (1280-150, 18, 131, 291), 2)
        pygame.draw.rect(screen, ORANGE, (1280-150, int(player.last_altitude/10)+18, 131, 76), 2)
        player.c_position = player.rect.center
        screen.blit(player.image_mini, (int(round(player.rect.center[0]*0.1, 0)+1280-150), int(round(player.rect.center[1]*0.1, 0)+18+player.last_altitude*0.1)))

    if player.rect.center[0] < 0:
        player.rect.center = (player.rect.center[0]+1280, player.rect.center[1])
        player.c_position = player.rect.center
    elif player.rect.center[0] > 1280:
        player.rect.center = (player.rect.center[0]-1280, player.rect.center[1])
        player.c_position = player.rect.center

def electro_mag(screen, player, planet):
    player.level_timer += 1
    font_small = pygame.font.SysFont('Courier New', 20, True, False)
    electro_warning = font_small.render("WARNNIG: ELECTRONIC SYSTEMS DISRUPTED!", True, RED)
    if (round(player.level_timer, -1)/10.0) % 2 == 0:
        screen.blit(electro_warning, (10, 150))

def wind_warning(screen, player, planet):
    player.level_timer += 1
    font_small = pygame.font.SysFont('Courier New', 20, True, False)
    electro_warning = font_small.render("WARNNIG: HIGH WINDS DETECTED!", True, RED)
    if (round(player.level_timer, -1)/10.0) % 2 == 0:
        screen.blit(electro_warning, (10, 150))
    player.velocities = (player.velocities[0]+int(random.random()*1.2), player.velocities[1])

def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            return event.key
        else:
            pass

def display_box(score, screen, message):
    font = pygame.font.SysFont("Courier New", 40, True, False)
    small_font = pygame.font.SysFont("Courier New", 20, True, False)
    pygame.draw.rect(screen, WHITE, (380, 180, 530, 300), 0)
    pygame.draw.rect(screen, BLACK, (450, 340, 380, 30), 1)
    title = font.render("New Highscore!", True, GREEN)
    subtitle = small_font.render("Enter your name below:", True, BLACK)
    scorecard = small_font.render("Your score: "+str(score), True, ORANGE)
    submit = small_font.render("Press [ENTER] to submit your name", True, GREEN)
    anonymous = small_font.render("or press [ESC] to submit anonymously.", True, RED)
    screen.blit(title, (475, 200))
    screen.blit(scorecard, (545, 250))
    screen.blit(subtitle, (500, 300))
    screen.blit(submit, (442, 400))
    screen.blit(anonymous, (430, 430))
    if len(message) != 0:
        screen.blit(small_font.render(message, True, BLACK), (455, 343))
    pygame.display.flip()

def write_highscore_to_file(name, score):
    highscores = [("Example", 50)]
    try:
        with open('.highscores.txt', 'r') as f:
            try:
                highscores = pickle.load(f)
            except EOFError:
                with open('.highscores.txt.', 'w+') as f:
                    pickle.dump(highscores, f)
    except IOError:
        with open('.highscores.txt', 'w+') as f:
            pickle.dump(highscores, f)
    highscores.append((str(name), int(score)))
    highscores = sorted(highscores, key=itemgetter(1), reverse=True)[:10]
    with open('.highscores.txt', 'w') as f:
        pickle.dump(highscores, f)

def register_highscore(screen, high_score):
    current_string = []
    display_box(high_score, screen, "Name: "+string.join(current_string,""))
    while 1:
        inkey = get_key()
        if inkey == pygame.K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == pygame.K_RETURN:
            break
        elif inkey == pygame.K_ESCAPE:
            current_string = ""
            break
        elif len(current_string)>22:
            pass
        elif inkey <= 127:
            current_string.append(chr(inkey))
        display_box(high_score, screen, "Name: "+string.join(current_string,""))
    if current_string == "":
        current_string = "Anonymous"
    write_highscore_to_file(string.join(current_string,""), high_score)

def display_highscores(screen):
    while 1:
        number = 0
        highscores = [("Example", 50)]
        font = pygame.font.SysFont("Courier New", 40, True, False)
        small_font = pygame.font.SysFont("Courier New", 20, True, False)
        pygame.draw.rect(screen, WHITE, (400, 100, 490, 500), 2)
        title = font.render("Highscores", True, WHITE)
        exit = small_font.render("Press [ESC] to exit.", True, WHITE)
        screen.blit(title, (520, 130))
        screen.blit(exit, (525, 540))
        try:
            with open('.highscores.txt', 'r') as f:
                try:
                    highscores = pickle.load(f)
                except EOFError:
                    with open('.highscores.txt.', 'w+') as f:
                        pickle.dump(highscores, f)
        except IOError:
            with open('.highscores.txt', 'w+') as f:
                pickle.dump(highscores, f)
        for i in highscores:
            text = small_font.render(i[0]+" - "+str(i[1]), True, WHITE)
            hp = 635-int((text.get_rect().width)/2)
            screen.blit(text, (hp, 180+(number*30)))
            number += 1
        pygame.display.flip()
        inkey = get_key()
        if inkey == pygame.K_ESCAPE:
            break
        pass
    pass
