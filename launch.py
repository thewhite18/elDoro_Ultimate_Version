import RPi.GPIO as GPIO
import os
import time
path = '/home/pi/Desktop/V3/Serial_V2/main.py'

def config (): #	Configuración de los pines: entrada o saldia
	
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	#Switches y botones
	#GPIO.setup(17, GPIO.IN) # Boton empiece partido
	GPIO.setup(26, GPIO.OUT) # Led morado
	GPIO.setup(19, GPIO.OUT) # Led amarillo
	GPIO.setup(13, GPIO.OUT) # Led verde
	GPIO.setup(5, GPIO.IN) # Boton inicio
	
	
	
	GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP) #	Modificación de las resistencias para poder unir tierra o vcc con el pin y que sea detectado
	GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	
def encenderLeds():
	GPIO.output(26, True)
	GPIO.output(19, True)
	GPIO.output(13, True)
	
def apagarLeds():
	GPIO.output(26, False)
	GPIO.output(19, False)
	GPIO.output(13, False)
def leds():
	time.sleep(250/1000)
	encenderLeds()
	time.sleep(250/1000)
	apagarLeds()
def main():
	
	global path
	config()
	configuracion = 0
	while(1):
		if configuracion == 1:
			GPIO.cleanup()
			config()
		configuracion = 0
		leds()	
		if GPIO.input(5) == 0 or GPIO.input(5) == False : 
			GPIO.cleanup()
			time.sleep(2)
			os.system('python ' + path)	
			configuracion = 1	

	
	
main()

