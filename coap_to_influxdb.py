#encoding: utf-8

import os
import time
import sys

host = '192.168.1.38'
db = 'tomas_laborde'
ipv6_base = 'aaaa::c30c:0:0:2'
cant_nodos = 3

"""
#Obtener los valores desde parametros
host = sys.argv[1]
db = sys.argv[2]
ipv6_base = sys.argv[3]
cant_nodos = sys.argv[4]
"""

""" 
Se podria haber resuelto tambien leyendo del logfile que genera el cliente
y que quede mas prolija la obtencion de datos, pero lo implemente asi para ajustarme al enunciado
4) Escribir un programa que lea mediante su cliente COAP 
el valor del sensor de temperatura de las mota cada 10 segundos 
y lo inserte en la base de datos creada anteriormente.
Hay un par de cuestiones que podrian haberse resuelto de una mejor forma,
pero involucraba hacer cambios en el cliente ya entregado.
"""

#Asumo que la mota siempre va a estar declarada despues de un border, y que la primera va a tener el id 2

try:
	while True:
		#No entrego el recurso de temperatura porque implemente uno que solo retorna un par de valores
		#Tuve problemas con C y su tipado
		salida = os.popen("python client.py -g {} {} temperature".format(ipv6_base, cant_nodos)).read()
		if cant_nodos <= 1:
			temperatura = salida_seccionada.split('\n')[len(salida_seccionada.split('\n')) - 2]
			mota = 2
			#Resolvi con curl por conflictos con la libreria de influxdb en la VM
			os.system("curl -i -XPOST 'http://{}:8086/write?db={}' --data-binary 'la_plata mota={},temp={}'".format(host,db,mota,int(temperatura)))
		else:
			salida_seccionada = salida.split('Thread due to request\n')
			for i in range(cant_nodos):
				print(i)
				if i == cant_nodos - 1:
					temperatura = salida_seccionada[cant_nodos]
					print(temperatura)
				else:
					temperatura = salida_seccionada[cant_nodos - 1].split('\n')[0]
					#print(salida_seccionada[cant_nodos])
					print(temperatura)
				mota = i + 2
				try:
					#Me aseguro haber recibido un valor numerico y no un None o vacio 
					#(En este caso int porque eso retorna mi recurso).
					int(temperatura)
					os.system("curl -i -XPOST 'http://{}:8086/write?db={}' --data-binary 'la_plata mota={},temp={}'".format(host,db,mota,int(temperatura)))
				except:
					print('No fue posible obtener valor')
		
		time.sleep(10)
except KeyboardInterrupt:
	exit(0)
