import cv2

import numpy as np

import matplotlib.pyplot as plt

#Pegando o vídeo
cap = cv2.VideoCapture('pedra-papel-tesoura.mp4')

player1_points = 0
player2_points = 0
previous_moves = []

res = ""
#Expection se o Vídeo não abrir
if not cap.isOpened():
    raise Exception("Erro ao abrir o vídeo!")

while True:

    #Lendo os frames do vídeo
    ret, frame = cap.read()

    foto = frame.copy() #Copio o frame para fazer outro retorno

    #Aplicando filtro de cinza
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Aplicando suavização na imagem
    img = cv2.blur(img_hsv, (15, 15), 0)

    #Criando os ranges para as mascáras HSV
    hsv_low1 = np.array([0, 20, 10])
    hsv_up1 = np.array([18, 200, 200])
    hsv_low2 = np.array([0, 1, 1])
    hsv_up2 = np.array([255, 150, 250])

    #Criando as mascaras
    mask1 = cv2.inRange(img, hsv_low1, hsv_up1)
    mask2 = cv2.inRange(img, hsv_low2, hsv_up2)

    #Juntando as mascaras
    img_filtro = cv2.bitwise_or(mask1, mask2)

    #Encontrando os contornos da imagem
    contours, _ = cv2.findContours(img_filtro, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Desenhando os contornos
    cv2.drawContours(foto, contours, -1, [0, 0, 255], 5)

    #Criando listas de contornos de acordo com a posição encontrada para identificar os Players 1 e 2
    c1 = contours[1]
    c2 = contours[0]

    #Pegando os momentos dos contornos para pegar a área
    m1 = cv2.moments(c1)
    m2 = cv2.moments(c2)
    

    #Pegando as áreas dos contornos (mãos dos jogadores)
    area1 = int(m1['m00'])
    area2 = int(m2['m00'])

    # Lógica para definir os tipos de objeto de acordo com sua área total (Player 1)
    if area1 < 58000:
        area1 = "Scissors"

    elif area1 > 58000 and area1 < 70000:
        area1 = "Rock"

    elif area1 > 70000:
        area1 = "Paper"

    # Lógica para definir os tipos de objeto de acordo com sua área total (Player 2)
    if area2 < 58000:
        area2 = "Scissors"

    elif area2 > 58000 and area2 < 70000:
        area2 = "Rock"

    elif area2 > 70000:
        area2 = "Paper"

    #Inversão para uma Das Detecções que foram processadas invertidas
    if area1 == "Rock" and area2 == "Scissors":
        area1 = "Scissors"
        area2 = "Rock"

    if len(previous_moves) == 0:
        if area1 == area2:
            res = "Draw!"
            previous_moves.append((area1, area2))
        elif (area1 == "Scissors" and area2 == "Paper"):
                res = "Player 1 Win!"
                player1_points = player1_points + 1
                previous_moves.append((area1, area2))
        elif (area1 == "Paper" and area2 == "Scissors"):
            res = "Player 2 Win!"
            player2_points = player2_points + 1
            previous_moves.append((area1, area2))
        elif (area1 == "Rock" and area2 == "Scissors"):
            res = "Player 1 Win!"
            player1_points = player1_points + 1
            previous_moves.append((area1, area2))
        elif (area1 == "Scissors" and area2 == "Rock"):
            res = "Player 2 Win!"
            player2_points = player2_points + 1
            previous_moves.append((area1, area2))
        elif (area1 == "Paper" and area2 == "Rock"):
            res = "Player 1 Win!"
            player1_points = player1_points + 1
            previous_moves.append((area1, area2))
        elif (area1 == "Rock" and area2 == "Paper"):
            res = "Player 2 Win!"
            player2_points = player2_points + 1
            previous_moves.append((area1, area2))
    else:
        if (area1, area2) != previous_moves[-1]:
            # atualizar as pontuações de acordo com a jogada atual
            if area1 == area2:
                res = "Draw!"
                previous_moves.append((area1, area2))
            elif (area1 == "Scissors" and area2 == "Paper"):
                res = "Player 1 Win!"
                player1_points = player1_points + 1
                previous_moves.append((area1, area2))
            elif (area1 == "Paper" and area2 == "Scissors"):
                res = "Player 2 Win!"
                player2_points = player2_points + 1
                previous_moves.append((area1, area2))
            elif (area1 == "Rock" and area2 == "Scissors"):
                res = "Player 1 Win!"
                player1_points = player1_points + 1
                previous_moves.append((area1, area2))
            elif (area1 == "Scissors" and area2 == "Rock"):
                res = "Player 2 Win!"
                player2_points = player2_points + 1
                previous_moves.append((area1, area2))
            elif (area1 == "Paper" and area2 == "Rock"):
                res = "Player 1 Win!"
                player1_points = player1_points + 1
                previous_moves.append((area1, area2))
            elif (area1 == "Rock" and area2 == "Paper"):
                res = "Player 2 Win!"
                player2_points = player2_points + 1
                previous_moves.append((area1, area2))

    #Título
    (cv2.putText(foto, "Rock, Paper, Scissors: LET'S PLAY!",(415, 50), cv2.FONT_HERSHEY_DUPLEX,2, (0, 0, 0), 2, cv2.LINE_AA))

    #Jogada do Player 1
    (cv2.putText(foto, ("Player 1: " + str(area1)), (25, 150), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA))
    
    #Jogada do Player 2
    (cv2.putText(foto, ("Player 2: " + str(area2)), (25, 250), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA))
    
    #Resultado da Jogada
    (cv2.putText(foto, str(res), (650, 1000), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA))
    
    #Pontuação do Player 1
    (cv2.putText(foto, ("Pontos Player 1 = " + str(player1_points)), (1100, 150), cv2.FONT_HERSHEY_DUPLEX, 2,(0, 0, 255), 2, cv2.LINE_AA))
    
    # Pontuação do Player 2
    (cv2.putText(foto,("Pontos Player 2 = " + str(player2_points)), (1100, 250), cv2.FONT_HERSHEY_DUPLEX, 2,(0, 0, 255), 2, cv2.LINE_AA))
    
    #Criando as janelas de output
    frame = cv2.resize(img_filtro, (640, 480))
    img_final = cv2.resize(foto, (640, 480))

    #Mostrando as janelas
    cv2.imshow("Detecção", frame)

    cv2.imshow("Gameplay", img_final)

    #Finalizar o programa apertando a tecla Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if not ret:
        break

#Printando os momentos dos contornos (ajudou a decidir como fazer a lógica para identificar os tipos dos objetos)
print(m1)
print(m2)    

cap.release()

cv2.destroyAllWindows()