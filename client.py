from coapthon.client.helperclient import HelperClient
from coapthon.resources.resource import Resource
import sys
import time
import os
from datetime import datetime

port = 5683

def post(host,port,endpoint):
	try:
		client = HelperClient(server=(host, port))
		response = client.post(str(endpoint), None, None , None, 2)
	except:
		print('Not work')
	client.stop()
	if response is not None:
		return response.pretty_print()
	else:
		return None


def get(host,port,endpoint):
	try:
		client = HelperClient(server=(host, port))		
		response = client.get(endpoint, timeout=2)
	except:
		print('Not work')
	client.stop()
	if response is not None:
		return response.payload
	else:
		return None
	

def obtenerParametros():
	method = str(sys.argv[1])
	#Asigno a la variable method la funcion que corresponda al metodo a ejecutarse
	if(method == '-p'):
		method = post
	elif method == '-g':
		method = get
	else:
		print('El metodo ingresado no es valido. Pruebe con -g (GET) o -p (POST)')
		exit(0)

	host = sys.argv[2]
	cantNodos = sys.argv[3]
	endpoint = str(sys.argv[4])

	#Chequeo formato de endpoint valido, y sino no acomodo
	if(endpoint[0] == '/'):
		endpoint = endpoint[1:len(endpoint)]

	#Verifico si se paso un intervalo de tiempo por parametro, sino asigno 0 para ejecute solo una vez	
	try:
		timeinterval = int(sys.argv[5])
	except IndexError:
		timeinterval = 0
		print('Ejecutando sin intervalos de tiempo')
	
	return method, host, cantNodos, endpoint, timeinterval

def saveLog(output, endpoint):
	if output is None:
		output = 'request failed .. redirecting..'

	method = str(sys.argv[1])
	if(method == '-p'):
		method = 'POST'
	elif method == '-g':
		method = 'GET'

	cwd = os.getcwd()
	filename = cwd + '/logfile'
	logfile = open(filename, "a+")
	logfile.seek(0)
	entry = str(datetime.now()) + "\n\n" + 'REQUEST: ' + str(method)+ ' ' + str(endpoint) + "\n" + str(output) + '\n' + '--------------' + "\n"
	logfile.write(entry)

def make_requests(cantNodos, last_number, host,endpoint):
	for i in range(int(cantNodos)):
		if(i + last_number >= 10):
			host = ip_minima[:-1] + str(hex(i + last_number)[-1])
		else:
			host = ip_minima[:-1] + str(i + last_number)
		print(host)
		output = method(host,port,endpoint)
		saveLog(output, endpoint)
		print(output)


#Debe haber al menos 4 parametros (metodo, ipv6, cantidad de nodos, endpoint)
if len(sys.argv) < 5:
	print('Parametros: (-g | -p) server_ipv6_minima cantNodos endpoint timeinterval(OPCIONAL)')
	exit(0)

#Obtengo los parametros
method, ip_minima, cantNodos, endpoint, timeinterval = obtenerParametros()


#Ejecuto metodo correspondiente al parametro
#De forma iterativa si hay un intervalo de tiempo, sino una unica vez

last_number = int(ip_minima.split(':')[len(ip_minima.split(':')) -1])

if timeinterval == 0:
	make_requests(cantNodos,last_number,host,endpoint)
else:
	try:
		while True:
			make_requests(cantNodos,last_number,host,endpoint)
			time.sleep(timeinterval)
	except KeyboardInterrupt:
		print('Saliendo...')

	

