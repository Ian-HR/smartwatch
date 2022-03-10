def ShoppinglistApp(display, utime, ujson, bluetooth, startNewThread, playBuzzer, loadJSON, saveJSON, showControls, update, clear):
        
    run = True
    shoppingItems = loadJSON("boodschappen.json")
    shoppingItemsList = list(shoppingItems.keys())
    index = 0
    
    utime.sleep(0.5)#Sleep cause else it exits the app
            
    while run:
        clear()
        
        #Draw the app
        showControls(display.get_width(), display.get_height(), "esc", "X", "/\\", "\/")

        if len(shoppingItemsList[index]) < 6:
            display.text(shoppingItemsList[index], display.get_width()//2 - (len(shoppingItemsList[index]) * 13) - 5 ,
                         display.get_height()//2 - 15, 500, 5) #Size 5
        elif len(shoppingItemsList[index]) < 10:
            display.text(shoppingItemsList[index], display.get_width()//2 - (len(shoppingItemsList[index]) * 10) - 7 ,
                         display.get_height()//2 - 15, 500, 4) #Size 4
        elif len(shoppingItemsList[index]) < 15:
            display.text(shoppingItemsList[index], display.get_width()//2 - (len(shoppingItemsList[index]) * 10) + 20,
                         display.get_height()//2 - 10, 500, 3) #Size 3
        else:
            display.text(shoppingItemsList[index], display.get_width()//2 - (len(shoppingItemsList[index]) * 6) + 20,
                         display.get_height()//2 - 10, 500, 2) #Size 2
        display.text("klaar: " + shoppingItems[shoppingItemsList[index]], display.get_width()//2 - 20,
                     display.get_height() - 20, 500, 2)
        
        #App Controls
        buttonPressed = False
        
        while display.is_pressed(display.BUTTON_X):
            if not buttonPressed:
                startNewThread(playBuzzer)
                index += 1
                if index == len(shoppingItemsList):
                    index = 0
            buttonPressed = True
         
        while display.is_pressed(display.BUTTON_Y):
            if not buttonPressed:
                startNewThread(playBuzzer)
                index -= 1
                if index < 0:
                    index = len(shoppingItemsList) - 1
            buttonPressed = True
            
        while display.is_pressed(display.BUTTON_A):
            if not buttonPressed:
                startNewThread(playBuzzer)
                run = False
                saveJSON("boodschappen.json", shoppingItems)
            buttonPressed = True
       
        while display.is_pressed(display.BUTTON_B):
            if not buttonPressed:
                startNewThread(playBuzzer)
                if shoppingItems[shoppingItemsList[index]] == " ":
                    shoppingItems[shoppingItemsList[index]] = "X"
                else:
                    shoppingItems[shoppingItemsList[index]] = " "
            buttonPressed = True
        buttonPressed = False
        
        update()
    