import serial, time, os
import transformaPuntos as transforma

import comandosRutinaSKR as comandosSKR
import comandosRutinaMKS as comandosMKS
import comandosBrazo as brazo

import numpy as np

velocidad_MKS = 1000 #	Velocidad de los motores paso a paso mm/min
constanteAngulo_MKS = 360/150 # Ajusta los angulos que queremos hacer a los que de verdad hace
constanteDistanciaX_MKS = 1 # Ajusta las distancias que queremos hacer a las que de verdad hace eje x
constanteDistanciaY_MKS= 1 # Ajusta las distancias que queremos hacer a las que de verdad hace eje y, deberian ser iguales
velocidad_SKR = 15000 #	Velocidad de los motores paso a paso mm/min    10000 es muy tocho
constanteAngulo_SKR= 222/180#220.59/180 # Ajusta los angulos que queremos hacer a los que de verdad hace
constanteDistanciaX_SKR = 10.14 # Ajusta las distancias que queremos hacer a las que de verdad hace eje x
constanteDistanciaY_SKR= 10.14 # Ajusta las distancias que queremos hacer a las que de verdad hace eje y, deberian ser iguales
distancia = [ 0 , 0 , 0]

def ejecucionRutina(rutaElegida,fila, traccionOmnidireccional, controlador , puertoSerieESP):
	global distancia
	emergencyStop = False
	
	if rutaElegida[fila][0] == "A":
		print("***	Rutina: ",fila, " Avanza\n")
		emergencyStop = False
		time.sleep(.1)
		if controlador == "SKR" :
			distancia = transforma.mapa2skr(rutaElegida[fila][1]*constanteDistanciaX_SKR,rutaElegida[fila][2]*constanteDistanciaY_SKR,90,0)
			emergencyStop = comandosSKR.rutinaAvance(traccionOmnidireccional,distancia[0],distancia[1],distancia[2],velocidad_SKR) #Si se usa marlin
		if controlador == "MKS" :
			distancia = transforma.mapa2mks(rutaElegida[fila][1]*constanteDistanciaX_MKS,rutaElegida[fila][2]*constanteDistanciaY_MKS,90,0)
			#emergencyStop = comandosMKS.rutinaAvance(traccionOmnidireccional,distancia[0],distancia[1],distancia[2],velocidad_MKS) #Si se usa marlin	
		puntoX = rutaElegida[fila][1]
		puntoY = rutaElegida[fila][2]	
		angulo = 0		
		time.sleep(500/1000)	#	Ver cuanto se puede disminuir, ojo va a haber q modificar rampas de aceleracion o hacerlo manual
		
	elif rutaElegida[fila][0] == "G":
		print("***	Rutina: ",fila, " Gira\n")
		emergencyStop = False
		if controlador == "SKR" :
			distancia = transforma.mapa2skr(0,0,90,rutaElegida[fila][1]*constanteAngulo_SKR)
			emergencyStop = comandosSKR.rutinaAvance(traccionOmnidireccional,distancia[0],distancia[1],distancia[2],velocidad_SKR) #Si se usa marlin
		if controlador == "MKS" :
			distancia = transforma.mapa2mks(0,0,90,rutaElegida[fila][1]*constanteAngulo_MKS)
			emergencyStop = comandosMKS.rutinaAvance(traccionOmnidireccional,distancia[0],distancia[1],distancia[2],velocidad_MKS) #Si se usa marlin	
		puntoX = 0
		puntoY = 0
		angulo = rutaElegida[fila][1]
		time.sleep(500/1000)
		
	elif rutaElegida[fila][0] == "B":
		print("***	Rutina: ",rutaElegida[fila][1].encode("ascii"), " Brazo\n")
		
		puertoSerieESP.write(rutaElegida[fila][1].encode("ascii"))
		puertoSerieESP.flushInput()
		puertoSerieESP.flushOutput()
		#brazo.comunicacionBrazo(puertoSerieESP, rutaElegida[fila][1])
		if rutaElegida[fila][1].encode("ascii") == "Pusher":
			time.sleep(2)
		else :
			time.sleep(500/1000)
		puntoX = 0
		puntoY = 0
		angulo = 0
		emergencyStop = False
		
		
	elif rutaElegida[fila][0] == "E" :
		print("			* Movimiento emergencia")
		emergencyStop = False	

		if controlador == "SKR" :
			emergencyStop = comandosSKR.rutinaAvanceEmergencia(traccionOmnidireccional,distancia[0],distancia[1],distancia[2],velocidad_SKR) #fALTA LAS CNTS
		if controlador == "MKS" :
			emergencyStop = comandosMKS.rutinaAvanceEmergencia(traccionOmnidireccional,distancia[0],distancia[1],distancia[2],velocidad_MKS) #Si se usa marlin
		puntoX = 0
		puntoY = 0
		angulo = 0
		time.sleep(500/1000)
		
	else :
		print("		->No esta correctamente definida la ruta ")
		puntoX = 0
		puntoY = 0
		angulo = 0
		emergencyStop = False

	return puntoX, puntoY, angulo, emergencyStop
