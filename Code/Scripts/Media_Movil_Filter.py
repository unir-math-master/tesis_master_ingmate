def MediaMovilFilter(ArrayData,Window):
	FilterArray=[]
	for x in range(len(ArrayData)):
		if(x>=Window):#si ya paso el minimo del indice del arreglo, el valor del promedio es en base al ancho de la ventana
			FilterArray.insert(x,MediaMovilOperation(ArrayData,x,Window))
		else:#Si x es menor al indice del arreglo, el valor a dividir es x
			FilterArray.insert(x,MediaMovilOperation(ArrayData,x,x+1))
	return FilterArray