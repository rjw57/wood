import pygtk
pygtk.require('2.0')

import gio
import gtk

class TreeView(gtk.TreeView):
	def __init__(self, *args, **kwargs):
		gtk.TreeView.__init__(self, *args, **kwargs)

		self.set_property('rules-hint', True)

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
		# tc.set_attributes(cell, text=2)
		tc.set_cell_data_func(cell, self.content_type_description_)
		tc.set_sort_column_id(2)
		self.append_column(tc)
	
	def content_type_description_(self, column, cell, model, iter):
		content_type = model.get(iter, 2)[0]
		cell.set_property('text', gio.content_type_get_description(content_type))

