import pygame

def play(screen, clock,):
    pygame.mixer.quit()
    video = pygame.movie.Movie("./resources/videos/video1.mpg")
    video.set_display(screen, [0, 0, 1280, 720])
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
