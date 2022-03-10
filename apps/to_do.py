def toDoApp(display, utime, ujson, bluetooth, startNewThread, playBuzzer, loadJSON, saveJSON, showControls, update, clear):
        
    run = True
    toDo = loadJSON("to-do.json")
    toDoList = list(toDo.keys())
    index = 0
    
    utime.sleep(0.5)#Sleep cause else it exits the app
    
    while run:
        clear()
        
        #Draw the app
        showControls(display.get_width(), display.get_height(), "esc", "X", "/\\", "\/")
        if len(toDoList[index]) < 6:
            display.text(toDoList[index], display.get_width()//2 - (len(toDoList[index]) * 13) - 5 ,
                         display.get_height()//2 - 15, 500, 5) #Size 5
        elif len(toDoList[index]) < 10:
            display.text(toDoList[index], display.get_width()//2 - (len(toDoList[index]) * 10) - 7 ,
                         display.get_height()//2 - 15, 500, 4) #Size 4
        elif len(toDoList[index]) < 15:
            display.text(toDoList[index], display.get_width()//2 - (len(toDoList[index]) * 10) + 20,
                         display.get_height()//2 - 10, 500, 3) #Size 3
        else:
            display.text(toDoList[index], display.get_width()//2 - (len(toDoList[index]) * 6) + 20,
                         display.get_height()//2 - 10, 500, 2) #Size 2
        display.text("klaar: " + toDo[toDoList[index]], display.get_width()//2 - 20, display.get_height() - 20, 500, 2)
        
        #App Controls
        buttonPressed = False
        while display.is_pressed(display.BUTTON_X):
            if not buttonPressed:
                startNewThread(playBuzzer)
                index += 1
                if index == len(toDoList):
                    index = 0
            buttonPressed = True
         
        while display.is_pressed(display.BUTTON_Y):
            if not buttonPressed:
                startNewThread(playBuzzer)
                index -= 1
                if index < 0:
                    index = len(toDoList) - 1
            buttonPressed = True
            
        while display.is_pressed(display.BUTTON_A):
            if not buttonPressed:
                startNewThread(playBuzzer)
                run = False
                saveJSON("to-do.json", toDo)
            buttonPressed = True
       
        while display.is_pressed(display.BUTTON_B):
            if not buttonPressed:
                startNewThread(playBuzzer)
                if toDo[toDoList[index]] == " ":
                    toDo[toDoList[index]] = "X"
                else:
                    toDo[toDoList[index]] = " "
            buttonPressed = True
        buttonPressed = False
        
        update()