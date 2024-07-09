import serial # to read from serial comms
from picamera import PiCamera # for camera module
from time import sleep
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

camera = PiCamera() # allows me to control camera module
camera.rotation = 180 # rotate by 90 degrees

#for incrementing later
frame = 1
vid_num = 1

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
GPIO.setup(snap_mode, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(rec_mode, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#setup output pins
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)

current_mode = "snap_mode"

def OFF_LED(): # turn off
          GPIO.output(R, GPIO.LOW)
          GPIO.output(G, GPIO.LOW)
          GPIO.output(B, GPIO.LOW)

def R_LED(): # red
          GPIO.output(R, GPIO.HIGH)
          GPIO.output(G, GPIO.LOW)
          GPIO.output(B, GPIO.LOW)

def B_LED(): # blue
          GPIO.output(R, GPIO.LOW)
          GPIO.output(G, GPIO.LOW)
          GPIO.output(B, GPIO.HIGH)
def G_LED(): # green
          GPIO.output(R, GPIO.LOW)
          GPIO.output(G, GPIO.HIGH)
          GPIO.output(B, GPIO.LOW)
def W_LED(): # white
          GPIO.output(R, GPIO.HIGH)
          GPIO.output(G, GPIO.HIGH)
          GPIO.output(B, GPIO.HIGH)

def P_LED(): # purple
          GPIO.output(R, GPIO.HIGH)
          GPIO.output(G, GPIO.LOW)
          GPIO.output(B, GPIO.HIGH)


def get_mode(): # setting mode of files being saved, either recording or snapshot
          global current_mode
          
          while (True):
                    if (GPIO.input(rec_mode)): #
                              B_LED()
                              current_mode = "rec_mode"
                              sleep(0.5)
                              OFF_LED()
                              return current_mode
                    elif GPIO.input(snap_mode): #
                              W_LED()
                              current_mode = "snap_mode"
                              sleep(0.5)
                              OFF_LED()
                              return current_mode
                    else:
                              return current_mode #return previously set mode

                    sleep(0.1)

try:

          arduino = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)
          arduino.flush()
          
          while True:
                    #print("checking mode...")
                    current_mode = get_mode()
                    #mode = mode()
                    #print(f"current mode: {current_mode}")
                    BPM = arduino.readline().decode('utf-8').rstrip()
                    #print(f"Read BPM: {BPM}")
                    
                    
                    if BPM.isdigit():
                              integer = int(BPM)
                              #print(integer)
                              print(f" BPM: {integer}")

                              if (int(BPM) > 97): # 97 to be safe
                                        if (current_mode == "snap_mode"):
                                                  print("taking a pic")
                                                  # saves pic in following location with name
                                                  camera.capture('/media/pi/31 GB Volume/image%03d.jpg' % frame)
                                                  P_LED()
                                                  sleep(1)
                                                  OFF_LED()

                                                  frame += 1
                                                  sleep(1) #delay for 3 seconds
                                                  
                                        elif (current_mode == "rec_mode"):
                                                  print("taking a vid")
                                                  G_LED()
                                                  
                                                  video_filename = f'/media/pi/31 GB Volume/video_{vid_num:03d}.h264'
                                                  
                                                  #save video in file location
                                                  camera.start_recording(video_filename)
                                                  camera.wait_recording(3)
                                                  camera.stop_recording()
                                                  
                                                  OFF_LED()
                                                  
                                                  vid_num += 1
                                                  sleep(1)
                                                  
                              elif (int(BPM) < 50):
                                        print("BPM is less than 50")
                                        R_LED()
                                        sleep(1)
                                        OFF_LED()
                    else:
                              print("invalid bpm reading")

finally:
          try:
                    camera.stop_recording()
          except:
                    pass
          camera.close()
          GPIO.cleanup()
