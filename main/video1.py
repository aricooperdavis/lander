import pygame

def play(screen, clock,):
    pygame.mixer.quit()
    video = pygame.movie.Movie(r"C:\Users\Ari.DESKTOP-REV5O0M\Google Drive\University Stuff\Year 3 NSC\Group Project\python-lander\resources\videos\video1.mpg")
    video.set_display(screen)
    video.play()
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video.stop()
                playing = False
            elif event.type == pygame.KEYDOWN:
                video.stop()
                playing =  False
        screen.blit(screen, (0, 0))
        pygame.display.update()
        clock.tick(30)
        playing = video.get_busy()
    return True
