import math
import random

alpha = float(input("Por favor, ingrese el valor de alpha: "))

with open('C:/Users/salva/Desktop/Tsiligirides 2/tsiligirides_problem_2_budget_15.txt', 'r') as archivo:
    lineas = archivo.readlines()

contenido_sin_espacios = []
for linea in lineas:
    contenido_sin_espacios.append(linea.strip())

obtenerTmax = contenido_sin_espacios[0]
valoresPrincipales = obtenerTmax.split()
tmax = int(valoresPrincipales[0])
numRutas = int(valoresPrincipales[1])

print("Tmax =", tmax, "\nNumero de rutas =", numRutas)

x1 = 0
x2 = 0
y1 = 0
y2 = 0
score = 0
distancia = []
valorEntreScore = []
scores = []

for i in range(1, len(contenido_sin_espacios)):
    distanciasGuardadas = []
    scoreValor = []
    elemento = contenido_sin_espacios[i]
    valores = elemento.split()
    x1 = float(valores[0])
    y1 = float(valores[1])
    scores.append(int(valores[2]) * alpha)

    for i in range(1, len(contenido_sin_espacios)):
        elemento = contenido_sin_espacios[i]
        valores = elemento.split()
        x2 = float(valores[0])
        y2 = float(valores[1])
        scorePrueba = int(valores[2]) * alpha
        distanciaTotal = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        distanciasGuardadas.append(distanciaTotal)
        if scorePrueba > 0 and distanciaTotal > 0:
            scoreValor.append(scorePrueba / distanciaTotal)
        else:
            scoreValor.append(0)

    distancia.append(distanciasGuardadas)
    valorEntreScore.append(scoreValor)

# Algoritmo
sumTmax = 0
sumScore = 0
quitPosicion = 0
cancelacion2 = False
positionResume = []
for i in range(1, len(contenido_sin_espacios)):
    if sumTmax >= tmax:
        break
    cancelarion = False
    contador = 0
    while cancelarion == False:
        maxValor = max(valorEntreScore[i - 1])
        posicion = 0
        for j in valorEntreScore[i - 1]:
            posicion = posicion + 1
            if maxValor == j:
                quitPosicion = posicion

                # eliminacion
                posicionDistancia = 0
                for distancias in distancia[i - 1]:
                    posicionDistancia = posicionDistancia + 1
                    if posicionDistancia == quitPosicion:
                        if sumTmax + distancias <= tmax:
                            cancelarion = True
                        else:
                            for encontrarMax in valorEntreScore[i - 1]:
                                contador = contador + 1
                                if encontrarMax == maxValor:
                                    encontrarMax = 0
                                if contador > len(distancia):
                                    cancelarion = True
                                    cancelacion2 = True
                if cancelarion == True:
                    for subArray in valorEntreScore:
                        subArray[quitPosicion - 1] = 0

    if cancelacion2 == True:
        break

    print("Posicion:", quitPosicion)
    positionResume.append(quitPosicion)

    # sumarScore
    sumScore = sumScore + scores[quitPosicion - 1]

    # sumarDistancia
    posicionDistancia = 0
    for distancias in distancia[i - 1]:
        posicionDistancia = posicionDistancia + 1
        if posicionDistancia == quitPosicion:
            sumTmax = sumTmax + distancias

    print("Suma distancias:", sumTmax, "\nSuma Score:", sumScore)

print("------------------------------------------------------------------------\nResultado")
print("Suma Distancias:", sumTmax)
print("Suma Score:", sumScore)
print(positionResume)

# Multi-Start Heuristic
best_solution = float('inf')  # Initialize with a large value
best_score = 0
num_iterations = 100  # Number of iterations for the multi-start heuristic

for _ in range(num_iterations):
    # Randomly shuffle the position resume
    random.shuffle(positionResume)

    sumTMaxLS = 0
    indexValue = 0
    contadorFirts = 0
    sumScoreLS = 0  # Variable para almacenar el score en cada iteración

    for positions in positionResume:
        if contadorFirts == 0:
            for index, distance in enumerate(distancia[0]):
                if index == positions:
                    sumTMaxLS = distance
                    indexValue = index
                    contadorFirts = contadorFirts + 1
        else:
            for index, distance in enumerate(distancia[indexValue]):
                if index == positions:
                    sumTMaxLS = sumTMaxLS + distance
                    indexValue = index
                    sumScoreLS += scores[positions - 1]  # Sumar el score correspondiente

    print("Multi-Start Heuristic Iteration:", _ + 1, ", Suma Distancias:", sumTMaxLS)
    print("Score:", sumScoreLS)  # Imprimir el score en cada iteración

    if sumTMaxLS < best_solution:
        best_solution = sumTMaxLS
        best_score = sumScoreLS

print("Best solution found:", best_solution)
print("Best score found:", best_score)


