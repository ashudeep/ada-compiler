from collections import *  #for namedtuple
import globalitems
from recordtype import recordtype
#Every time get_newlabel()() is is called, different label has to be returned. Python doesn't support static variables. So, class has been made to store the previous label. Make a instance of this class and call the approriate functions. The instance has to be made just once at the time of start of parser.
	#returns different label each time. Label is of the form ' 'L' followed by interger' eg. L0, L1, L2

# get_newtemp() function
def iterate_tempvar():
		k=0;
		while True:
			k=k+1
			yield k

static_tempvar = iterate_tempvar().next

def get_newtemp(Type, Base, Class):
	new_temp_var = 'temp' + str(static_tempvar())
	
	globalitems.symbol_table.add_entry(new_temp_var, {'type':Type, 'base':Base, 'class':Class})
	globalitems.symbol_table.update_entry(new_temp_var, 'offset', globalitems.symbol_table.get_width())
	globalitems.symbol_table.increment_width(globalitems.widths[Type.lower()])
	globalitems.stack.append(new_temp_var)
	return new_temp_var

	
# emit_code() function : emits code to global store of quadraples
def emit_code(op, arg1, arg2, result):
	Quadruple = recordtype('Quadruple', 'instr_num op arg1 arg2 result')
	globalitems.three_addr_code.code.append(Quadruple(None,'label', str(globalitems.three_addr_code.next_instr), None, None))	
	globalitems.three_addr_code.code.append(Quadruple(globalitems.three_addr_code.next_instr, op, arg1, arg2, result))
	globalitems.three_addr_code.next_instr +=1

# BackPatching - list:list of instruction numbers (i.e. three_addr_code.next_inst)	; i:instruction number(i.e. three_addr_code.next_inst)
def merge(list1, list2):
	return list1 + list2

def back_patch(list, i):
	print 'Backpatching... ',list
	for line in globalitems.three_addr_code.code:
		if line.instr_num in list:
			#print each
			if line.result==None:
				line.result = i

def make_list(i):
	return [i]
	
# Function to print code
def print_three_addr_code():
	fpout=open('Output_3addr.txt','w')
	fpout.write('% Full Three Address Generated Code is here.\n\n')
	for line in globalitems.three_addr_code.code:
		if(line.instr_num!=None):
			out = str(line.instr_num) + " :  " + str(line.op) + " " + str(line.arg1) + " " + str(line.arg2) + " " + str(line.result) + "\n"
		else:
			out = str(line.op) + " " + str(line.arg1) + " :\n"
		fpout.write(out)
	print '\ncode written to : Output_3addr.txt\n'
	fpout.close()