import pygtk
pygtk.require('2.0')

import gio
import gtk

from node import Node

class GioNode(Node):
	def __init__(self, file, parent = None):
		Node.__init__(self, parent)
		self.file_ = file
		self.file_info_ = self.file_.query_info(','.join([
			gio.FILE_ATTRIBUTE_STANDARD_TYPE,
			gio.FILE_ATTRIBUTE_STANDARD_NAME,
			gio.FILE_ATTRIBUTE_STANDARD_DISPLAY_NAME,
			gio.FILE_ATTRIBUTE_STANDARD_ICON,
			gio.FILE_ATTRIBUTE_STANDARD_CONTENT_TYPE,
		]))
		self.children_ = None

	def show_file(self):
		try:
			gtk.show_uri(None, self.file_.get_uri(), gtk.gdk.CURRENT_TIME)
		except gio.Error as e:
			print(e)

	def name(self):
		return self.file_info_.get_display_name()

	def icon(self):
		return self.file_info_.get_icon()

	def has_children(self):
		if self.file_info_.get_file_type() != gio.FILE_TYPE_DIRECTORY:
			return False
		elif self.children() is None:
			return False
		elif len(self.children()) == 0:
			return False
		return True

	def children(self):
		if self.file_info_.get_file_type() != gio.FILE_TYPE_DIRECTORY:
			return None

		if self.children_ is not None:
			return self.children_

		attributes = ','.join([
			gio.FILE_ATTRIBUTE_STANDARD_NAME,
		])

		child_enumerator = self.file_.enumerate_children(attributes)

		self.children_ = []

		next_file = child_enumerator.next_file()
		while next_file is not None:
			self.children_.append(GioNode(
				self.file_.get_child(next_file.get_name()),
				self
			))
			next_file = child_enumerator.next_file()

		return self.children_

	def content_type(self):
		return self.file_info_.get_attribute_as_string(gio.FILE_ATTRIBUTE_STANDARD_CONTENT_TYPE)

