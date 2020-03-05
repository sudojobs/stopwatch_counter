import RPi.GPIO as GPIO
import pygame, sys
import time
from pygame.locals import *
import threading
cnt =0
down=0
starti= 0
start=0
first =1
prev_inp=1
elapsed =0

def start_funct(channel):
    global down
    global starti
    global cnt
    global first
    print("Button Pressed")
    print(cnt)
    down=1
    cnt=cnt+1
    if(first==1):
       starti=1
       first =0

def reset_funct(channel):
    global down
    global cnt
    global starti
    global first
    global msg
    global windowSurffaceObj 
    global msgSurfaceObj
    global cntSuraceObj
    starti =0
    first =1
    down=0
    cnt =0

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
switch = 7  # pin 7
reset  = 11  # pin 11
GPIO.setup(switch,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(reset,GPIO.IN, pull_up_down=GPIO.PUD_UP)
redColor = pygame.Color(255,0,0)
blackColor = pygame.Color(0,0,0)
whiteColor = pygame.Color(255,255,255)
pygame.init()
width = 1400
height = 1200
GPIO.add_event_detect(switch,GPIO.FALLING,callback=start_funct,bouncetime=2000) # Setup event on pin 10 rising edge
GPIO.add_event_detect(reset,GPIO.FALLING,callback=reset_funct,bouncetime=200) # Setup event on pin 10 rising edge
windowSurfaceObj = pygame.display.set_mode((0,0),FULLSCREEN)
#windowSurfaceObj = pygame.display.set_mode((width,height),1,24)
pygame.display.set_caption('STOPWATCH')
fontObj = pygame.font.Font('freesansbold.ttf',200)
msg = "00:00:00:000"
msgSurfaceObj = fontObj.render(msg, False,redColor)
cntSurfaceObj = fontObj.render(str(cnt), False,whiteColor)
msgRectobj = msgSurfaceObj.get_rect()
msgRectobj.center=(1000,200) 
cntRectobj=cntSurfaceObj.get_rect()
cntRectobj.bottomright=(1000,700) 
windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
windowSurfaceObj.blit(cntSurfaceObj, cntRectobj)

pygame.display.update()

try:
   running=True
   while running :
     if starti  == 1:
            start = time.time()
            starti =0 
     if down == 1:
         now = time.time() - start
         m,s = divmod(now,60)
         h,m = divmod(m,60)
         msg= "%02d:%02d:%02d" % (h,m,s)
         psec = str(now-int(now))
         pstr = psec[1:5]
         msg = msg + str(pstr)
         pygame.draw.rect(windowSurfaceObj,blackColor,Rect(0,0,width,height))
         windowSurfaceObj.fill(blackColor)
         msgSurfaceObj = fontObj.render(msg, False,redColor)
         msgRectobj = msgSurfaceObj.get_rect()
         msgRectobj.center=(1000,200)
         cntSurfaceObj = fontObj.render(str(cnt), False,whiteColor)
         cntRectobj = cntSurfaceObj.get_rect()
         cntRectobj.bottomright=(1000,700)
         windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
         windowSurfaceObj.blit(cntSurfaceObj, cntRectobj)
         pygame.display.update()
     else :
         windowSurfaceObj.fill(blackColor)
         msg = "00:00:00:000"
         msgSurfaceObj = fontObj.render(msg, False,redColor)
         msgRectobj = msgSurfaceObj.get_rect()
         msgRectobj.center=(1000,200) 
         cntSurfaceObj = fontObj.render("0", False,whiteColor)
         cntRectobj = cntSurfaceObj.get_rect()
         cntRectobj.bottomright=(1000,700) 
         windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
         windowSurfaceObj.blit(cntSurfaceObj, cntRectobj)
         pygame.display.update()

     for event in pygame.event.get():
         if event.type == QUIT:
               pygame.quit()
               running  = False 
         elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  # Set running to False to end the while loop.
                sys.exit()
except KeyboardInterrupt:
  print "Quit"
  GPIO.cleanup()
