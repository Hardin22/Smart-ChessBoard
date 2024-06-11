#chiamata dopo che il sensore di pressione rileva qualcosa

showlegalmoves()
    if square_isempty():
        pylabel("nessun pezzo sulla casella")
        pass
    else:
        listoflegalmoves = engine.showlegalmoves()
        sendtoesp32(listoflegalmoves)



