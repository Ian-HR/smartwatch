def jumpmanApp(display, utime, ujson, bluetooth, startNewThread, playBuzzer, loadJSON, saveJSON, showControls, update, clear):
   
    width = display.get_width()   #240
    height = display.get_height() #135

    def drawDude(x, y):
        display.rectangle(x+5,y-40,10,10)#Head
        display.rectangle(x-15,y-30,15,5)#Left Arm 
        display.rectangle(x+20,y-30,15,5)#right Arm 
        display.rectangle(x,y-30,20,30)#Body
        display.rectangle(x,y,5,20)#Left Leg
        display.rectangle(x+15,y,5,20)#Right Leg

    def drawBox(x, y):
        display.rectangle(x,y,10,20)#Head
        
    settings = loadJSON("settings.json")

    x = 50
    y = height - 20

    jump = False
    jumpCnt = 0
    frameCnt = 0

    box = False
    boxX = width
    boxY = height - 20
    
    dead = False

    score = 0

    run = True

    while run:    
        clear()
        
        showControls(width, height, "", "X", "", "/\\")
        
        drawDude(x, y)
        
        if box:
            drawBox(boxX, boxY)
            boxX -= 3
            if boxX < -20:
                box = False
                score += 1
        
        display.text("Score: " + str(score), width//2 - 30 , 20, 500, 2)
        
        buttonPressed = False
        if not jump:
            while display.is_pressed(display.BUTTON_X):
                if not buttonPressed:
                    startNewThread(playBuzzer)
                buttonPressed = True
                
            while display.is_pressed(display.BUTTON_Y):
                if not buttonPressed:
                    startNewThread(playBuzzer)
                    jump = True
                    jumpCnt = 60
                buttonPressed = True

            while display.is_pressed(display.BUTTON_A):
                if not buttonPressed:
                    startNewThread(playBuzzer)
                buttonPressed = True
                
            while display.is_pressed(display.BUTTON_B):
                if not buttonPressed:
                    startNewThread(playBuzzer)
                    run = False
                    pass
                buttonPressed = True
                
            buttonPressed = False
        
        if jump:
            if jumpCnt == 0:
                jump = False
            elif jumpCnt > 30:
                y -= 2
                jumpCnt -= 1
            elif jumpCnt <= 30:
                y += 2
                jumpCnt -= 1
                
        if boxX in range(x, x+20) and boxY <= y:
            dead = True
        
        
        if frameCnt != 60:
            frameCnt += 1
        else:
            frameCnt = 1
            
        if not box and frameCnt == 60:
            box = True
            boxX = width
            boxY = height - 20
        
        update()
        
        while dead:
            
            clear()
            
            if score > settings["jumpmanHS"]:
                settings["jumpmanHS"] = score
                saveJSON("settings.json", settings)
            
            showControls(width, height, "", "X", "", "<3")
            
            display.text("High-Score: " + str(settings["jumpmanHS"]), width//2 - 50 , 40, 500, 2)
            display.text("Score: " + str(score), width//2 - 50 , 20, 500, 2)
            display.text("Game-Over", width//2 - 100 , height - 60, 500, 4)
            
            
            buttonPressed = False
            if not jump:
                while display.is_pressed(display.BUTTON_X):
                    if not buttonPressed:
                        startNewThread(playBuzzer)
                    buttonPressed = True
                    
                while display.is_pressed(display.BUTTON_Y):
                    if not buttonPressed:
                        startNewThread(playBuzzer)
                        x = 50
                        y = height - 20
                        jump = False
                        jumpCnt = 0
                        frameCnt = 0
                        box = False
                        boxX = width
                        boxY = height - 20
                        score = 0
                        dead = False
                    buttonPressed = True

                while display.is_pressed(display.BUTTON_A):
                    if not buttonPressed:
                        startNewThread(playBuzzer)
                    buttonPressed = True
                    
                while display.is_pressed(display.BUTTON_B):
                    if not buttonPressed:
                        startNewThread(playBuzzer)
                        run = False
                        dead = False
                    buttonPressed = True
                    
                buttonPressed = False
                
            update()
            
