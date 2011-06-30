import weakref

class Node(object):
	def __init__(self, parent):
		self.parent_ref_ = weakref.ref(parent) if parent is not None else None

	def parent(self):
		if self.parent_ref_ is not None:
			return self.parent_ref_()
		return None

	def show_file(self):
		raise NotImplementedError

	def name(self):
		raise NotImplementedError

	def icon(self):
		raise NotImplementedError

	def has_children(self):
		raise NotImplementedError

	def children(self):
		raise NotImplementedError

	def content_type(self):
		raise NotImplementedError

