# -*- coding: utf-8 -*-
"""
Created on 24 october 2024

@author: Johanna Vargas


"""

import math
import matplotlib.pyplot as plt
import time

def distancia(p, q):
    """
    Calcula la distancia euclidiana entre dos puntos en el plano.

    Parameters
    ----------
    p : tuple of float
        Coordenadas del primer punto (x1, y1).
    q : tuple of float
        Coordenadas del segundo punto (x2, y2).

    Returns
    -------
    float
        La distancia entre los dos puntos.
        
        References
    ----------
    Este código fue desarrollado con la asistencia de ChatGPT, un modelo de lenguaje
    de OpenAI, que proporcionó recomendaciones de estilo y buenas prácticas para 
    mejorar la eficiencia del código.
    
    Examples
    --------
    >>> distancia((0, 0), (3, 4))
    5.0
    """
    return math.sqrt((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)

def fuerza_bruta(lista_pares):
    """
    Encuentra los dos pares de puntos más cercanos utilizando la búsqueda por fuerza bruta.

    Parameters
    ----------
    lista_pares : list of tuple
        Lista de tuplas donde cada tupla contiene las coordenadas (x, y) de un punto.

    Returns
    -------
    pares_cercanos : list of tuple
        Lista con los dos puntos más cercanos.
    dis_minima : float
        La distancia mínima entre los dos puntos más cercanos.

    Examples
    --------
    >>> fuerza_bruta([(0, 0), (1, 1), (2, 2)])
    ([(0, 0), (1, 1)], 1.414)
    """
    num_pares = len(lista_pares)
    dis_minima = math.inf
    pares_cercanos = []

    for i in range(num_pares):
        for j in range(i + 1, num_pares):
            dis_temporal = distancia(lista_pares[i], lista_pares[j])
            if dis_temporal < dis_minima:
                dis_minima = dis_temporal
                pares_cercanos = [lista_pares[i], lista_pares[j]]
    return pares_cercanos, dis_minima

def ordenar_lista(lista_pares, coordenada):
    """
    Ordena una lista de puntos en el plano en base a una coordenada.

    Parameters
    ----------
    lista_pares : list of tuple
        Lista de tuplas con las coordenadas (x, y) de los puntos.
    coordenada : int
        Coordenada a usar para ordenar. 0 para ordenar por x, 1 para ordenar por y.

    Returns
    ------- 
    list
        Lista de puntos ordenada por la coordenada seleccionada.

    Examples
    --------
    >>> ordenar_lista([(2, 3), (1, 2)], 0)
    [(1, 2), (2, 3)]
    """
    if len(lista_pares) > 1:
        mitad = len(lista_pares) // 2
        lista_izq = lista_pares[:mitad]
        lista_der = lista_pares[mitad:]

        ordenar_lista(lista_izq, coordenada)
        ordenar_lista(lista_der, coordenada)

        i = j = k = 0

        while i < len(lista_izq) and j < len(lista_der):
            if lista_izq[i][coordenada] < lista_der[j][coordenada]:
                lista_pares[k] = lista_izq[i]
                i += 1
            else:
                lista_pares[k] = lista_der[j]
                j += 1
            k += 1

        while i < len(lista_izq):
            lista_pares[k] = lista_izq[i]
            i += 1
            k += 1

        while j < len(lista_der):
            lista_pares[k] = lista_der[j]
            j += 1
            k += 1

    return lista_pares

def par_mas_cercano_linea(lista_x, lista_y, pares, dist):
    """
    Busca el par de puntos más cercano en una franja definida por la distancia.

    Parameters
    ----------
    lista_x : list of tuple
        Lista de puntos ordenados por la coordenada x.
    lista_y : list of tuple
        Lista de puntos ordenados por la coordenada y.
    pares : list of tuple
        Par de puntos más cercanos encontrados hasta el momento.
    dist : float
        Distancia mínima entre los puntos más cercanos.

    Returns
    -------
    pares : list of tuple
        Par de puntos más cercanos dentro de la franja.
    min_dist : float
        Distancia mínima encontrada.

    Examples
    --------
    >>> par_mas_cercano_linea([(0, 0), (2, 2)], [(0, 0), (2, 2)], [(0, 0), (2, 2)], 2.0)
    ([(0, 0), (2, 2)], 2.0)
    """
    mitad = len(lista_x) // 2
    punto_medio_x = lista_x[mitad][0]

    sub_lista_y = [i for i in lista_y if punto_medio_x - dist <= i[0] <= punto_medio_x + dist]
    min_dist = dist
    for i in range(len(sub_lista_y) - 1):
        for j in range(i + 1, min(i + 6, len(sub_lista_y))):
            p, q = sub_lista_y[i], sub_lista_y[j]
            dist_pares = distancia(p, q)
            if dist_pares < min_dist:
                min_dist = dist_pares
                pares = [p, q]

    return pares, min_dist

def par_mas_cercano_recur(lista_x, lista_y):
    """
    Busca recursivamente el par más cercano en el plano utilizando el enfoque divide y vencerás.

    Parameters
    ----------
    lista_x : list of tuple
        Lista de puntos ordenados por la coordenada x.
    lista_y : list of tuple
        Lista de puntos ordenados por la coordenada y.

    Returns
    -------
    pares : list of tuple
        Par de puntos más cercanos.
    dist : float
        Distancia mínima entre los puntos más cercanos.

    Examples
    --------
    >>> par_mas_cercano_recur([(0, 0), (2, 2)], [(0, 0), (2, 2)])
    ([(0, 0), (2, 2)], 2.0)
    """
    if len(lista_x) <= 3:
        return fuerza_bruta(lista_x)

    mitad = len(lista_x) // 2
    lista_izq_x = lista_x[:mitad]
    lista_der_x = lista_x[mitad:]

    punto_medio_x = lista_x[mitad][0]
    lista_izq_y = [punto for punto in lista_y if punto[0] <= punto_medio_x]
    lista_der_y = [punto for punto in lista_y if punto[0] > punto_medio_x]

    pares_izq, dist_izq = par_mas_cercano_recur(lista_izq_x, lista_izq_y)
    pares_der, dist_der = par_mas_cercano_recur(lista_der_x, lista_der_y)

    if dist_izq <= dist_der:
        dist_min = dist_izq
        pares_min = pares_izq
    else:
        dist_min = dist_der
        pares_min = pares_der

    pares_linea, dist_linea = par_mas_cercano_linea(lista_x, lista_y, pares_min, dist_min)

    if dist_min <= dist_linea:
        return pares_min, dist_min
    else:
        return pares_linea, dist_linea

def par_mas_cercano(lista_pares):
    """
    Encuentra el par de puntos más cercanos en una lista de puntos.

    Parameters
    ----------
    lista_pares : list of tuple
        Lista de tuplas con las coordenadas (x, y) de los puntos.

    Returns
    -------
    pares : list of tuple
        El par de puntos más cercanos.
    dist : float
        La distancia entre los puntos más cercanos.

    Examples
    --------
    >>> par_mas_cercano([(0, 0), (3, 4), (1, 1)])
    ([(0, 0), (1, 1)], 1.414)
    """
    lista_x = ordenar_lista(lista_pares[:], 0)
    lista_y = ordenar_lista(lista_pares[:], 1)

    return par_mas_cercano_recur(lista_x, lista_y)

def grafica(lista_pares, par_cercano, distancia):
    """
    Genera una gráfica que muestra los puntos en el plano y resalta el par más cercano.

    Parameters
    ----------
    lista_pares : list of tuple
        Lista de puntos (x, y) en el plano.
    par_cercano : list of tuple
        Par de puntos más cercanos.
    distancia : float
        Distancia mínima entre el par de puntos.

    Returns
    -------
    None
    """
    x = [i[0] for i in lista_pares]
    y = [i[1] for i in lista_pares]
    xc = [i[0] for i in par_cercano]
    yc = [i[1] for i in par_cercano]
    x_medio = (xc[0] + xc[1]) / 2
    y_medio = (yc[0] + yc[1]) / 2    
    plt.plot(x, y, 'b.', xc, yc, 'g.', xc, yc, 'g')
    plt.grid()
    s = f"  dmín = {distancia:.3f}"
    plt.text(x_medio, y_medio, s, color='g', fontsize=8)
    plt.show()

# Lectura de datos y ejecución principal
archivo = "datos_1000.txt"
with open(archivo) as datos:
    x = list(map(int, datos.readline().split(",")))
    y = list(map(int, datos.readline().split(",")))

lista = [(x[i], y[i]) for i in range(len(x))]

# Obtiene el par más cercano y la distancia con ambos métodos
inicio1 = time.time()
pares, dist = par_mas_cercano(lista)
fin1 = time.time()

inicio2 = time.time()
pares2, dist2 = fuerza_bruta(lista)
fin2 = time.time()

# Muestra los resultados
print(f"Los pares más cercanos (divide y vencerás) son {pares[0]} y {pares[1]}.")
print(f"La distancia entre ellos es {dist:.3f}.")
print(f"Tiempo de ejecución (divide y vencerás): {fin1 - inicio1:.3f} s.")

print(f"Los pares más cercanos (fuerza bruta) son {pares2[0]} y {pares2[1]}.")
print(f"La distancia entre ellos es {dist2:.3f}.")
print(f"Tiempo de ejecución (fuerza bruta): {fin2 - inicio2:.3f} s.")
