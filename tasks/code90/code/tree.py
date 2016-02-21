class Node:
	def __init__(self, val):
		self.value = val
		self.left = None
		self.right = None

class BST:
	def __init__(self):
		self.root = None

	def insertVal(self, val):
		n = Node(val)
		self.insert(self.root, n)

	def insert(self, root, node):
		if not self.root:
			self.root = node
			return

		if node.value <= root.value:
			if not root.left:
				root.left = node
			else: 
				self.insert(root.left, node)
		else:
			if not root.right:
				root.right = node
			else:
				self.insert(root.right, node)

	def serialize(self, root):
		if not root:
			return []
		if not root.left and not root.right:
			return [root.value]

		return [root.value] + self.serialize(root.left) + self.serialize(root.right)

	def invert(self, root):
		if not root:
			return
		tmp = root.left
		root.left = root.right
		root.right = tmp
		self.invert(root.left)
		self.invert(root.right)

# for i in range(10):
# 	tree = BST()
# 	for val in [1,2,3,4,5]:
# 		tree.insertVal(val)
# 	print(tree.serialize(tree.root))
# 	tree.invert(tree.root)
# 	print(tree.serialize(tree.root))