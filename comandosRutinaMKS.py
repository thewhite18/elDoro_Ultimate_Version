'''
	SCRIP para rutinas de MKS
'''


import serial, time, os
import numpy as np
import RPi.GPIO as GPIO

def comandoMov(x,y,z,f): #	Genera el comando deseado para desplazarse a la ubicación deseada
	print("	-> Movimiento: Rueda X:", x," Rueda Y:",y," Rueda Z:",z)
	x = x*640/(2*np.pi*100) 		#	Conversion de mm del campo a pulsos en la rueda que lo que entiende marlin
	y = y*640/(2*np.pi*100)			#	Conversion de mm del campo a pulsos en la rueda que lo que entiende marlin
	z = z*640/(2*np.pi*100)			#	Conversion de mm del campo a pulsos en la rueda que lo que entiende marlin
	return "G1 X"+str(x)+" Y"+str(y)+" Z"+str(z)+" F"+str(f)+"\n"
def comandoOrigen(): #	Establece la coordenada actual como origen del sistema
	print("	-> Origen")
	return "G92 X0 Y0 Z0 \n"
def comandoLiberaRueda(): #	Comando que libera las ruedas
	print("	-> Liberar ruedas")
	return "M84 \n"
def comandoTempExtrusor(): # Comando que devuelve la temperatura del extrusor
	print("	-> Temperatur extrusor")
	return "M105 \n"
def comandoParametrosIniciales(): #	Comando que devuelve los parametros iniciales (CONFIGURADA EN MARLIN)
	print("	-> Parametros iniciales")
	return "M503 \n"
def comandoEnableMotores(): #	Comando que activa todos los motores
	print("	-> Motores con corriente")
	return "M17 \n"
def comandoDisableMotores(): #	Comando que desactiva todos los motores
	print("	-> Motores sin corriente")
	return "M18 \n"

def rutinaAvance(puerto,x,y,z,f):
	#Primera forma de hacerlo
	finalizar = False 															#	Variable que nos indica cuando ha finalizado una acción
	inicio = time.time()
	emergencyStop = False		
	puerto.write(("M92 x5 y5 z5 \n").encode("ascii"))													#	Medimos el tiempo con esta variabe
	puerto.write(("M203 X300 Y300 Z300 \n").encode("ascii"))
	puerto.write(("M201 X3000 Y3000 Z3000 \n").encode("ascii"))
	puerto.write(comandoOrigen().encode("ascii")) 								#	Establecemos la coordenada actual como origen
	puerto.write(comandoMov(x,y,z,f).encode("ascii"))							#	Avanzamos hasta la posicion deseada
	puerto.write(comandoDisableMotores().encode("ascii"))						#	Dejamos sin corriente los motores, comando que nos establece el final del movimientol, hay q hacerlo con otra cosa porq asi perdemos pulsos
	puerto.write(comandoEnableMotores().encode("ascii"))						#	Encendemos los motores, hay q ver si no se resbala ya que antes le pedimos que nos deje sin corriente
	while(not finalizar):														#	Cuando se libera el motor marlin manda un mensaje de ok, por tanto es aqui cuando sabemso que ya no nos movemos
		while puerto.inWaiting()==0:pass
		while puerto.inWaiting() >0:
			respuesta = puerto.readline()
			if respuesta==b'ok\n':
				print("	-> Movimiento finalizado")
				finalizar = True
			if GPIO.input(4) == 0 or GPIO.input(4) == False :
				emergencyStop = True
			puerto.flushInput()													
	fin = time.time()
	print("	-> Tiempo ejecucion: ",fin-inicio)
	
	return emergencyStop