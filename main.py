import serial, time, os
import transformaPuntos as coordenadas # Antes transforma
import configEntradaRutas as  config # Para todo lo relacionado con la configuracion
import rutina as rutina
import RPi.GPIO as GPIO
import comandosRutinaSKR as comandosMov
import emergencia as emergencia

# Variables globales
puntoX = 850 # Almacenamiento de la coordenada X del robot, el valor puesto es su coordenada incial
puntoY = 250 # Almacenamiento de la coordenada Y del robot, el valor puesto es su coordenada incial
angulo = 0 # Almacenamiento del ángulo que tiene el robot, el valor puesto es el ángulo inical
controlador = "SKR" # SKR o MKS
'''
    Estados = ["configuracion" , "incio" , "fin" , "rutina" , "avanza" , "brazo" , "gira" , "emergencyStop" ]
'''
estado = "configuracion" # Estado en el que nos encontramos
estado_anterior = "configuracion" # Estado en el que estuvimos
emergencyStop = False 

def main():

    global puntoX, puntoY, angulo, estado, estado_anterior, emergencyStop	# Para poder modificar estas variables aqui y siendo a su vez globales
    rutaElegida = [["A",0,0],"FIN"]
    i = 0
    # Podemos usar un pin del switch para bloquear los motores y liberarlos
    while(True):
        
        '''
            Estado 1 **Configuracion**
        '''
        if estado == "configuracion" :
            if estado_anterior == "configuracion": # Solo se va a ejecutar la primera vez que lancemos el programa. Luego ya no hace falta estableccer conexión de nuevo
                print("\n--------------------------------------------------------------------\n")
                print("***	ElDoro le da la bienvenida")
                print("\n--------------------------------------------------------------------\n")
                print("***	Establecimiento de conexión\n")
                config.configGPIO() # Configuracion de los pines de la Raspi
                puertoSerieSKR = config.configSerial_Master() # Puerto SKR o MKS
                puertoSerieSKR.flushInput()
                puertoSerieESP = config.configSerial_ESP() 
                #puertoSerieESP = 5
            puertoSerieSKR.write(comandosMov.comandoEnableMotores().encode("ascii"))	# Bloqueamos motores para colocar el robot en su debida posicion
            puertoSerieSKR.write(comandosMov.encenderVentilador().encode("ascii")) #Encender ventilador
            puntoX = 850 # Reset variables
            puntoY = 250 # Reset variables
            angulo = 0 # Reset variables
            i = 0 # Reset variables
            
            print("\n--------------------------------------------------------------------\n")
            print("***	Acciones:\n")
            print("	* Boton inicio -> Empiece de rutina")
            print("	* Boton fin -> Finaliza programa")
            print("\n--------------------------------------------------------------------\n")
            estado = "inicio" # Una vez configurado todo pasamos al estado 2 
            estado_anterior = "configuracion"

        '''
            Estado 2 **Inicio**
        '''
        if estado == "inicio" : 
            ruta = config.configCampo() # Se establece campo y rutina en función switch
            #print(ruta)
            i = 0 # Reseteamos
            
            if GPIO.input(5) == 0 or GPIO.input(5) == False : #	Si pulsamos el botón de inicio
                estado = "rutina" # Cambio a estado 3
                estado_anterior = "inicio"
                rutaElegida = ruta
                inicioPartido = 1
                GPIO.output(13, True) # Encendemos el led verde para saber que estamos a punto de iniciar
                while(inicioPartido):
                    print("17",GPIO.input(17) )
                    if  GPIO.input(17) == 1 or  GPIO.input(17) == True :
                        inicioPartido = 0
                        print("***	Inicio de rutina")
                        print("\n--------------------------------------------------------------------\n")
                    if GPIO.input(6) == 0 or GPIO.input(6) == False : # Si pulsamos le boton de fin 
                        estado = "fin" # Cambio a estado 4
                        estado_anterior = "inicio"
                        inicioPartido = 0
                
                GPIO.output(13, False) # Apagamos el led verde, esto indica que la rutina va a comenzar
            if GPIO.input(6) == 0 or GPIO.input(6) == False : # Si pulsamos le boton de fin 
                estado = "fin" # Cambio a estado 4
                estado_anterior = "inicio"

        '''
            Estado 3 **Rutina**
        '''
        if estado == "rutina" : 
            print(rutaElegida[i])
            if rutaElegida[i] == "FIN" : # Si en el array ruta en contramos fin entonces se ha acabado el script y por tanto volvemos al estado 1
                estado = "fin"
                estado_anterior = "rutina"
                time.sleep(3)
            else :
                # La siguiente línea ejecuta la rutina y nos devuelve la posición a la que se supone que ha mandado el robot y si estamos en situación de emergencia
                time.sleep(0.1)
                puntoX_aux, puntoY_aux , angulo_aux, emergencyStop = rutina.ejecucionRutina(rutaElegida,i, puertoSerieSKR, controlador , puertoSerieESP) # Ejecución de rutina
                puntoX = puntoX_aux + puntoX # Almacenamos posición X
                puntoY= puntoY_aux + puntoY # Almacenamos posición Y
                angulo = angulo_aux + angulo # Almacenamos posición theta
               
                print("		* Robot situado en: X", puntoX, " Y",puntoY," Theta", angulo,"\n")
 
                if emergencyStop : # Si tenemos emergencia
                    estado = "emergencyStop" # Cambio a estado 5
                    estado_anterior = "rutina"
                if GPIO.input(6) == 0 or GPIO.input(6) == False : # Si pulsamos el boton de fin 
                    print("\n--------------------------------------------------------------------\n")
                    estado = "fin" # Cambio a estado 4
                    estado_anterior = "rutina"
                    time.sleep(3)
                if GPIO.input(5) == 0 or GPIO.input(5) == False : # Si pulsamos el boton de inicio estando en rutina volvemos a configuración y el programa comienza de nuevo 
                    estado = "configuracion" # Cambio a estado 1
                    estado_anterior = "rutina"
                    time.sleep(3)
            i = i + 1
       

        
        '''
            Estado 4 **Fin**
        '''
        if estado == "fin" :
            print("***	Programa finalizado")
            print("\n--------------------------------------------------------------------\n")
            GPIO.cleanup()
            puertoSerieSKR.write(comandosMov.apagarVentilador().encode("ascii")) #Apagar ventilador
            puertoSerieSKR.write(comandosMov.comandoDisableMotores().encode("ascii"))	
            quit()
        '''
            Estado 5 **Parada emergencia**
        '''
        if estado == "emergencyStop" :
            print("     ","***	Parada de emergencia\n")
            distancia = [0,0,0]
            emergencia.emergencia(puertoSerieSKR)
            i = i - 1
            print(rutaElegida)
            rutaElegida[i][0] = "E"
            print(rutaElegida)
            puntoX_aux, puntoY_aux , angulo_aux, emergencyStop = rutina.ejecucionRutina(rutaElegida,i, puertoSerieSKR, controlador, 300) # El 300 no vale para nada
            
            i = i + 1
            print(i)
           
            if emergencyStop:
                
                estado = "emergencyStop" # Cambio a estado 5
                estado_anterior = "emergencyStop"
                
            else:
                print("     ","***	Fin de parada de emergencia\n")
                estado_anterior = "emergencyStop"
                estado = "rutina"
main()
