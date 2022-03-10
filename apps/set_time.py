def setTimeApp(display, utime, ujson, bluetooth, startNewThread, playBuzzer, loadJSON, saveJSON, showControls, update, clear):

    def updateTime():
        clock = "".join(str(utime.localtime(utime.time() + setTime)).replace("(", "").replace(")", "").split(",")[3:6])[1:]
        clock = clock.split(" ")
    
        for i in range(len(clock)):
            if len(clock[i]) < 2:
                clock[i] = "0" + clock[i]
        return ":".join(clock)
    
    run = True
    clock = ""
    index = 0
    settings = loadJSON("settings.json")
    setTime = settings["time"]
    
    utime.sleep(0.5)#Sleep cause else it exits the app
            
    while run:
        clear()
        
        #Draw the app
        showControls(display.get_width(), display.get_height(), "->", "<-", "/\\", "\/")
        display.text(clock, 20 , 50, 500, 5)
        display.text("_", 47 + (60 * index) , 60, 500, 5)
        
        buttonPressed = False
        while display.is_pressed(display.BUTTON_X):
            if not buttonPressed:
                startNewThread(playBuzzer)
                if index == 2:  
                    setTime += 1
                elif index == 1:
                    setTime += 60
                elif index == 0:
                    setTime += 3600
                settings["time"] = setTime
            buttonPressed = True
            
        while display.is_pressed(display.BUTTON_Y):
            if not buttonPressed:
                startNewThread(playBuzzer)
                if index == 2:  
                    setTime -= 1
                elif index == 1:
                    setTime -= 60
                elif index == 0:
                    setTime -= 3600
                settings["time"] = setTime
            buttonPressed = True
        
        while display.is_pressed(display.BUTTON_A):
            if not buttonPressed:
                startNewThread(playBuzzer)
                if index < 2:
                    index += 1
                else:
                    run = False
                    saveJSON("settings.json", settings)
            buttonPressed = True
                
            
        while display.is_pressed(display.BUTTON_B):
            if not buttonPressed:
                startNewThread(playBuzzer)
                if index > 0:
                    index -= 1
                else:
                    run = False
                    saveJSON("settings.json", settings)
            buttonPressed = True
        buttonPressed = False
        
        clock = updateTime()
        update()