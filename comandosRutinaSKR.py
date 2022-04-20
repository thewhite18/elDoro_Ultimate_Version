'''
	SCRIP para rutinas de SKR
'''

import serial, time, os
import numpy as np
import RPi.GPIO as GPIO

def comandoMov(x,y,z,f): #	Genera el comando deseado para desplazarse a la ubicación deseada
	#print("	-> Movimiento: Rueda X:", x," Rueda Y:",y," Rueda Z:",z)
	x = x*640/(2*np.pi*100) 		#	Conversion de mm del campo a pulsos en la rueda que lo que entiende marlin
	y = y*640/(2*np.pi*100)			#	Conversion de mm del campo a pulsos en la rueda que lo que entiende marlin
	z = z*640/(2*np.pi*100)			#	Conversion de mm del campo a pulsos en la rueda que lo que entiende marlin
	return "G1 X"+str(x)+" Y"+str(y)+" Z"+str(z)+" F"+str(f)+"\n"
	
def comandoOrigen(): #	Establece la coordenada actual como origen del sistema
	#print("	-> Origen")
	return "G92 X0 Y0 Z0 \n"
	
def comandoLiberaRueda(): #	Comando que libera las ruedas
	#print("	-> Liberar ruedas")
	return "M84 \n"
def encenderVentilador(): #	Comando que libera las ruedas
	#print("	-> Liberar ruedas")
	return "M106 S255 \n"
def apagarVentilador(): #	Comando que libera las ruedas
	#print("	-> Liberar ruedas")
	return "M106 S0 \n"
	
def comandoTempExtrusor(): # Comando que devuelve la temperatura del extrusor
	#print("	-> Temperatur extrusor")
	return "M105 \n"
	
def comandoParametrosIniciales(): #	Comando que devuelve los parametros iniciales (CONFIGURADA EN MARLIN)
	#print("	-> Parametros iniciales")
	return "M503 \n"
	
def comandoEnableMotores(): #	Comando que activa todos los motores
	#print("	-> Motores con corriente")
	return "M17 \n"
	
def comandoDisableMotores(): #	Comando que desactiva todos los motores
	#print("	-> Motores sin corriente")
	return "M18 \n"
	
def comdanoSetStep():
	#print("	-> Set Step")
	return "M92 x20 y20 z20 \n"
	
def paradaEmergencia():
	#print("	-> Set Step")
	return "M410 \n"
	
def comandoSetAceleration():
	#print(" -> Set aceleration")
	#return "M204 P50 R50 T50 \n"
	return "M204 P100 R100 T100 \n"
	
def rutinaAvance(puerto,x,y,z,f):
	
	finalizar = False 															#	Variable que nos indica cuando ha finalizado una acción
	inicio = time.time()
	emergencyStop = False	
	emergencyStop = False	
	puerto.write(comdanoSetStep().encode("ascii"))	
	time.sleep(0.01)
	puerto.write(comandoSetAceleration().encode("ascii"))
	time.sleep(0.01)	
	puerto.write(comandoOrigen().encode("ascii")) 								#	Establecemos la coordenada actual como origen
	time.sleep(0.01)
	puerto.write(comandoMov(x,y,z,f).encode("ascii"))							#	Avanzamos hasta la posicion deseada
	time.sleep(0.01)
	puerto.write(comandoDisableMotores().encode("ascii"))						#	Dejamos sin corriente los motores, comando que nos establece el final del movimientol, hay q hacerlo con otra cosa porq asi perdemos pulsos
	time.sleep(0.01)
	puerto.write(comandoEnableMotores().encode("ascii"))						#	Encendemos los motores, hay q ver si no se resbala ya que antes le pedimos que nos deje sin corriente
	time.sleep(0.01)
	puerto.flushInput()	
	while(not finalizar):														#	Cuando se libera el motor marlin manda un mensaje de ok, por tanto es aqui cuando sabemso que ya no nos movemos
		while puerto.inWaiting()==0 and finalizar == False:
			if GPIO.input(4) == 0 or GPIO.input(4) == False :			
				finalizar = True
				emergencyStop = True
		while puerto.inWaiting() >0 and finalizar == False:
			respuesta = puerto.readline()
			if respuesta==b'ok\n':
				print("		* Movimiento finalizado")
				finalizar = True
			if GPIO.input(4) == 0 or GPIO.input(4) == False :
				finalizar = True
				emergencyStop = True
			puerto.flushInput()													
	fin = time.time()
	print("		* Tiempo de ejecución",fin-inicio)
	return emergencyStop	


def rutinaAvanceEmergencia(puerto,x,y,z,f):
	time.sleep(2)
	finalizar = False 															#	Variable que nos indica cuando ha finalizado una acción
	inicio = time.time()
	emergencyStop = False	
	
	puerto.write(comdanoSetStep().encode("ascii"))								#	Establecer STEP
	time.sleep(0.01)
	puerto.write(comandoSetAceleration().encode("ascii"))						#	Establecemos aceleracion
	time.sleep(0.01)	
	puerto.write(comandoMov(x,y,z,f).encode("ascii"))							#	Avanzamos hasta la posicion deseada
	time.sleep(0.01)
	puerto.write(comandoDisableMotores().encode("ascii"))						#	Dejamos sin corriente los motores, comando que nos establece el final del movimientol, hay q hacerlo con otra cosa porq asi perdemos pulsos
	time.sleep(0.01)
	puerto.write(comandoEnableMotores().encode("ascii"))						#	Encendemos los motores, hay q ver si no se resbala ya que antes le pedimos que nos deje sin corriente
	time.sleep(0.01)
	puerto.flushInput()	

	while(not finalizar):														#	Cuando se libera el motor marlin manda un mensaje de ok, por tanto es aqui cuando sabemso que ya no nos movemos
		while puerto.inWaiting()==0 and finalizar == False:
	
			if GPIO.input(4) == 0 or GPIO.input(4) == False :
			
				finalizar = True
				emergencyStop = True
			if  time.time()	- inicio  > 10:
				finalizar = True
				emergencyStop = False
				
		while puerto.inWaiting() >0 and finalizar == False:
			tiempo_movimiento = time.time()		
			respuesta = puerto.readline()
			if respuesta==b'ok\n':
	
				print("			* Movimiento finalizado")
				finalizar = True
			if GPIO.input(4) == 0 or GPIO.input(4) == False :
	
				finalizar = True
				emergencyStop = True
			puerto.flushInput()															
	fin = time.time()
	print("			* Tiempo de ejecución",fin-inicio,"\n")
	return emergencyStop
