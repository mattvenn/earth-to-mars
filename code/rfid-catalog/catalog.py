import serial
import pygame.mixer

#initialise the mixer to 44.1khz, 16bit, 2channel with 4096 buffer
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()

#load the sound
ok_sound = pygame.mixer.Sound('beep.wav') 
ok_sound.set_volume(1.0)
bad_sound = pygame.mixer.Sound('error.wav') 
bad_sound.set_volume(1.0)
file_name = "rfid.txt"
s = serial.Serial('/dev/ttyUSB0', 9600)
count = 0
last_code = None
while True:
    code = s.read(14)
    assert code[0] == '\x02'
    assert code[13] == '\x03'
    code = code[1:13]  # 12 characters
    assert len(code) == 12
    if code == last_code:
        print("re-read")
        bad_sound.play()
        continue
    last_code = code
    ok_sound.play()
    print("%03d : %s" % (count, code))
    with open(file_name, 'a') as fh:
        fh.write(code + "\n")
    count += 1

