'''
    En este script va lo relacionado con la transformación de las
    coordenadas x e y a las que queremos ir a velocidades de motor
'''


import math
import numpy as np




def mapa2mks(x,y, angulo_rodillos, rotacion): 
    '''
    Funcion que transforma las variables del mapa a las variables marlin
    Tiene como entrada la posición X [mm], Y[mm] , el angulo que forman los rodillos respecto a x [º] y la rotación respecto el eje z[º]

            y

            |
            |
            |
            |
            |--------------------->     x
    
    '''
    radio_rueda = 50 #Radio de la rueda en mm
    #pi = 3.1415
    #No se considera la variable tiempo ya que despues se nos iría si realziamos todos los pasos, usaremos las ecuaciones en vez de con velocidad con solo distancia y la salida  en vez de ser rads/s será rads
    x_mapa = x #x
    y_mapa = y #y
    angulo_rodillos_mapa = (angulo_rodillos)*(np.pi/180)
    angulo_rodillos_mapatheta_mapa = (rotacion)*(np.pi/180) #Angulo en radianes
    longitud = 100 #Distancia del centro de la rueda al centro del robot

    #Modelo pagina: https://www.fing.edu.uy/inco/grupos/mina/pGrado/easyrobots/doc/SOA.pdf
    matriz_transformacion = np.float32([[-math.sin(angulo_rodillos_mapa) , math.cos(angulo_rodillos_mapa) , longitud] , [-math.sin(np.pi/3-angulo_rodillos_mapa) , -math.cos(np.pi/3-angulo_rodillos_mapa) , longitud],[math.sin(np.pi/3+angulo_rodillos_mapa) , -math.cos(np.pi/3+angulo_rodillos_mapa) , longitud]])
    input = np.float32([x_mapa,y_mapa,angulo_rodillos_mapatheta_mapa])
    theta1 , theta2 , theta3 = (np.matmul(matriz_transformacion,input))/radio_rueda
    #Para convertir de rad/s a mm, pasasmos de rad a vueltas dividiendo entre 2*Pi, para pasar de vueltas a mm lo multiplicamso por 2*Pi*R. Por tanto con multiplciar por R vale
    distancia_x = theta1*radio_rueda
    distancia_y = theta2*radio_rueda
    distancia_z = theta3*radio_rueda
    
    return distancia_x,distancia_y, distancia_z

def mapa2skr(x,y, angulo_rodillos, rotacion): 
    '''
    Funcion que transforma las variables del mapa a las variables marlin
    Tiene como entrada la posición X [mm], Y[mm] , el angulo que forman los rodillos respecto a x [º] y la rotación respecto el eje z[º]

           

            |--------------------->     x
            |
            |
            |
            |
            y
    '''
    radio_rueda = 50 #Radio de la rueda en mm
    #pi = 3.1415
    #No se considera la variable tiempo ya que despues se nos iría si realziamos todos los pasos, usaremos las ecuaciones en vez de con velocidad con solo distancia y la salida  en vez de ser rads/s será rads
    x_mapa = x #x
    y_mapa = y #y
    angulo_rodillos_mapa = (angulo_rodillos)*(np.pi/180)
    angulo_rodillos_mapatheta_mapa = (rotacion)*(np.pi/180) #Angulo en radianes
    longitud = 100 #Distancia del centro de la rueda al centro del robot

    #Modelo pagina: https://www.fing.edu.uy/inco/grupos/mina/pGrado/easyrobots/doc/SOA.pdf
    matriz_transformacion = np.float32([[-math.sin(angulo_rodillos_mapa) , math.cos(angulo_rodillos_mapa) , longitud] , [-math.sin(np.pi/3-angulo_rodillos_mapa) , -math.cos(np.pi/3-angulo_rodillos_mapa) , longitud],[math.sin(np.pi/3+angulo_rodillos_mapa) , -math.cos(np.pi/3+angulo_rodillos_mapa) , longitud]])
    input = np.float32([x_mapa,y_mapa,angulo_rodillos_mapatheta_mapa])
    theta1 , theta2 , theta3 = (np.matmul(matriz_transformacion,input))/radio_rueda
    #Para convertir de rad/s a mm, pasasmos de rad a vueltas dividiendo entre 2*Pi, para pasar de vueltas a mm lo multiplicamso por 2*Pi*R. Por tanto con multiplciar por R vale
    distancia_x = theta1*radio_rueda
    distancia_y = theta2*radio_rueda # Se pone menos por que el eje de este robot es en la otra dirección
    distancia_z = theta3*radio_rueda
    
    return distancia_x,distancia_y, distancia_z
    
