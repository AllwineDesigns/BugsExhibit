#!/usr/bin/python

import RPi.GPIO as GPIO
import pygame
import time
import random
from threading import Thread, Lock
from serial import Serial

GPIO.setmode(GPIO.BCM)

class Bug:
    channels = 0
    def __init__(self, pinNumber, soundFile, duration):
      self.duration = duration
      self.pin = pinNumber
      self.soundFile = soundFile
      self.sound = pygame.mixer.Sound("/home/pi/sounds/%s" % soundFile)
      self.channel = pygame.mixer.Channel(Bug.channels+1)
      self.channel.set_volume(.2)
      self.lastPlayTime = time.time()
      GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

      Bug.channels += 1

      def playSound(pin):
        print "detected interrupt on pin %s" % pin
        time.sleep(.05)
        if GPIO.input(pin) == False and time.time()-self.lastPlayTime > self.duration:
            self.lastPlayTime = time.time()
            print "playing %s" % self.soundFile
            self.channel.play(self.sound)

      GPIO.add_event_detect(self.pin, GPIO.FALLING, playSound, bouncetime=1000)

class Firefly:
  def __init__(self, pinNumber):
    self.pin = pinNumber
    self.lastPlayTime = time.time()
    self.totalTime = 1
    GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def lightFirefly(pin):
      time.sleep(.05)
      if GPIO.input(pin) == False and time.time()-self.lastPlayTime > self.totalTime:
        print "detected interrupt on pin %s" % pin
        self.lastPlayTime = time.time()

        colors = [ (220,229,30), (234,100,15), (255,255,0) ]

        color = random.choice(colors)
        if random.randint(0, 10) == 0:
          flashes = random.randint(1, 9)
        else:
          flashes = random.randint(1, 2)

        flashTime = 1000/(flashes)+random.randint(0,100)

        flashTimeMSB = flashTime >> 8
        flashTimeLSB = flashTime & 255

        speed = random.randint(5, 25)

        repeat = random.randint(2, 4)
        pause = random.uniform(1.5, 3.5)

        self.totalTime = ((flashes*flashTime)/1000)*repeat+pause*(repeat-1)

  #      print "color: %s" % (color,)
  #      print "flashes: %s" % flashes
  #      print "flashTime: %s = (%s << 8) | %s" % (flashTime, flashTimeMSB, flashTimeLSB)
  #      print "speed: %s" % speed

        for i in range(repeat):
          speed += random.randint(-5, 5)
          if speed < 5:
              speed = 5

          bytes = bytearray([color[0], color[1], color[2], flashes, flashTimeMSB, flashTimeLSB, speed])
          print "%s" % [ b for b in bytes ]
          ser.write(bytes)
          if i < repeat-1:
            time.sleep(pause)

    GPIO.add_event_detect(self.pin, GPIO.FALLING, lightFirefly, bouncetime=1000)

ser = Serial('/dev/ttyACM0', 9600);

pygame.mixer.init()

bugs = [ Bug(6, "bee.wav", 7.5),
         Bug(5, "clickbeetle.wav", 9),
         Bug(23, "cricket.wav", 10.5),
         Bug(17, "fly.wav", 10.5),
         Bug(16, "cockroach.wav", 10) ]

firefly = Firefly(24)



try:
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  GPIO.cleanup()
