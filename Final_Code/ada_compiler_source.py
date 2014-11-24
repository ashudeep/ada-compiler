#Lexer for ada compiler
import ply.lex as lex
import inspect
from copy import deepcopy
from globalitems import *
from three_addr_generator import *
import sys
global show
show=0		#declared in globalitems

symbol_table.add_entry('Integer',{'type': 'Integer', 'base':'INTEGER', 'class':'INTEGER', 'lexeme':'integer', 'isdatatype':True})
symbol_table.add_entry('Float',{'type': 'Float', 'base':'FLOAT', 'class':'FLOAT', 'lexeme':'float', 'isdatatype':True})
symbol_table.add_entry('Char',{'type': 'Char', 'base':'CHAR', 'class':'CHAR', 'lexeme':'char', 'isdatatype':True})
symbol_table.add_entry('String',{'type': 'String', 'base':'STRING', 'class':'STRING', 'lexeme':'string', 'isdatatype':True})
symbol_table.add_entry('Boolean',{'type': 'Boolean', 'base':'BOOLEAN', 'class':'BOOLEAN', 'lexeme':'boolean', 'isdatatype':True})

reserved = {
        #CHAPTER-31 Manual - Reserved Keywords for ada 2005
        'abort':'ABORT',
        'abs':'ABS',
        'abstract':'ABSTRACT',
        'accept':'ACCEPT',
        'access':'ACCESS',
        'aliased':'ALIASED',
        'all':'ALL',
        'and':'AND',
        'array':'ARRAY',
        'at':'AT',
        'begin':'BEGIN',
        'body':'BODY',
        'case':'CASE',
        'constant':'CONSTANT',
        'declare':'DECLARE',
        'delay':'DELAY',
        'delta':'DELTA',
        'digits':'DIGITS',
        'do':'DO',
        
        'else':'ELSE',
        'elsif':'ELSIF',
        'end':'END',
        'entry':'ENTRY',
        'exception':'EXCEPTION',
        'exit':'EXIT',
        'for':'FOR',
        'function':'FUNCTION',
        'generic':'GENERIC',
        'goto':'GOTO',
        'if':'IF',
        'in':'IN',
        'interface':'INTERFACE',
        'is':'IS',
        'limited':'LIMITED',
        'loop':'LOOP',
        'mod':'MOD',

        'new':'NEW',
        'not':'NOT',
        'null':'NuLL',
        'of':'OF',
        'or':'OR',
        'others':'OTHERS',
        'out':'OUT',
        'overriding':'OVERRIDING',
        'package':'PACKAGE',
        'pragma':'PRAGMA',
        'private':'PRIVATE',
        'procedure':'PROCEDURE',
        'protected':'PROTECTED',
        'raise':'RAISE',
        'range':'RANGE',
        'record':'RECORD',
        'rem':'REM',
        'renames':'RENAMES',
        'requeue':'REQUEUE',

        'return':'RETURN',
        'reverse':'REVERSE',
        'select':'SELECT',
        'separate':'SEPARATE',
        'subtype':'SUBTYPE',
        'synchronized':'SYNCHRONIZED',
        'tagged':'TAGGED',
        'task':'TASK',
        'terminate':'TERMINATE',
        'then':'THEN',
        'type':'TYPE',
        'until':'UNTIL',
        'use':'USE',
        'when':'WHEN',
        'while':'WHILE',
        'with':'WITH',
        'xor':'XOR',

        #Attributes
        '\'Pos':'A_POS',
        '\'Val':'A_VAL',
        '\'Value':'A_VALUE',
        '\'Image':'A_IMAGE',
        '\'First':'A_FIRST',
        '\'Last':'A_LAST',
        '\'Length':'A_LENGTH',
        '\'Range':'A_RANGE'

        }
        
literals = ['&','(',')','*','+',',','-','.','/',':',';','<','=','>','|'] + ['\"','#']              #CHAPTER-32 and 33 OPERATORS , DELIMITERS

tokens = ['ID','NUMLITERAL_INT','NUMLITERAL_FLOAT','NUMLITERAL_BASE_INT','NUMLITERAL_BASE_FLOAT','CHARLITERAL','STRLITERAL','COMMENT','LEQUAL','GEQUAL','ASSIGNMENT','ARROW','DOUBLEDOT','DOUBLESTAR','NOTEQUAL','LEFTLABEL','RIGHTLABEL','BOX','SINGLEQUOTE'] + list(reserved.values())

#Identifier definition (e.g. - variable names)
def t_ID(t):                            #the reserved keywords would also be matched here
        r'[a-zA-Z](_?([a-zA-Z]|[0-9]))*'                #_ is optional
        t.type=reserved.get(t.value,'ID')       #if reserved keyword, change type
        return t

#Floating numbers expressed in different base using "x#y#z" format
# "." character compulsory to represent floating numbers in ada
#optional "e or E" can also be used eith optional " + or - " sign 
def t_NUMLITERAL_BASE_FLOAT(t):
        r'(\d(_?\d)*)\#([0-9A-Fa-f](_?[0-9A-Fa-f])*)\.([0-9A-Fa-f](_?[0-9A-Fa-f])*)\#([eE][-+]?(\d(_?\d)*))?'               # eg: 16#2B#e+2 true, 16#2B#e+C false- write 16#2B#e+12 true.... exponential whole is optional
        t.value=(t.value).replace("_","")
        return t
        

#Decimal numbers expressed in different base using "x#y#z" format
#optional "e or E" can also be used eith optional "+" sign (" - " sign not allowed) 

def t_NUMLITERAL_BASE_INT(t):
        r'(\d(_?\d)*)\#([0-9A-Fa-f](_?[0-9A-Fa-f])*)\#([eE](\+)?(\d(_?\d)*))?'                # eg: 16#2B#e+2 true, 16#2B#e+C false- write 16#2B#e+12 true.... exponential whole is optional
        t.value=(t.value).replace("_","")
        return t

		
#Floating numbers in base 10(similar to based floating numbers) 		
def t_NUMLITERAL_FLOAT(t):              #There are no negative literals; e.g. -1 is not a literal, rather it is the literal 1 preceded by the unary minus operator.
        r'((\d(_?\d)*)\.(\d(_?\d)*))([eE][-+]?(\d(_?\d)*))?'
        t.value=(t.value).replace("_","")
        t.value=float(t.value)
        return t
		
#Decimal numbers in base 10 (similar to based decimal numbers)       
def t_NUMLITERAL_INT(t):                #There are no negative literals; e.g. -1 is not a literal, rather it is the literal 1 preceded by the unary minus operator.
        r'(\d(_?\d)*)([eE](\+)?(\d(_?\d)*))?'           #exponential part is optional.. '?'
        s=t.value
        s=s.replace("_","")
        if s.find('e')==-1 and s.find('E')==-1:
                t.value=int(s)
        else:
                t.value=int(float(s))
        return t


def t_CHARLITERAL(t):                   #match all single character except newline eg 'a'
        r'(\'.?\')'                     #? is to match this as well '' i.e. empty
        return t

def t_STRLITERAL(t):                    #strings eg "asdf"
        r'\"((\"\")|[^"])*\"'   #assuming " is a special character in ply
        return t

def t_COMMENT(t):
        r'(--)(.)*'                     # -- ...Comments... are ignored
        pass
    
def t_newline(t):                       #to count newline, not a token
        r'\n+'
        t.lexer.lineno += len(t.value)

t_LEQUAL = r'<='
t_GEQUAL = r'>='
t_ASSIGNMENT = r':='
t_ARROW = r'=>'
t_DOUBLEDOT = r'\.\.'
t_DOUBLESTAR = r'\*\*'
t_NOTEQUAL = r'/='
t_LEFTLABEL = r'<<'
t_RIGHTLABEL = r'>>'
t_BOX = r'<>'
t_SINGLEQUOTE = r'\''

t_ignore = ' \t'                        #ignore spaces and tabs

# Error handling rule
def t_error(t):
        print("Illegal character '%s' at line:" % t.value[0],t.lineno)
        t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


#######test case###############################################################################################################
# file_name=input("Input File: ");                        #give input in double quotes in python 2.7 and direcly with out quotes in py3.3
# fp=open(file_name,'r')
# data = fp.read()

# Give the lexer some input
# lexer.input(data)

#s_table=SymbolTable()

## Tokenize
##while True:
##        tok = lexer.token()
##        if not tok: break      # No more input
##        print(tok)
##        s_table.insert_id(tok)
##		
##print ("\n\nHere is the final table : \n")
##s_table.print_table()
###############################################################################################################################
#Note: longest sequence match means
##############################################################################################################################
import ply.yacc as yacc
#####################################################################################

#notes:

#variables:
debug1=False	#for showing handled and unhandled production rules numbers
show_ast=False		#for printing AST
debug2=False	#for printing useful information for debugging

#global_file: global_file containing variable symbol_table

# watch_out : yet to be seen or confirmed

# variable_attribute_list
# we will not add all attributes, but only required ones and else will autmatically be returned as NONE. So for is_array either True or NONE
#{'lexeme':i.lower(), 'value':value_of_variable, 'type': element_type, 'ispackage':True ,'isprocedure':True ,'isconstant':True, 'isdatatype':False(for_datatypes_themselves), 'isarray':True, 'arr_low' : list_of_lows_in_all_dims, 'arr_high' : list_of_highs_in_all_dims , 'index_type' : list_of_index_types_in, 'class': class, 'base':base, 'range_low':constraint_low, 'range_high':constraint_high , 'code_inside': code of procedure/package provided isprocedure is true , 'in_var' : input of procedure , 'out_var' : output of procedure , 'env_ptr': ptr to env of procedure}
#procedure entry in symboltable: 'isprocedure' ,'code_inside', 'in_var' , 'out_var', 'env_ptr'
#lexeme,type,base,class,value

#Each p[0],p[2] etc are dictionaries in general so we access their key 'code'...  and in some cases p[1] etc can be list eg: variable declarations def_id_s
#attribute 'code' is list of strings eg: ["t1=2+3","t2=4+3","t1+t2"]
#so (p[0]['code']) is the final code list.

#to be made:
#t1 = p[1]['type']
#t2 = p[3]['type']
#t3 = compatible_type(t1, t2)

# basic types to be enterd: Integer , Float , String , Char , Boolean

#####################################################################################
def p_start_symbol(p) : 
	''' start_symbol :  compilation'''
	print "\n\nStart Symbol parsed\n"
	if (debug1): print "handled: 1"
	p[0]=p[1]		#automatically code is also transferred
	# print "Final code is :\n",p[0]		#,p[0]
	# for i in p[0]['code']:
		# print i
	print "\nFinal Symbol Table is :"
	symbol_table.print_table()

def p_pragma(p): 
	''' pragma : PRAGMA ID ';'
	| PRAGMA simple_name '(' pragma_arg_s ')' ';'
	 '''
	if (debug1): print "unhandled: 2"

def p_pragma_arg_s (p) : 
 ''' pragma_arg_s :   pragma_arg
	| pragma_arg_s ',' pragma_arg
	 '''
 if (debug1): print "unhandled: 3"

def p_pragma_arg (p) : 
 ''' pragma_arg :   expression
	| simple_name ARROW expression
	 '''
 if (debug1): print "unhandled: 4"

def p_pragma_s (p) : 
 ''' pragma_s :  
	| pragma_s pragma
	 '''
 if (debug1): print "unhandled: 5"

def p_decl(p): 
	''' decl : object_decl
	| number_decl
	| type_decl
	| subtype_decl
	| pkg_decl
	| task_decl
	| prot_decl
	| exception_decl
	| rename_decl
	| generic_decl
	| body_stub
	| error ';'
	 '''
	if (show==1): print "\t\t\t\t\t\t\t decl"
	if (debug1): print "handled: 6"
	p[0]=p[1]

def p_decl2(p):
	'''decl : subprog_decl '''
	
	symbol_table.add_entry(p[1]['lexeme'], {'isprocedure':True , 'in_var': p[1]['in_var'] , 'out_var': p[1]['out_var']})
	
#object_qualifier_opt = EMPTY | ALIASED | CONSTANT | ALIASED CONSTANT 
#object_subtype_def = subtype_ind | array_type
#init_opt = empty | := expression
#EXAMPLE: a, b, c : EMPTY Integer := 5 ; 
#object_subtype_def if array_type then returns a dictionary {'low' : list_of_lows_in_all_dims, 'high' : list_of_highs_in_all_dims , 'index_type' : list_of_index_types_in, 'type': element_type, 'isarray':True, 'class': class, 'base':base}
#object_subtype_def if subtype_ind then returns {'type':name, 'isarray':False , 'min':constraint_low, 'max':constraint_high,'class': class, 'base':base} or {'type':name, 'isarray':False, 'class': class, 'base':base}
def p_object_decl (p) : 
	''' object_decl :   def_id_s ':' object_qualifier_opt object_subtype_def init_opt ';'
		 '''
	if ( show==1 ): print "\t\t\t\t\t\t\t object_decl"
	if (debug1): print "handled: 7 - i"
	
	if(p[5]!=None):
		p[0]=deepcopy(p[5])
		#del p[0]['code'][-1]#DOUBT

	for i in p[1]:  #p[1] is list of lexemes of the identifiers
		valid = True
		if symbol_table.is_present_current_block(i):
			valid = False
			print "\n\nDECLARATION ERROR(in object decl) : " + i + " has already been declared.\n\n"
			p_error(p)
		
		else:
			for j in reserved:
				if i == j:
					valid = False
					print "\n\nDECLARATION ERROR(in object decl) : Variable",i," is a reserved keyword.\n\n"
					p_error(p)

		if p[5] != None: 					#if the statement does assignment in addition to declaration
			if p[4]['type'] == None:
				print "p[4].type is None"
				valid=False					# watch_out
				p_error(p)					# watch_out
			if p[4]['type'].lower() != p[5]['type'].lower():
				valid = False
				print "\n\nTYPE MISMATCH(in object decl) : data type :",p[4]['type'], "		expression type :", p[5]['type'] ,"(ARE DIFFERENT)\n\n"
				p_error(p)

		if valid:
			if(p[4]['isarray'] == False):
				if(debug2): print p[4]['class']		# watch_out
				
				# watch_out still left##########
				#symbol_table.add_entry(i.lower(), {'type':p[4]['type'], 'lexeme':i.lower(), 'class': p[4]['class'], 'base':p[4]['base']})
				#if p[5] != None:
				#	symbol_table.update_entry(i, 'value', p[5]['value'])
				#else:
				#	symbol_table.update_entry(i, 'value', None)
				#################################
				
				symbol_table.add_entry(i.lower(), p[4])		#p[4] is a dictionary and it does not have code .. its all evaluated
				symbol_table.update_entry(i.lower(), 'lexeme', i.lower())
				symbol_table.update_entry(i.lower(), 'offset',symbol_table.get_width())
				symbol_table.increment_width(widths[p[4]['class'].lower()])
				
				#symbol_table.update_entry(i, 'value', None)			#it is so b/c p[5] is code
				
				if (p[5]==None):
					p[0]={}
					#p[0]['code']=[]
				else:
					if(symbol_table.get_attribute_value(i.lower(), 'isconstant')==True):
						print "\n\nASSIGNMENT ERROR(in object decl) : constant identifiers cannot be reassigned\n\n"
					else:
						#print "Yet to be handled"
						emit_code('=',p[5]['place'],None,i)
						#p[0]['code'] = p[0]['code'] + [ i.lower() + p[5]['code'][-1] ]#doubt
						#CORRECTION(is type ke assignments bhi handle karna hai)
			
			else:
				symbol_table.add_entry(i.lower(), p[4])		#p[4] is a dictionary and it does not have code .. its all evaluated
				symbol_table.update_entry(i.lower(), 'lexeme', i.lower())			#every other thing done at array level
				
				#symbol_table.update_entry(i, 'value', None)			#it is so b/c p[5] is code
				if (p[5]==None):
					p[0]={}
					#p[0]['code']=[]
				else:
					print "\n\nERROR: initialisation of array while declaration is not supported!\n\n"
				

		if(debug2): print "Declaration of " + str(p[1]) + " done."
 
def p_def_id_s (p) : 		#list of strings
	''' def_id_s :   def_id
	| def_id_s ',' def_id
	 '''
	if ( show==1 ): print "\t\t\t\t\t\t\t\t  def_id_s"
	if (debug1): print "handled: 7 - ii"
	if (len(p)==2):
		p[0]=[p[1]]					#here since p's are structures(i.e. dictionary) so here address is passed not value
	else:
		p[0]=p[1]+[p[3]]
	
def p_def_id(p): 
 ''' def_id : ID ''' 
 if ( show==1 ): print "\t\t\t\t\t\t\t\t   def_id"
 if (debug1): print "handled: 8"
 p[0]=p[1]
 
 
def p_object_qualifier_opt (p) : 
 ''' object_qualifier_opt :  
	| ALIASED
	| CONSTANT
	| ALIASED CONSTANT
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t\t   object_qualifier_opt"
 if (debug1): print "unhandled: 9"

def p_object_subtype_def (p) : 
 ''' object_subtype_def :   subtype_ind
	| array_type
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t\t\t   object_subtype_def"
 if (debug1): print "handled: 10"
 p[0]=p[1]
 
def p_init_opt (p) : 
	''' init_opt :  
		| ASSIGNMENT expression
		 '''
	if ( show==1 ): print "\t\t\t\t\t\t\t\t init_opt"
	if (debug1): print "handled: 11"
	if (len(p)==1):
		p[0]=None
	else:
		p[0]=p[2]					#address same.. dictionary (like structure)
		#(p[0]['code'])[-1] = " = " + (p[0]['code'])[-1]
		#CORRECTION
	
 
def p_number_decl (p) : 
	''' number_decl :   def_id_s ':' CONSTANT ASSIGNMENT expression ';'
	 '''
	if ( show==1 ): print "\t\t\t\t\t\t\t\t number_decl"
	if (debug1): print "handled: 12"

	p[0]=deepcopy(p[5])
	#del p[0]['code'][-1]
	#p[0]['nextlist']=make_list(None)
	for i in p[1]:
		valid = True
		if symbol_table.is_present_current_block(i):
			valid = False
			print i + " has already been declared."
			p_error(p)
		#ERROR HANDLING
		else:
			for j in reserved:
				if i == j:
					valid = False
					print "Variable %s is a reserved keyword." % i
					p_error(p)
	
		if valid:
			symbol_table.add_entry(i.lower(),{'lexeme':i.lower() , 'type':p[5]['type'] , 'base':p[5]['base'] , 'class':p[5]['class'] ,'isconstant':True})		#p[4] is a dictionary and it does not have code .. its all evaluated
			symbol_table.update_entry(i, 'value', None)			#it is so b/c p[5] is code
			emit_code('=',p[5]['place'],None,i)
			#p[0]['code'] = p[0]['code'] + [ i.lower() + " = " + p[5]['code'][-1] ]
			#CORRECTION
 
def p_type_decl (p) : 
	''' type_decl :   TYPE ID discrim_part_opt type_completion ';' '''
	
	if ( show==1 ): print "\t\t\t\t\t\t\t\t type_decl"
	if (debug1): print "handled: 13"
	
	# watch_out doubtful
	flag = True
	if symbol_table.is_present_current_block(p[2]):
		flag = False
		print "\n\nERROR :%s:%s: Redeclaration of %s\n\n" % (p.lineno(0), p.lexpos(0), p[2])
		p_error(p)
	
	if not symbol_table.is_present(p[4]['type'].lower()):
		flag = False
		print "\n\nERROR :%s:%s: %s is an undefined type\n\n" % (p.lineno(0), p.lexpos(0), p[4]['type'])
		p_error(p)
	
	elif flag:
		symbol_table.add_entry(p[2].lower(), {'isdatatype':True, 'lexeme':p[2].lower(), 'type':p[2].lower(), 'base':p[4]['base'], 'class':p[4]['class']})		#type is also added in symbol_table
		p[0]={'isdatatype':True, 'lexeme':p[2], 'type':p[2].lower(), 'base':p[4]['base'], 'class':p[4]['class']}
		if (debug2): print "Added subtype " + p[2] + " in the symbol table "
		if p[4]['isarray'] == True:
			symbol_table.update_entry(p[2].lower(), 'arr_low', p[4]['arr_low'])
			symbol_table.update_entry(p[2].lower(), 'arr_high', p[4]['arr_high'])
			p[0]['arr_high']=p[4]['arr_high']
			p[0]['arr_low']=p[4]['arr_low']
		elif 'range_low' in p[4]:
			symbol_table.update_entry(p[2].lower(), 'range_low', p[4]['range_low'])
			symbol_table.update_entry(p[2].lower(), 'range_high', p[4]['range_high'])
			p[0]['range_high']=p[4]['range_high']
			p[0]['range_low']=p[4]['range_low']
 
 
def p_discrim_part_opt (p) : 
 ''' discrim_part_opt :  
	| discrim_part
	| '(' BOX ')'
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t\t\t     discrim_part_opt"
 if (debug1): print "unhandled: 14"
 
def p_type_completion (p) : 
	''' type_completion :  
		| IS type_def
		 '''
	if ( show==1 ): print "\t\t\t\t\t\t\t\t\t    type_completion"
	if (debug1): print "handled: 15"
	if (len(p)==1): 
		p[0]={}
		p[0]['base']=None
		p[0]['class']=None
	else:
		p[0]=p[2]

def p_type_def (p) :  #handled are int , array , record
 ''' type_def :   enumeration_type 
	| integer_type
	| real_type
	| array_type
	| record_type
	| access_type
	| derived_type
	| private_type
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t\t\t\t        type_def"
 if (debug1): print "handled: 16"
 p[0]=p[1]

def p_subtype_decl (p) :			# implemented exactly same as type 
	''' subtype_decl :   SUBTYPE ID IS subtype_ind ';' '''
	if ( show==1 ): print "\t\t\t\t\t\t\t\t    subtype_decl"
	if (debug1): print "handled: 17"
	
	# watch_out doubtful
	flag = True
	if symbol_table.is_present_current_block(p[2]):
		flag = False
		print "\n\nERROR :%s:%s: Redeclaration of %s\n\n" % (p.lineno(0), p.lexpos(0), p[2])
		p_error(p)
	
	if not symbol_table.is_present(p[4]['type'].lower()):
		flag = False
		print "\n\nERROR :%s:%s: %s is an undefined type\n\n" % (p.lineno(0), p.lexpos(0), p[4]['type'])
		p_error(p)
	
	elif flag:
		symbol_table.add_entry(p[2].lower(), {'isdatatype':True, 'lexeme':p[2], 'type':p[2].lower(), 'base':p[4]['base'], 'class':p[4]['class']})
		p[0]={'isdatatype':True, 'lexeme':p[2], 'type':p[2].lower(), 'base':p[4]['base'], 'class':p[4]['class']}
		if (debug2): print "Added subtype " + p[2] + " in the symbol table "
		elif 'range_low' in p[4]:
			symbol_table.update_entry(p[2].lower(), 'range_low', p[4]['range_low'])
			symbol_table.update_entry(p[2].lower(), 'range_high', p[4]['range_high'])
			p[0]['range_high']=p[4]['range_high']
			p[0]['range_low']=p[4]['range_low']

	
 
def p_subtype_ind (p) : 
	''' subtype_ind :   name constraint
						| name '''
	if ( show==1 ): print "\t\t\t\t\t\t\t\t\t    type_completion"
	if (debug1): print "handled: 18"
	
	if not symbol_table.is_present(p[1]['lexeme']):
		print "\n\nTYPE ERROR : unknown type : %s \n\n"%p[1]['lexeme']
		p_error()
	
	if not symbol_table.get_attribute_value(p[1]['lexeme'], 'isdatatype'):
		print "\n\nTYPE ERROR : %s not a datatype \n\n"%p[1]['lexeme']
		p_error()
	
	if (len(p)==3):
		p[0] = {'type':p[1]['type'], 'isarray':False , 'range_low': p[2]['range_low'], 'range_high': p[2]['range_high'], 'class':p[1]['class'], 'base':p[1]['base']}
	else:
		p[0] = {'type':p[1]['type'], 'isarray':False, 'class':p[1]['class'], 'base':p[1]['base']}
	
	 
def p_constraint (p) :
 ''' constraint :   range_constraint
	| decimal_digits_constraint
	 '''
 if (debug1): print "handled: 19"
 p[0]=p[1]

def p_decimal_digits_constraint (p) : 
 ''' decimal_digits_constraint :   DIGITS expression range_constr_opt
	 '''
 if (debug1): print "unhandled: 20"

def p_derived_type (p) : 
 ''' derived_type :   NEW subtype_ind
	| NEW subtype_ind WITH PRIVATE
	| NEW subtype_ind WITH record_def
	| ABSTRACT NEW subtype_ind WITH PRIVATE
	| ABSTRACT NEW subtype_ind WITH record_def
	 '''
 if (debug1): print "unhandled: 21"

def p_range_constraint (p) : 
 ''' range_constraint :   RANGE range
	 '''
 if (debug1): print "handled: 22"
 p[0]=p[2]

def p_range (p) : 
	''' range :   simple_expression DOUBLEDOT simple_expression
	| name SINGLEQUOTE RANGE
	| name SINGLEQUOTE RANGE '(' expression ')'
	 '''
	if (debug1): print "handled: 23"
	if (p[2]=='..'):
		t1 = p[1]['type']
		t2 = p[3]['type']
		if(t1==t2):
			t3=t1
		else :
			print "TYPE MISMATCH : incompatible types used for range declaration"
		#t3 = compatible_type(t1, t2)
		#compatibility check to be implemented
		#if t3 == None:
		#	print "ERROR:%s:%s: Incompatible range types with operator \"..\"" % (p.lineno(0), p.lexpos(0))
		p[0] = dict([('range_low', p[1]['place']),('range_high', p[3]['place']), ('index_type', t3)])
	else:
		print "unhandled: 23"
	

def p_enumeration_type (p) : 
 ''' enumeration_type :   '(' enum_id_s ')' '''
 # watch_out may do it later
 if (debug1): print "unhandled: 24"

def p_enum_id_s (p) : 
 ''' enum_id_s :   enum_id
	| enum_id_s ',' enum_id
	 '''
 if (debug1): print "unhandled: 25"

def p_enum_id (p) : 
 ''' enum_id :   ID
	| CHARLITERAL
	 '''
 if (debug1): print "unhandled: 26"

def p_integer_type (p) : 
	''' integer_type :   range_spec
		| MOD expression
		 '''
	if (debug1): print "handled: 27"
	if (len(p)==3):
		print "unhandled"
	else:
		p[0]=p[1]	

def p_range_spec (p) : 
	''' range_spec :   range_constraint
		 '''
	if (debug1): print "handled: 28"
	p[0]=p[1]

def p_range_spec_opt (p) : 
	''' range_spec_opt :  
		| range_spec
		'''
	if (debug1): print "handled: 29"
	if (len(p)==1):
		p[0]=None
	else:
		p[0]=p[1]

def p_real_type (p) : 
 ''' real_type :   float_type
	| fixed_type
	 '''
 if (debug1): print "unhandled: 30"

def p_float_type (p) : 
 ''' float_type :   DIGITS expression range_spec_opt
	 '''
 if (debug1): print "unhandled: 31"
	 
def p_fixed_type (p) : 
 ''' fixed_type :   DELTA expression range_spec
	| DELTA expression DIGITS expression range_spec_opt
	 '''
 if (debug1): print "unhandled: 32"

def p_array_type (p) : 
 ''' array_type :   unconstr_array_type
	| constr_array_type
	 '''
 if (debug1): print "handled: 33"
 p[0]=p[1]

def p_unconstr_array_type (p) : 
 ''' unconstr_array_type :   ARRAY '(' index_s ')' OF component_subtype_def
	 '''
 if (debug1): print "unhandled: 34" 

def p_constr_array_type (p) : 
	''' constr_array_type :   ARRAY iter_index_constraint OF component_subtype_def '''
	if (debug1): print "handled: 35" 
	low = []			#list for multidimensional array
	high = []
	index_type = []
	numval = 1
	
	for elem in p[2]:
		low.append(elem['range_low'])
		high.append(elem['range_high'])
		numval = numval*(elem['range_high']-elem['range_low']+1)
		index_type.append(elem['index_type'])
	p[0] = {'isarray':True, 'offset':symbol_table.get_width(), 'array_low':low, 'array_high':high, 'index_type':index_type, 'type':p[4]['type'], 'base':p[4]['base'], 'class':p[4]['class']}# to add constraints from component_subtype_def
	symbol_table.increment_width(numval * widths[p[4]['class'].lower()])
	print "numval",numval

def p_component_subtype_def (p) : 
 ''' component_subtype_def :   aliased_opt subtype_ind
	 '''
 if (debug1): print "handled: 36" 
 p[0]=p[2]

def p_aliased_opt (p) : 
 ''' aliased_opt :   
	| ALIASED
	 '''
 if (debug1): print "unhandled: 37" 

def p_index_s (p) : 
 ''' index_s :   index
	| index_s ',' index
	 '''
 if (debug1): print "unhandled: 38"

def p_index (p) : 
 ''' index :   name RANGE BOX
	 '''
 if (debug1): print "unhandled: 39"

def p_iter_index_constraint (p) : 
	''' iter_index_constraint :   '(' iter_discrete_range_s ')'
	 '''
	if (debug1): print "handled: 40"
	p[0]=p[2]

def p_iter_discrete_range_s (p) : 
 ''' iter_discrete_range_s :   discrete_range
	| iter_discrete_range_s ',' discrete_range
	 '''
 if (debug1): print "handled: 41"
 if (len(p)==2):
	 p[0]=[p[1]]
 else:
	 p[0]=p[1]+[p[3]]
 

def p_discrete_range (p) : 
	''' discrete_range :   name range_constr_opt
	| range
	 '''
	if (debug1): print "handled: 41"
	if (len(p)==3):
		# watch_out may do later
		print "unhandled"
	else:
		p[0]=p[1]

def p_range_constr_opt (p) : 
 ''' range_constr_opt :  
	| range_constraint
	 '''
 if (debug1): print "unhandled: 42"
 # watch_out may do later

############################################ left #####################################################
 
def p_record_type (p) : 
 ''' record_type :   tagged_opt limited_opt record_def
	 '''
 # watch_out left to do
 if (debug1): print " to be handled: 43"

def p_record_def (p) : 
 ''' record_def :   RECORD pragma_s comp_list END RECORD
	| NuLL RECORD
	 '''
 if (debug1): print " to be handled: 44"

def p_tagged_opt (p) : 
 ''' tagged_opt :  
	| TAGGED
	| ABSTRACT TAGGED
	 '''
 if (debug1): print " to be handled: 45"

def p_comp_list (p) : 
 ''' comp_list :   comp_decl_s variant_part_opt
	| variant_part pragma_s
	| NuLL ';' pragma_s
	 '''
 if (debug1): print " to be handled: 46"

def p_comp_decl_s (p) : 
 ''' comp_decl_s :   comp_decl
	| comp_decl_s pragma_s comp_decl
	 '''
 if (debug1): print " to be handled: 47"

def p_variant_part_opt (p) : 
 ''' variant_part_opt :   pragma_s
	| pragma_s variant_part pragma_s
	 '''
 if (debug1): print " to be handled: 48"

def p_comp_decl (p) : 
 ''' comp_decl :   def_id_s ':' component_subtype_def init_opt ';'
	| error ';'
	 '''
 if (debug1): print " to be handled: 49"

def p_discrim_part (p) : 
 ''' discrim_part :   '(' discrim_spec_s ')'
	 '''
 if (debug1): print " to be handled: 50"

def p_discrim_spec_s (p) : 
 ''' discrim_spec_s :   discrim_spec
	| discrim_spec_s ';' discrim_spec
	 '''
 if (debug1): print " to be handled: 51"

def p_discrim_spec (p) : 		# mark is yet to be defined
 ''' discrim_spec :   def_id_s ':' access_opt mark init_opt
	| error
	 '''
 if (debug1): print " to be handled: 52"

def p_access_opt (p) : 
 ''' access_opt :  
	| ACCESS
	 '''
 if (debug1): print " to be handled: 53"

def p_variant_part (p) : 
 ''' variant_part :   CASE simple_name IS pragma_s variant_s END CASE ';'
	 '''
 if (debug1): print " to be handled: 54"

def p_variant_s (p) : 
 ''' variant_s :   variant
	| variant_s variant
	 '''
 if (debug1): print " to be handled: 55"

def p_variant (p) : 
 ''' variant :   WHEN choice_s ARROW pragma_s comp_list
	 '''
 if (debug1): print " to be handled: 56"

def p_choice_s (p) : 
 ''' choice_s :   choice
	| choice_s '|' choice
	 '''
 if (debug1): print " to be handled: 57"

def p_choice (p) : 
 ''' choice :   expression
	| discrete_with_range
	| OTHERS
	 '''
 if (debug1): print " to be handled: 58"

def p_discrete_with_range (p) : 
 ''' discrete_with_range :   name range_constraint
	| range
	 '''
 if (debug1): print " to be handled: 59"

#################################################################################################
 
def p_access_type (p) : 
 ''' access_type :   ACCESS subtype_ind
	| ACCESS CONSTANT subtype_ind
	| ACCESS ALL subtype_ind
	| ACCESS prot_opt PROCEDURE formal_part_opt
	| ACCESS prot_opt FUNCTION formal_part_opt RETURN mark
	 '''
 if (debug1): print "unhandled: 60"

def p_prot_opt (p) : 
 ''' prot_opt :  
	| PROTECTED
	 '''
 if (debug1): print "unhandled: 61"

def p_decl_part (p) : 
 ''' decl_part :  
	| decl_item_or_body_s1
	 '''
 if (debug1): print "handled: 62"
 if (len(p)==1): p[0]=None
 else: p[0]=p[1]

def p_decl_item_s (p) : 
 ''' decl_item_s :   
	| decl_item_s1
	 '''
 if ( show==1 ): print "\t\t\t\t\t decl_item_s"
 if (debug1): print "handled: 63"
 if (len(p)==1): p[0]=None
 else: p[0]=p[1]
 
def p_decl_item_s1 (p): 
	''' decl_item_s1 : decl_item
		| decl_item_s1 decl_item
		'''
	if ( show==1 ): print "\t\t\t\t\t\t decl_item_s1"
	if (debug1): print "handled: 64"
	if (len(p)==2): p[0]=[p[1]]
	else: p[0]=p[1]+[p[2]]
	

def p_decl_item (p) : 
 ''' decl_item :   decl
	| use_clause
	| rep_spec
	| pragma
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t\t decl_item"
 if (debug1): print "handled: 65"
 p[0]=p[1]

def p_decl_item_or_body_s1(p) : 
	''' decl_item_or_body_s1 : decl_item_or_body
		| decl_item_or_body_s1 decl_item_or_body '''
	if ( show==1 ): print "\t\t\t\t\t\t\t decl_item_or_body_s1"
	if (debug1): print "handled: 66"
	if(len(p)==2):p[0]=[p[1]]
	else: 
		p[0]=p[1]+[p[2]]
	

def p_decl_item_or_body (p) : 
 ''' decl_item_or_body :   body
	| decl_item
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t\t decl_item_or_body"
 if (debug1): print "handled: 67"
 p[0]=p[1]

def p_body (p) : 
 ''' body :   subprog_body
	| pkg_body
	| task_body
	| prot_body
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t\t body"
 if (debug1): print "handled: 68"
 p[0]=p[1]

def p_name (p) : 
 ''' name :   simple_name
	| indexed_comp
	| selected_comp
	| attribute
	| operator_symbol
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t name"
 if (debug1): print "handled: 69"
 p[0]=p[1]
 #print "name "
 #print p[1]
 

def p_mark (p) : 
 ''' mark :   simple_name
	| mark SINGLEQUOTE attribute_id
	| mark '.' simple_name
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t mark"
 if (debug1): print "handled: 70"
 p[0]=p[1]		
 # watch_out left
 
def p_simple_name (p) : 
 ''' simple_name :   ID
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t simple_name"
 if (debug1): print "handled: 71"
 #doubt -- NOT THE RIGHT PLACE TO CHECK WHETHER THE NAME HAS ALREADY BEEN DECLARED
 if symbol_table.is_present(p[1].lower()):
	if(debug2): print "Found " + p[1].lower() + " in the symboltable."
	p[0] = {'type': symbol_table.get_attribute_value(p[1].lower(), 'type'), 'isdatatype':symbol_table.get_attribute_value(p[1].lower(), 'isdatatype'), 'lexeme': p[1], 'class':symbol_table.get_attribute_value(p[1].lower(), 'class'), 'base':symbol_table.get_attribute_value(p[1].lower(), 'base'),'isconstant':symbol_table.get_attribute_value(p[1].lower(), 'isconstant'),'place':p[1] ,'truelist':[],'falselist':[]}
 else:				# watch_out whether to give error or no.. completely unsure
	 #print "this ID is not declared",p[1]
	 #p_error(p)
	 p[0] = {'lexeme':p[1], 'value':p[1], 'type':p[1],'place':p[1]}
 #print "simple_name"
 #print p[1]
		
def p_compound_name (p) : 
 ''' compound_name :   simple_name
	| compound_name '.' simple_name
	 '''
 if ( show==1 ): print "\t\t\t\t\t compound_name"
 if (debug1): print "handled: 72"
 if (len(p)==2): p[0]=p[1]
 else: 
	p[0]=deepcopy(p[3])
	p[0]['lexeme']=p[1]['lexeme'] + '.' + p[3]['lexeme']

def p_c_name_list (p) : 
 ''' c_name_list :   compound_name
	 | c_name_list ',' compound_name
	 '''
 if ( show==1 ): print "\t\t\t\t\t c_name_list"
 if (debug1): print "handled: 73"
 if (len(p)==2): p[0]=[p[1]]
 else: p[0]=p[1] + [p[3]]


def p_used_char (p) : 
 ''' used_char :   CHARLITERAL
	 '''
 if ( show==1 ): print "\t\t\t\t\t used_char"
 if (debug1): print "handled: 74"
 p[0]={}
 #p[0]['code']=p[1]
 p[0]['value']=p[1]
 p[0]['place']=p[1]
 p[0]['lexeme']=p[1]
 p[0]['type']='Char'

def p_operator_symbol (p) : 
 ''' operator_symbol :   STRLITERAL
	 '''
 if ( show==1 ): print "\t\t\t\t\t operator_symbol"
 if (debug1): print "handled: 75"
 # watch_out see later .. I think only value is required
 p[0]= {'value':p[1] , 'type': 'String','place':p[1],'lexeme':p[1]}
 #p[0] = dict([('value', p[1]), ('type', '_string')])
 #p[0]['base'] = 'string'
 #p[0]['class'] = 'string'
 
def p_indexed_comp (p) : 
	''' indexed_comp :   name '(' value_s ')'
	 '''
	if (debug1): print "handled: 76"
	
	p[0]=deepcopy(p[1])
	if(symbol_table.get_attribute_value(p[1]['lexeme'].lower(), 'isarray')):
		low= symbol_table.get_attribute_value(p[1]['lexeme'].lower(), 'array_low')
		high=symbol_table.get_attribute_value(p[1]['lexeme'].lower(), 'array_high')
		
		#p[0]['place']=p[1]['place']+"("+str(p[3][0]['place'])+")"
		if(len(low)==len(p[3])):
		
			# if(low[0] <=p[3][0]['place'] and p[3][0]['place']<=high[0]):
				# p[0]['place']=p[1]['place']+"("+str(p[3][0]['place'])
			# else:
				# print "\n\nARRAY ERROR : array index "+"0"+" out of bounds\n\n"
				# p_error(p)
			

			# for num in range(1, len(p[3])):
				# if(low[num] <=p[3][num]['place'] and p[3][num]['place']<=high[num]):
					# p[0]['place']=p[0]['place']+","+str(p[3][num]['place'])
				# else:
					# print "\n\nARRAY ERROR : array index "+ str(num) +" out of bounds\n\n"
					# p_error(p)
					
		
			p[0]['place']=p[1]['place']+"("+str(p[3][0]['place'])
			for num in range(1, len(p[3])):
				p[0]['place']=p[0]['place']+","+str(p[3][num]['place'])
				
		else:
			print "\n\nARRAY ERROR : array  dimensions don't match\n\n"
			p_error(p)
			
			
		p[0]['place']+=")"
		
	elif (symbol_table.get_attribute_value(p[1]['lexeme'].lower(), 'isprocedure')):
		low= symbol_table.get_attribute_value(p[1]['lexeme'].lower(), 'in_var')
		high=symbol_table.get_attribute_value(p[1]['lexeme'].lower(), 'out_var')
		if(len(low)+len(high)!=len(p[3])):
			print "\n\nARGUMENT ERROR : NUMBER OF ARGUMENTS DON'T MATCH for", p[1]['lexeme']
			print "\n"
			p_error(p)
		
		#printing in reverse
		i=len(p[3])-1
		out_count = len(symbol_table.get_attribute_value(p[1]['lexeme'].lower(), 'out_var'))
		while i>=0:
			if out_count > 0:
				emit_code('param',(p[3][i])['place'],'out',None);
				out_count = out_count -1
			else:
				emit_code('param',(p[3][i])['place'],None,None);
			i=i-1
		# for i in range(p[3]):
			# emit_code('param',i['lexeme'],None,None);
			
		emit_code('call',p[1]['lexeme'],len(p[3]),None);
		
		# for i in (symbol_table.get_attribute_value(p[1]['lexeme'].lower(), 'out_var')):
			# emit_code('return',i['lexeme'],None,None);	
	elif (p[1]['lexeme']=='Print'):
		for i in p[3]:
			emit_code('syscall','print_int',i['place'],None)
	elif (p[1]['lexeme']=='Print_String'):
		for i in p[3]:
			emit_code('syscall','print_string',i['place'],None)
	elif (p[1]['lexeme']=='Print_Float'):
		for i in p[3]:
			emit_code('syscall','print_float',i['place'],None)	
	elif (p[1]['lexeme']=='Print_Char'):
		for i in p[3]:
			emit_code('syscall','print_char',i['place'],None)	
	elif (p[1]['lexeme']=='Print_Newline'):
		for i in range(0,p[3][0]['place']):
			emit_code('syscall','print_newline',None,None)	
	else :
		print "\n\nunhandled 'indexed_comp :'"
		print p[1],p[3]
		print "\n\n"

def p_value_s (p) : 
	''' value_s :   value
		| value_s ',' value '''
	if (debug1): print "handled: 77"
	if (len(p)==2): p[0]=[p[1]]
	else: p[0]=p[1] + [p[3]]

def p_value (p) : 
	''' value :   expression
	| comp_assoc
	| discrete_with_range
	| error
	 '''
	if (debug1): print "handled: 78"
	p[0]=p[1]

def p_selected_comp (p) : 
	''' selected_comp :   name '.' simple_name
		| name '.' used_char
		| name '.' operator_symbol
		| name '.' ALL
		 '''
	if (debug1): print "unhandled: 79"

def p_attribute (p) : 
 ''' attribute :   name SINGLEQUOTE attribute_id
	 '''
 if (debug1): print "unhandled: 80"

def p_attribute_id (p) : 
 ''' attribute_id :   ID
	| DIGITS
	| DELTA
	| ACCESS
	 '''
 if (debug1): print "unhandled: 81"
#doubt 
def p_numeric_lit_numbi(p):
 ''' numeric_lit : NUMLITERAL_BASE_INT '''
 if ( show==1 ): print "\t\t\t\t\t\t\t\t numeric_literal"
 if (debug1): print "handled: 82"
 #print "base int"
 p[0]= {'value':p[1] , 'type': 'Integer','place' : p[1],'base':'Integer','class':'Integer'}				# we store value as well b/c it is used in case of range_constarint, while at all other places code is used
 
def p_numeric_lit_numbf(p):
 ''' numeric_lit : NUMLITERAL_BASE_FLOAT '''
 if ( show==1 ): print "\t\t\t\t\t\t\t\t numeric_literal"
 if (debug1): print "handled: 83"
 p[0]= {'value':p[1], 'type': 'Float','place' : p[1],'base':'Float','class':'Float'}

def p_numeric_lit_numi(p):
 ''' numeric_lit : NUMLITERAL_INT '''
 if ( show==1 ): print "\t\t\t\t\t\t\t\t numeric_literal"
 if (debug1): print "handled: 84"
 p[0]= { 'value':p[1] ,'type': 'Integer','place' : p[1],'base':'Integer','class':'Integer'}
 
def p_numeric_lit_numf(p):
 ''' numeric_lit : NUMLITERAL_FLOAT '''
 if ( show==1 ): print "\t\t\t\t\t\t\t\t numeric_literal"
 if (debug1): print "handled: 85"
 p[0]= {'value':p[1] , 'type': 'Float','place' : p[1],'base':'Float','class':'Float'}

 
 
def p_literal (p) : 
 ''' literal :   numeric_lit
	| used_char
	| NuLL
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t\t literal"
 if (debug1): print "handled: 86"
 p[0]=p[1]
 
def p_aggregate (p) : 
 ''' aggregate :   '(' comp_assoc ')'
	| '(' value_s_2 ')'
	| '(' expression WITH value_s ')'
	| '(' expression WITH NuLL RECORD ')'
	| '(' NuLL RECORD ')'
	 '''
 if (debug1): print "unhandled: 87"

def p_value_s_2(p) : 
	''' value_s_2 : value ',' value
	| value_s_2 ',' value
	 '''
	if (debug1): print "unhandled: 88"

def p_comp_assoc (p) : 
 ''' comp_assoc :   choice_s ARROW expression
	 '''
 if (debug1): print "unhandled: 89"

def p_expression1 (p) : 
 ''' expression :   relation
	| expression logical m relation '''
 if ( show==1 ): print "\t\t\t\t expression"
 if (debug1): print "handled: 90"
 if (len(p)==2):
	p[0]=p[1]
 else:
	 print p[1]
	 print p[4]
	 if p[1]['type'] != 'Boolean':
		 print 'TYPE MISMATCH: %s is not boolean' % p[1]['type']
		 p_error(p)
	
	 elif p[4]['type'] != 'Boolean':
		 print 'TYPE MISMATCH: %s is not boolean' % p[3]['type']
		 p_error(p)
	
	 else:
		 p[0]= deepcopy(p[1])
		 temp = deepcopy(p[4])
		 
		 print p[2]
		 if p[2]== 'and' :
			back_patch(p[1]['truelist'],p[3]['instr'])
			p[0]['falselist']=merge(p[1]['falselist'],p[4]['falselist'])
			p[0]['truelist']=p[4]['truelist']
			t1= get_newtemp(p[1]['type'],p[1]['class'],p[1]['base'])
			emit_code('and',p[1]['place'],p[4]['place'],t1)
			#new change p[0]['place']=t1
			
		 elif p[2]== 'or' :
			back_patch(p[1]['falselist'],p[3]['instr'])
			p[0]['truelist']=merge(p[1]['truelist'],p[4]['truelist'])
			p[0]['falselist']=p[4]['falselist']
			t1= get_newtemp(p[1]['type'],p[1]['class'],p[1]['base'])
			emit_code('or',p[1]['place'],p[4]['place'],t1)
			#new change p[0]['place']=t1
		 else :
			print "unhandled XOR"
		 # t1=get_newtemp()
		 # t2=get_newtemp()
		 # x = [ t1 + "=" + p[1]['code'][-1] ]
		 # y = [ t2 + "=" + p[3]['code'][-1] ]
		 
		 # del p[0]['code'][-1]
		 # p[0]['code'] = p[0]['code'] + x
		 
		 # del temp['code'][-1]
		 # p[0]['code'] = p[0]['code'] + temp['code'] + y
		 # z = [ t1 + p[2] + t2]
		 # p[0]['code'] = p[0]['code'] + z
		#CORRECTION
		
def p_expression2 (p) : 
	''' expression :  expression short_circuit m relation '''
	if ( show==1 ): print "\t\t\t\t expression"
	if (debug1): print "handled: 91"
	if p[1]['type'] != 'Boolean':
		 print 'TYPE MISMATCH : %s is not boolean' % p[1]['type']
		 p_error(p)
	
	elif p[3]['type'] != '':
		 print 'TYPE MISMATCH : %s is not boolean' % p[3]['type']
		 p_error(p)
	
	else:
		 p[0]= deepcopy(p[1])
		 temp = deepcopy(p[4])
		 
		 if p[2]== 'AND THEN' :
			back_patch(p[1]['truelist'],p[3]['instr'])
			p[0]['falselist']=merge(p[1]['falselist'],p[4]['falselist'])
			p[0]['truelist']=p[4]['truelist']
			
		 elif p[2]== 'OR ELSE' :
			back_patch(p[1]['falselist'],p[3]['instr'])
			p[0]['truelist']=merge(p[1]['truelist'],p[4]['truelist'])
			p[0]['falselist']=p[4]['falselist']
		 else :
			print "\n\nERROR: unknown short circuit operator\n\n"
		# t1=get_newtemp()
		# t2=get_newtemp()
		# x = [ t1 + "=" + p[1]['code'][-1] ]
		# y = [ t2 + "=" + p[3]['code'][-1] ]
		
		# del p[0]['code'][-1]
		# p[0]['code'] = p[0]['code'] + x
		
		# del temp['code'][-1]
		# p[0]['code'] = p[0]['code'] + temp['code'] + y
		# z = [ t1 + p[2] + t2]
		# p[0]['code'] = p[0]['code'] + z
		#CORRECTION

def p_logical (p) : 
 ''' logical :   AND
	| OR
	| XOR
	 '''
 if ( show==1 ): print "\t\t\t\t\t boolean"
 if (debug1): print "handled: 92"
 p[0]=p[1]
 
def p_short_circuit (p) : 
 ''' short_circuit :   AND THEN
	| OR ELSE
	 '''
 if ( show==1 ): print "\t\t\t\t\t short_circuit"
 if (debug1): print "handled: 92"
 p[0]=p[1] + " " + p[2]
 
def p_relation1 (p) : 
	''' relation :   simple_expression
		| simple_expression relational simple_expression
		 '''
	if ( show==1 ): print "\t\t\t\t\t relation"
	if (debug1): print "handled: 93"
	if (len(p)==2):
		p[0]=p[1]
	else:
	 
		if p[1]['type'] != p[3]['type']:
			print "TYPE MISMATCH : data types of relational expression different 	(%s)  and (%s) " % (p[1]['type'],p[3]['type'])
			p_error(p)
	 
		p[0]= deepcopy(p[1])
		temp = deepcopy(p[1])
		p[0]['type']='Boolean'
		
		p[0]['truelist']=make_list(three_addr_code.next_instr)
		p[0]['falselist']=make_list(three_addr_code.next_instr+1)
		
		emit_code(p[2],p[1]['place'],p[3]['place'],None)#if p[1]['place'] relop p[3]['place'] goto ...
														# bleq = <=
														# ble <
		emit_code('goto',None,None,None)# goto ...
		# t1=get_newtemp()
		# t2=get_newtemp()
		# x = [ t1 + "=" + p[1]['code'][-1] ]
		# y = [ t2 + "=" + p[3]['code'][-1] ]
		
		# del p[0]['code'][-1]
		# p[0]['code'] = p[0]['code'] + x
		
		# del temp['code'][-1]
		# p[0]['code'] = p[0]['code'] + temp['code'] + y
		# z = [ t1 + p[2] + t2]
		# p[0]['code'] = p[0]['code'] + z
		
		#CORRECTION
		
def p_relation2 (p) : 
	''' relation : simple_expression membership range '''
	# watch_out may do it later
	if (debug1): print "unhandled: 94"
	
def p_relation3 (p) : 
	''' relation : simple_expression membership name '''
	# watch_out may do it later
	if (debug1): print "unhandled: 95"

def p_relational (p) : 
 ''' relational :   '='
	| NOTEQUAL
	| '<'
	| LEQUAL
	| '>'
	| GEQUAL
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t relational"
 if (debug1): print "handled: 96"
 if p[1]=='=': p[0]='beq'
 elif p[1]=='/=': p[0]='bneq'
 elif p[1]=='<': p[0]='bless'
 elif p[1]=='<=': p[0]='bleq'
 elif p[1]=='>': p[0]='bgreater'
 else: p[0]='bgeq'
 
 

def p_membership (p) : 
 ''' membership :   IN
	| NOT IN
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t membership"
 if (debug1): print "handled: 97"
 if (len(p)==2): p[0]=p[1]
 else: p[0]=p[1] + " " + p[2]
 
def p_simple_expression (p): 
	''' simple_expression :   unary term
		| term
		| simple_expression adding term
		 '''
	if ( show==1 ): print "\t\t\t\t\t\t simple_expression"
	if (debug1): print "handled: 98"
	if (len(p)==3):
		if p[2]['type'] != 'Integer' and p[2]['type'] != 'Float':
			print "\n\nTYPE ERROR\n\n"
			p_error(p)
	 
		p[0]=p[2]
		temp=get_newtemp(p[2]['type'],p[2]['base'],p[2]['class'])
		
		if(p[1]=='+'):
			emit_code('unary+',p[2]['place'],None,temp)# newtemp = -1/+1 * term
		elif(p[1]=='-'):
			emit_code('unary-',p[2]['place'],None,temp)# newtemp = -1/+1 * term
	
		
		p[0]['place']=temp
		# x= [ p[1] + p[0]['code'][-1] ]
		# del p[0]['code'][-1]
		# p[0]['code'] = p[0]['code'] + x
	elif (len(p)==2):
		p[0]=p[1]
	else:
		#if p[1]['type'] != p[3]['type']:
		#	print "TYPE MISMATCH: data types different for operands (%s) and (%s)"% (p[1]['type'],p[3]['type'])
		#	p_error(p)
		
		if p[1]['type']!='Integer' and p[1]['type']!='Float':
			print "\n\nTYPE ERROR: incorrect datatype for %s ,%s\n\n" %(p[1]['lexeme'],p[1]['type'])
			p_error(p)
			
		if p[3]['type'] != 'Integer' and p[3]['type'] != 'Float':
			print "\n\nTYPE ERROR: incorrect datatype for %s ,%s\n\n" %(p[3]['lexeme'],p[3]['type'])
			p_error(p)
		
		p[0]= deepcopy(p[1])
		
		temp = get_newtemp(p[1]['type'],p[1]['base'],p[1]['class'])
		p[0]['place']=temp
		emit_code(p[2],p[1]['place'],p[3]['place'],temp )# newtemp = p[1]['place'] + p[3]['place']
		# t1=get_newtemp()
		# x = [ t1 + "=" + p[1]['code'][-1] ]
		
		# del p[0]['code'][-1]
		# p[0]['code'] = p[0]['code'] + x
		# t2=get_newtemp()
		# y = [ t2 + "=" + p[3]['code'][-1] ]
		
		# del temp['code'][-1]
		# p[0]['code'] = p[0]['code'] + temp['code'] + y

		# z = [ t1 + p[2] + t2]
		# p[0]['code'] = p[0]['code'] + z
		#CORRECTION

def p_unary(p):
	''' unary : '+'
	| '-'
	 '''
	if ( show==1 ): print "\t\t\t\t\t\t\t\t unary"
	if (debug1): print "handled: 99"
	p[0]=p[1]
	
def p_adding(p): 
	''' adding : '+'
	| '-'
	| '&'
	 '''
	if ( show==1 ): print "\t\t\t\t\t\t\t\t adding"
	if (debug1): print "handled: 100"
	p[0]=p[1]
	
def p_term(p): 
	''' term : factor
	| term multiplying factor
	 '''
	if ( show==1 ): print "\t\t\t\t\t\t\t term"
	if (debug1): print "handled: 101"
	if (len(p)==2):
		p[0]=p[1]
	else:
		if p[1]['type'] != p[3]['type']:
			print "\n\nTYPE MISMATCH : data types different for operands (%s) and (%s) \n\n"% (p[1]['type'],p[3]['type'])
			p_error(p)
		
		if p[1]['type'].lower() != 'integer' and p[1]['type'].lower != 'float':
			print "\n\nTYPE ERROR: multiplication only valid for integer and float %s\n\n" % p[1]['type']
			p_error(p)
		
		p[0]= deepcopy(p[1])
		print p[1]
		temp = get_newtemp(p[1]['type'],p[1]['base'],p[1]['class'])
		p[0]['place']=temp
		emit_code(p[2],p[1]['place'],p[3]['place'],temp)#newtemp = p[1]['place'] * p[3]['place']
		# t1=get_newtemp()
		# t2=get_newtemp()
		# x = [ t1 + "=" + p[1]['code'][-1] ]
		# y = [ t2 + "=" + p[3]['code'][-1] ]
		
		# del p[0]['code'][-1]
		# p[0]['code'] = p[0]['code'] + x
		
		# del temp['code'][-1]
		# p[0]['code'] = p[0]['code'] + temp['code'] + y
		# z = [ t1 + p[2] + t2]
		# p[0]['code'] = p[0]['code'] + z
		#CORRECTION
 
def p_multiplying (p) : 
 ''' multiplying :   '*'
	| '/'
	| MOD
	| REM
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t\t\t multiplying"
 if (debug1): print "handled: 102"
 p[0]=p[1]
 
def p_factor (p) : 
	''' factor :   primary
		| NOT primary
		| primary DOUBLESTAR primary
		 '''
	if (debug1): print "handled: 103"
	if (len(p)==2):
		p[0]=p[1]
		#note this will have: 'code' , 'type' from literals and 'value' as well required in range_low constraints.. so no problem!
	elif (len(p)==3):
		if p[2]['type'] != 'Boolean':
			print "Boolean type required"
			p_error(p)

		p[0]=p[2]
		p[0]['truelist']=p[2]['falselist']
		p[0]['falselist']=p[0]['truelist']
		#p[0]['code'][-1] = p[1] + p[0]['code'][-1] 
	else:
		if p[3]['type'] != 'Integer':
			print "\n\nERROR : 2nd operand for ** must be an integer type %s\n\n" % p[3]['type']
			p_error(p)
		
		elif p[1]['type'] != 'Integer' and p[1]['type'] != 'Float':
			print "\n\nERROR: 1st operand for ** must be an integer or float %s\n\n" % p[1]['type']
			p_error(p)
		else:
			p[0]=deepcopy(p[1])
			temp=get_newtemp()
			p[0]['place']=temp
			emit_code('power',p[1]['place'],p[3]['place'],temp)# new_temp = power(p[1]['place'],p[3]['place'])
			# t1=get_newtemp()
			# x=[ t1 + "=" + "power(" + p[1]['code'] + "," + p[3]['code'] +")" ]		#p[1]['code'] is directly a string ( a literal) .. not list of strings
			#p[0]['code']=x
			#CORRECTION
			
#DOUBT.. what?
def p_factor2 (p) : 
 ''' factor : ABS primary '''
 if (debug1): print "handled: 103"
 if p[2]['type'] != 'Integer' and p[2]['type'] != 'Float':
		print "\n\nERROR: Float or Integer to be used with ABS(Absolute)\n\n"
		p_error(p)

 p[0]=p[2]
 #p[0]['code'][-1] = p[1] + p[0]['code'][-1] 

def p_primary (p) : 
 ''' primary :   literal
	| name
	| allocator
	| qualified
	| parenthesized_primary
	 '''
 if (debug1): print "handled: 104"
 p[0]=p[1]
 
def p_parenthesized_primary (p) : 
 ''' parenthesized_primary :   aggregate
	| '(' expression ')'
	 '''
 # watch_out may handle later
 if (debug1): print "unhandled: 105"

def p_qualified (p) : 
 ''' qualified :   name SINGLEQUOTE parenthesized_primary
	 '''
 # watch_out may handle later
 if (debug1): print "unhandled: 106"

def p_allocator (p) : 
 ''' allocator :   NEW name
	| NEW qualified
	 '''
 # watch_out may handle later
 if (debug1): print "unhandled: 107"
 
###############################PART -2#####################################
def p_statement_s (p) : 
 ''' statement_s :   statement
	| statement_s m statement
	 '''
 if (debug1): print "handled: 108"
 if(len(p)==2): 
	p[0]=deepcopy(p[1])
 else:
	p[0]=deepcopy(p[1])
	back_patch(p[1]['nextlist'],p[2]['instr'])
	print "here",p[3]
	p[0]['nextlist']=p[3]['nextlist']
	#print p[1]
	#print p[2]
	#p[0]['code'] = p[0]['code'] + p[2]['code']

def p_statement (p) : 
 ''' statement :   unlabeled
	| label statement
	 '''
 if (debug1): print "handled: 109"
 if(len(p)==2): 
	p[0]=p[1]
 # watch_out labelling left 
 else: 
	p[0]= p[2]
 #print "statement"
 #print p[1]
 

def p_unlabeled (p) : 
 ''' unlabeled :   simple_stmt
	| compound_stmt
	| pragma
	 '''
 if (debug1): print "handled: 110"
 p[0]=p[1]
 #print "unlabeled"
 #print p[1]
 
def p_simple_stmt (p) : 
 ''' simple_stmt :   null_stmt
	| assign_stmt
	| exit_stmt
	| return_stmt
	| goto_stmt
	| procedure_call
	| delay_stmt
	| abort_stmt
	| raise_stmt
	| code_stmt
	| requeue_stmt
	 '''
 if (debug1): print "handled: 111"
 p[0]=p[1]
 #print "simple_stmt"
 #print p[1]
 
def p_simple_stmt2(p):
 ''' simple_stmt : error ';' 
	'''
 if (debug1): print "handled: 111 - ii"
 p_error(p)
 #print "error"
 #print p[1]
	
def p_compound_stmt (p) : 
 ''' compound_stmt :   if_stmt
	| case_stmt
	| loop_stmt
	| block
	| accept_stmt
	| select_stmt
	 '''
 if (debug1): print "handled: 112"
 p[0]=p[1]

def p_label (p) : 
 ''' label :   LEFTLABEL ID RIGHTLABEL
	 '''
 if (debug1): print " to be handled: 113"
 # watch_out to be done

def p_null_stmt (p) : 
 ''' null_stmt :   NuLL ';'
	 '''
 if (debug1): print "handled: 114"
 p[0]={}
 #p[0]['code']=['null']

def p_assign_stmt (p) : 
	''' assign_stmt :   name ASSIGNMENT expression ';'
	 '''			# watch_out name should only be simple name and error is raised there is not declared.. but is its operator symbol then TO BE HANDLED by raising error NOT DONE
	if ( show==1 ): print "\t\t\t\t\t assign_stmt"
	if (debug1): print "handled: 115"
	#print "assign_stmt err"
	#print p[3]
	#print p[0]
	if not symbol_table.is_present(p[1]['lexeme'].lower()):
		print "\n\nASSIGNMENT ERROR : undeclared variable %s\n\n"%p[1]['lexeme']
		p_error(p)
		
	if p[1]['type'].lower() != p[3]['type'].lower():
		print "\n\nTYPE MISMATCH(IN ASSIGNMENT) : data types for " ,p[1]['lexeme'], ":" ,p[1]['type'], "and expression :" ,p[3]['type'], "(DON'T MATCH)\n\n"
		p_error(p)

	if 'isdatatype' in p[1] and p[1]['isdatatype']:
		print "\n\nASSIGNMENT ERROR : data types cannot be assigned values\n\n"
		p_error(p)
		

	if 'isconstant' in p[1] and p[1]['isconstant']:
		print "\n\nASSIGNMENT ERROR : constant types cannot be assigned values\n\n"
		p_error(p)

	p[0]= deepcopy(p[3])
	p[0]['nextlist']=make_list(None)
	
	if p[3]['type']=='Boolean' :
		x=get_newtemp(p[3]['type'],p[3]['base'],p[3]['class'])
		back_patch(p[3]['truelist'],three_addr_code.next_instr)
		back_patch(p[3]['falselist'],three_addr_code.next_instr+1)
		emit_code('=',1,None,x)
		emit_code('=',0,None,x)
		emit_code('=',x,None,p[1]['place'])
		
		
	else :
		emit_code('=',p[3]['place'],None,p[1]['place'])
	#x = [ p[1]['lexeme'] + "=" + p[3]['code'][-1] ]
	
	# del p[0]['code'][-1]
	# p[0]['code'] = p[0]['code'] + x
	#CORRECTION
	#print "assign_stmt"
	#print p[3]
	#print p[0]
 
def p_if_stmt (p) : 
	''' if_stmt :   IF cond_clause_s else_opt END IF ';'
	 '''
	if ( show==1 ): print "\t\t\t\t\t if_stmt"
	if (debug1): print "handled: 116"
	p[0]=deepcopy(p[2])
	p[0]['nextlist']=merge(p[2]['nextlist'],p[3]['nextlist'])
	back_patch(p[2]['falselist'],p[3]['instr'])
	# t=deepcopy(p[2]['code'])
	# t[0] = "if " + t[0]
	# p[0]['code'] = p[2]['remcode'] + t + p[3]['code'] + ["end if"]
	#CORRECTION

def p_cond_clause_s (p) : 
	''' cond_clause_s :   cond_clause
	| cond_clause ELSIF m cond_clause_s
	 '''
	if ( show==1 ): print "\t\t\t\t\t cond_clauses"
	if (debug1): print "handled: 117"
	if (len(p)==2):
		p[0]=deepcopy(p[1])
	else:
		p[0]=deepcopy(p[1])
		p[0]['nextlist']=merge(p[0]['nextlist'],p[4]['nextlist'])
		back_patch(p[1]['falselist'],p[3]['instr'])
		p[0]['falselist']=p[4]['falselist']								# Crucial Step : for last elseif statement (just before else)
		# t=deepcopy(p[3]['code'])
		# t[0] = "else if " + t[0]
		# p[0]['code'] = p[0]['code'] + t
		# p[0]['remcode'] = p[1]['remcode'] + p[3]['remcode'] 
		#CORRECTION
		
def p_cond_clause (p) : 
 ''' cond_clause :   cond_part m statement_s n
	 '''
 if ( show==1 ): print "\t\t\t\t\t\t cond_clause"
 if (debug1): print "handled: 118"
 p[0]=deepcopy(p[1])
 p[0]['nextlist']=merge(p[3]['nextlist'],p[4]['nextlist'])
 back_patch(p[1]['truelist'],p[2]['instr'])
 #print p[1]
 #print p[2]
 #p[0]['code']=p[0]['code'] + p[2]['code'] 
 #CORRECTION
 
def p_cond_part (p) : 
	''' cond_part :   condition THEN
	 '''
	if (debug1): print "handled: 119"
	p[0]=p[1]
	# t=get_newtemp()
	# x = [ t + "=" + p[0]['code'][-1] ]
	# del p[0]['code'][-1]
	# p[0]['remcode'] = p[0]['code'] + x 
	# p[0]['code'] = [ "(" + t + ") then "]
	#CORRECTION
	
def p_condition (p) : 
	''' condition :   expression
	 '''
	if (debug1): print "handled: 120"
	if p[1]['type'] != 'Boolean':
		print "\n\nTYPE ERROR : condition must be a boolean expression ",(p[1]['type'])
		print "\n"
		p_error(p)
	else:
		p[0]=p[1]

def p_else_opt (p) : 
	''' else_opt :  
	| ELSE m statement_s
	 '''
	if (debug1): print "handled: 121"
	if (len(p)==4):
		p[0]=deepcopy(p[3])
		p[0]['instr']=p[2]['instr']
		print "first"
		#p[0]['code']=["else"] + p[2]['code']
	else:
		p[0]={}
		print "second"
		p[0]['instr']=three_addr_code.next_instr
		p[0]['nextlist']=[]
		#p[0]['code']=[]
		
	#CORRECTION

# watch_out to be handled	.... if is handled so case can be handled lately	

def p_case_stmt (p) : 
	''' case_stmt :   case_hdr pragma_s alternative_s END CASE ';'
	 '''
	if ( show==1 ): print "\t\t\t\t\t case_stmt"
	if (debug1): print "to be handled: 122"

def p_case_hdr (p) : 
 ''' case_hdr :   CASE expression IS
	 '''
 if (debug1): print "to be handled: 123"

def p_alternative_s (p) : 
 ''' alternative_s :  
	| alternative_s alternative
	 '''
 if (debug1): print "to be handled: 124"

def p_alternative (p) : 
 ''' alternative :   WHEN choice_s ARROW statement_s
	 '''
 if (debug1): print "to be handled: 125"
################################
	 
def p_loop_stmt (p) : 
	''' loop_stmt :   label_opt iteration m basic_loop id_opt ';'
	 '''
	if ( show==1 ): print "\t\t\t\t\t loop_stmt"
	if (debug1): print "handled: 126"
	if p[1]!=None and p[5]!=None and p[1]['lexeme']!=p[5]['lexeme']:
		print "\n\nLOOP ERROR : starting : %s and ending : %s (LABELS ARE DIFFERENT)\n\n" %( p[1]['lexeme'] ,p[5]['lexeme'])
	
	if p[1]!=None :
		if symbol_table.is_present_current_block(p[1]['lexeme']):
				print "\n\nDECLARATION ERROR(in loop decl) : " + p[1]['lexeme'] + " has already been declared.\n\n"
				p_error(p)
			
		else:
				for j in reserved:
					if p[1]['lexeme'] == j:
						print "\n\nDECLARATION ERROR(in loop decl) : Variable %s is a reserved keyword.\n\n" % p[1]['lexeme']
						p_error(p)
					
	p[0]=deepcopy(p[4])
	back_patch(p[2]['truelist'],p[3]['instr'])
	back_patch(p[4]['nextlist'],p[2]['instr'])
	p[0]['nextlist']=p[2]['falselist']
	emit_code('goto',None,None,p[2]['instr'])#emit()goto p[2]['instr']
	#p[0]['code'] = p[2]['code'] + p[0]['code']
	
def p_label_opt (p) : 
	''' label_opt :  
		| ID ':'
		'''
	if (debug1): print "unhandled: 127"
	if len(p)==3:
		p[0]={'lexeme':p[1]}
	else :
		p[0]=None

def p_iteration (p) : 
	''' iteration :  
		| WHILE m condition
		| iter_part reverse_opt discrete_range
		 '''
	if (debug1): print "handled: 128"
	if (len(p)==1): p[0]=[]
	elif (p[1]=='while'):
		p[0]=p[3]
		p[0]['instr']=p[2]['instr']
		# t=get_newtemp()
		# x = [ t + "=" + p[0]['code'][-1] ]
		# del p[0]['code'][-1] 
		# p[0]['code'] = p[0]['code'] + x + [ "while (" + t + ") "]
	else:
		#p[0]= deepcopy(p[1])
		p[0]={}
		# print p[1]
		# print p[3]
		
		if(p[2]=='reverse'):
			emit_code('=',p[3]['range_high'],None,p[1])
			emit_code('goto',None,None,three_addr_code.next_instr+2)
			p[0]['instr']=three_addr_code.next_instr
			emit_code('-',p[1],1,p[1])
			p[0]['truelist']=make_list(three_addr_code.next_instr)
			emit_code('bgeq',p[1],p[3]['range_low'],None)
			p[0]['falselist']=make_list(three_addr_code.next_instr)
			emit_code('goto',None,None,None)
		else:
			emit_code('=',p[3]['range_low'],None,p[1])
			#change
			emit_code('goto',None,None,three_addr_code.next_instr+2)
			p[0]['instr']=three_addr_code.next_instr
			emit_code('+',p[1],1,p[1])
			p[0]['truelist']=make_list(three_addr_code.next_instr)
			emit_code('bleq',p[1],p[3]['range_high'],None)
			p[0]['falselist']=make_list(three_addr_code.next_instr)
			emit_code('goto',None,None,None)
		
		
		#p[0]['code'][-1]+= str(p[3]['range_low']) + " to " + str(p[3]['range_high'])
		#CORRECTION
		
def p_iter_part (p) : 
	''' iter_part :   FOR ID IN
	 '''
	if (debug1): print "handled: 129"
	if symbol_table.is_present(p[2].lower()):
		if(debug2): print "Found " + p[2].lower() + " in the symboltable."
		#p[0]={}
		p[0]=p[2]
		#p[0]['code'] = ["for " + p[2] + " in "]
	else:
		print "\n\nDECLARATION ERROR(IN LOOP) : undeclared variable = %s\n\n"%p[2]
		p_error(p)
		
	#CORRECTION

def p_reverse_opt (p) : 
	''' reverse_opt :  
		| REVERSE
		'''
	if (debug1): print "unhandled: 130"
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0]={}

def p_basic_loop (p) : 
	''' basic_loop :   LOOP statement_s END LOOP
	 '''
	if (debug1): print "handled: 131"
	p[0]=deepcopy(p[2])
	print "statements",p[2]
	#p[0]['code'] = ["loop"] + p[0]['code'] + ["end loop"]
	#CORRECTION

def p_id_opt (p) : 
 ''' id_opt :  
	| designator
	 '''
 if (debug1): print "handled: 132"
 if len(p)==2: p[0]=p[1]
 else: p[0]=None

##############
	 
def p_block (p) : 
 ''' block :   label_opt block_decl block_body END id_opt ';'
	 '''
 if (debug1): print "handled: 133"
 #doubt whether to start a new env. or not
 if p[1]!=None and p[5]!=None and p[1]['lexeme']!=p[5]['lexeme']:
		print "\n\nBLOCK ERROR : starting : %s and ending : %s (LABELS ARE DIFFERENT)\n\n" % (p[1]['lexeme'],p[5]['lexeme'])
		
 if p[1]!=None :
	 if symbol_table.is_present_current_block(p[1]['lexeme']):
				print "\n\nDECLARATION ERROR(in block decl) : " + p[1]['lexeme'] + " has already been declared.\n\n"
				p_error(p)
			
	 else:
				for j in reserved:
					if p[1]['lexeme'] == j:
						print "\n\nDECLARATION ERROR(in block decl) : Variable %s is a reserved keyword.\n\n" % p[1]['lexeme']
						p_error(p)
					
 p[0]=p[3]
 

def p_block_decl (p) : 
 ''' block_decl :  
	| DECLARE decl_part
	 '''
 if (debug1): print "unhandled: 134"

def p_block_body (p) : 
 ''' block_body :   BEGIN handled_stmt_s
	 '''
 if (debug1): print "handled: 135"
 p[0]=p[2]
 #print "block_body"
 #print p[2]
 

def p_handled_stmt_s (p) : 
 ''' handled_stmt_s :   statement_s except_handler_part_opt 
	'''
# here pass code of statements to head of program
 if (debug1): print "handled: 136"
 p[0]=p[1]
 #print "handled_stmts"
 #print p[1]

def p_except_handler_part_opt (p) : 
 ''' except_handler_part_opt :  
	| except_handler_part
	 '''
 if (debug1): print "unhandled: 137"

def p_exit_stmt (p) : 
 ''' exit_stmt :   EXIT name_opt when_opt ';'
	 '''
 if (debug1): print "unhandled: 138"

def p_name_opt (p) : 
 ''' name_opt :  
	| name
	 '''
 if (debug1): print "unhandled: 139"

def p_when_opt (p) : 
 ''' when_opt :  
	| WHEN condition
	 '''
 if (debug1): print "unhandled: 140"

def p_return_stmt (p) : 
 ''' return_stmt :   RETURN ';'
	| RETURN expression ';'
	 '''
 if (debug1): print "unhandled: 141"

def p_goto_stmt (p) : 
 ''' goto_stmt :   GOTO name ';'
	 '''
 if (debug1): print "unhandled: 142"

def p_subprog_decl (p) : 
 ''' subprog_decl :   subprog_spec ';'
	| generic_subp_inst ';'
	| subprog_spec_is_push ABSTRACT ';'
	 '''
 if ( show==1 ): print "\t\t\t subprog_decl"
 if (debug1): print "handled: 143"
 p[0]=p[1]
 
	 
def p_subprog_spec (p) : 
 ''' subprog_spec :   PROCEDURE compound_name formal_part_opt
	| FUNCTION designator formal_part_opt RETURN name
	| FUNCTION designator
	 '''
 if ( show==1 ): print "\t\t\t\t subprog_spec"
 if (debug1): print "unhandled: 144"
 # if symbol_table.is_present_current_block(p[2]['lexeme']):
			# print "\n\nDECLARATION ERROR(in procedure) " + p[2]['lexeme'] + " has already been declared.\n\n"
			# p_error(p)
		
 # else:
 for j in reserved:
	 if p[2]['lexeme'] == j:
		valid = False
		print "\n\nDECLARATION ERROR(in procedure) " + "Variable %s is a reserved keyword.\n\n" % p[2]['lexeme']
		p_error(p)
					
 if len(p)==4:
	 p[0]=deepcopy(p[2])			#passing name of procedure or function so that we can verify it when it ends
	 if p[3]!=None:
		p[0]['in_var']=p[3]['in_var']
		p[0]['out_var']=p[3]['out_var']
	 else: 
		p[0]['in_var']=[]
		p[0]['out_var']=[]
 else :
	print "unhandled"
	 
	
 #symbol_table.add_entry(p[2]['lexeme'].lower(),{})
 #yahan par function aur procedure ke liye arguments and return type store karna hai
 #symbol_table.begin_scope()
 #doubt-- kya-kya handle karna hai?
 
def p_designator1 (p) : 
 ''' designator :   compound_name
	 '''
 if ( show==1 ): print "\t\t\t\t\t designator"
 if (debug1): print "handled: 145 - i"
 p[0]=p[1]
 
def p_designator2 (p) : 
 ''' designator : STRLITERAL
	 '''
 if ( show==1 ): print "\t\t\t\t\t designator"
 if (debug1): print "handled: 145 - ii"
 p[0]={'lexeme':p[1] , 'value':p[1] , 'type':'String'}
 
def p_formal_part_opt (p) : 
 ''' formal_part_opt :   
	| formal_part
	 '''
 if (debug1): print "unhandled: 146"
 if len(p)==1: p[0]=None
 else: p[0]=p[1]

def p_formal_part (p) : 
 ''' formal_part :   '(' param_s ')'
	 '''
 if (debug1): print "handled: 147"
 p[0]=p[2]

def p_param_s (p) : 
 ''' param_s :   param
	| param_s ';' param
	 '''
 if (debug1): print "handled: 148"
 if(len(p)==2):
	 p[0]=p[1]
 else:
	 p[0]=deepcopy(p[1])
	 p[0]['in_var']=p[0]['in_var']+p[3]['in_var']
	 p[0]['out_var']=p[0]['out_var']+p[3]['out_var']

def p_param (p) : # mark is datatype
 ''' param :   def_id_s ':' mode mark init_opt
	| error
	 '''	#init_opt not handled
 if (debug1): print "unhandled: 149"
 p[0]={}
 p[0]['in_var']=[]
 p[0]['out_var']=[]
 if(p[3] == 'in') :
	for id in p[1]:
		p[0]['in_var']=p[0]['in_var']+ [{'lexeme':id , 'type':p[4]['lexeme']}]
 if(p[3] == 'out'):
	for id in p[1]:
		p[0]['out_var']=p[0]['out_var']+ [{'lexeme':id , 'type':p[4]['lexeme']}]
  

def p_mode (p) : 
 ''' mode :  
	| IN
	| OUT
	| IN OUT
	| ACCESS
	 '''
 if (debug1): print "unhandled: 150"
 if (len(p)==1): p[0]=None
 else: p[0]=p[1]
 
def p_subprog_spec_is_push (p) : 
 ''' subprog_spec_is_push :   subprog_spec IS
	 '''
 if (debug1): print "handled: 151"
 
 p[0]=p[1]
 if (symbol_table.get_current_env()).prev_env!= None: 		#avoiding for outermost procedure
	 p[0]['nextlist']=make_list(three_addr_code.next_instr)
	 emit_code('goto',None,None,None)
 else:
	p[0]['nextlist']=[]
 symbol_table.begin_scope()
 emit_code("proc_begin",p[1]['lexeme'],None,None)  		# here its start procedure label
 symbol_table.add_beginning_procedure(p[1]['lexeme'],p[1]['in_var'],p[1]['out_var'])

def p_subprog_body (p) : 
 ''' subprog_body :   subprog_spec_is_push decl_part block_body END id_opt ';' '''
 if ( show==1 ): print "\t\t\t subprog_body"
 if (debug1): print "handled: 152"
 if p[5]!=None and p[1]['lexeme'] != p[5]['lexeme']:
	print "\n\nSUBPROG ERROR : Opening : %s and Closing : %s (LABELS ARE DIFFERENT) \n\n"% (p[1]['lexeme'],p[5]['lexeme'] )
	p_error(p)
	
 p[0]=p[3]
 
 symbol_table.update_exiting_procedure(p[1]['lexeme'])
 #CORRECTION
 symbol_table.end_scope()
 
 outlist_temp=''
 if len(symbol_table.get_attribute_value(p[1]['lexeme'].lower(), 'out_var')) > 0:
	for i in (symbol_table.get_attribute_value(p[1]['lexeme'].lower(), 'out_var')):
		outlist_temp=outlist_temp+i['lexeme']+',';
	emit_code('return',outlist_temp[:-1],None,None);
 else:
	emit_code('return',None,None,None);
			
 back_patch(p[1]['nextlist'],three_addr_code.next_instr)
 #print "subprog_body"
 #print "DEEPAK",p[3]

def p_procedure_call (p) : 
 ''' procedure_call :   name ';'
	 '''
 if ( show==1 ): print "\t\t procedure_call"
 if (debug1): print "handled: 153"
 #print "procedure call"			#handled in indexed_comp
 p[0]=p[1]
 p[0]['nextlist']=make_list(None)
 
def p_pkg_decl (p) : 
 ''' pkg_decl :   pkg_spec ';'
	| generic_pkg_inst ';'
	 '''
 if ( show==1 ): print "\t\t\t pkg_decl"
 if (debug1): print "unhandled: 154"
	 
def p_pkg_spec (p) : 
 ''' pkg_spec :   PACKAGE compound_name IS decl_item_s private_part END c_id_opt
	 '''
 if ( show==1 ): print "\t\t\t\t pkg_spec"
 if (debug1): print "unhandled: 155"

def p_private_part (p) : 
 ''' private_part :  
	| PRIVATE decl_item_s
	 '''
 if (debug1): print "unhandled: 156"

def p_c_id_opt (p) : 
 ''' c_id_opt :   
	| compound_name
	 '''
 if (debug1): print "unhandled: 157"

def p_pkg_start (p) :
	''' pkg_start : PACKAGE BODY compound_name IS ''';
	if (debug1): print "handled: 158i"
	
	p[0]=p[3]
	#symbol_table.begin_scope()
	emit_code("package_begin",p[3]['lexeme'],None,None)  		# here its start procedure label
	#symbol_table.add_beginning_procedure(p[1]['lexeme'],p[1]['in_var'],p[1]['out_var'])
 
def p_pkg_body (p) : 
 ''' pkg_body :   pkg_start decl_part body_opt END c_id_opt ';'
	 '''
 if ( show==1 ): print "\t\t\t pkg_body"
 if (debug1): print "handled: 158"

def p_body_opt (p) : 
 ''' body_opt :  
	| block_body
	 '''
 if (debug1): print "unhandled: 159"

def p_private_type (p) : 
 ''' private_type :   tagged_opt limited_opt PRIVATE
	 '''
#not handle
 if (debug1): print "unhandled: 160"

def p_limited_opt (p) : 
 ''' limited_opt :  
	| LIMITED
	 '''
 if (debug1): print "unhandled: 161"

def p_use_clause (p) : 
 ''' use_clause :   USE name_s ';'
	| USE TYPE name_s ';'
	 '''
 if ( show==1 ): print "\t\t\t use Clause"
 if (debug1): print "unhandled: 162"
 
def p_name_s (p) : 
 ''' name_s :   name
	| name_s ',' name
	 '''
 if (debug1): print "unhandled: 163"

def p_rename_decl (p) : 
 ''' rename_decl :   def_id_s ':' object_qualifier_opt subtype_ind renames ';'
	| def_id_s ':' EXCEPTION renames ';'
	| rename_unit
	 '''
 if (debug1): print "unhandled: 164"

def p_rename_unit (p) : 
 ''' rename_unit :   PACKAGE compound_name renames ';'
	| subprog_spec renames ';'
	| generic_formal_part PACKAGE compound_name renames ';'
	| generic_formal_part subprog_spec renames ';'
	 '''
 if ( show==1 ): print "\t\t\t rename_unit"
 if (debug1): print "unhandled: 165"

def p_renames (p) : 
 ''' renames :   RENAMES name
	 '''
 if (debug1): print "unhandled: 166"

def p_task_decl (p) : 
 ''' task_decl :   task_spec ';'
	 '''
 if (debug1): print "unhandled: 167"

def p_task_spec (p) : 
 ''' task_spec :   TASK simple_name task_def
	| TASK TYPE simple_name discrim_part_opt task_def
	 '''
 if (debug1): print "unhandled: 168"

def p_task_def (p) : 
 ''' task_def :  
	| IS entry_decl_s rep_spec_s task_private_opt END id_opt
	 '''
 if (debug1): print "unhandled: 169"

def p_task_private_opt (p) : 
 ''' task_private_opt :  
	| PRIVATE entry_decl_s rep_spec_s
	 '''
 if (debug1): print "unhandled: 170"

def p_task_body (p) : 
 ''' task_body :   TASK BODY simple_name IS decl_part block_body END id_opt ';'
	 '''
 if (debug1): print "unhandled: 171"

def p_prot_decl (p): 
 ''' prot_decl : prot_spec ';'
	 '''
 if (debug1): print "unhandled: 172"

def p_prot_spec (p) : 
 ''' prot_spec :   PROTECTED ID prot_def
	| PROTECTED TYPE simple_name discrim_part_opt prot_def
	 '''
 if (debug1): print "unhandled: 173"

def p_prot_def (p) : 
 ''' prot_def :   IS prot_op_decl_s prot_private_opt END id_opt
	 '''
 if (debug1): print "unhandled: 174"

def p_prot_private_opt (p) : 
 ''' prot_private_opt :  
	| PRIVATE prot_elem_decl_s '''
 if (debug1): print "unhandled: 175"


def p_prot_op_decl_s (p) : 
 ''' prot_op_decl_s :   
	| prot_op_decl_s prot_op_decl
	 '''
 if (debug1): print "unhandled: 176"

def p_prot_op_decl (p) : 
 ''' prot_op_decl :   entry_decl
	| subprog_spec ';'
	| rep_spec
	| pragma
	 '''
 if (debug1): print "unhandled: 177"

def p_prot_elem_decl_s (p) : 
 ''' prot_elem_decl_s :   
	| prot_elem_decl_s prot_elem_decl
	 '''
 if (debug1): print "unhandled: 178"

def p_prot_elem_decl (p) : 
 ''' prot_elem_decl :   prot_op_decl 
			| comp_decl  '''
 if (debug1): print "unhandled: 179"

def p_prot_body (p) : 
 ''' prot_body :   PROTECTED BODY simple_name IS prot_op_body_s END id_opt ';'
	 '''
 if (debug1): print "unhandled: 180"

def p_prot_op_body_s (p) : 
 ''' prot_op_body_s :   pragma_s
	| prot_op_body_s prot_op_body pragma_s
	 '''
 if (debug1): print "unhandled: 181"

def p_prot_op_body (p) : 
 ''' prot_op_body :   entry_body
	| subprog_body
	| subprog_spec ';'
	 '''
 if (debug1): print "unhandled: 182"

def p_entry_decl_s (p) : 
 ''' entry_decl_s :   pragma_s
	| entry_decl_s entry_decl pragma_s
	 '''
 if (debug1): print "unhandled: 183"

def p_entry_decl (p) : 
 ''' entry_decl :   ENTRY ID formal_part_opt ';'
	| ENTRY ID '(' discrete_range ')' formal_part_opt ';'
	 '''
 if (debug1): print "unhandled: 184"

def p_entry_body (p) : 
 ''' entry_body :   ENTRY ID formal_part_opt WHEN condition entry_body_part
	| ENTRY ID '(' iter_part discrete_range ')' formal_part_opt WHEN condition entry_body_part
	 '''
 if (debug1): print "unhandled: 185"
 
def p_entry_body_part (p) : 
 ''' entry_body_part :   ';'
	| IS decl_part block_body END id_opt ';'
	 '''
 if (debug1): print "unhandled: 186"
 
def p_rep_spec_s (p) : 
 ''' rep_spec_s :  
	| rep_spec_s rep_spec pragma_s
	 '''
 if (debug1): print "unhandled: 187"
 
def p_entry_call (p) : 
 ''' entry_call :   procedure_call
	 '''
 if (debug1): print "unhandled: 188"
  
def p_accept_stmt (p) : 
 ''' accept_stmt :   accept_hdr ';'
	| accept_hdr DO handled_stmt_s END id_opt ';'
	 '''
 if (debug1): print "unhandled: 189"
 
def p_accept_hdr (p) : 
 ''' accept_hdr :   ACCEPT entry_name formal_part_opt
	 '''
 if (debug1): print "unhandled: 190"
 
def p_entry_name (p) : 
 ''' entry_name :   simple_name
	| entry_name '(' expression ')'
	 '''
 if (debug1): print "unhandled: 191"
 
def p_delay_stmt (p) : 
 ''' delay_stmt :   DELAY expression ';'
	| DELAY UNTIL expression ';'
	 '''
 if (debug1): print "unhandled: 192"
 
def p_select_stmt (p) : 
 ''' select_stmt :   select_wait
	| async_select
	| timed_entry_call
	| cond_entry_call
	 '''
 if (debug1): print "unhandled: 193"
 
def p_select_wait (p) : 
 ''' select_wait :   SELECT guarded_select_alt or_select else_opt END SELECT ';'
	 '''
 if (debug1): print "unhandled: 194"
 
def p_guarded_select_alt (p) : 
 ''' guarded_select_alt :   select_alt
	| WHEN condition ARROW select_alt
	 '''
 if (debug1): print "unhandled: 194"
 
def p_or_select (p) : 
 ''' or_select :  
	| or_select OR guarded_select_alt
	 '''
 if (debug1): print "unhandled: 195"
 
def p_select_alt (p) : 
 ''' select_alt :   accept_stmt stmts_opt
	| delay_stmt stmts_opt
	| TERMINATE ';'
	 '''
 if (debug1): print "unhandled: 196"
 
def p_delay_or_entry_alt (p) : 
 ''' delay_or_entry_alt :   delay_stmt stmts_opt
	| entry_call stmts_opt '''
 if (debug1): print "unhandled: 197"
 
def p_async_select (p) : 
 ''' async_select :   SELECT delay_or_entry_alt THEN ABORT statement_s END SELECT ';'
	 '''
 if (debug1): print "unhandled: 198"
 
def p_timed_entry_call (p) : 
 ''' timed_entry_call :   SELECT entry_call stmts_opt OR delay_stmt stmts_opt END SELECT ';'
	 '''
 if (debug1): print "unhandled: 199"
 
def p_cond_entry_call (p) : 
 ''' cond_entry_call :   SELECT entry_call stmts_opt ELSE statement_s END SELECT ';'
	 '''
 if (debug1): print "unhandled: 200"
 
def p_stmts_opt (p) : 
 ''' stmts_opt :  
	| statement_s
	 '''
 if (debug1): print "unhandled: 201"
 
def p_abort_stmt (p) : 
 ''' abort_stmt :   ABORT name_s ';'
	 '''
 if (debug1): print "unhandled: 202"
 
def p_compilation (p) : 
 ''' compilation :  
	| compilation comp_unit
	| pragma pragma_s
	 '''
 if (show==1) : print " Compilation "
 if (debug1): print "handled: 203"
 if(len(p)==1):
	 p[0]=[]
 else:
	 p[0]=p[1]+[p[2]]
 
def p_comp_unit (p) : 
 ''' comp_unit :   context_spec private_opt unit pragma_s
	| private_opt unit pragma_s
	 '''
 if ( show==1 ): print "\t comp_unit"
 if (debug1): print "handled: 204"
 if(len(p)==5):
	 p[0]=p[3]
 else:
	 p[0]=p[2]
 
def p_private_opt (p) : 
 ''' private_opt :  
	| PRIVATE
	 '''
 if ( show==1 ): print "\t\t private_opt"
 if (debug1): print "unhandled: 205"
 
def p_context_spec (p) : 
 ''' context_spec :   with_clause use_clause_opt
	| context_spec with_clause use_clause_opt
	| context_spec pragma
	 '''
 if ( show==1 ): print "\t\t context_spec"
 if (debug1): print "to be handled: 206"
 
def p_with_clause (p) : 
 ''' with_clause :   WITH c_name_list ';'
	 '''
 if ( show==1 ): print "\t\t\t with_clause"
 if (debug1): print "to be handled: 207"
 
def p_use_clause_opt (p) : 
 ''' use_clause_opt :  
	| use_clause_opt use_clause
	 '''
 if ( show==1 ): print "\t\t\t use_clause_opt"
 if (debug1): print "to be handled: 208"
 
def p_unit (p) : 
 ''' unit :   pkg_decl
	| pkg_body
	| subprog_body
	| subunit
	| generic_decl
	| rename_unit
	| subprog_decl
	 '''
 if ( show==1 ): print "\t\t unit"
 if (debug1): print "handled: 209"
 #print "unit"
 p[0]=p[1]
 

 
def p_subunit (p) : 
 ''' subunit :   SEPARATE '(' compound_name ')' subunit_body
	 '''
 if ( show==1 ): print "\t\t\t subunit"
 if (debug1): print "unhandled: 210"
 
def p_subunit_body (p) : 
 ''' subunit_body :   subprog_body
	| pkg_body
	| task_body
	| prot_body
	 '''
 if (debug1): print "handled: 211"
 p[0]=p[1]
 
def p_body_stub (p) : 
 ''' body_stub :   TASK BODY simple_name IS SEPARATE ';'
	| PACKAGE BODY compound_name IS SEPARATE ';'
	| subprog_spec IS SEPARATE ';'
	| PROTECTED BODY simple_name IS SEPARATE ';'
	 '''
 if (debug1): print "unhandled: 212"
 
def p_exception_decl (p) : 
 ''' exception_decl :   def_id_s ':' EXCEPTION ';'
	 '''
 if (debug1): print "unhandled: 213"
 
def p_except_handler_part (p) : 
 ''' except_handler_part :   EXCEPTION exception_handler
	| except_handler_part exception_handler
	 '''
 if (debug1): print "unhandled: 214"
 
def p_exception_handler (p) : 
 ''' exception_handler :   WHEN except_choice_s ARROW statement_s
	| WHEN ID ':' except_choice_s ARROW statement_s
	 '''
 if (debug1): print "unhandled: 215"
 
def p_except_choice_s (p) : 
 ''' except_choice_s :   except_choice
	| except_choice_s '|' except_choice
	 '''
 if (debug1): print "unhandled: 216"
 
def p_except_choice (p) : 
 ''' except_choice :   name
	| OTHERS
	 '''
 if (debug1): print "unhandled: 217"
 
def p_raise_stmt (p) : 
 ''' raise_stmt :   RAISE name_opt ';'
	 '''
 if (debug1): print "unhandled: 218"
 
def p_requeue_stmt (p) : 
 ''' requeue_stmt :   REQUEUE name ';'
	| REQUEUE name WITH ABORT ';'
	 '''
 if (debug1): print "unhandled: 219"
 
def p_generic_decl (p) : 
 ''' generic_decl :   generic_formal_part subprog_spec ';'
	| generic_formal_part pkg_spec ';'
	 '''
 if ( show==1 ): print "\t\t\t generic_decl"
 if (debug1): print "unhandled: 220"
 
def p_generic_formal_part (p) : 
 ''' generic_formal_part :   GENERIC
	| generic_formal_part generic_formal
	 '''
 if (debug1): print "unhandled: 221"
 
def p_generic_formal (p) : 
 ''' generic_formal :   param ';'
	| TYPE simple_name generic_discrim_part_opt IS generic_type_def ';'
	| WITH PROCEDURE simple_name formal_part_opt subp_default ';'
	| WITH FUNCTION designator formal_part_opt RETURN name subp_default ';'
	| WITH PACKAGE simple_name IS NEW name '(' BOX ')' ';'
	| WITH PACKAGE simple_name IS NEW name ';'
	| use_clause
	 '''
 if (debug1): print "unhandled: 222"
 
def p_generic_discrim_part_opt (p) : 
 ''' generic_discrim_part_opt :  
	| discrim_part
	| '(' BOX ')'
	 '''
 if (debug1): print "unhandled: 223"
 
def p_subp_default (p) : 
 ''' subp_default :  
	| IS name
	| IS BOX
	 '''
 if (debug1): print "unhandled: 224"
 
def p_generic_type_def (p) : 
 ''' generic_type_def :   '(' BOX ')'
	| RANGE BOX
	| MOD BOX
	| DELTA BOX
	| DELTA BOX DIGITS BOX
	| DIGITS BOX
	| array_type
	| access_type
	| private_type
	| generic_derived_type
	 '''
 if (debug1): print "unhandled: 225"
 
def p_generic_derived_type (p) : 
 ''' generic_derived_type :   NEW subtype_ind
	| NEW subtype_ind WITH PRIVATE
	| ABSTRACT NEW subtype_ind WITH PRIVATE
	 '''
 if (debug1): print "unhandled: 226"
 
def p_generic_subp_inst (p) : 
 ''' generic_subp_inst :   subprog_spec IS generic_inst
	 '''
 if (debug1): print "unhandled: 227"
 
def p_generic_pkg_inst (p) : 
 ''' generic_pkg_inst :   PACKAGE compound_name IS generic_inst
	 '''
 if ( show==1 ): print "\t\t\t\t generic_pkg_inst"
 if (debug1): print "unhandled: 228"
  
def p_generic_inst (p) : 
 ''' generic_inst :   NEW name
	 '''
 if ( show==1 ): print "\t\t\t\t\t generic_inst"
 if (debug1): print "unhandled: 229"
 
def p_rep_spec (p) : 
 ''' rep_spec :   attrib_def
	| record_type_spec
	| address_spec
	 '''
 if (debug1): print "unhandled: 230"
 
def p_attrib_def (p) : 
 ''' attrib_def :   FOR mark USE expression ';'
	 '''
 if (debug1): print "unhandled: 231"
 
def p_record_type_spec (p) : 
 ''' record_type_spec :   FOR mark USE RECORD align_opt comp_loc_s END RECORD ';'
	 '''
 if (debug1): print "unhandled: 232"
 
def p_align_opt (p) : 
 ''' align_opt :  
	| AT MOD expression ';'
	 '''
 if (debug1): print "unhandled: 233"
 
def p_comp_loc_s (p) : 
 ''' comp_loc_s :  
	| comp_loc_s mark AT expression RANGE range ';'
	 '''
 if (debug1): print "unhandled: 234"
 
def p_address_spec (p) : 
 ''' address_spec :   FOR mark USE AT expression ';'
	 '''
 if (debug1): print "unhandled: 235"
 
def p_code_stmt (p) : 
 ''' code_stmt :   qualified ';'
	 '''
 if (debug1): print "unhandled: 236"
 
def p_m_empty(p):
	'm : '
	p[0] = {'instr':three_addr_code.next_instr}
	if (debug1): print "handled: 237"
	
def p_n_empty(p):
	'n : '
	# p[0] = {'instr':globalitems.three_addr_code.next_instr}
	p[0]={}
	p[0]['nextlist']=make_list(three_addr_code.next_instr)
	emit_code('goto',None,None,None)
	if (debug1): print "handled: 238"

########################### END OF GRAMMAR #################################	
	

	
		
#######################################################################################################				
# Error rule for syntax errors
def p_error(p):
	#print inspect.getframeinfo(inspect.currentframe().f_back)[2]
	#print inspect.getframeinfo(inspect.currentframe().f_back)[2]
	print "Syntax error in input! at line - ",p.lineno
	#assert(False)
	sys.exit(0)

# Build the parser
#parser = yacc.yacc(start = 'start_symbol', debug = True)

##while True:
##        try:
##                s = raw_input('calc > ')
##        except EOFError:
##                break
##        if not s: continue
##        result = parser.parse(s)
##        print (result)
#result = parser.parse(data)
#print ("Parse table output is : \n", result)



