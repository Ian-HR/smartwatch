def btSync(display, utime, ujson, bluetooth, startNewThread, playBuzzer, loadJSON, saveJSON, showControls, update, clear):

    run = True
    toDo = loadJSON("to-do.json")
    toDoList = list(toDo.keys())
    toDoDone = False
    shoppingItems = loadJSON("boodschappen.json")
    shoppingItemsList = list(shoppingItems.keys())
    shoppingItemsDone = False
    index = 0
    
    utime.sleep(0.5)#Sleep cause else it exits the app
    
    cnt = 0
    btData = ""
    
    while run:
        clear()
        
        #Get and format Bluetooth data
        
        if not toDoDone or not shoppingItemsDone:
            try:
                btData += bluetooth.read().decode("utf-8")
                if btData[0] == "[" and btData[-1] == "]":
                    print("valid data")
                    btData = ujson.loads(btData)
                    for i in range(1, len(btData)):
                        btData[i] = ujson.loads(btData[i])
                    print(btData)
                    if btData[0] == "to-do" and not toDoDone and len(btData) > 1:
                        print("TODO")
                        newDict = {}
                        for i in range(1, len(btData)):
                            newDict[btData[i]["name"]] = "x" if btData[i]["isComplete"] else " "
                        saveJSON("to-do.json", newDict)
                        toDoDone = True
                        print(newDict)
                    elif btData[0] == "boodschappen" and not shoppingItemsDone and len(btData) > 1:
                        newDict = {}
                        for i in range(1, len(btData)):
                            newDict[btData[i]["name"]] = "x" if btData[i]["checked"] else " "
                        saveJSON("boodschappen.json", newDict)
                        shoppingItemsDone = True
                        print(newDict)
                else:
                    print("INVALID_DATA")
                    bluetooth.write("INVALID_DATA")
            except:
                pass
        
        #Draw the app
        showControls(display.get_width(), display.get_height(), "esc", " ", " ", " ")
        if toDoDone and shoppingItemsDone:
            display.text("Sync: Klaar!", 20,
                        display.get_height()//2 - 10, 500, 3)
            if cnt == 10:
                bluetooth.write("ALL_DONE")
            if cnt > 100:
                cnt = 0
        elif cnt < 60:
            display.text("Sync: ." , 20,
                        display.get_height()//2 - 10, 500, 3)
        elif cnt < 120:
            display.text("Sync: ..", 20,
                        display.get_height()//2 - 10, 500, 3)
        elif cnt < 180:
            display.text("Sync: ...", 20,
                        display.get_height()//2 - 10, 500, 3)
        else:
            cnt = 0
            if toDoDone and shoppingItemsDone:
                pass
            elif toDoDone:
                bluetooth.write("BOODSCHAPPEN")
            else:
                bluetooth.write("TO-DO")
                pass
            print("WORKING") #<- remove this later fag
            btData = ""
        cnt += 1
                
        #App Controls
        buttonPressed = False
        while display.is_pressed(display.BUTTON_X):
            if not buttonPressed:
                startNewThread(playBuzzer)
            buttonPressed = True
         
        while display.is_pressed(display.BUTTON_Y):
            if not buttonPressed:
                startNewThread(playBuzzer)
            buttonPressed = True
            
        while display.is_pressed(display.BUTTON_A):
            if not buttonPressed:
                startNewThread(playBuzzer)
                run = False
            buttonPressed = True
       
        while display.is_pressed(display.BUTTON_B):
            if not buttonPressed:
                startNewThread(playBuzzer)
            buttonPressed = True
        buttonPressed = False
        
        update()
    
    
    

