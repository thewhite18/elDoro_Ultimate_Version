#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 20:42:03 2022

@author: ale
"""
import PyLidar3
import serial
import time # Time module
import RPi.GPIO as GPIO # Libreria para los pines de Raspi
#In linux type in terminal -- ls /dev/tty* 
#port = input("Enter port name which lidar is connected:") #windows


    

puerto = 0
while(puerto < 4):
        try:
            port = "/dev/ttyUSB"+str(puerto) #lynux
            print(port)
            Obj = PyLidar3.YdLidarX4(port) 
        except:
            print(" * puerto: ", puerto," no encontrado")
            puerto = puerto + 1
        else:
            print("conseguido")
            puerto=4
    
    
    
dic = {}
dic_aux = {}
dic_angulos = []
dic_distancias = []
dic_parada = []

lista_booleanos = []

condicion_parada = False

############### FUNCIONES CONFIGURACIÓN DE PINES RASPI #################################

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led = 21
GPIO.setup(led, GPIO.OUT)

############################################################################################
def envia_parada(condicion_parada):
    print('Running. Press CTRL-C to exit.')
    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino: #TRACCION
    
        #aperturaPuertoArduino()
        time.sleep(0.1)  # wait for serial to open
        
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
        #if arduino1.isOpen():
            #print("{} connected!".format(arduino1.port))
            
            try:
                            
                if(condicion_parada == True): # Si la condicion de parada es cierta envia un caracter para hacer algo en el arduino
                    msg = 'A'
                    arduino.write(msg.encode())
                    print('Se enviará: ', msg)
                else:
                    msg = 'B'
                    arduino.write(msg.encode())
                    print('Se enviará: ', msg)
                    
                arduino.close()
    
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")

##############################################################################################

def rellena_lista_falses(lista_booleanos, n):
    
    for i in range (n):
        lista_booleanos.append(False)
          
###############################################################################################
        
        
rellena_lista_falses(lista_booleanos, 360)




if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time 
    GPIO.output(led, 1) #Lo ponemos a 1 para q no pare            
    #while (time.time() - t) < 50: #scan for 10 seconds (antes tenía 30) 
    while True:        
            condicion_parada = False
            dic_aux.clear()
            dic_angulos.clear()
            dic_distancias.clear()
            dic = next(gen)
            lista_booleanos.clear()
            rellena_lista_falses(lista_booleanos, 360)
            #print(dic.items())
            
            #tupla_aux = dic.items()
            dic_aux = dict(dic) # La libreria Pylidar devuelve con la función StartScanning() un generador de diccionarios
            # Nosotros podemos coger los valores de ese generador de diccionarios con el operador cast 'dict' del valor recibido de la función
            dic_angulos = list(dic_aux.keys()) # EXTRAEMOS LAS CLAVES DE NUESTRO DICCIONARIO (ANGULOS)
            dic_distancias = list(dic_aux.values()) # EXTRAEMOS LOS VALORES DE NUESTRO DICCIONARIO (DISTANCIAS)
        
            time.sleep(0.1) # antes 0.5
            
         
            for i in range(len(dic_distancias)):
                
                if(dic_distancias[i] > 50) and (dic_distancias[i] < 200):
                    lista_booleanos[i] = True
              
            if(lista_booleanos.count(True) > 10):
                condicion_parada = True
            
            if(condicion_parada == True): # Si la condicion de parada es cierta envia un caracter para hacer algo en el arduino
                print("¡¡¡PARA!!!")
                GPIO.output(led, 0)
                
#                        msg = 'A'
#                        arduino.write(msg.encode())
#                        print('Se enviará: ', msg)
            else:
                print("CONTINUA")
                GPIO.output(led, 1)
#                        msg = 'B'
#                        arduino.write(msg.encode())
#                        print('Se enviará: ', msg)
            
    
        
    #    print(len(lista_booleanos))
    #    print(dic_angulos)
    #    print("\n\n\n", dic_distancias)
    #    print("\n\n\n", lista_booleanos)
    #    print("\n\n\n", lista_booleanos.__contains__(True))
                
    Obj.StopScanning()
    Obj.Disconnect()
    

            
    
else:
   print("Error connecting to device")
                
        
