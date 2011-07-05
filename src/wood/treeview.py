import gio
import gtk

from node import Node

class TreeView(gtk.TreeView):
	def __init__(self, *args, **kwargs):
		gtk.TreeView.__init__(self, *args, **kwargs)

		self.set_property('rules-hint', True)
		self.connect('row-activated', self.row_activated_)
		self.connect('button-press-event', self.button_press_event_)
		self.connect('popup-menu', self.popup_menu_)

		icon_cell = gtk.CellRendererPixbuf()
		cell = gtk.CellRendererText()
		tc = gtk.TreeViewColumn('Name')
		tc.pack_start(icon_cell, False)
		tc.pack_start(cell)
		tc.set_attributes(cell, text=0)
		tc.set_attributes(icon_cell, gicon=1)
		tc.set_sort_column_id(0)
		self.append_column(tc)

		cell = gtk.CellRendererText()
		tc = gtk.TreeViewColumn('Type', cell)
		tc.set_cell_data_func(cell, self.content_type_description_)
		tc.set_sort_column_id(2)
		self.append_column(tc)
	
	def content_type_description_(self, column, cell, model, iter):
		content_type = model.get(iter, 2)[0]
		if content_type == 'inode/directory':
			description = ''
		else:
			description = gio.content_type_get_description(content_type)
		cell.set_property('text', description)
	
	def row_activated_(self, treeview, path, column):
		model = treeview.get_model()
		row = model.get_iter(path)
		node = model.get_value(row, 3)
		node.show_file()
	
	def button_press_event_(self, treeview, event):
		if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
			# single right-click

			# find out what is under us
			path_tuple = self.get_path_at_pos(int(event.x), int(event.y))
			if path_tuple is None:
				return

			# we have some path, show the menu
			self.show_popup_for_path_(path_tuple[0],
					          event.x_root, event.y_root,
						  event.button, event.time)

	def popup_menu_(self, treeview):
		# not sure if we want to do something here yet
		pass

	def show_popup_for_path_(self, path, x, y, button, time):
		node_iter = self.get_model().get_iter(path)
		node = self.get_model().get_value(node_iter, 3)

		actions = node.actions()
		if len(actions) == 0:
			return

		menu = gtk.Menu()

		def activate_item(menuitem, func):
			func()

		for action in actions:
			if action is Node.SEPARATOR:
				menu.append(gtk.SeparatorMenuItem())
				continue

			(func, label, icon) = action

			item = gtk.ImageMenuItem()
			item.set_label(label)

			if icon is not None:
				item.set_image(gtk.image_new_from_gicon(icon, gtk.ICON_SIZE_MENU))
				item.set_always_show_image(True)

			item.connect('activate', activate_item, func)
			menu.append(item)

		menu.show_all()

		def pos_func(menu):
			return (int(x), int(y), True)
		menu.popup(None, None, pos_func, button, time)
