def quickmanApp(display, utime, ujson, bluetooth, startNewThread, playBuzzer, loadJSON, saveJSON, showControls, update, clear):

    width = display.get_width()   #240
    height = display.get_height() #135
        
    settings = loadJSON("settings.json")

    frameCnt = 0
    go = False
    score = 0
    missed = False
    hit = False

    run = True

    while run:    
        clear()        
        
        showControls(width, height, "", "X", "", "!")
        
        if not go:
            display.text("Ready?", width//2 - 60 , height//2 - 15, 500, 4)
        else:
            display.text("GO" , width//2 - 30 , height//2 - 15, 500, 5)            
        
        buttonPressed = False
        while display.is_pressed(display.BUTTON_X):
            if not buttonPressed:
                startNewThread(playBuzzer)
            buttonPressed = True
            
        while display.is_pressed(display.BUTTON_Y):
            if not buttonPressed:
                startNewThread(playBuzzer)
                if go:
                    hit = True
                else:
                    missed = True
                    score = 0
            buttonPressed = True

        while display.is_pressed(display.BUTTON_A):
            if not buttonPressed:
                startNewThread(playBuzzer)
            buttonPressed = True
            
        while display.is_pressed(display.BUTTON_B):
            if not buttonPressed:
                frameCnt = 0
                run = False
                pass
            buttonPressed = True
        buttonPressed = False
        
  
        frameCnt += 1
        
        if frameCnt == 100:
            go = True
        
        if frameCnt == 200:
            go = False
            missed = True
            score = 0
        
        update()
        
        while missed:
            clear()
            
            showControls(width, height, "", "X", "", "<3")
            
            display.text("High-Score: " + str(settings["quickmanHS"]), width//2 - 50 , 40, 500, 2)
            display.text("Score: " + str(score), width//2 - 50 , 20, 500, 2)
            display.text("MIS!", width//2 - 40 , height - 40, 500, 4)            
            
            buttonPressed = False
            while display.is_pressed(display.BUTTON_X):
                if not buttonPressed:
                    startNewThread(playBuzzer)
                buttonPressed = True
                    
            while display.is_pressed(display.BUTTON_Y):
                if not buttonPressed:
                    frameCnt = 0
                    go = False
                    score = 0
                    missed = False
                    hit = False
                buttonPressed = True

            while display.is_pressed(display.BUTTON_A):
                if not buttonPressed:
                    startNewThread(playBuzzer)
                buttonPressed = True
                
            while display.is_pressed(display.BUTTON_B):
                if not buttonPressed:
                    startNewThread(playBuzzer)
                    run = False
                    hit = False
                    missed = False
                buttonPressed = True
            buttonPressed = False
                
            update()
            
        while hit:
            clear()
            
            score = 100 - (frameCnt - 99)
            if score > settings["quickmanHS"]:
                settings["quickmanHS"] = score
                saveJSON("settings.json", settings)
            
            showControls(width, height, "", "X", "", "<3")
            
            display.text("High-Score: " + str(settings["quickmanHS"]), width//2 - 50 , 40, 500, 2)
            display.text("Score: " + str(score), width//2 - 50 , 20, 500, 2)
            display.text("RAAK!", width//2 - 40 , height - 40, 500, 4)            
            
            buttonPressed = False
            while display.is_pressed(display.BUTTON_X):
                if not buttonPressed:
                    startNewThread(playBuzzer)
                buttonPressed = True
                    
            while display.is_pressed(display.BUTTON_Y):
                if not buttonPressed:
                    frameCnt = 0
                    go = False
                    score = 0
                    missed = False
                    hit = False
                buttonPressed = True

            while display.is_pressed(display.BUTTON_A):
                if not buttonPressed:
                    startNewThread(playBuzzer)
                buttonPressed = True
                
            while display.is_pressed(display.BUTTON_B):
                if not buttonPressed:
                    startNewThread(playBuzzer)
                    run = False
                    hit = False
                    missed = False
                buttonPressed = True
                
            buttonPressed = False
                
            update()
            


