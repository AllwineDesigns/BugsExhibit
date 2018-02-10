import RPi.GPIO as GPIO
import pygame
import time

pygame.mixer.init()

butPin = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

sound = pygame.mixer.Sound("/home/pi/sounds/crickets.wav")
channel = pygame.mixer.Channel(1)
lastPlayTime = time.time()

def playSound(pin):
  global lastPlayTime
  print "detected interrupt on pin %s" % pin
  if time.time()-lastPlayTime > 6:
    print "playing crickets"
    channel.play(sound)
    lastPlayTime = time.time()

GPIO.add_event_detect(butPin, GPIO.FALLING, playSound)

try:
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  GPIO.cleanup()
