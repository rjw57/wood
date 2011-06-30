import pygtk
pygtk.require('2.0')

import gio
import gobject;
import gtk

class TreeModel(gtk.GenericTreeModel):
	column_types_ = [ str, gio.Icon, str, object ]

	def __init__(self, root_node, *args, **kwargs):
		gtk.GenericTreeModel.__init__(self, *args, **kwargs)
		self.root_node_ = root_node
	
	def on_get_flags(self):
		return 0

	def on_get_n_columns(self):
		return len(TreeModel.column_types_)

	def on_get_column_type(self, index):
		return TreeModel.column_types_[index]

	def on_get_iter(self, path):
		if len(path) == 1:
			assert(path[0] == 0)
			return self.root_node_

		parent_node = self.on_get_iter(path[:-1])
		siblings = parent_node.children()

		return siblings[path[-1]]

	def on_get_path(self, rowref):
		if rowref is self.root_node_:
			return (0,)

		parent = rowref.parent()
		siblings = parent.children()

		return on_get_path(parent) + (siblings.index(rowref),)

	def on_get_value(self, rowref, column):
		if column == 0:
			return rowref.name()
		elif column == 1:
			return rowref.icon()
		elif column == 2:
			return rowref.content_type()
		elif column == 3:
			return rowref

		raise IndexError('Invalid column index: %s' % (column,))

	def on_iter_next(self, rowref):
		parent = rowref.parent()
		if parent is None:
			return None

		siblings = parent.children()
		my_idx = siblings.index(rowref)

		try:
			return siblings[my_idx+1]
		except IndexError:
			return None

	def on_iter_children(self, parent):
		if parent is None:
			return None

		if not parent.has_children():
			return None

		try:
			return parent.children()[0]
		except IndexError:
			return None

	def on_iter_has_child(self, rowref):
		return rowref.has_children()

	def on_iter_n_children(self, rowref):
		if rowref is None:
			# There is one top-level element
			return 1

		# Return number of children in node
		return len(rowref.children()) if rowref.has_children() else 0

	def on_iter_nth_child(self, parent, n):
		if parent is None:
			return self.root_node_
		try:
			return parent.children()[n]
		except IndexError:
			return None

	def on_iter_parent(self, child):
		return child.parent()

