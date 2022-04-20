import serial, time, os


def comunicacionBrazo(puerto, comando):
	
	puerto.write(comando.encode("ascii"))
	print("		* Comunicacion Brazo")
	
