import pygame

def play_alert(sound_file):
    """
    Play an alert sound using Pygame.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()