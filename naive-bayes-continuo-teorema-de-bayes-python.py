import csv
import random
import math

def loadCsv(archivo):
	lines = csv.reader(open(archivo, "rb"))
	datos = list(lines)
	for i in range(len(datos)):
		datos[i] = [float(x) for x in datos[i]]
	return datos
