import pygtk
pygtk.require('2.0')

import gio
import gtk

from node import Node, ListNode
from gionode import GioNode

class GitRepoNode(ListNode):
	def __init__(self, repo, parent = None):
		all_heads = [ \
			GitTreeNode(head.object.tree, parent = self, name = head.name) for head in repo.heads
		]

		children = [ \
			GitTreeNode(repo.head.object.tree, parent = self, name = repo.head.name),
			ListNode(self, all_heads, name = 'all heads'),
		]

		ListNode.__init__(self, parent, children)

		self.repo_ = repo

	def name(self):
		return 'git repository'

	def children(self):
		return self.children_

class GitIndexObjectNode(Node):
	def __init__(self, git_object, parent, name = None):
		Node.__init__(self, parent)
		self.git_object_ = git_object
		self.specified_name_ = name

	def name(self):
		if self.specified_name_ is not None:
			return self.specified_name_
		return self.git_object_.name

	def children(self):
		return None

class GitBlobNode(GitIndexObjectNode, GioNode):
	def __init__(self, *args, **kwargs):
		GitIndexObjectNode.__init__(self, *args, **kwargs)
		GioNode.__init__(self, gio.File(self.git_object_.abspath), **kwargs)

class GitTreeNode(GitIndexObjectNode):
	def __init__(self, *args, **kwargs):
		GitIndexObjectNode.__init__(self, *args, **kwargs)
		self.children_ = None

	def children(self):
		if self.children_ is not None:
			return self.children_

		self.children_ = []
		self.children_.extend([GitTreeNode(child_tree, self) for child_tree in self.git_object_.trees])
		self.children_.extend([GitBlobNode(child_blob, self) for child_blob in self.git_object_.blobs])

		return self.children_

