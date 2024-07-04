import serial #to read from serial comms
from picamera import PiCamera #for camera module
from time import sleep
import RPi.GPIO as GPIO

camera = PiCamera() # allows me to control camera module
camera.rotation = 90 #rotate by 90 degrees

frame = 1 # for incrementing later
vid_num = 1 # for incrementing later
#use Broadcom pin mode
GPIO.setmode(GPIO.BCM)
#setup LED pins
R = 18
G = 19
B = 20
#setup push button pins
snap_mode = 17
rec_mode = 16
#setup of input pins
GPIO.setup(snap_mode, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(rec_mode, GPIO.IN, GPIO.PUD_DOWN)
#setup output pins
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)

mode = "snap_mode" #will be initially set to taking images only

def mode():
          while (True):
                    if (GPIO.input(rec_mode)):
                              #debounce the switch
                              while (GPIO.input(rec_mode)):
                                        sleep(0.1)
                              return "rec_mode"
                    if (GPIO.input(snap_mode)):
                              #debounce the switch
                              while (GPIO.input(snap_mode)):
                                        sleep(0.1)
                              return "snap_mode"
                    sleep(0.1)
while True:

          arduino = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)
          arduino.flush()
          try:          
                    mode = mode()
                    BPM = arduino.readline().decode('utf-8').rstrip()
                    #print(BPM)
                    if BPM.isdigit():
                              integer = int(BPM)
                              print(integer)
                              #print(type(integer))

                              if (int(BPM) > 97):
                                        if (mode == "snap_mode"):
                                                  # saves pic in following location with name
                                                  camera.capture('/home/pi/Documents/Camera project/frame%03d.jpg' % frame)
                                                  #format to at least 3 digits
                                                  GPIO.output(B, GPIO.HIGH)
                                                  sleep(1)
                                                  GPIO.output(B, GPIO.LOW)
                                                  frame += 1
                                                  sleep(3) #delay for 3 seconds
                                        elif (mode == "rec_mode"):
                                                  #save video in file location
                                                  GPIO.output(G, GPIO.HIGH)
                                                  camera.start_recording(f'/home/pi/Documents/Camera project/video_{vid_num:03d}.h264')
                                                  camera.wait_recording(5)
                                                  camera.stop_recording
                                                  GPIO.output(G, GPIO.LOW)
                                                  vid_num += 1
                                                  sleep(3)
                              if (int(BPM) < 50):
                                      GPIO.output(R, GPIO.HIGH)
                                      sleep(1)
                                      GPIO.output(R. GPIO.LOW)
          except:
                    #print("End")
                    GPIO.cleanup()
