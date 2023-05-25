import math
import random

with open("C:/Users/salva/Desktop/Tsiligirides 2/tsiligirides_problem_2_budget_15.txt", 'r') as archivo:
    lineas = archivo.readlines()

contenido_sin_espacios = []
for linea in lineas:
    contenido_sin_espacios.append(linea.strip())

obtener_tmax = contenido_sin_espacios[0]
valores_principales = obtener_tmax.split()
tmax = int(valores_principales[0])
num_rutas = int(valores_principales[1])

print("Tmax =", tmax)
print("Numero de rutas =", num_rutas)

x1 = 0
x2 = 0
y1 = 0
y2 = 0
score = 0
distancia = []
valor_entre_score = []
scores = []

for i in range(1, len(contenido_sin_espacios)):
    distancias_guardadas = []
    score_valor = []
    elemento = contenido_sin_espacios[i]
    valores = elemento.split()
    x1 = float(valores[0])
    y1 = float(valores[1])
    scores.append(int(valores[2]))

    for j in range(1, len(contenido_sin_espacios)):
        elemento = contenido_sin_espacios[j]
        valores = elemento.split()
        x2 = float(valores[0])
        y2 = float(valores[1])
        score_prueba = int(valores[2])
        distancia_total = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        distancias_guardadas.append(distancia_total)
        if score_prueba > 0 and distancia_total > 0:
            score_valor.append(score_prueba / distancia_total)
        else:
            score_valor.append(0)
    distancia.append(distancias_guardadas)
    valor_entre_score.append(score_valor)

i = 0
for distancias_completas in distancia:
    i = i+1
    print("\nDistancias desde ", i, ":", distancias_completas)
    print("-----------------------------------------------------------------")

alpha = float(input("Ingrese el valor de alpha (0 a 1): "))
sum_tmax = 0
sum_score = 0
quit_posicion = 0
cancelacion2 = False
position_resume = []

for i in range(1, len(contenido_sin_espacios)):
    if sum_tmax >= tmax:
        break
    cancelacion = False
    contador = 0
    
    while not cancelacion:
        mn_valor = min(valor_entre_score[i-1])
        mx_valor = max(valor_entre_score[i-1])
        umbral = mn_valor + (mx_valor - mn_valor) * alpha
        valores_cumplen = []

        for posicion, valor in enumerate(valor_entre_score[i - 1]):
            if valor >= umbral:
                valores_cumplen.append(valor)
               
        valor_aleatorio = random.randint(0, len(valores_cumplen) - 1)
        max_valor = valores_cumplen[valor_aleatorio]
        posicion = 0
        
        for j in valor_entre_score[i-1]:
            posicion = posicion + 1
            if max_valor == j:
                quit_posicion = posicion
                
                # Eliminación
                posicion_distancia = 0
                for distancias in distancia[i-1]:
                    posicion_distancia = posicion_distancia + 1
                    if posicion_distancia == quit_posicion:
                        if sum_tmax + distancias <= tmax:
                            cancelacion = True
                        else:
                            for encontrar_max in valor_entre_score[i-1]:
                                contador = contador + 1
                                if encontrar_max == max_valor:
                                    encontrar_max = 0
                                if contador > len(distancia):
                                    cancelacion = True
                                    cancelacion2 = True
                if cancelacion:
                    for sub_array in valor_entre_score:
                        sub_array[quit_posicion-1] = 0
    
    if cancelacion2:
        break
    
    print("Posicion:", quit_posicion)
    position_resume.append(quit_posicion)
    
    # Sumar Score
    sum_score = sum_score + scores[quit_posicion-1]
    
    # Sumar Distancia
    posicion_distancia = 0
    for distancias in distancia[i-1]:
        posicion_distancia = posicion_distancia + 1
        if posicion_distancia == quit_posicion:
            sum_tmax = sum_tmax + distancias
    
    print("Suma distancias:", sum_tmax)
    print("Suma Score:", sum_score)

print("------------------------------------------------------------------------\nResultado")
print("Suma Distancias:", sum_tmax)
print("Suma Score:", sum_score)
print(position_resume)

# Local Search
# distancia
# position_resume
iteraciones = int(input("Cuantas veces resolverá el local search: "))

# Inicializar la mejor distancia y posición
best_distance = sum_tmax
best_position_resume = position_resume.copy()

# Variable para rastrear si se encontraron mejores posiciones
found_better_position = False
max_repeticiones = len(distancia) * 3

for _ in range(iteraciones):
    # Seleccionar dos posiciones aleatorias para intercambiar
    pos1 = random.randint(0, len(position_resume) - 1)
    pos2 = random.randint(0, len(position_resume) - 1)
    
    # Intercambiar las posiciones en la solución
    position_resume[pos1], position_resume[pos2] = position_resume[pos2], position_resume[pos1]
    
    # Calcular la nueva distancia sumando las distancias en las nuevas posiciones
    new_distance = 0
    for i in range(len(position_resume)-1):
        pos_actual = position_resume[i]
        pos_siguiente = position_resume[i+1]
        new_distance += distancia[pos_actual-1][pos_siguiente-1]  # Restar 1 para obtener el índice correcto
    
    # Verificar si la nueva distancia es mejor que la mejor distancia anterior
    if new_distance < best_distance:
        best_distance = new_distance
        best_position_resume = position_resume.copy()
        found_better_position = True

    # Imprimir los resultados del mejor caso encontrado por el Local Search
    if found_better_position:
        found_better_position = False
        print("Mejor suma de distancias encontrada:", best_distance)
        print("Posiciones de la mejor solución encontrada:", best_position_resume)
        value_last = best_position_resume[-1]
        cancelacion = False
        cancelacion2 = False
        contador = 0
        contador2 = 0
        max_valor = max(valor_entre_score[value_last-1])
        posicion = 0
        node_added = False  # Variable para rastrear si se añadió algún nodo en cada iteración
        
        while not node_added and contador2 < max_repeticiones:
            contador2 = contador2 + 1
            
            for j in valor_entre_score[value_last-1]:
                posicion = posicion + 1
                if max_valor == j:
                    quit_posicion = posicion
                    
                    # Eliminación
                    posicion_distancia = 0
                    for distancias in distancia[value_last-1]:
                        posicion_distancia = posicion_distancia + 1
                        if posicion_distancia == quit_posicion:
                            if best_distance + distancias <= tmax:
                                cancelacion = True
                            else:
                                for encontrar_max in valor_entre_score[value_last-1]:
                                    contador = contador + 1
                                    if encontrar_max == max_valor:
                                        encontrar_max = 0
                                    if contador > len(distancia):
                                        cancelacion2 = True
                                        break
                                if cancelacion2:
                                    break
                                cancelacion = True
                    if cancelacion:
                        for sub_array in valor_entre_score:
                            sub_array[quit_posicion-1] = 0
            
            if cancelacion2:
                break
            
            if best_distance >= tmax or not cancelacion:
                break
            
            # Añadir el nuevo nodo solo si no supera tmax
            if best_distance + distancia[value_last-1][quit_posicion-1] <= tmax:
                best_position_resume.append(quit_posicion)
                
                # Sumar Distancia
                posicion_distancia = 0
                for distancias in distancia[value_last-1]:
                    posicion_distancia = posicion_distancia + 1
                    if posicion_distancia == quit_posicion:
                        best_distance = best_distance + distancias
                
                node_added = True  # Se añadió un nodo en esta iteración
                value_last = quit_posicion
        
        if node_added:
            sum_score = 0
            for position in best_position_resume:
                sum_score += scores[position - 1]
            
            print("Se añadió un nuevo elemento.")
            print("Suma Distancias:", best_distance)
            print("Suma Score:", sum_score)
            print("Ruta:", best_position_resume)
        else:
            sum_score = 0
            for position in best_position_resume:
                sum_score += scores[position - 1]
            
            print("No fue posible añadir otro nodo sin superar tmax.")
            print("Suma Score:", sum_score)
        
        continuar_recorrido = int(input("¿Desea continuar?\n1-Si\n2-No\n"))
        
        if continuar_recorrido == 1:
            iteraciones = int(input("Cuantas veces resolverá de nuevo el local search: "))
        elif continuar_recorrido == 2:
            print("El programa termino")
            exit()

print("El programa termino porque no se encontro otro mejor movimiento para añadir otro elemento")
