import gi
from configparser  import ConfigParser
from Recursos import data as Recursos
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GLib, Gdk, Gio

hb = Gtk.HeaderBar()
hb.set_show_close_button(True)
hb.props.title = Recursos.nombre_empresa
caja_headerbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

class MyWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self)
		self.set_default_size(800, 500)
		self.set_titlebar(hb)
		self.ventana_actual,self.linea_actual,self.proceso_actual=[],[],[]

		self.menu_principal=Gtk.Notebook()
		#self.menu_principal.set_tab_pos(Gtk.PositionType.LEFT)
		self.menu_principal.set_show_tabs(False)
		self.add(self.menu_principal)

		self.liststore_lineas=Gtk.ListStore(str)
		self.liststore_procesos=Gtk.ListStore(str)

		button = Gtk.Button()
		icon = Gio.ThemedIcon(name="applications-system-symbolic")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		button.add(image)
		button.connect('clicked',self.ir_ventana_configuracion)

		button2 = Gtk.Button()
		icon = Gio.ThemedIcon(name="preferences-system-details-symbolic")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		button2.add(image)

		
		ventanas_combo = Gtk.ComboBoxText()
		ventanas_combo.set_entry_text_column(0)
		ventanas_combo.connect("changed", self.cambio_ventanas_combo)
		for ventana,valor in Recursos.menu_lineas_por_plantas.items():
			ventanas_combo.append_text(ventana)
		
		self.lineas_combo = Gtk.ComboBox.new_with_model(self.liststore_lineas)
		self.lineas_combo.connect("changed", self.cambio_lineas_combo)
		renderer_text = Gtk.CellRendererText()
		self.lineas_combo.pack_start(renderer_text, True)
		self.lineas_combo.add_attribute(renderer_text, "text", 0)
		
		self.procesos_combo = Gtk.ComboBox.new_with_model(self.liststore_procesos)
		self.procesos_combo.connect("changed", self.cambio_procesos_combo)
		renderer_text2 = Gtk.CellRendererText()
		self.procesos_combo.pack_start(renderer_text2, True)
		self.procesos_combo.add_attribute(renderer_text2, "text", 0)
		
		ventanas_combo.set_active(0)
		self.lineas_combo.set_active(0)
		self.procesos_combo.set_active(0)
		
		caja_headerbar.add(button)
		caja_headerbar.add(ventanas_combo)
		caja_headerbar.add(self.lineas_combo)
		caja_headerbar.add(self.procesos_combo)

		
		hb.pack_start(caja_headerbar)
		hb.pack_end(button2)

		pagina = Paginas_normal(self.menu_principal,'Planta 1')
		self.menu_principal.append_page(pagina)

		#pagina = Pagina_Plantas(self.menu_principal,'Planta 2')
		#self.menu_principal.append_page(pagina)


		#self.box_configuraciones=Gtk.Grid()
		self.box_configuraciones=Gtk.Box(spacing=16)
		#self.box_configuraciones.set_column_homogeneous(True)
		self.ventana_configuracion()
		self.menu_principal.append_page(self.box_configuraciones)

	def ventana_configuracion(self):
		#grid_configuraciones=Gtk.Grid()


		grid_plantas=Gtk.Grid()
		#grid_plantas.set_column_homogeneous(True)

		label=Gtk.Label()
		label.set_text('Plantas')
		label.set_valign(Gtk.Align.CENTER)

		self.entry_agregar_planta = Gtk.Entry()
		self.entry_agregar_planta.set_valign(Gtk.Align.CENTER)
		button_agregar_planta = Gtk.Button.new_with_label('Agregar')
		button_agregar_planta.set_valign(Gtk.Align.CENTER)
		button_agregar_planta.connect("clicked", self.agregar_planta)
		self.plantas_liststore = Gtk.ListStore(str)
		for planta,valor in Recursos.menu_lineas_por_plantas.items():
			self.plantas_liststore.append([planta])
		self.treeview = Gtk.TreeView.new_with_model(self.plantas_liststore)
		renderer = Gtk.CellRendererText()
		renderer.set_alignment(0.5,0)
		column = Gtk.TreeViewColumn('', renderer, text=0)
		self.treeview.append_column(column)
		self.tree_selection=self.treeview.get_selection()
		self.tree_selection.connect('changed',self.seleccion_planta_configuraciones)
		grid_plantas.attach(label, 0, 0, 2, 1)
		grid_plantas.attach_next_to(self.entry_agregar_planta, label, Gtk.PositionType.BOTTOM, 1, 1)
		grid_plantas.attach_next_to(button_agregar_planta,self.entry_agregar_planta, Gtk.PositionType.RIGHT, 1, 1)
		grid_plantas.attach_next_to(self.treeview,self.entry_agregar_planta, Gtk.PositionType.BOTTOM, 2, 1)
		#self.box_configuraciones.attach(grid_plantas,0,0,1,1)

		#grid_configuraciones.attach(grid_plantas, 0, 0, 1, 1)
		self.box_configuraciones.pack_start(grid_plantas, True, False, 0)

		grid_lineas=Gtk.Grid()
		#grid_lineas.set_column_homogeneous(True)
		label=Gtk.Label()
		label.set_text('Lineas')
		label.set_valign(Gtk.Align.CENTER)
		self.entry_agregar_linea = Gtk.Entry()
		self.entry_agregar_linea.set_valign(Gtk.Align.CENTER)
		button_agregar_linea = Gtk.Button.new_with_label('Agregar')
		button_agregar_linea.set_valign(Gtk.Align.CENTER)
		button_agregar_linea.connect("clicked", self.agregar_linea_planta)
		self.lineas_liststore = Gtk.ListStore(str)
		self.treeview = Gtk.TreeView.new_with_model(self.lineas_liststore)
		renderer = Gtk.CellRendererText()
		renderer.set_alignment(0.5,0)
		column = Gtk.TreeViewColumn('', renderer, text=0)
		self.treeview.append_column(column)
		self.treeview.expand_all()
		self.tree_selection=self.treeview.get_selection()
		self.tree_selection.connect('changed',self.seleccion_linea_configuraciones)
		grid_lineas.attach(label, 0, 0, 2, 1)
		grid_lineas.attach_next_to(self.entry_agregar_linea, label, Gtk.PositionType.BOTTOM, 1, 1)
		grid_lineas.attach_next_to(button_agregar_linea,self.entry_agregar_linea, Gtk.PositionType.RIGHT, 1, 1)
		grid_lineas.attach_next_to(self.treeview,self.entry_agregar_linea, Gtk.PositionType.BOTTOM, 2, 1)
		#self.box_configuraciones.attach_next_to(grid_lineas, grid_plantas, Gtk.PositionType.RIGHT, 1, 1)

		#grid_configuraciones.attach_next_to(grid_lineas, grid_plantas, Gtk.PositionType.RIGHT, 1, 1)
		self.box_configuraciones.pack_start(grid_lineas, True,False, 0)

		grid_proceso=Gtk.Grid()
		#grid_proceso.set_column_homogeneous(True)
		label=Gtk.Label()
		label.set_text('Procesos')
		label.set_valign(Gtk.Align.CENTER)
		self.entry_agregar_proceso = Gtk.Entry()
		self.entry_agregar_proceso.set_valign(Gtk.Align.CENTER)
		button_agregar_proceso = Gtk.Button.new_with_label('Agregar')
		button_agregar_proceso.set_valign(Gtk.Align.CENTER)
		button_agregar_proceso.connect("clicked", self.agregar_proceso_planta)
		self.proceso_liststore = Gtk.ListStore(str)
		self.treeview = Gtk.TreeView.new_with_model(self.proceso_liststore)
		renderer = Gtk.CellRendererText()
		renderer.set_alignment(0.5,0)
		column = Gtk.TreeViewColumn('', renderer, text=0)
		self.treeview.append_column(column)
		grid_proceso.attach(label, 0, 0, 2, 1)
		grid_proceso.attach_next_to(self.entry_agregar_proceso, label, Gtk.PositionType.BOTTOM, 1, 1)
		grid_proceso.attach_next_to(button_agregar_proceso,self.entry_agregar_proceso, Gtk.PositionType.RIGHT, 1, 1)
		grid_proceso.attach_next_to(self.treeview,self.entry_agregar_proceso, Gtk.PositionType.BOTTOM, 2, 1)
		#self.box_configuraciones.attach_next_to(grid_proceso, grid_lineas, Gtk.PositionType.RIGHT, 1, 1)

		#grid_configuraciones.attach_next_to(grid_proceso,grid_lineas, Gtk.PositionType.RIGHT, 1, 1)
		self.box_configuraciones.pack_end(grid_proceso, True, False, 0)

		#grid___=Gtk.Grid()

		#grid_configuraciones.attach_next_to(grid___,grid_configuraciones, Gtk.PositionType.BOTTOM, 1, 1)

		#self.box_configuraciones.pack_start(grid_configuraciones, True, False, 0)

		
	def agregar_planta(self, widget):
		if self.entry_agregar_planta.get_text() != "":
			self.plantas_liststore.append([self.entry_agregar_planta.get_text()])
			Recursos.plantas.append(self.entry_agregar_planta.get_text())
	def agregar_linea_planta(self, widget):
		if self.entry_agregar_linea.get_text() != "":
			self.lineas_liststore.append([self.entry_agregar_linea.get_text()])
	def agregar_proceso_planta(self, widget):
		if self.entry_agregar_proceso.get_text() != "":
			self.proceso_liststore.append([self.entry_agregar_proceso.get_text()])
	def seleccion_planta_configuraciones(self,selection):
		try:
			(self.modelo_arbol,self.numero_iter)=selection.get_selected()
			self.planta_seleccionada_configuraciones=self.modelo_arbol[self.numero_iter][0]
			self.lineas_liststore.clear()
			if self.ventana_actual!=(len(self.menu_principal)-1):
				for linea,valor in Recursos.menu_lineas_por_plantas[self.planta_seleccionada_configuraciones].items():
					self.lineas_liststore.append([linea])
		except:
			pass
	def seleccion_linea_configuraciones(self,selection):
		try:
			(self.modelo_arbol,self.numero_iter)=selection.get_selected()
			self.linea_seleccionada_configuraciones=self.modelo_arbol[self.numero_iter][0]
			self.proceso_liststore.clear()
			if self.ventana_actual!=2:
				for proceso,valor in Recursos.menu_lineas_por_plantas[self.planta_seleccionada_configuraciones][self.linea_seleccionada_configuraciones].items():
					self.proceso_liststore.append([proceso])
		except:
			pass
	def ir_ventana_configuracion(self,button):
		if self.menu_principal.get_current_page()==0:
			self.menu_principal.set_current_page(1)
		else:
			self.menu_principal.set_current_page(0)


	def cargar_configuraciones(self):
		parser = ConfigParser()
		parser.read('config.cfg')
		for llave,valor in parser.items('Plantas'):
			self.plantas.append(valor)
			self.lineas_por_planta[valor],self.menu_lineas_por_plantas[valor]=[],[]
		self.checkbutton=[]
		for seccion in self.plantas:
			for llave,valor in parser.items(seccion):
				self.checkbutton.append(0)
				self.lineas_por_planta[seccion].append(valor)
		#print(self.plantas)
		#print(self.lineas_por_planta
		
	def ventana_pfmea(self):
		#self.page2=Gtk.Box()
		#self.page2.set_border_width(10)

		#456 000 000 000 * 20

		#self.grid = Gtk.Grid()
		#self.page2.add(self.grid)
		#self.grid.set_column_homogeneous(True)
		#self.grid.set_row_homogeneous(True)


		self.entry_filtro = Gtk.Entry()

		button_filtro = Gtk.Button.new_with_label('Filtro')
		#button_filtro
		button_borrar_filtro = Gtk.Button.new_with_label('Borrar')
		button_filtro.connect("clicked", self.filtro_boton)
		button_borrar_filtro.connect("clicked", self.filtro_boton_borrar)
		#button_filtro.set_text()

		#Creating the ListStore model
		self.software_liststore = Gtk.ListStore(str, int, str)
		for software_ref in software_list:	self.software_liststore.append(list(software_ref))
		self.current_filter_language = None

		#Creating the filter, feeding it with the liststore model
		self.language_filter = self.software_liststore.filter_new()
		#setting the filter function, note that we're not using the
		self.language_filter.set_visible_func(self.language_filter_func)
		#creating the treeview, making it use the filter as a model, and adding the columns
		self.treeview = Gtk.TreeView.new_with_model(self.language_filter)

		for i, column_title in enumerate(["Software", "Release Year", "Programming Language"]):
			#print(i, column_title)
			button = Gtk.Button.new_with_label(column_title)
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			self.treeview.append_column(column)

		#creating buttons to filter by programming language, and setting up their events
		#self.buttons = list()
		#for prog_language in ["Java", "C", "C++", "Python", "None"]:
		#	button = Gtk.Button(prog_language)
		#	self.buttons.append(button)
		#	button.connect("clicked", self.on_selection_button_clicked)

		


		#vbox.pack_start(self.entry, True, True, 0)
		#setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
		self.scrollable_treelist = Gtk.ScrolledWindow()
		self.scrollable_treelist.set_vexpand(True)


		#self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)

		self.grid.attach(button_borrar_filtro, 0, 0, 1, 1)
		#self.grid.attach_next_to(self.entry, self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
		self.grid.attach_next_to(self.entry_filtro, button_borrar_filtro, Gtk.PositionType.RIGHT, 8, 1)
		self.grid.attach_next_to(button_filtro, self.entry_filtro, Gtk.PositionType.RIGHT, 1, 1)
		#self.grid.attach_next_to(self.buttons[0], self.entry, Gtk.PositionType.RIGHT, 1, 1)
		self.grid.attach_next_to(self.scrollable_treelist, self.entry_filtro, Gtk.PositionType.BOTTOM, 8, 10)
		
		#self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
		#for i, button in enumerate(self.buttons[1:]):
		#	self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)

		self.scrollable_treelist.add(self.treeview)


		#self.texto=Gtk.Label()
		#self.texto.set_text('PFMEA')
		#self.menu_principal.append_page(self.page2,self.texto)

	def cambio_ventanas_combo(self, combo):
		self.ventana_actual = combo.get_active()
		print(combo.get_text(0))
		self.liststore_lineas.clear()
		if self.ventana_actual!=(len(self.menu_principal)-1):
			for linea in Recursos.lineas_por_planta[Recursos.plantas[self.ventana_actual]]:
				self.liststore_lineas.append([linea])

		self.lineas_combo.set_active(0)
		self.menu_principal.set_current_page(self.ventana_actual)

	def cambio_lineas_combo(self, combo):
		self.linea_actual = combo.get_active()
		#print(self.ventana_actual,self.linea_actual)
		#print(Recursos.lineas_por_planta[Recursos.plantas[self.ventana_actual]][self.linea_actual])
		#print(Recursos.menu_lineas_por_plantas[Recursos.plantas[self.ventana_actual]])

		self.liststore_procesos.clear()
		if self.ventana_actual!=2:
		#	print(self.ventana_actual,self.linea_actual)
		#	print(Recursos.menu_lineas_por_plantas[Recursos.plantas[self.ventana_actual]][Recursos.lineas_por_planta[Recursos.plantas[self.ventana_actual]][self.linea_actual]])
			for proceso in Recursos.menu_lineas_por_plantas[Recursos.plantas[self.ventana_actual]][Recursos.lineas_por_planta[Recursos.plantas[self.ventana_actual]][self.linea_actual]]:
		#		print(proceso)
				self.liststore_procesos.append([proceso])

		

		self.procesos_combo.set_active(0)

		#if text==0:
		#	self.liststore_lineas.clear()
		#	for linea in Recursos.lineas_por_planta['Planta 1']:
		#		self.liststore_lineas.append([linea])
		#if text==1:
		#	self.liststore_lineas.clear()
		#	for linea in Recursos.lineas_por_planta['Planta 2']:
		#		self.liststore_lineas.append([linea])
		#if text==2:
		#	self.liststore_lineas.clear()
		#self.lineas_combo.set_active(0)
		#self.menu_principal.set_current_page(text)

	def cambio_procesos_combo(self, combo):
		self.proceso_actual = combo.get_active()
		#text = combo.get_active()
		#print(text)
		'''if text==0:
			#self.liststore_lineas.clear()
			#for linea in Recursos.lineas_por_planta['Planta 1']:
			#	self.liststore_lineas.append([linea])
			self.menu_principal.set_current_page(0)
		if text=='Planta 2':
			self.liststore_lineas.clear()
			for linea in Recursos.lineas_por_planta['Planta 2']:
				self.liststore_lineas.append([linea])
			self.menu_principal.set_current_page(1)
		if text=='Configuraciones':
			self.menu_principal.set_current_page(2) '''

	def ventana_ppap(self):
		self.image = Gtk.Image.new_from_file("wallet.png")
		#self.texto=Gtk.Label()
		#self.texto.set_text('PPAP')
		self.page1=Gtk.Box()
		self.page1.set_border_width(10)

		self.button_image=Gtk.Button()
		self.button_image.add(self.image)
		self.button_image.set_border_width(0)
		self.button_image.set_size_request(32,32)
		self.page1.pack_start(self.button_image, True, True, 0)
		#self.menu_principal.append_page(self.page1,self.texto)

	def on_timeout(self, user_data):
		new_value = self.liststore[self.current_iter][1] + 1
		if new_value > 100:
			self.current_iter = self.liststore.iter_next(self.current_iter)
			if self.current_iter is None:
				self.reset_model()
			new_value = self.liststore[self.current_iter][1] + 1

		self.liststore[self.current_iter][1] = new_value
		return True

	def reset_model(self):
		for row in self.liststore:
			row[1] = 0
		self.current_iter = self.liststore.get_iter_first()

	def on_button_clicked(self, widget):
		print(widget.get_label())

	def language_filter_func(self, model, iter, data):
		columna=0
		if self.current_filter_language is None or self.current_filter_language == "None":
			return True
		else:
			try:
				self.current_filter_language=int(self.current_filter_language)
			except:
				pass
			for i in range(3):
				if model[iter][i] == self.current_filter_language:
					columna=i
			return model[iter][columna] == self.current_filter_language

class Paginas_normal(Gtk.Box):
	def __init__(self, parent,planta_fin):
		super().__init__(spacing=10)
		self.__parent = parent
		grid_principal=Gtk.Grid()
		self.pack_start(grid_principal, True, True, 0)
		grid_principal.set_row_homogeneous(True)
		'''stack = Gtk.Stack()
		stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
		stack.set_transition_duration(500)
		espacio_linea=Gtk.Box()
		self.pack_start(espacio_linea, True, True, 0)
		for linea in Recursos.lineas_por_planta[planta_fin]:
			espacio_linea=Gtk.Box()
			grid_linea=Gtk.Grid()
			espacio_linea.pack_start(grid_linea, True, True, 0)
			grid_linea.set_row_homogeneous(True)
			self.menu_lineas = Gtk.Stack()
			self.menu_lineas.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
			self.menu_lineas.set_transition_duration(500)
			for proceso in Recursos.menu_lineas_por_plantas[planta_fin][linea]:
				buttonpoo = Gtk.Button.new_with_label("Click me! - "+proceso)
				buttonpoo.set_border_width(10)
				buttonpoo.set_valign(Gtk.Align.CENTER)
				self.menu_lineas.add_titled(buttonpoo, "check"+proceso, proceso)
			self.stack_menu = Gtk.StackSidebar()
			self.stack_menu.set_stack(self.menu_lineas)
			grid_linea.attach(self.stack_menu, 0, 0, 1, 1)
			grid_linea.attach_next_to(self.menu_lineas, self.stack_menu, Gtk.PositionType.RIGHT, 1, 1)
			stack.add_titled(espacio_linea, "check"+linea , linea)
		stack_switcher = Gtk.StackSidebar()
		stack_switcher.set_stack(stack)
		grid_principal.attach(stack_switcher, 0, 0, 1, 1)
		grid_principal.attach_next_to(stack, stack_switcher, Gtk.PositionType.RIGHT, 1, 1)'''
	def cambio_ventanas_combo(self, combo):
		text = combo.get_active_text()
		if text=='Planta 1':
			self.menu_principal.set_current_page(0)
		if text=='Planta 2':
			self.menu_principal.set_current_page(1)
		if text=='Configuraciones':
			self.menu_principal.set_current_page(2)

'''class Pagina_Plantas(Gtk.Box):
	def __init__(self, parent,planta_fin):
		super().__init__(spacing=10)
		self.__parent = parent

		grid_principal=Gtk.Grid()
		self.pack_start(grid_principal, True, True, 0)
		grid_principal.set_row_homogeneous(True)
		stack = Gtk.Stack()
		stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
		stack.set_transition_duration(500)
		espacio_linea=Gtk.Box()
		self.pack_start(espacio_linea, True, True, 0)
		for linea in Recursos.lineas_por_planta[planta_fin]:
			espacio_linea=Gtk.Box()
			grid_linea=Gtk.Grid()
			espacio_linea.pack_start(grid_linea, True, True, 0)
			grid_linea.set_row_homogeneous(True)
			self.menu_lineas = Gtk.Stack()
			self.menu_lineas.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
			self.menu_lineas.set_transition_duration(500)
			for proceso in Recursos.menu_lineas_por_plantas[planta_fin][linea]:
				buttonpoo = Gtk.Button.new_with_label("Click me! - "+proceso)
				buttonpoo.set_border_width(10)
				buttonpoo.set_valign(Gtk.Align.CENTER)
				self.menu_lineas.add_titled(buttonpoo, "check"+proceso, proceso)
			self.stack_menu = Gtk.StackSidebar()
			self.stack_menu.set_stack(self.menu_lineas)
			grid_linea.attach(self.stack_menu, 0, 0, 1, 1)
			grid_linea.attach_next_to(self.menu_lineas, self.stack_menu, Gtk.PositionType.RIGHT, 1, 1)
			stack.add_titled(espacio_linea, "check"+linea , linea)
		stack_switcher = Gtk.StackSidebar()
		stack_switcher.set_stack(stack)
		grid_principal.attach(stack_switcher, 0, 0, 1, 1)
		grid_principal.attach_next_to(stack, stack_switcher, Gtk.PositionType.RIGHT, 1, 1)
	def cambio_ventanas_combo(self, combo):
		text = combo.get_active_text()
		if text=='Planta 1':
			self.menu_principal.set_current_page(0)
		if text=='Planta 2':
			self.menu_principal.set_current_page(1)
		if text=='Configuraciones':
			self.menu_principal.set_current_page(2)

class Pagina_Configuraciones(Gtk.Grid):
	def __init__(self, parent):
		super().__init__()
		self.__parent = parent

		grid_plantas=Gtk.Grid()
		#self.pack_start(grid_plantas, True, True, 0)
		#grid_plantas.set_row_homogeneous(True)

		label=Gtk.Label()
		label.set_text('Plantas')
		label.set_valign(Gtk.Align.CENTER)

		self.entry_agregar_planta = Gtk.Entry()
		self.entry_agregar_planta.set_valign(Gtk.Align.CENTER)
		button_agregar_planta = Gtk.Button.new_with_label('Agregar')
		button_agregar_planta.set_valign(Gtk.Align.CENTER)
		button_agregar_planta.connect("clicked", self.agregar_planta)

		self.plantas_liststore = Gtk.ListStore(str)
		for planta in Recursos.plantas:	
			self.plantas_liststore.append([planta])

		self.treeview = Gtk.TreeView.new_with_model(self.plantas_liststore)
		button = Gtk.Button.new_with_label('Plantas')
		renderer = Gtk.CellRendererText()
		renderer.set_alignment(0.5,0)
		column = Gtk.TreeViewColumn('Plantas', renderer, text=0)

		self.treeview.append_column(column)

		grid_plantas.attach(label, 0, 0, 1, 1)
		grid_plantas.attach_next_to(self.entry_agregar_planta, label, Gtk.PositionType.RIGHT, 1, 1)
		grid_plantas.attach_next_to(button_agregar_planta,self.entry_agregar_planta, Gtk.PositionType.RIGHT, 1, 1)
		grid_plantas.attach_next_to(self.treeview,label, Gtk.PositionType.BOTTOM, 3, 1)

		self.attach(grid_plantas,0,0,1,1)

		grid_lineas=Gtk.Grid()

		label=Gtk.Label()
		label.set_text('Lineas')
		label.set_valign(Gtk.Align.CENTER)


		#vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		#self.add(vbox)

		stack = Gtk.Stack()
		stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		stack.set_transition_duration(1000)

		checkbutton = Gtk.CheckButton("Click me!")
		stack.add_titled(checkbutton, "check", "Check Button")

		label = Gtk.Label()
		label.set_markup("<big>A fancy label</big>")
		stack.add_titled(label, "label", "A label")

		stack_switcher = Gtk.StackSwitcher()
		stack_switcher.set_stack(stack)
		vbox.pack_start(stack_switcher, True, True, 0)
		vbox.pack_start(stack, True, True, 0)


		#self.current_filter_language = None
		self.entry_filtro = Gtk.Entry()
		self.entry_filtro.set_valign(Gtk.Align.CENTER)
		button_filtro = Gtk.Button.new_with_label('Filtro')
		button_filtro.set_valign(Gtk.Align.CENTER)
		button_filtro.connect("clicked", self.filtro_boton)
		button_borrar_filtro = Gtk.Button.new_with_label('Borrar')
		button_borrar_filtro.set_valign(Gtk.Align.CENTER)
		button_borrar_filtro.connect("clicked", self.filtro_boton_borrar)

		button_agregar = Gtk.Button.new_with_label('Agregar')
		button_agregar.set_valign(Gtk.Align.CENTER)
		button_agregar.connect("clicked", self.agregar_boton)

		self.software_liststore = Gtk.ListStore(str, int, str)
		for software_ref in software_list:	self.software_liststore.append(list(software_ref))
		self.current_filter_language = None

		#Creating the filter, feeding it with the liststore model
		self.language_filter = self.software_liststore.filter_new()
		#setting the filter function, note that we're not using the
		self.language_filter.set_visible_func(self.language_filter_func)

		#self.language_filter.set_visible_func(self.three_boton_borrar)
		#creating the treeview, making it use the filter as a model, and adding the columns
		self.treeview = Gtk.TreeView.new_with_model(self.language_filter)

		for i, column_title in enumerate(["Software", "Release Year", "Programming Language"]):
			#print(i, column_title)
			button = Gtk.Button.new_with_label(column_title)
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			self.treeview.append_column(column)


		#self.tree_selection=self.treeview.get_selection()
		#self.tree_selection.connect('changed',self.selectionchanged)


		self.entry_item1 = Gtk.Entry()
		self.entry_item1.set_valign(Gtk.Align.CENTER)
		#self.entry_item1.set_text(self.item1)

		self.entry_item2 = Gtk.Entry()
		self.entry_item2.set_valign(Gtk.Align.CENTER)
		#self.entry_item2.set_text(self.item2)

		self.entry_item3 = Gtk.Entry()
		self.entry_item3.set_valign(Gtk.Align.CENTER)
		#self.entry_item3.set_text(self.item3)

		button_borrar_tree = Gtk.Button.new_with_label('Borrar tree')
		button_borrar_tree.set_valign(Gtk.Align.CENTER)
		button_borrar_tree.connect("clicked", self.three_boton_borrar)

		#creating buttons to filter by programming language, and setting up their events
		#self.buttons = list()
		#for prog_language in ["Java", "C", "C++", "Python", "None"]:
		#	button = Gtk.Button(prog_language)
		#	self.buttons.append(button)
		#	button.connect("clicked", self.on_selection_button_clicked)

		


		#vbox.pack_start(self.entry, True, True, 0)
		#setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
		self.scrollable_treelist = Gtk.ScrolledWindow()
		self.scrollable_treelist.set_vexpand(True)


		#self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)

		grid_principal.attach(button_borrar_filtro, 0, 0, 1, 1)
		#grid_principal.attach_next_to(self.entry, self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
		grid_principal.attach_next_to(self.entry_filtro, button_borrar_filtro, Gtk.PositionType.RIGHT, 8, 1)
		grid_principal.attach_next_to(button_filtro, self.entry_filtro, Gtk.PositionType.RIGHT, 1, 1)
		grid_principal.attach_next_to(button_agregar, button_filtro, Gtk.PositionType.RIGHT, 1, 1)

		grid_principal.attach_next_to(self.entry_item1, button_agregar, Gtk.PositionType.RIGHT, 1, 1)
		grid_principal.attach_next_to(self.entry_item2, self.entry_item1, Gtk.PositionType.RIGHT, 1, 1)
		grid_principal.attach_next_to(self.entry_item3, self.entry_item2, Gtk.PositionType.RIGHT, 1, 1)
		grid_principal.attach_next_to(button_borrar_tree, self.entry_item3, Gtk.PositionType.RIGHT, 1, 1)
		#grid_principal.attach_next_to(self.buttons[0], self.entry, Gtk.PositionType.RIGHT, 1, 1)
		grid_principal.attach_next_to(self.scrollable_treelist, self.entry_filtro, Gtk.PositionType.BOTTOM, 8, 10)
		grid_principal.attach_next_to(label,self.scrollable_treelist, Gtk.PositionType.BOTTOM, 8, 10)
		
		#self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
		#for i, button in enumerate(self.buttons[1:]):
		#	self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)

		self.scrollable_treelist.add(self.treeview)


		#self.texto=Gtk.Label()
		#self.texto.set_text('PFMEA')
		#self.menu_principal.append_page(self.page2,self.texto)

		stack = Gtk.Stack()
		stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
		stack.set_transition_duration(500)
		espacio_linea=Gtk.Box()
		self.pack_start(espacio_linea, True, True, 0)
		for linea in Recursos.lineas_por_planta[planta_fin]:
			espacio_linea=Gtk.Box()
			grid_linea=Gtk.Grid()
			espacio_linea.pack_start(grid_linea, True, True, 0)
			grid_linea.set_row_homogeneous(True)
			self.menu_lineas = Gtk.Stack()
			self.menu_lineas.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
			self.menu_lineas.set_transition_duration(500)
			for proceso in Recursos.menu_lineas_por_plantas[planta_fin][linea]:
				buttonpoo = Gtk.Button.new_with_label("Click me! - "+proceso)
				buttonpoo.set_border_width(10)
				buttonpoo.set_valign(Gtk.Align.CENTER)
				self.menu_lineas.add_titled(buttonpoo, "check"+proceso, proceso)
			self.stack_menu = Gtk.StackSidebar()
			self.stack_menu.set_stack(self.menu_lineas)
			grid_linea.attach(self.stack_menu, 0, 0, 1, 1)
			grid_linea.attach_next_to(self.menu_lineas, self.stack_menu, Gtk.PositionType.RIGHT, 1, 1)
			stack.add_titled(espacio_linea, "check"+linea , linea)
		stack_switcher = Gtk.StackSidebar()
		stack_switcher.set_stack(stack)
		grid_principal.attach(stack_switcher, 0, 0, 1, 1)
		grid_principal.attach_next_to(stack, stack_switcher, Gtk.PositionType.RIGHT, 1, 1) 

	def filtro_boton(self, widget):
		self.current_filter_language = self.entry_filtro.get_text()
		if self.current_filter_language=="": self.current_filter_language=None
		self.language_filter.refilter()
	def filtro_boton_borrar(self, widget):
		self.entry_filtro.set_text('None')
		self.current_filter_language = self.entry_filtro.get_text()
		self.language_filter.refilter()
		self.entry_filtro.set_text('')
	def agregar_boton(self, widget):
		self.software_liststore.append(["PFMEA",2020,'Python'])
	def agregar_planta(self, widget):
		self.plantas_liststore.append([self.entry_agregar_planta.get_text()])
		Recursos.plantas.append(self.entry_agregar_planta.get_text())
	def language_filter_func(self, model, iter, data):
		columna=0
		try:
			if len(self.current_filter_language)!=2:
				if self.current_filter_language is None or self.current_filter_language == "None":
					return True
				else:
					try:
						self.current_filter_language=int(self.current_filter_language)
					except:
						pass
					for i in range(3):
						print(model[iter][i])
						if model[iter][i] == self.current_filter_language:
							columna=i
					return model[iter][columna] == self.current_filter_language
			else:
				for i in range(3):
					if model[iter][i] == self.modelo_arbol[self.numero_iter][i]:
						print(model)
						print('iter filter ',iter)
		except:
			pass

	def selectionchanged(self,selection):
		(self.modelo_arbol,self.numero_iter)=selection.get_selected()
		
		current_iter = self.software_liststore.get_iter_first()
		#print(current_iter)
		

		#self.software_liststore.remove(current_iter)
		print(self.software_liststore)
		print('modelo arbol',self.modelo_arbol)
		print(self.numero_iter)
		#print(self.modelo_arbol[self.numero_iter][0],self.modelo_arbol[self.numero_iter][1],self.modelo_arbol[self.numero_iter][2])
		self.item1,self.item2,self.item3=self.modelo_arbol[self.numero_iter][0],self.modelo_arbol[self.numero_iter][1],self.modelo_arbol[self.numero_iter][2]

		self.entry_item1.set_text(self.item1)
		self.entry_item2.set_text(str(self.item2))
		self.entry_item3.set_text(self.item3)

		self.current_filter_language=[self.modelo_arbol[self.numero_iter][0],self.modelo_arbol[self.numero_iter][1],self.modelo_arbol[self.numero_iter][2]]

		print(self.software_liststore.iter_is_valid(self.numero_iter))
		#self.software_liststore.remove(self.numero_iter)
		
		#print("trview.get_cursor() returns: {}".format(self.treeview.get_cursor()))
		#(model, pathlist) = self.tree_selection.get_cursor()
		#print(model, pathlist)
		#print(self.tree_selection)
		for path in pathlist :
			tree_iter = model.get_iter(path)
			value = model.get_value(tree_iter,0)
			print (value) 

	def three_boton_borrar(self, widget):
		pass
		#print(type(self.numero_iter))
		#print(self.modelo_arbol[self.numero_iter])
		#print(self.software_liststore[self.numero_iter])
		#print(self.modelo_arbol[self.numero_iter][0],self.modelo_arbol[self.numero_iter][1],self.modelo_arbol[self.numero_iter][2])
		
		#self.software_liststore.remove(self.numero_iter)

		#print(self.software_liststore[iter]) '''

		


if __name__ == '__main__':
	win = MyWindow()
	win.connect("destroy", Gtk.main_quit)
	win.show_all()
	Gtk.main()

