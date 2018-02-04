import pygame
from time import sleep

keys = [1, 2, 3, 4, 5, 6, 7, 8]
notes = {"C" : 1, "D" : 2, "E": 3, "F":4, "G":5, "A":6, "B":7, "C2":8}

pygame.mixer.init()

# initialize pygame.mixer
pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
# init() channels refers to mono vs stereo, not playback Channel object
# create separate Channel objects for simultaneous playback
channel1 = pygame.mixer.Channel(0) # argument must be int
channel2 = pygame.mixer.Channel(1)

def playSong(song):
    for key in song:
        playNote(key, song[key])


def playNote(note, duration):
    key = notes[note]
    print ("Playing %s (%d) for %d seconds" % (note, key, duration))
    playKey(key, duration)

def playWav(key, duration):
##    pygame.mixer.init()
    fileName = "/home/pi/Music/%d.wav" % key
    sound = pygame.mixer.Sound(fileName)
    if channel1.get_busy():
        channel2.play(sound)
    else:
        channel1.play(sound)
##    sound.play()

playWav(1, 5)
playWav(2, 5)
playWav(3, 5)
playWav(2, 5)
playWav(1, 5)

def playKey(key, duration):
##    pygame.mixer.init()
    fileName = "/home/pi/Music/%d.mp3" % key
    pygame.mixer.music.load(fileName)

    pygame.mixer.music.play()
    sleep(duration)
    pygame.mixer.music.fadeout(duration * 250)
##    while (pygame.mixer.music.get_busy() == True):
##        continue

##playKey(1, 5)

aSong = {
    "C" : 2.5,
    "C" : 2.5,
    "G" : 2.5,
    "G" : 2.5,
    "A" : 1,
    "A" : 1,
    "A" : 1,
    "A" : 1,
    "G" : 3,
    "F" : 2,
    "F" : 2,
    "G" : 2,
    "G" : 2,
    "F" : 2,
    "F" : 2,
    "C" : 1
}
playSong(aSong)


for key in keys:
    playKey(key, 1)
while (pygame.mixer.music.get_busy() == True):
    continue
##pygame.mixer.quit()
