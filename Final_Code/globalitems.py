from symbol_table import *

symbol_table=SymbolTable()

show=0			#for debugging

stack = []				#stack of new_temporaries    [used in three_addr_generator in get_newtemp()]

genCode = True

# what about String : It is same as array
widths = {'integer':4, 'float':8, 'char':4, 'boolean':4}			#used in three_addr_generator in get_newtemp()

# Global storage of 3-address code
class Code:
	def __init__(self):
		self.next_instr = 0;
		self.code=[]

three_addr_code = Code()
