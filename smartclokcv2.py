

from machine import Pin, ADC, I2C, RTC

from micropython import const
import utime 
import framebuf
from sh1106 import SH1106, SH1106_I2C
import random


#if needed, overwrite default time server
import time

import ntptime
import network

# Replace these with your Wi-Fi credentials
SSID ="FiberHGW_TP8966_2.4GHz"
PASSWORD ="fY3cNuKR"

def connect_to_wifi(ssid, password):
    """Connect to a Wi-Fi network."""
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if not sta.isconnected():
        print("Connecting to Wi-Fi...")
        sta.connect(ssid, password)
        while not sta.isconnected():
            time.sleep(2)
            pass
    print("Connection successful:", sta.ifconfig())

def sync_time():
    """Synchronize time using NTP."""
    try:
        ntptime.settime()
        print("Time synchronized with NTP server.")
    except Exception as e:
        print("Failed to synchronize time:", e)


    """Main function to connect to Wi-Fi and fetch the current time."""
    

  

    
connect_to_wifi(SSID, PASSWORD)
sync_time()

dt = time.localtime()
dt=list(dt)

print("Current time:", 
"{:04}-{:02}-{:02} {:02}:{:02}:{:02}"
.format(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5]))




#from ir_rx import IR_RX, NEC_ABC, NEC_8

_SET_CONTRAST        = const(0x81)
_SET_NORM_INV        = const(0xa6)
_SET_DISP            = const(0xae)
_SET_SCAN_DIR        = const(0xc0)
_SET_SEG_REMAP       = const(0xa0)
_LOW_COLUMN_ADDRESS  = const(0x00)
_HIGH_COLUMN_ADDRESS = const(0x10)
_SET_PAGE_ADDRESS    = const(0xB0)


# Button Pins

esc = Pin(12, Pin.IN)
OK = Pin(35, Pin.IN)
shutdown = Pin(16, Pin.IN)
b2 = Pin(2, Pin.IN)

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

# I2C setup
sda = Pin(21)
scl = Pin(22)
i2c = I2C(0, sda=sda, scl=scl)

# Screen size
width = 128
height = 64
oled = SH1106_I2C(width, height, i2c, Pin(4), 0x3c)

trigx=[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9]
trigy=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 3, 4, 5, 6, 7, 8, 9, 10, 4, 5, 6, 7, 8, 9, 5, 6, 7, 8, 6, 7]
oled.flip() #origin becomes top left

"""oled.fill(0)
oled.text("Brightness",15,0,1)
oled.text("Temperature",15,15,1)
oled.text("Dinasour Game",15,30,1)   #Add buzzer for sound 
oled.show()

  for i in range(0,len(trigx)):
  oled.pixel(trigx[i],trigy[i],1)
  
oled.show()"""

trigy2=trigy
trigy3=trigy

bx= [5, 5, 6, 6, 7, 7, 8, 8, 8, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 11, 11, 12, 12, 12, 12, 12,  #bird
13, 13, 13, 14, 14, 14, 14, 14, 15, 15, 15, 15, 16, 16, 16, 16, 16]
bx_initial=bx[::]
by= [26, 27, 25, 28, 25, 29, 24, 25, 29, 23, 24, 25, 26, 29, 23, 26, 27, 28,
29, 23, 30, 23, 24, 25, 26, 30, 23, 27, 30, 23, 24, 25, 27, 30, 23, 27, 29, 30, 24, 25, 26, 27, 28]
dt[3]+=3
while True:
  oled.fill(0)
  oled.text("Brightness",15,0,1)
  oled.text("Clock and Date",15,15,1)
  oled.text("Dinasour Game",15,30,1)
  
  pot_value = pot.read()
  pot_value=int(pot_value*10000/4095)
  if shutdown.value()==1:
    oled.poweroff()
  if 3000>pot_value>=0:                    #BRIGHTNESS    this part is fine maybe toogle switch
    for i in range(0,len(trigx)):
      oled.pixel(trigx[i],trigy[i],1)
      oled.pixel(trigx[i],trigy2[i],0)
      oled.pixel(trigx[i],trigy3[i],0)
      if OK.value()==1:
        while esc.value()==0:
          oled.fill(0)
          pot_value = pot.read()
          pot_value=int(pot_value*10000/4095)
          x=(int(pot_value*255/10000))
          oled.text(f"Brightness : {x}" ,0,16,1)
          oled.contrast(int(pot_value*255/10000))
          oled.show()
          
            
       
  elif 6000>pot_value>2999:
    trigy2=list(map(lambda n:n+15, trigy))
    for i in range(0,len(trigx)):
      oled.pixel(trigx[i],trigy[i],0)
      oled.pixel(trigx[i],trigy2[i],1)
      oled.pixel(trigx[i],trigy3[i],0)
      if OK.value()==1:       #CLOCK AND DATE
        while esc.value()==0:
          oled.show()
          
          dt=time.localtime()
          dt=list(dt)
         
          oled.fill(0)
          oled.text(f"{dt[2]}/{dt[1]}/{dt[0]}",5,0,1)
          oled.text(f"{dt[3]+3}:{dt[4]}: {dt[5]}",5,25,1)     #to adjust timezone
          oled.show()
          
            
  else:                          #GAME
    trigy3=list(map(lambda n:n+30, trigy))
    for i in range(0,len(trigx)):
      oled.pixel(trigx[i],trigy[i],0)
      oled.pixel(trigx[i],trigy2[i],0)
      oled.pixel(trigx[i],trigy3[i],1)
    flappy_bird=True
    if OK.value()==1:
      oled.fill(0)
      startx=50
      difficulty=8
      hole=random.randint(18,32)
      hole_width=random.randint(4,difficulty)
            
      pot_value = pot.read()
      pot_value=int(pot_value*10000/4095)
      upperbound=hole+hole_width
      lowerbound=hole-hole_width
        
      while esc.value()==0:
        oled.fill(0)
        pot_value = pot.read()
        pot_value=int(pot_value*10000/4095)
        for i in range(0,len(by)):                           #THERE IS A PROBLEM
            if startx in bx:
                if by[i]>upperbound or by[i]<lowerbound:
                    
                    #print(upperbound,lowerbound)
                    #print(by[i])
                    oled.fill(0)
                    oled.text("game over",4,0,1)
                    break
            else:
              continue
        if flappy_bird==True:
            
            oled.fill(0)
            
            life=3
            if startx==0:
              difficulty=8
              hole=random.randint(26,40)
              hole_width=random.randint(4,difficulty)
                  
           
              upperbound=hole+hole_width
              lowerbound=hole-hole_width
        
              startx=63

            """hole=random.randint(16,30)
            hole_width=random.randint(4,difficulty)
            
            pot_value = pot.read()
            pot_value=int(pot_value*10000/4095)"""
            
            oled.vline(startx,0,lowerbound,1)
            oled.vline(startx,upperbound,64,1)
            oled.vline(startx+1,0,64,0)
            #oled.show()
            
            startx-=1
            position=pot_value//156
            
            
            for i in range(0,len(by),1):
              oled.pixel(bx[i],by[i],0)
            
            max_height=max(by)
            position_diff=position-max_height
            by=list(map(lambda n:n+position_diff,by))
            
            
            for i in range(0,len(by),1):
              oled.pixel(bx[i],by[i],1)
            oled.show()
            
           
            
           
              
            
            # ORIGIN TOP LEFT
        
  oled.show()
  dt=time.localtime()
  dt=list(dt)














