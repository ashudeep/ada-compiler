#from collections import *  #for namedtuple

'''Symbol table entries:
1. Data type entry under its name - only for standard prebuilt ones 			'isdatatype':True
2. Variable entry under its name - enter(id.name, T.type, offset);	
	it canbe 		- type-standard one
					- array of type-standard									'isarray':True
					- string of size											'isstring': , 'type' = String
					- type: predefined record
3. Record entry	under its name - similar to procedure							'isrecord':True
4. Procedure entry under its name  - enterproc (table, name, newtable)			'isprocedure':True
5. Package entry under its name  - enterpackage (table, name, newtable)			'ispackage':True
'''

'''
add_entry() -> for variables
add_beginnig_procedure -> for procedure

for package,record -- left!!
'''

#Hashtable Class: it contains the table
#self.table is dictionary with key=name_of_entry & value=list_of_attributes  eg: a=5.. then name='a'(i.e. lexeme) attribute={'value':5} .. note ada is case-insensitive
#list_of_attributes is a dictionary (list is implemented as dictionary) with many entries with key(attribute_name):value(attribute_value) pairs like - {'type': 'Integer', 'value':'Integer', 'isdatatype':True}
class HashTable:
	def __init__(self):
		self.table={}   # a dictionary

	def add_entry (self, name, list_attributes):
		name=name.lower()			#ada is case-institute
		if name in self.table:
			print 'Error: Entry already present - [' + name + ']'
		else:
			#print "Deepak4iii - ",name," - ",list_attributes
			self.table[name]= {}	# a dictionary
			for i_key in list_attributes:	
				self.table[name][i_key]=list_attributes[i_key]
		
	#update if already present else add it.
	def update_entry(self, name, attribute_name, attribute_value):
		name=name.lower()
		try:						#try catch exception
			self.table[name][attribute_name] = attribute_value
			return True
		except:	
			return False
		
	def get_attribute_value (self, name, attribute_name):
		name=name.lower()
		try:
			return self.table[name][attribute_name]
		except:
			return None			
	
	def is_present(self, name):
		name=name.lower()
		if name in self.table:
			return True
		else: 
			return False
	
	def get_table(self):
		return self.table				
	
	def print_table(self):
		print "Table is : Entry name ==> Attribute_list"
		for name in self.table:
			print name,' ==> ', self.table[name]


#Environment Class: Contains current current_hashtable and pointer to parent Environment
class Env:
	def __init__(self, prev=None):
		self.current_hashtable = HashTable()
		self.width = 0						# overall offset/width of this env
		self.paramwidth = 0
		self.prev_env=prev
		
	#adds entry in current hashtable
	def add_entry(self,name, list_attributes):
		self.current_hashtable.add_entry(name, list_attributes)

	#updates the entry in most recent hashtable (recent ancestor) i.e. correct scope
	def update_entry(self, name, attribute_name, attribute_value):
		env=self
		while env!=None:
			if env.current_hashtable.update_entry(name, attribute_name, attribute_value) == True:
				return
			env=env.prev_env
		print 'Error: Entry not present for updation - [' + name + ']'

	#Returns list of attributes from most recent hashtable (recent ancestor) corresponding to name. Returns None if entry not found
	def get_attribute_value(self,name, attribute_name):
		env=self
		while env!=None:
			found=env.current_hashtable.get_attribute_value(name, attribute_name)
			if found != None:
				return found
			env=env.prev_env
		return None
	
	#returns table only in current scope, not ancestral ones
	def get_current_table(self):
		return self.current_hashtable.get_table()
	
	#is_present in the current scope only
	def is_present_current_block(self, name):
		return self.current_hashtable.is_present(name)
		
	def is_present(self,name):
		env=self
		while env!=None:
			if env.current_hashtable.is_present(name):
				return True
			env = env.prev_env
		return False
		
	def print_table(self):
		env=self
		i=0
		while env!=None:
			print "Ancestor - ",i
			env.current_hashtable.print_table()
			env = env.prev_env
			i=i+1
	
	# ==========================================
	def get_width(self):
		return self.width

	def increment_width(self, inc):		#similar to addwidth() in lecture notes
		self.width += inc

	def get_paramwidth(self):
		return self.paramwidth
		
	def increment_paramwidth(self, inc):
		self.paramwidth += inc
		
	# get_entry(self,name)		#return full attribute list.
	# get_entryheight(self,name)		#how many levles abov it was found

#SymbolTable Class: Just abstraction layer over the Environment Class
class SymbolTable:
	def __init__(self):
		self.current_env = Env(None)		
		
	def add_entry(self, name, list_attributes): 
		self.current_env.add_entry(name, list_attributes)
		
	def update_entry(self, name, attribute_name, attribute_value):
		self.current_env.update_entry(name, attribute_name, attribute_value)
		
	def get_attribute_value(self, name, attribute_name):
		return self.current_env.get_attribute_value(name, attribute_name)
	
	def get_current_table(self):
		return self.current_env.get_current_table()
		
	def is_present(self, name):
		return self.current_env.is_present(name)
	
	def is_present_current_block(self, name):
		return self.current_env.is_present_current_block(name)
	
	def get_current_env(self):
		return self.current_env
	
	#create new environment
	def begin_scope(self):
		self.current_env = Env(self.current_env)
		return self.current_env
	
	#============================================================================
	#'isprocedure' ,'code_inside', 'in_var' , 'out_var', 'env_ptr'
	# format of in_var : [{'lexeme':,'type':}]		.. each variable is a dictionary and in_var is list of such dictionaries
	#after calling begin scope : 	after when procedure starts then add its entry to parent
	def add_beginning_procedure(self,name,in_var=None,out_var=None):
		if self.current_env.prev_env != None:
			prev=self.current_env.prev_env
			#'isprocedure' ,'code_inside', 'in_var' , 'out_var', 'env_ptr'
			prev.add_entry(name, {'isprocedure':True , 'in_var': in_var , 'out_var': out_var})
			ofs = 32
			ind = 0
			if in_var!=None:
				for each in in_var:
					self.current_env.add_entry(each['lexeme'], each)			#values to these variables will be added in function calling
					self.current_env.update_entry(each['lexeme'], 'offset',ofs+(ind*4))
					ind=ind+1
			if out_var!=None:
				for each in out_var:
					self.current_env.add_entry(each['lexeme'], each)			#values to these variables will be added in function calling
					self.current_env.update_entry(each['lexeme'], 'offset',ofs+(ind*4))
					ind=ind+1
			
	
	
	#before ending scope .. store the pointer of symbol_table of exiting procedure as the symbol table entry in parent
	def update_exiting_procedure(self,name):
		if self.current_env.prev_env != None:
			prev=self.current_env.prev_env
			#prev.update_entry(name,'code_inside',code)
			prev.update_entry(name,'env_ptr',self.current_env)
	#=============================================================================
		
	#exit environment.. go to parent
	def end_scope(self):
		self.current_env = self.current_env.prev_env
		
	#prints the current scope and no the complete symbol table
	def print_table(self):
		self.current_env.print_table()	

	# Read and Edit the width (size of all local variables put together) of the symboltable
	def get_width(self):
		return self.current_env.get_width()
		
	def get_paramwidth(self):
		return self.current_env.get_paramwidth()

	def increment_width(self, inc):
		self.current_env.increment_width(inc)

	def increment_paramwidth(self, inc):
		self.current_env.increment_paramwidth(inc)
		
	# used to restore main environment ... see spim code generator
	def set_env(self,env):
		self.current_env = env
		
		
		
		
		