import csv
import random
import math
from matplotlib import pyplot as plt
#cargamos nuestros datos
def loadCsv(archivo):
	lines = csv.reader(open(archivo, "rb"))
	datos = list(lines)
	for i in range(len(datos)):
		datos[i] = [float(x) for x in datos[i]]
	return datos

#separamos los datos de entrenamiento de los de test
def DatosEntrenamiento(datos,porcentaje):
	muestra = int(len(datos)*porcentaje)
	EntrenamientoDatos = []
	test = list(datos)
	while len(EntrenamientoDatos)< muestra:
		index = random.randrange(len(test))
		EntrenamientoDatos.append(test.pop(index))
	return(EntrenamientoDatos, test)

#separamos nuestra data de entrenamiento en clases
def porClase(datos):
	datosClase = {}
	for i in range(len(datos)):
		vector = datos[i]
		if (vector[-1] not in datosClase):
			datosClase[vector[-1]] = []
		datosClase[vector[-1]].append(vector)
	return datosClase
#calculamos lo necesario para saber la probabilidad
def mean(feature):
	return sum(feature)/float(len(feature))

def stdev(feature):
	avg = mean(feature)
	varianza = sum([pow(x-avg,2) for x in feature])/float(len(feature)-1)
	return math.sqrt(varianza)

#creamos una lista con la media y la desviacion, recibimos datos de entrenamiento
def elemento(Entrenamiento):
	elementos = [(mean(atributo), stdev(atributo)) for atributo in zip(*Entrenamiento)]
	del elementos[-1]
	return elementos

def elemento_por_clase(datos):
	DatosenClase = porClase(datos)
	summaries = {}
	for clase, feature in DatosenClase.iteritems():
		summaries[clase] = elemento(feature)
	return summaries

def probabilidad(x,mean,stdev):
	exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
	return (1/(math.sqrt(2*math.pi)*stdev)) * exponent

def probabilidadPorClases(summaries, dato_entrenamiento):
	probabilidades = {}
	for classValue, ClassSummaries in summaries.iteritems():
		probabilidades[classValue] = 1
		for i in range(len(ClassSummaries)):
			mean, stdev = ClassSummaries[i]
			x = dato_entrenamiento[i]
			probabilidades[classValue] *=probabilidad(x,mean,stdev)
	return probabilidades

def predict(summaries, dato_entrenamiento):
	probabilidades = probabilidadPorClases(summaries, dato_entrenamiento)
	return probabilidades

def getPredict(summaries, test):
	predicciones = []
	for i in range(len(test)):
		resultado = predict(summaries, test[i])
		predicciones.append(resultado)
	return predicciones

def decide(probabilidades):
	asignar = []
	for i in probabilidades:
		if i[0]>i[1]:
			asignar.append(0)
		else:
			asignar.append(1)
	return asignar

def desempenho(decisiones,test):
	c = 0 
	for i in range(len(test)):
		if float(decisiones[i]) == test[i][-1]:
			c = c+1
	return c/float(len(test))

def main():
	filename = 'diabetes.txt'
	data = loadCsv(filename)
	porcentaje = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
	result = []
	for i in porcentaje:
		Entrenamiento, test = DatosEntrenamiento(data,i)
		summaries = elemento_por_clase(Entrenamiento)
		probabilidades = getPredict(summaries, test)
		decisiones = decide(probabilidades)
		resultado = desempenho(decisiones,test)
		result.append(resultado)

	plt.plot(porcentaje, result, color='green', marker='o', linestyle='solid')
	plt.show()
	#print test[1]
	#prueba = [[1.0, 85.0, 66.0, 29.0, 0.0, 26.6, 0.351, 31.0, 0.0],[2.0, 197.0, 70.0, 45.0, 543.0, 30.5, 0.158, 53.0, 1.0]]
	

main()
