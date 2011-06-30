import pygtk
pygtk.require('2.0')

import gio
import gtk
import os
import sys

from treemodel 	import TreeModel
from treeview	import TreeView
from gionode 	import GioNode

class Application(object):
	def __init__(self):
		self.window_ = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window_.connect("delete_event", self.delete_event_)
		self.window_.connect("destroy", self.destroy_)

		path = os.getcwd()
		if len(sys.argv) > 1:
			path = sys.argv[1]

		self.root_ = GioNode(gio.File(path = path), None)
		self.model_ = TreeModel(self.root_)

		tree_view = TreeView(model = gtk.TreeModelSort(self.model_))

		scrolled_window = gtk.ScrolledWindow()
		scrolled_window.add(tree_view)
		self.window_.add(scrolled_window)

		self.window_.show_all()

	def main(self):
		gtk.main()

	def destroy_(self, widget, data=None):
		gtk.main_quit()
	
	def delete_event_(self, widget, event, data=None):
		return False
