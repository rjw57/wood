import gio
import weakref

class Node(object):
	def __init__(self, parent):
		self.parent_ref_ = weakref.ref(parent) if parent is not None else None

	def parent(self):
		if self.parent_ref_ is not None:
			return self.parent_ref_()
		return None

	def name(self):
		raise NotImplementedError

	def children(self):
		raise NotImplementedError

	SEPARATOR = 'SEPARATOR'

	def actions(self):
		"""Return a sequence of (callable, label, gio.Icon) actions for
		this node. Sequences may contain the special value Node.SEPARATOR to
		indicate there should be a separator.

		The icon may be None.
		
		"""
		return ((self.show_file, 'Show', None), )

	def show_file(self):
		pass

	def has_children(self):
		if self.children() is not None and len(self.children()) > 0:
			return True
		return False

	def icon(self):
		return gio.content_type_get_icon(self.content_type())

	def content_type(self):
		if self.has_children():
			return 'inode/directory'
		return gio.content_type_guess(self.name(), None, False)

class ListNode(Node):
	def __init__(self, parent, children, name = None):
		self.children_ = children
		self.name_ = name
	
	def children(self):
		return self.children_

	def name(self):
		return self.name_
