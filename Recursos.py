from configparser  import ConfigParser


ventanas,plantas,lineas_por_planta=[],[],{}
menu_lineas_por_plantas={}
parser = ConfigParser()
parser.read('config.cfg')
nombre_empresa=parser.get('general','nombre')
for llave,valor in parser.items('Ventanas'):
	ventanas.append(valor)
for llave,valor in parser.items('Plantas'):
	plantas.append(valor)
	lineas_por_planta[valor],menu_lineas_por_plantas[valor]=[],{}
checkbutton=[]
for seccion in plantas:
	for llave,valor in parser.items(seccion):
		menu_lineas_por_plantas[seccion][valor]=[]
		checkbutton.append(0)
		lineas_por_planta[seccion].append(valor)
for planta in plantas:
	for linea in lineas_por_planta[planta]:
		try: 
			for llave,valor in parser.items(linea):	
				#print(llave,valor)
				menu_lineas_por_plantas[planta][linea].append(valor)
		except:
			pass

#print(plantas)
#print(lineas_por_planta)
#print(menu_lineas_por_plantas)
