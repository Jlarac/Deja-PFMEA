from configparser  import ConfigParser

class datos(object):
	def cargar_configuraciones(self):
		self.plantas,self.lineas_por_planta=[],{}
		self.menu_lineas_por_plantas={}
		parser = ConfigParser()
		parser.read('config.cfg')
		self.nombre_empresa=parser.get('general','nombre')

		for numero,planta in parser.items('Plantas'):
			#self.plantas.append(planta)
			#self.lineas_por_planta[planta],
			self.menu_lineas_por_plantas[planta]={}

			for numero,linea in parser.items(planta):
				self.menu_lineas_por_plantas[planta][linea]={}

				parser = ConfigParser()
				parser.read(linea+'.cfg')
				try: 
					for llave,valor in parser.items('Procesos'):	
						self.menu_lineas_por_plantas[planta][linea][valor]={}
				except:
					pass

		#for llave,valor in self.menu_lineas_por_plantas.items():
		#	print(llave,valor)

		'''for planta,valor in self.menu_lineas_por_plantas.items():
			for llave,valor in parser.items(planta):
				self.menu_lineas_por_plantas[planta][valor]={}
				#self.lineas_por_planta[seccion].append(valor)

		for seccion in self.plantas:
			for llave,valor in parser.items(seccion):
				self.menu_lineas_por_plantas[seccion][valor]={}
				self.lineas_por_planta[seccion].append(valor)

		for llave,valor in self.menu_lineas_por_plantas.items():
			print(llave,valor)
			for llave2,valor2 in self.menu_lineas_por_plantas[llave].items():
				print(llave2,valor2)

		for planta in self.plantas:
			for linea in self.lineas_por_planta[planta]:
				parser = ConfigParser()
				parser.read(linea+'.cfg')
				try: 
					for llave,valor in parser.items('Procesos'):	
						self.menu_lineas_por_plantas[planta][linea][valor]={}
				except:
					pass'''

		#print(plantas)
		#print(lineas_por_planta)
		print(self.menu_lineas_por_plantas)


	def guardar_configuraciones(self):
		pass



data=datos()

data.cargar_configuraciones()

#print(data.nombre_empresa)