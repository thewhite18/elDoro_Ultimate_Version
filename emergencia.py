import serial, time, os
import RPi.GPIO as GPIO
import comandosRutinaSKR as comandosSKR

def emergencia(puertoSerieSKR):
	puertoSerieSKR.write((comandosSKR.paradaEmergencia()).encode("ascii")) # Comando de parada de emergencia
	puertoSerieSKR.write((comandosSKR.comandoEnableMotores()).encode("ascii")) # Comando de enable de motores
	puertoSerieSKR.flushInput()
	print("HOLA")
	while GPIO.input(4) == 0 or GPIO.input(4) == False : pass
		
	puertoSerieSKR.flushInput()


