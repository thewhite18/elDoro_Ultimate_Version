import RPi.GPIO as GPIO
import serial, time, os


def configGPIO (): #	Configuración de los pines: entrada o saldia
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	#Switches y botones
	GPIO.setup(5, GPIO.IN) # Boton inicio
	GPIO.setup(12, GPIO.IN) 
	GPIO.setup(16, GPIO.IN)
	GPIO.setup(20, GPIO.IN)
	GPIO.setup(6, GPIO.IN) # Boton fin
	GPIO.setup(21, GPIO.IN)
	GPIO.setup(17, GPIO.IN) # Boton empiece partido
	GPIO.setup(27, GPIO.OUT) # Boton empiece partido
	GPIO.output(27, False)
	#EMERGENCYSTOP PIN 
	GPIO.setup(4, GPIO.IN)  # Pin de parada
	#LEDs
	GPIO.setup(26, GPIO.OUT) # Led morado
	GPIO.setup(19, GPIO.OUT) # Led amarillo
	GPIO.setup(13, GPIO.OUT) # Led verde
	
	GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
	GPIO.setup(6, GPIO.IN, pull_up_down = GPIO.PUD_UP) #	Modificación de las resistencias para poder unir tierra o vcc con el pin y que sea detectado
	GPIO.setup(5, GPIO.IN , pull_up_down = GPIO.PUD_UP) 
	GPIO.setup(21, GPIO.IN , pull_up_down = GPIO.PUD_UP) 
	GPIO.setup(12, GPIO.IN , pull_up_down = GPIO.PUD_UP) 
	GPIO.setup(16, GPIO.IN , pull_up_down = GPIO.PUD_UP)
	GPIO.setup(20, GPIO.IN , pull_up_down = GPIO.PUD_UP)
	GPIO.setup(4, GPIO.IN , pull_up_down = GPIO.PUD_UP)		

def configCampo ():	# Función para que dependiendo del switch de elección de campo la variable campo se establezca correctamente y se ilumine un led con el color del lado
	'''
	Las rutas tienen este formato:
		A -> Avanza (A,x,y)
		G -> Giro  (G, thetha)
		AG -> Avanza y gira (x,y,theta)
		B -> Brazo ,comando a enviar del brazo y descripcion de lo que hace 
	'''
	#rutaAmarilla = [["A",15,0],["G",0],["B","comando a enviar", "ComentariO"], "FIN"]
	#rutaAmarilla = [["A",60,0],["G",-45,0],["A",16.5,0],["A",0,-9.3],["A",0,9],["G",120],["A",8.32,4.6],["A",-7.89,-4.5],["G",-120],["A",-16.5,0],["G",45],["A",-120,0],["G",90],["A",0,-9],["A",10,0],["A",0,42], "FIN"]
	
	#Ruta carlos rutaAmarilla = [["A",38,-23],["B", "Pim","Medir"],"FIN"]
	rutaAmarilla = [["A",100,0],["B","Pusher","a"],["G",360],["A",-100,100],["B","Pim","a"],["A",0,-100],["B","Pusher"],["B","Pim"],"FIN"]
	#rutaMorada = [["A",71.67,11.67],["G",-165,0],["A",-7.9,4.3],["A",7.9,-4.3],["G",-120],["A",8.32,4.6],["B","Pusher","puser"],["A",-7.89,-4.5],["G",-75],["A",-71.67,-11.67],["A",-60,0],["G",-30],"FIN",["A",0,-9],["A",10,0],["A",0,42], "FIN"]
	#rutaMorada = [["A",71.67,11.67],["G",-165,0],["A",-7.9,4.3],["A",7.9,-4.3],["G",-120],["A",8.32,4.6],["B","Pusher","puser"],["A",-7.89,-4.5],["G",-75],["A",-71.67,-11.67],["A",-60,0],["G",-30],"FIN",["A",0,-9],["A",10,0],["A",0,42], "FIN"]
	rutaMorada = [["A",71.67,11.67],["G",-45,0],["A",0,-8],["A",0,8],["G",120],["A",7.6,4.3],["B", "Pusher","Medir"],["A",-7.6,-4.3],["G",-75],["A",-71.67,-11.67],["A",-60,0],["G",90],["A",-6,0],["A",0,-5.5],["A",17.5,0],["A",0,42], "FIN"]
	#rutaAmarilla = [["A", 25.73, -67.90], ["G", -45], ["A", -8.05, 4.65], ["A", 7.8, -4.5], ["G", -120], ["A", -8.23, 4.75], ["A", -7.79, 4.5], ["G", 75],"FIN"]
	#Nombres  Mide WS0 Pusher Pim

	#GPIO.output(13, False)
	if GPIO.input(21) == 0 or GPIO.input(21) == False : #	Compruebo los dos formatos porque depende de la raspi es uno u otro
		campo = "purple"
		
		GPIO.output(26, True)
		GPIO.output(19, False)
		
		ruta_a_realizar = rutaMorada # Si se escogiese rutina se implementa aqui
	else:
		campo = "yellow" 
		
		GPIO.output(26, False)
		GPIO.output(19, True)	
		ruta_a_realizar = rutaAmarilla
	
	return ruta_a_realizar

def configSerial_ESP():
	serialport = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
	serialport.write("WS0".encode("ascii"))
	respuesta = serialport.readline().decode("ascii")
	print("Respuesta",respuesta)
	if "Esp" in respuesta:
		print("	-> Conexion establecida con ESP en el puerto 0: ")
	return serialport
	
	
	
def configSerial_Master():
	conexion_Arduino = True
	conexion_LPC = True #Poner true sino esta conectada y asi no lo comprueba
	conexion_MKS = False
	puerto = 0
	while(puerto <= 4): #	Busca un puerto del 0 al 4 que son las posibilidades que hay
		try:
			puertoSerie = serial.Serial("/dev/ttyACM"+str(puerto),250000,timeout=1) #115200
		except:
			print("	* PuertoACM: ",puerto," no encontrado")
			puerto = puerto + 1
		else:
			time.sleep(1/10) #Reducir el número de segundos
			puertoSerie.flushInput()
			if puertoSerie.isOpen():
				
				puertoSerie.write("M84 \n".encode("ascii")) #	Este comando retorna ok si es la MKS quien lo recibe
				while puertoSerie.inWaiting()==0: pass
				while puertoSerie.inWaiting() >0:
					
					respuesta = puertoSerie.readline().decode("ascii")
					
					if 'ok' in respuesta:
						conexion_MKS = True
						print("	* Conexion establecida con SKR/MKS en el puertoUSB: ",puerto)
						puertoSerieMKS = puertoSerie
						
					puertoSerie.flushInput()
					if 'LPC' in respuesta:
						print("	* Conexion establecida con LPC en el puertoUSB: ",puerto)
						conexion_LPC = True
						puertoSerieLPC = puertoSerie
					puertoSerie.flushInput()
					
					if 'arduino' in respuesta:
						print("	* Conexion establecida con ARDUINO en el puertoUSB: ",puerto)
						conexion_Arduino = True
						puertoSerieARDUINO = puertoSerie
					puertoSerie.flushInput()
				puerto = puerto + 1		
	if conexion_Arduino == False or conexion_LPC == False or conexion_MKS == False: #Puede ser que la conexión sea falsa porque en vez de ser puerto TTYACM sea TTYUSB
		puerto = 0
		while(puerto <= 4):
			try:
				puertoSerie = serial.Serial("/dev/ttyUSB"+str(puerto),250000,timeout=1)
				print("Mensaje")
			except:
				print("	* puertoTTY: ",puerto," no encontrado")
				puerto = puerto + 1
			else:
				puertoSerie.write("M84 \n".encode("ascii"))
				while puertoSerie.inWaiting()==0:pass
				while puertoSerie.inWaiting() >0:
					respuesta = puertoSerie.readline()
					print(respuesta)
					if respuesta == b'ok\n' or respuesta == b'start\n':
						conexion_MKS = True
						print("	* Conexion establecida con MKS/SKR en el puertoUSB: ",puerto)
						puertoSerieMKS = puertoSerie
					puertoSerie.flushInput()
				
					if respuesta == b'arduino':
						print("	* Conexion establecida con ARDUINO en el puertoUSB: ",puerto)
						conexion_Arduino = True
						puertoSerieARDUINO = puertoSerie
					puertoSerie.flushInput()
				puerto = puerto + 1	
			
	if conexion_Arduino == False or conexion_LPC == False or conexion_MKS == False:
		print("	* Dispositivos no encontrados")
		quit()
		puertoSerieLPC = serial.Serial("/dev/ttyACM"+str(puerto),115200,timeout=1)
		puertoSerieARDUINO = serial.Serial("/dev/ttyACM"+str(puerto),115200,timeout=1)
		puertoSerieARDUINO = serial.Serial("/dev/ttyACM"+str(puerto),115200,timeout=1)
		
	return  puertoSerieMKS # puertoSerieLPC puertoSerieARDUINO puertoSerieMKS
