#Import needed libraries
import picodisplay as display
import _thread as thread
import uos, ujson, sys
from utime import sleep, localtime, time
import utime
from machine import Pin, UART

#Import Functions
# from tools import *

#Import apps
sys.path.insert(1, './apps/')
from set_brightness import brightnessApp
from set_time import setTimeApp
from to_do import toDoApp
from shopping_list import ShoppinglistApp
from sync import btSync
from jumpman import jumpmanApp
from quickman import quickmanApp


# Initialize display with a bytearray display buffer
width = display.get_width()   #240
height = display.get_height() #135
displayBuffer = bytearray(width * height * 2)# 2-bytes per pixel (RGB565)
display.init(displayBuffer)
display.set_backlight(0.5)
displayBrightness = 5
display.set_led(0,0,0)

#Initialize IO
buzzer = Pin(5, Pin.OUT)
bluetooth = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1, timeout=0)


#Initialize Vars
clock = ""
frameCounter = 1
setTime = 0
settings = {}
lowEnergyMode = False
jobs = []
lock = thread.allocate_lock()

#Functions
def showControls(width, height, symA, symB, symX, symY):
    display.text(symA, 5, 7, 50, 2) # a Button
    display.text(symB, 5, height - 20, 50, 2) # b Button
    display.text(symX, width - 20, 7, 50, 2) # x Button
    display.text(symY, width - 20, height - 20, 50, 2)  # y Button

def clear():
    display.clear()
    display.set_pen(255, 255, 255)

def update():
    startJob()
    display.update()
    display.set_pen(0, 0, 0)
    sleep(1/200)
    
def updateTime():
    global clock
    clock = "".join(str(localtime(time() + setTime)).replace("(", "").replace(")", "").split(",")[3:6])[1:]
    clock = clock.split(" ")
    
    for i in range(len(clock)):
        if len(clock[i]) < 2:
            clock[i] = "0" + clock[i]
    clock = ":".join(clock)
    
def showTime():
    display.text(clock, width//2 - len(clock) * 3 - 5 , height - 20, 500, 2)
        
def loadFile(fileName):
    with open(fileName) as file:
        txtFile = file.readlines()
    for i in range(len(txtFile)):
        txtFile[i] = txtFile[i][:-1]
    return txtFile

def loadJSON(fileName):
    with open(fileName) as file:
        txtFile = file.readlines()
    return ujson.loads(txtFile[0])

def saveJSON(fileName, jsonObject):
    data = ujson.dumps(jsonObject)
    with open(fileName, 'w') as file:
        file.write(data)

def loadSettings():
    global settings, setTime, displayBrightness
    settings = loadJSON("settings.json")
    setTime = settings["time"]
    display.set_backlight(settings["brightness"])
    displayBrightness = int(settings["brightness"] * 10)

def playBuzzer():
    buzzer.value(1)
    for i in range(15):
        sleep(0.01)
    buzzer.value(0)
    lock.release()

def startNewThread(job):
    global jobs
    jobs.append(job)
    
def startJob():
    global jobs
    if not lock.locked() and len(jobs) > 0:
        lock.acquire()
        thread.start_new_thread(jobs[0], ())
        jobs.remove(jobs[0])
    else:
        pass
    

def wakeUp():
    global frameCounter, lowEnergyMode
    loadSettings()
    lowEnergyMode = False
    frameCounter = 1
    

#Classes
class Menu:
    def __init__(self, menuName, menuEntries, icons):
        self.menuName = menuName
        self.menuEntries = menuEntries
        self.icons = icons
        self.index = 0
        self.buttonPressed = False
    
    def controls(self):
        global activeMenu, menuList, menuDepth, frameCounter
        while display.is_pressed(display.BUTTON_X):
            if not self.buttonPressed:
                startNewThread(playBuzzer)
                frameCounter = 1
                if lowEnergyMode:
                    wakeUp()
                else:
                    if self.index == len(self.menuEntries) - 1:
                        self.index = 0
                    else:
                        self.index += 1
            self.buttonPressed = True
            
            
        while display.is_pressed(display.BUTTON_Y):
            if not self.buttonPressed:
                startNewThread(playBuzzer)
                frameCounter = 1
                if lowEnergyMode:
                    wakeUp()
                else:
                    if self.index == 0:
                        self.index = len(self.menuEntries) - 1
                    else:
                        self.index -= 1
            self.buttonPressed = True
            
        while display.is_pressed(display.BUTTON_A):
            
            if not self.buttonPressed:
                startNewThread(playBuzzer)
                frameCounter = 1
                if lowEnergyMode:
                    wakeUp()
                else:
                    try:
                        for i in menuList:
                            if i.menuName == self.menuEntries[self.index]:
                                activeMenu = i
                                menuDepth.append(i)
                    except Exception as e: #Uncomment print for developing
                        # print(e)
                        pass
                    try:
                        apps[self.menuEntries[self.index]](display, utime, ujson, bluetooth, 
                                                           startNewThread, playBuzzer, loadJSON, saveJSON,
                                                           showControls, update, clear)
                        #sleep(1) #This somehow prevents a crash ;')
                        loadSettings()
                    except Exception as e: #Uncomment print for developing
                        print(e)
                        pass
            self.buttonPressed = True
            
        while display.is_pressed(display.BUTTON_B):
            if not self.buttonPressed:
                startNewThread(playBuzzer)
                frameCounter = 1
                if lowEnergyMode:
                    wakeUp()
                else:
                    if len(menuDepth) > 1:
                        menuDepth.pop()
                        activeMenu = menuDepth[-1]
                        self.index = 0
                self.buttonPressed = True
        self.buttonPressed = False

    def showMenuItem(self):
        if len(self.menuEntries[self.index]) < 6:
            display.text(self.menuEntries[self.index], width//2 - (len(self.menuEntries[self.index]) * 13) - 5 , height//2 - 15, 500, 5) #Size 5
        elif len(self.menuEntries[self.index]) < 10:
            display.text(self.menuEntries[self.index], width//2 - (len(self.menuEntries[self.index]) * 10) - 7 , height//2 - 15, 500, 4) #Size 4
        elif len(self.menuEntries[self.index]) < 15:
            display.text(self.menuEntries[self.index], width//2 - (len(self.menuEntries[self.index]) * 10) + 20, height//2 - 10, 500, 3) #Size 3
        else:
            display.text(self.menuEntries[self.index], width//2 - (len(self.menuEntries[self.index]) * 10) + 20, height//2 - 10, 500, 2) #Size 2
    
    def drawIcon(self):
        try:
            icon = self.icons[self.menuEntries[self.index]]
            for i in range(len(icon)):
                for j in range(len(icon)):
                    if icon[i][j] == "1":
                        display.pixel(width//2 - 16 + j, 5 + i)
        except:
            pass
    
    def getMenuName(self):
        return self.menuName[self.menuEntries[self.index]]
    
    
#Load Icons
icons = {}
for i in range(len(uos.listdir("/icons"))):
    try:
        icons[uos.listdir("/icons")[i][:-4]] = loadFile("icons/" + uos.listdir("/icons")[i])
    except:
        #print("Failed to get: " + menuList[i].getMenuName()) #uncomment for debugging
        pass

#Initialize menu classes
mainMenu = Menu("mainMenu", ["spellen", "opties", "to-do", "boodschappen", "synchroniseren", "STOP"], icons)
gamesMenu = Menu("spellen", ["jump-man", "quick-man"], icons)
optionsMenu = Menu("opties", ["helderheid", "tijd"], icons)
stopMenu = Menu("STOP", ["BYE"], icons)
activeMenu = mainMenu
menuDepth = [mainMenu]
menuList = [mainMenu, gamesMenu, optionsMenu, stopMenu] 

#Load Apps
apps = {"helderheid": brightnessApp,
        "tijd": setTimeApp,
        "to-do": toDoApp,
        "boodschappen": ShoppinglistApp,
        "synchroniseren": btSync,
        "jump-man": jumpmanApp,
        "quick-man": quickmanApp
        }

#Load Settings
loadSettings()
    
run = True

#Main Loop
while run:
    clear()
    
    if not lowEnergyMode:
        #Draw active menu
        showControls(width, height, "->", "<-", "/\\", "\/")
        activeMenu.showMenuItem()
        activeMenu.drawIcon()
        showTime()
        
        if activeMenu.menuName == "STOP":
            run = False
        
        frameCounter += 1
    
        #Enter low energy mode if not being used
        if frameCounter == 1000:
            lowEnergyMode = True
            display.set_backlight(0.0)

    activeMenu.controls()
    updateTime()
    
    update()
#Shut Down if run == False
display.set_backlight(0.0)

#TODO
    #Use other thread with a buffer for other things
        #.menuName == "STOP"
        #Update clock
        #Maybe Buttons
        #Because of the buffer now the buzzer plays after an app has loaded... but that's okay?
    #Finish up sync.py
    #Set Date App
    #graphical Glitch (happens if the program is too slow i think)
    #Make low energy mode
    #IRQ doesn't work yet with pico display pack's micropython (check for future update where it does)
    #Make Animations for menu