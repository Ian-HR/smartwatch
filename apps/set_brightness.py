def brightnessApp(display, utime, ujson, bluetooth, startNewThread, playBuzzer, loadJSON, saveJSON, showControls, update, clear):

    run = True
    settings = loadJSON("settings.json")
    display.set_backlight(settings["brightness"])
    displayBrightness = int(settings["brightness"] * 10)
            
    while run:        
        clear()
        
        #Draw the app
        showControls(display.get_width(), display.get_height(), "", "<-", "+", "-")
        display.text("Helderheid: " + str(displayBrightness), 20 , 60, 500, 3)

        #App Controls 
        buttonPressed = False
        while display.is_pressed(display.BUTTON_X):
            if not buttonPressed and displayBrightness < 10:
                startNewThread(playBuzzer)
                displayBrightness += 1
                display.set_backlight(displayBrightness/10)
                settings["brightness"] = displayBrightness/10
            buttonPressed = True
            
        while display.is_pressed(display.BUTTON_Y):
            if not buttonPressed and displayBrightness > 1:
                startNewThread(playBuzzer)
                displayBrightness -= 1
                display.set_backlight(displayBrightness/10)
                settings["brightness"] = displayBrightness/10
            buttonPressed = True
        
        while display.is_pressed(display.BUTTON_A):
            pass
            
        while display.is_pressed(display.BUTTON_B):
            if not buttonPressed and displayBrightness > 1:
                startNewThread(playBuzzer)
                run = False
                saveJSON("settings.json", settings)
            buttonPressed = True
    
        buttonPressed = False
    
        update()
    
    