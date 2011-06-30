import weakref

class Node(object):
	def __init__(self, parent):
		self.parent_ref_ = weakref.ref(parent) if parent is not None else None

	def name(self):
		raise NotImplemented

	def icon(self):
		raise NotImplemented

	def parent(self):
		if self.parent_ref_ is not None:
			return self.parent_ref_()
		return None

	def has_children(self):
		raise NotImplemented

	def children(self):
		raise NotImplemented

	def content_type(self):
		raise NotImplemented

