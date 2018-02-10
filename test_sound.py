import pygame
import time

pygame.mixer.init()

sound = pygame.mixer.Sound("/home/pi/sounds/crickets.wav")
channel = pygame.mixer.Channel(1)
channel.set_volume(.2)

channel.play(sound)
time.sleep(5)
