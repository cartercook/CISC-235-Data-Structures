#By Carter Cook - "I confirm that this submission is my own work and is consistent with the Queen's regulations on Academic Integrity."
#----------IMPORTS AND CLASSES----------#
from __future__ import division #prevent integer division
import random #to generate random lists
import csv #for exporting data to a spreadsheet

class Binary_Tree_vertex(object):
	def __init__(self, value):
			self.value = value
			self.left_child = None
			self.right_child = None

	def __str__(self):
		string = ""
		if self.left_child is not None:
			string = str(self.left_child)
		string = string + str(self.value) + ", "
		if self.right_child is not None:
			string = string + str(self.right_child)
		return string

class RB_Vertex(Binary_Tree_vertex):
	def __init__(self, value, isLeaf=False):
		if not isLeaf:
			self.value = value
			self.left_child = RB_Vertex(None, True)
			self.right_child = RB_Vertex(None, True)
			self.red = True
		else:
			self.value = None
			self.black = True
		self.is_a_leaf = isLeaf

	def has_Red_child(self):
		if self.left_child is None or self.right_child is None:
			return False
		return (self.left_child.red) or (self.right_child.red)

	@property
	def black(self):
		return not self.red
	@black.setter
	def black(self, value):
		self.red = not value

	def __str__(self):
		if not self.is_a_leaf:
			return str(self.left_child) + str(self.value) + ", " + str(self.right_child)
		return ""

#----------BINARY SEARCH TREE FUNCTIONS----------#
def Total_Depth(root, depth):
	if root is None:
		return 0
	elif root.value is None:
		return 1
	else:
		return depth + Total_Depth(root.left_child, depth + 1) + Total_Depth(root.right_child, depth + 1)
def BST_Insert(root, x):
	root = rec_BST_Insert(root, x)
	return root
def rec_BST_Insert(current, x):
	if current == None:
		return Binary_Tree_vertex(x)
	elif current.value < x:
		current.right_child = rec_BST_Insert(current.right_child,x)
	else:
		current.left_child = rec_BST_Insert(current.left_child,x)
	return current

#----------RED BLACK TREE FUNCTIONS----------#
def RB_insert(root, x):
	# insert the value x into the Red-Black tree
	root = rec_RB_insert(root, x)
	root.black = True      # we always colour the root Black
	return root
def rec_RB_insert(current, x):
	if current.is_a_leaf:      # is_a_leaf is a Boolean attribute of RB_Vertex objects - you might prefer a different solution to the 
							   # problem of identifying leaves
		return RB_Vertex(x)
		# the constructor for RB_Vertex creates the vertex, colours it Red, and
		# gives it two empty leaves coloured Black
	elif current.value < x:
		# we recurse down the right side
		current.right_child = rec_RB_insert(current.right_child, x)
		# now check for balance
		if current.red:
			# we don't have to check for balance at Red vertices - current's parent will take care of it
			return current
		elif current.right_child.red:
			# if current's right child is Red, check the grandchildren
			if current.right_child.has_Red_child():
				# there are two consecutive Red vertices - fix the problem
				return RB_fix_R(current, x)
			else:
				# no rebalance needed
				return current
		else:
			# current.right_child is Black - there is no Red-Red conflict so no rebalance is needed
			return current
	else:
		# current.value < x
		# we recurse down the left side
		#     logic is the same as for the right side
		current.left_child = rec_RB_insert(current.left_child, x)
		if current.red:
			return current
		elif current.left_child.red:
			if current.left_child.has_Red_child():
				return RB_fix_L(current, x)
			else:
				return current
		else:
			return current
def RB_fix_L(current, x):
	# current's left child is Red with a Red child, so we need to fix things
	child = current.left_child
	sib = current.right_child
	if sib.red:
		# no rotation, just recolour and continue
		child.black = True
		sib.black = True
		current.red = True
		return current
	else:
		# sib.black, so we need to rotate
		# we can use x to figure out which rotation is needed
		if x < child.value:
			# single rotation case - the LL situation
			# identify the important grandchild
			grandchild = child.left_child
			# fix the pointers
			current.left_child = child.right_child
			child.right_child = current
			# fix the colours
			child.black = True
			current.red = True
			# return the new root of this subtree
			return child
		else:
			# double rotation case - the LR situation
			# identify the important grandchild
			grandchild = child.right_child
			# fix the pointers
			child.right_child = grandchild.left_child
			current.left_child = grandchild.right_child
			grandchild.left_child = child
			grandchild.right_child = current
			# fix the colours
			grandchild.black = True
			current.red = True
			# return the new root of this subtree
			return grandchild
def RB_fix_R(current, x):
	# just the mirror image of RB_fix_L(current,value)
	# current's right child is Red with a Red child, so we need to fix things
	child = current.right_child
	sib = current.left_child
	if sib.red:
		# no rotation, just recolour and continue
		child.black = True
		sib.black = True
		current.red = True
		return current
	else:
		# sib.black == True, so we need to rotate
		# we can use x to figure out which rotation is needed
		if x > child.value:
			# single rotation case - the LL situation
			# identify the important grandchild
			grandchild = child.right_child
			# fix the pointers
			current.right_child = child.left_child
			child.left_child = current
			# fix the colours
			child.black = True
			current.red = True
			# return the new root of this subtree
			return child
		else:
			# double rotation case - the LR situation
			# identify the important grandchild
			grandchild = child.left_child
			# fix the pointers
			child.left_child = grandchild.right_child
			current.right_child = grandchild.left_child
			grandchild.right_child = child
			grandchild.left_child = current
			# fix the colours
			grandchild.black = True
			current.red = True
			# return the new root of this subtree
			return grandchild

#----------OPEN SPREADSHEET FOR WRITING----------#
myFile = open("RedBlackTreeResults.csv", 'wb')
wr = csv.writer(myFile, quoting=csv.QUOTE_ALL)

#----------BEGIN EXPERIMENT----------#
#first column are my n values
data = [[  20,0,0,0,0,0],
		[ 100,0,0,0,0,0], 
		[ 500,0,0,0,0,0],
		[2500,0,0,0,0,0]]
for row in data:
	for k in xrange(1000): #xrange is faster than range deal wit it
		testBST = None
		testRBT = RB_Vertex(None, True) #create a leaf vertex
		for i in random.sample(xrange(row[0]*3), row[0]): #randomly pick n out of n*3 possibilities
			testBST = BST_Insert(testBST, i)
			testRBT = RB_insert(testRBT, i)
		R = Total_Depth(testBST, 1)/Total_Depth(testRBT, 1)
		if R < 0.75:
			row[1] = row[1] + 1
		elif R < 0.92:
			row[2] = row[2] + 1
		elif R <= 1.08:
			row[3] = row[3] + 1
		elif R <= 1.25:
			row[4] = row[4] + 1
		else:
			row[5] = row[5] + 1
#convert amounts to percentages
for row in data:
	total = 0
	for col in range(1,len(row)):
		total = total + row[col]
	for col in range(1,len(row)):
		row[col] = "{0:.0f}%".format(row[col]/total * 100)

#----------WRITE TO CSV AND CLOSE----------#
wr.writerow(["n","R < 0.75", "0.75 <= R < 0.92", "0.92 <= R <= 1.08", "1.08 < R <= 1.25", "R > 1.5"])
for i in xrange(len(data)):
	wr.writerow(data[i])
myFile.close()
