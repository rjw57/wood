import pygtk
pygtk.require('2.0')

import gio
import gtk
import os
import sys

from git.repo	import Repo

from treemodel 	import TreeModel
from treeview	import TreeView

from gionode 	import GioNode
from gitnode	import GitRepoNode

class Application(object):
	def __init__(self):
		self.window_ = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window_.connect("delete_event", self.delete_event_)
		self.window_.connect("destroy", self.destroy_)

		path = os.getcwd()
		if len(sys.argv) > 1:
			path = sys.argv[1]

		notebook = gtk.Notebook()
		notebook.set_tab_pos(gtk.POS_LEFT)

		def label(text):
			widget = gtk.Label(text)
			widget.set_property('angle', 90)
			return widget

		file_root = GioNode(gio.File(path = path))
		file_model = TreeModel(file_root)
		file_view = TreeView(model=gtk.TreeModelSort(file_model))
		file_scrolled_window = gtk.ScrolledWindow()
		file_scrolled_window.add(file_view)
		notebook.append_page(file_scrolled_window, label('filesystem'))

#		git_root = GitRepoNode(Repo(path))
#		git_model = TreeModel(git_root)
#		git_view = TreeView(model=gtk.TreeModelSort(git_model))
#		git_scrolled_window = gtk.ScrolledWindow()
#		git_scrolled_window.add(git_view)
#		notebook.append_page(git_scrolled_window, label('git'))

		self.window_.add(notebook)

		self.window_.show_all()

	def main(self):
		gtk.main()

	def destroy_(self, widget, data=None):
		gtk.main_quit()
	
	def delete_event_(self, widget, event, data=None):
		return False
