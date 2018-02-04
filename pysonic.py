from psonic import *
from threading import Thread, Condition, Event


sleep(2)

s = scale(C3, MAJOR)
s
s.reverse()
play_pattern_timed(s, 0.125, release = 0.1)
random.shuffle(s)
play_pattern_timed(s, 0.125, release = 0.1)


sleep(2)
stop()
synth(SINE, note=D4)
synth(SQUARE, note=D4)
synth(TRI, note=D4, amp=0.4)

sleep(2)
##use_synth(PROPHET)
play (60, attack=0.5, decay=1, sustain_level=0.4, sustain=2, release=0.5)
sleep(4)
sample(AMBI_LUNAR_LAND, amp=0.5)
sleep(1)
for i in range(5):
    play(random.randrange(50, 100))
    sleep(0.5)

def my_loop():
    use_synth(TB303)
    sample(DRUM_BASS_HARD, rate = random.uniform(0.5, 2))
    play(random.choice(chord(E3, MINOR)), release= 0.2, cutoff=random.randrange(60, 130))
    sleep(0.25)


def looper(condition,stop_event):
    while not stop_event.is_set():
        my_loop()

condition = Condition()
stop_event = Event()
looper_thread = Thread(name='looper', target=looper, args=(condition,stop_event))

looper_thread.start()

input("Press Enter to continue...")

stop_event.set()

use_synth(PRETTY_BELL)

play_pattern( chord(E4, 'm7'))
play_pattern_timed( chord(E4, 'm7'), 0.25)
play_pattern_timed(chord(E4, 'dim'), [0.25, 0.5])
sleep(2)
use_synth(PIANO)


play_pattern( chord(E4, 'm7'))
play_pattern_timed( chord(E4, 'm7'), 0.25)
play_pattern_timed(chord(E4, 'dim'), [0.25, 0.5])

play_pattern_timed(scale(C3, MAJOR), 0.125, release = 0.1)
play_pattern_timed(scale(C3, MAJOR, num_octaves = 2), 0.125, release = 0.1)
play_pattern_timed(scale(C3, MAJOR_PENTATONIC, num_octaves = 2), 0.125, release = 0.1)