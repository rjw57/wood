import pygtk
pygtk.require('2.0')

import gio
import gtk

class TreeView(gtk.TreeView):
	def __init__(self, *args, **kwargs):
		gtk.TreeView.__init__(self, *args, **kwargs)

		self.set_property('rules-hint', True)
		self.connect('row-activated', self.row_activated_)

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
		cell.set_property('text', gio.content_type_get_description(content_type))
	
	def row_activated_(self, treeview, path, column):
		model = treeview.get_model()
		row = model.get_iter(path)
		node = model.get_value(row, 3)
		node.show_file()

