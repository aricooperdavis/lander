import functions
#I've split functions off into a different script for ease of editing/adding new levels/resolutions etc
import math
#math gives us access to absolute magnitude functions
import pygame
#pygame gives us easy graphics toys

def play(screen, clock, difficulty, muted):
    #is the play function that's called by the launcher
    BLACK  = (  0,   0,   0)
    WHITE  = (255, 255, 255)
    GREEN  = (  0, 255,   0)
    YELLOW = (255, 255,   0)
    RED    = (255,   0,   0)
    ORANGE = (255, 127,   0)
    #the above is just defining RGB colours for text and screen changes

    def safe_landing(player_velocities, difficulty):
        #is a function that is called to determine whether a landing was safe or not
        if math.fabs(player_velocities[0]) <= difficulty and math.fabs(player_velocities[1]) <= difficulty:
            return True
        else:
            return False

    class Craft(pygame.sprite.Sprite):
        """Craft class for landers, child of Sprite"""
        def __init__(self):
            super(Craft, self).__init__()

            self.image = pygame.image.load("./resources/images/probe_ld.png").convert_alpha()
            #takes an image from the resources folder appropriate to the resolution to be used as the player
            self.image_mini = pygame.image.load("./resources/images/probe_mini.png").convert_alpha()
            #an image used for the little player on the minimap
            self.rect = self.image.get_rect()
            #gets pygame to automatically work out the boundaries of the player
            self.mask = pygame.mask.from_surface(self.image)
            #gets pygame to build a mask that goes around the edge of the player for collision detection
            self.velocities = (6, 6)
            #variable stores the players velocity and is defaulted to an intial velocity value stored in the functions script
            self.c_position = (640, 360)
            #stores the players current position and is defaulted to a intial position value stored in the functions script
            self.angle = 0
            #stores the players angle and is defaulted to vertical
            self.thrust = 0
            #stores a value for the thrust currently exerted on the player, 0 unless the up button is being pressed
            self.angular_thrust = 0
            #stores a value for the angle change currently exerted on the player, 0 unless a sideways arrow key is pressed
            self.fuel = 100
            #stores a value for the amount of fuel that the player has
            self.fuel_rate = 0.2
            #defines the rate at which fuel is burnt for every frame in which the up arrow is pressed
            self.burn_sound = pygame.mixer.Sound("./resources/audio/burn.ogg")
            #loads a burn sound to be played whilst thrusting
            self.explosion_sound = pygame.mixer.Sound("./resources/audio/explosion.ogg")
            #loads an explosion sound to be played on crashing
            self.landed_sound = pygame.mixer.Sound("./resources/audio/landed.ogg")
            #Loads a voice-over sound to be played when landed successfully
            self.explosion_image = pygame.image.load("./resources/images/explosion.png").convert_alpha()
            #Loads the explosion spritesheet
            self.altitude = 0
            #effective altitude of player above planet surface for determining player/background interactions
            self.last_altitude = 0
            #variable for saving the previous altitude
            self.hovering_time = 0

        def update(self, planet):
            """ this is a function which is updated each frame to calculate where the player should next appear given their position, velocity, thrust, and the current gravity """
            if self.fuel <= 0.0:
                #checks to see if the fuel is empty (or less than empty since the fuel rate is simply subtracted from the total fuel)
                self.fuel = 0.0
                #sets the fuel level to 0 so that we don't see negetive amounts of fuel in the tank
                self.thrust = 0
                #stops the player from being able to thrust up if there's no fuel
            self.angle += self.angular_thrust
            #takes the players current angle and alters it by the angular thrust
            self.x_thrust = (self.thrust * math.sin(math.radians(float(self.angle))))
            #takes the thrust on the player and the players angle and works out the x component of that thrust
            self.y_thrust = (self.thrust * math.cos(math.radians(float(self.angle))))
            #takes the thrust on the player and the players angle and works out the y component of that thrust

            self.drag_x = functions.drag(planet.airDensity,self.velocities[0],1,1)
			#calculates drag for x axis
            self.drag_y = functions.drag(planet.airDensity,self.velocities[1],1,1)
			#calculates drag for y axis
            lander_mass = 1000
			#m for mass, defined arbitrarily as 1000 for now
            drag_decel_x = (self.drag_x)/lander_mass
			#horizontal deceleration due to drag
            drag_decel_y = (self.drag_y)/lander_mass
			#vertical deceleration due to drag

            self.velocities = (self.velocities[0]+self.x_thrust-drag_decel_x, self.velocities[1]+planet.accel_g-self.y_thrust-drag_decel_y)
            #changes the players velocity by adding gravity, thrust and drag deceleration

            if self.thrust == 0:
                #checks to see if the player is not thrusting
                self.image = pygame.image.load("./resources/images/probe_ld.png").convert_alpha()
                #ensures that the image describing the player is does not have flames coming out the bottom
            elif self.thrust != 0:
                #checks to see if the player is thrusting
                self.fuel -= self.fuel_rate
                #subtracts the amount of fuel previously set from the amount of fuel left
                self.image = pygame.image.load("./resources/images/probe_l.png").convert_alpha()
                #ensures that the image of the player has flames coming out of the bottom
            self.image = pygame.transform.rotate(self.image, -1*player.angle)
            #rotates the image of the player by its current angle

    class Planet(pygame.sprite.Sprite):
        """Object class for planet"""
        def __init__(self):
            super(Planet, self).__init__()

            self.name = "HD 189733 b"
            #the name to be displayed in the top left info section
            self.image = pygame.image.load("./resources/images/HD_surface.png").convert_alpha()
            #the image used for the planet surface
            self.bg_image = pygame.image.load("./resources/images/HD_long.png").convert_alpha()
            #the image used as a background for the planet (including planet surface)
            self.map = pygame.image.load("./resources/images/HD_map.png").convert_alpha()
            #map image
            self.rect = self.image.get_rect()
            #calcultes the dimensions of the surface so that its location can be determined
            self.mask = pygame.mask.from_surface(self.image, 10)
            #works out the border of the surface for collision detection
            self.accel_g = 2.3
            #the acceleration due to gravity from the planet
            self.thrust = 3
            #the thrust that the player can exert (don't ask me why I put this in this section..)
            self.airDensity = 6.83
			#Defines the density of the planets atmosphere

    class Object(pygame.sprite.Sprite):
        """Object class for collision objects that are not the landing zone, since that's included in the planet definition"""
        def __init__(self):
            super(Object, self).__init__()

            self.image = pygame.image.load("./resources/images/HD_clouds.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.topleft = (-1280, 0)
            self.velocity = (3, 0)

    sprite_list = pygame.sprite.Group()
    object_sprite_list = pygame.sprite.Group()
    #creates a list of sprites
    planet = Planet()
    #make a planet called planet
    player = Craft()
    #make a craft called player
    clouds = Object()
    rain = Object()
    rain.image = pygame.image.load("./resources/images/HD_rain.png").convert_alpha()
    rain.rect = rain.image.get_rect()
    rain.mask = pygame.mask.from_surface(rain.image)

    sprite_list.add(player, planet)
    object_sprite_list.add(clouds, rain)
    #add the player to a list of sprites

    font_small = pygame.font.SysFont('Courier New', 20, True, False)
    #define what font will be used to print the info in the top left depending on the resolution

    player.rect.center = player.c_position
    #load the image of the player onto the screen at its current position

    in_level = True
    #a variable to enable us to quit out of the level
    playing = True
    #a variable to check whether the game itself is running (so should leaking fuel still be being lost from the tank etc)
    safe_landing_check = True
    #check to see if we've landed safely
    next_level = False
    #check to see if we're advancing to the next level this frame
    score_multiplier = 2

    if not muted:
        #check to see if we're muted (i know this looks weird, but it makes sense in other contexts)
        player.burn_sound = pygame.mixer.Sound("./resources/audio/silence.ogg")
        #if we are muted then set the burn sound to silence
        player.explosion_sound = pygame.mixer.Sound("./resources/audio/silence.ogg")
        #if we are muted then set the explosion sound to silence
        player.landed_sound = pygame.mixer.Sound("./resources/audio/silence.ogg")
        #if we are muted then set the landed sound to silence

    while in_level:
        #enables us to drop out of the level if we choose to
        while playing:
            #if the game is running
            for event in pygame.event.get():
                #check for input events to the game
                if event.type == pygame.QUIT:
                    #check to see if the x in the corner of the screen has been pressed
                    in_level = False
                    #if it has been then drop out to the main menu
                elif event.type == pygame.KEYDOWN:
                    #check to see if a key has been pressed
                    if event.key == pygame.K_UP and player.fuel > 0.0:
                        #check to see if the up arrow key was pressed and the player still has fuel
                        player.thrust = planet.thrust
                        #if so then give the player the predetermined amount of thrust
                        player.burn_sound.play()
                        #and play the rocket sound
                    elif event.key == pygame.K_LEFT:
                        #check to see if the left arrow key was pressed
                        player.angular_thrust = -2
                        #if it was then produce angular thrust of -2
                    elif event.key == pygame.K_RIGHT:
                        #check to see if the right arrow key was pressed
                        player.angular_thrust = 2
                        #if it was then produce angular thrust of 2
                    elif event.key == pygame.K_ESCAPE:
                        #check to see if the esc key was pressed
                        in_level = False
                        #if it was then drop back to the main menu
                    elif event.key == pygame.K_EQUALS:
                        safe_landing_check = True
                        next_level = True
                        playing = False
                        #a debug tool to skip levels
                elif event.type == pygame.KEYUP:
                    #check to see if a key has been released
                    if event.key == pygame.K_UP:
                        #if the up arrow key has been released
                        player.thrust = 0
                        #then stop the player from thrusting
                        player.burn_sound.stop()
                        #and stop the burn sound
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        #if either of the direction arrows was released
                        player.angular_thrust = 0
                        #stop the players angle from altering further
                        #we could potentially remove this if we wanted scientific accuracy, but it makes the game seriously fucking difficult

            screen.fill(BLACK)
            #wipe anything from the screen
            player.update(planet)
            #update the center of the player based on the update function defined in the craft definition at the top
            functions.player_planet_motion(player, planet, screen, object_sprite_list)
            #determine player/background interactions for final position

            drag_txt_x = font_small.render("Horizontal Drag: "+str(round(player.drag_x)), True, WHITE)
			#creates the text that says what horizontal drag is
            drag_txt_y = font_small.render("Vertical Drag: "+str(round(player.drag_y)), True, WHITE)
			#creates the text that says what Vertical drag is

            if ((100*player.hovering_time)/119) <= 33:
                data_collected = font_small.render("Data collected: "+str((100*player.hovering_time)/119)+"%", True, RED)
            elif ((100*player.hovering_time)/119) <= 66:
                data_collected = font_small.render("Data collected: "+str((100*player.hovering_time)/119)+"%", True, ORANGE)
            elif ((100*player.hovering_time)/119) < 100:
                data_collected = font_small.render("Data collected: "+str((100*player.hovering_time)/119)+"%", True, YELLOW)
            else:
                data_collected = font_small.render("Data collected: "+str((100*player.hovering_time)/119)+"%", True, GREEN)

            planet_tag = font_small.render("Planet: "+str(planet.name), True, WHITE)
            #create the text that names the planet
            if math.fabs(player.velocities[0]) > difficulty:
                #check to see if the horizontal velocity is above the difficulty level (of max landing velocity)
                x_vel_txt = font_small.render("Horizontal velocity: "+str(round(player.velocities[0], 1)), True, RED)
                #if it is then create the text that shows horizontal velocity in red
            else:
                x_vel_txt = font_small.render("Horizontal velocity: "+str(round(player.velocities[0], 1)), True, GREEN)
                #if its not then create the text that shows the horizontal velocity in green
            if math.fabs(player.velocities[1]) > difficulty:
                #check to see if the vertical velocity is above the difficulty level (of max landing velocity)
                y_vel_txt = font_small.render("Vertical velocity: "+str(round(player.velocities[1], 1)), True, RED)
                #if it is then create the text that shows vertical velocity in red
            else:
                y_vel_txt = font_small.render("Vertical velocity: "+str(round(player.velocities[1], 1)), True, GREEN)
                #if its not then create the text that shows horizontal velocity in green

            if player.fuel > 75:
                #check to see if the fuel is more than 75 percent full
                fuel_txt = font_small.render("Fuel: "+str(player.fuel)+"%", True, GREEN)
                #if it is then create the fuel text in green
            elif player.fuel > 50:
                #check to see if its more than 50 percent full (but less than 75)
                fuel_txt = font_small.render("Fuel: "+str(player.fuel)+"%", True, YELLOW)
                #if it is then create the fuel text in yellow
            elif player.fuel > 25:
                #check to see if its more than 25 percent full (but less than 50)
                fuel_txt = font_small.render("Fuel: "+str(player.fuel)+"%", True, ORANGE)
                #if it is then create the fuel text in orange
            elif player.fuel > 0:
                #check to see if the fuel level is between 0 and 25 percent full
                fuel_txt = font_small.render("Fuel: "+str(round(math.fabs(player.fuel), 1))+"% [FUEL LOW]", True, RED)
                #if it is then create the fuel text in red
            elif player.fuel == 0:
                #check to see if there's no fuel left
                fuel_txt = font_small.render("Fuel: 0% [FUEL EMPTY]", True, RED)
                #if there's not then display that in red

            if pygame.sprite.collide_mask(player, planet) != None:
                #check to see if the player has collide with the planet
                player.hovering_time += 1
                if player.hovering_time >= 120:
                    player.hovering_time = 120
                #call the safe landing check function described above, and remember whether the landing was safe or not

            xy_font = pygame.font.SysFont('Courier New', 33, True, False)
            xy_success_text = xy_font.render("Good Hovering, Commander!", True, GREEN)
            xy_next_level_text = xy_font.render("Press [SPACE] to continue.", True, GREEN)
            xy_instruct_text = xy_font.render("Press [A] to play again.", True, WHITE)
            xy_exit_text = xy_font.render("Press [ESC] to exit.", True, WHITE)
            xy_crash_text = xy_font.render("You burned up in the atmosphere, Commander!", True, RED)

            if player.rect.center[1]>740:
                if player.hovering_time >= 120:
                    player.hovering_time = 0
                    player.burn_sound.stop()
                    player.landed_sound.play()
                    screen.blit(xy_success_text, (400, 140))
                    screen.blit(xy_instruct_text, (403, 207))
                    screen.blit(xy_exit_text, (447, 257))
                    screen.blit(xy_next_level_text, (403, 407))
                    #And ensure craft stops moving and stays on surface
                    accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
                    #Set safe landing check to True
                    safe_landing_check = True
                    playing = False
                elif player.hovering_time < 120:
                    player.hovering_time = 0
                    player.burn_sound.stop()
                    player.explosion_sound.play()
                    screen.blit(xy_crash_text, (200, 140))
                    screen.blit(xy_instruct_text, (403, 207))
                    screen.blit(xy_exit_text, (447, 257))
                    #And ensure craft stops moving and stays on surface
                    accel_g, player.thrust, player.velocities = 0, 0, [0, 0]
                    #Set safe landing check to False
                    safe_landing_check = False
                    playing = False

            sprite_list.draw(screen)
            #display the player on the screen
            clock.tick(30)
            #ensure that at least 1/30th of a second has passed

            frame_rate = clock.get_fps()
            #gets the current framerate of the game
            frame_rate_txt = font_small.render("FPS: "+str(round(frame_rate, 1)), True, WHITE)
            #generates text to render that frame rate
            #screen.blit(frame_rate_txt, (10, 150))
            #prints that text on the screen in an appropriate place for the chosen resolution

            screen.blit(x_vel_txt, (10, 10))
            #display the horizontal velocity text on the screen (in a place appropraite for the resolution)
            screen.blit(y_vel_txt, (10, 30))
            #display the vertical velocity text on the screen (in a place appropraite for the resolution)
            screen.blit(fuel_txt, (10, 50))
            #display the fuel level on the screen (in a place appropraite for the resolution)
            screen.blit(planet_tag, (10, 70))
            #display the planet name on the screen (in a place appropraite for the resolution)
            screen.blit(drag_txt_x, (10, 90))
			#display the horizontal drag text on the screen
            screen.blit(drag_txt_y, (10, 110))
			#display the horizontal drag text on the screen
            screen.blit(data_collected, (10, 130))

            pygame.display.flip()
            #show the screen to the user

        for event in pygame.event.get():
            #if we're no longer playing i.e. on a crash or success screen check for events
            if event.type == pygame.QUIT:
                #check for clicking on the x in the corner of the window
                in_level = False
                #close the level if its clicked
            elif event.type == pygame.KEYDOWN:
                #check for the pushing down of a key
                if event.key == pygame.K_a:
                    score_multiplier = score_multiplier * 0.7
                    #check for the a key being pressed, which replays the level
                    player.c_position = (640, 360)
                    #reset the player position
                    player.velocities = (6, 6)
                    #reset the player velocity
                    player.angle = 0
                    #reset the player tilt
                    player.angular_thrust = 0
                    #reset the player thrust
                    player.fuel = 100
                    #reset the player fuel
                    player.altitude = 0
                    #resets the player altitude
                    playing = True
                    #get back into the playing loop
                if event.key == pygame.K_SPACE:
                    #check for the space key being pressed
                    player.c_position = (640, 360)
                    #reset the player position
                    player.velocities = (6, 6)
                    #reset the player velocity
                    player.angle = 0
                    #reset the player angle
                    player.angular_thrust = 0
                    #reset the player thrust
                    player.altitude = 0
                    #resets the player altitude
                    if safe_landing_check == True:
                        #check if the landing was safe
                        next_level = True
                        #if it was then tell launcher.py to try the next level
                        in_level = False
                        #and break out of this level
                    elif safe_landing_check == False:
                        player.fuel = 100
                        #resets player fuel
                        score_multiplier = score_multiplier * 0.7
                        playing = True
                        #if the landing wasn't safe replay the current level
                if event.key == pygame.K_ESCAPE:
                    #check if esc key is pressed
                    in_level = False
                    #if it is break out to the launcher screen

#this bit returns true or false depending on whether you've chosen to go to the next level or not, for processing by launcher.py
    if next_level == False:
        return False, player.fuel*score_multiplier
    elif next_level == True:
        return True, player.fuel*score_multiplier
