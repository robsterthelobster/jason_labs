#Jason Li
#Date: 1/27/15

import math

class VectorN(object):
	"""Creates a VectorN object"""       				   
	def __init__(self, param):
		"""Initializes the VectorN object."""
		 #mData is a list of scalars
		 #mDim  is the number of elements in mData
		if isinstance(param, int):
			"""Creates a VectorN object with [param] length 
			   and initializes values with 0.0s"""
			self.mDim = param
			self.mData = [0.0] * param
				
		elif hasattr(param, "__len__") and hasattr(param, "__getitem__"):
			"""Creates a VectorN object with the values in the parameter
			   **CONVERTS values into FLOAT**"""
			#Below ONLY checks the values in [param] if they are numbers.
			#(Allows string representation of numbers)
			self.mDim = len(param)
			self.mData = []
			for i in range(len(param)):
				self.mData.append(float(param[i]))

		else:
			"""If the param is neither the above two, give user a Error message"""
			raise TypeError(param + " is not integer or list of scalars!")
	
	def __str__(self):
		"""Changes the string representation of print([VectorN object])
		   Format: <VectorN: num, num, ...>"""
		temp = "<Vector" + str(self.mDim) + ": "
		temp += str(self.mData)[1:-1]
		temp += ">"
		return temp
	
	def __len__(self):
		"""Returns the number of elements in mData by using mDim"""
		return self.mDim
	
	def __getitem__(self, index):
		"""Returns the value of mData[index]"""
		return self.mData[index]
	
	def __setitem__(self, index, value):
		"""Sets the value of mData[index] to the passed value"""
		#First checks if index is a integer
		#Then checks if value is either int or float. Allows string numbers
		if isinstance(index, int):
			if isinstance(value, (int, float)) or value.isnumeric():
				self.mData[index] = float(value)
			else:
				raise ValueError(str(value) + " is not a valid value")
		else:
			raise ValueError(str(index) + " is not a valid index")
		return None
		
	def copy(self):
		"""Creates a new VectorN object with the same values of this VectorN object"""
		return VectorN(self.mData)
	
	def __eq__(self, vector):
		"""Checks if two VectorN object values are equal to each other
		   Returns True or False"""
		#Checks if vector is a VectorN object before comparison
		if isinstance(vector, VectorN) and self.mDim == vector.mDim:
			for i in range(self.mDim):
				if  self.mData[i] != vector.mData[i]:
					return False
			return True
		else:
			return False
			
	def iTuple(self):
		"""Returns a tuple with the integer values of mData"""
		tempList = []
		for i in self.mData:
			tempList.append(int(i))
		return tuple(tempList)
		
	#--------------------------------Lab 2 starts here--------------------------------
	
	def __add__(self, vector):
		"""Returns a vector with values of this and the passed vector added to each other"""
		tempList = []
		if isinstance(vector, VectorN) and self.mDim == vector.mDim:
				for i in range(0, self.mDim):
					tempList.append(self.mData[i] + vector.mData[i])
				newVector = VectorN(tempList)
				return newVector
		else:
			raise TypeError("You can only add another Vector"+str(self.mDim)+" to this Vector"+str(self.mDim))
			
	def __sub__(self, vector):
		"""Returns a vector with values of this subtracted by the passed vector"""
		if isinstance(vector, VectorN) and self.mDim == vector.mDim:
			return self + (-vector)
		else:
			raise TypeError("You can only subtract another Vector"+str(self.mDim)+" to this Vector"+str(self.mDim))
			
	def __mul__(self, num):
		"""Multiply this vector by the passed value
		   Format: self * num"""
		tempList = []
		if isinstance(num, (int, float)):
			for i in self.mData:
				tempList.append(float(i*num))
			newVector = VectorN(tempList)
			return newVector
		else:
			raise TypeError("You can only multiply this Vector by a scalar")
			return NotImplemented                      #If self*num format fails, tries num*self by using __rmul__
		
	def __rmul__(self, num):
		"""Multiply the passed value with this vector
		   Format: num * self"""
		return self * num
			
	def __truediv__(self, num):
		"""Divide this vector by the passed num
		   Format: self / num"""
		if isinstance(num, (int, float)):
			return self * (1/num)
		else:
			raise TypeError("You can only divide this Vector by a scalar")
			return NotImplemented                      #If self/num format fails, goes to __rtruediv___
			
	def __rtruediv__(self, num):
		"""Since you cannot divide anything by a VectorN, this just displays a error"""
		raise NotImplementedError("You cannot divide anything by a VectorN")
			
	def __neg__(self):
		"""Returns a vector with the negative values of this vector"""
		tempList = []
		for i in self.mData:
			tempList.append(-1*i)
		newVector = VectorN(tempList)
		return newVector
			
	def isZero(self):
		"""Returns True or False values depending on this VectorN's values are all 0"""
		for i in self.mData:
			if i != 0:                       #Check for a value NOT 0
				return False
		return True
		
	def magnitude(self):
		"""Returns the magnitude of this vector using pythagorean theorem"""
		tempValue = 0
		for i in self.mData:
			tempValue += math.pow(i,2)
		tempValue = math.sqrt(tempValue)
		return tempValue
	
	def normalized_copy(self):
		"""Returns a vector with the normalized values of the original vector
		   Normalized value is vector[i] / magnitude"""
		return self/self.magnitude()
		