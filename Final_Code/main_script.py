import os
import globalitems
from ada_compiler_source import *
from spim_code_gen import *
import three_addr_generator

#-----------Set the absolute path to the folder---------------------#
#-----------containing the one example code you want to run---------#
	
#file_name=input("Input File: "); #give input in double quotes in python 2.7 and direcly with out quotes in py3.3
#path="D:/Dropbox/Compiler Project/Project/sample_codes/final_examples/test/"
#path="C:/Users/welcome/Dropbox/Compiler Project/Project/Final Submission/final_examples/test/"
path=sys.argv[1]#"C:/Users/Ashudeep Singh/Dropbox/Compiler Project/Project/Final Submission/final_examples/test/"

#path="./all/"
for f in os.listdir(path):
	print "\nFile name :",f
	f = path + f
	fp=open(f,'r')
	data = fp.read()    
	# Give the lexer some input
	lexer.input(data)

	#symbol table entry takes place in the parser itself so here entry commented
	# Symbol Table
	# s_table=SymbolTable()
	#while True:
			#tok = lexer.token()
			#if not tok: break      # No more input
			#print(tok)
		# if tok.type == 'ID' :
			# s_table.insert(tok.value,tok.lineno)		
	# print ("\n\nHere is the final table : \n")
	# s_table.print_table()
	parser = yacc.yacc(start = 'start_symbol', debug = True)
	result = parser.parse(data)
	print ("Parse table output is:", result)
	print ""
	three_addr_generator.print_three_addr_code()
	threeaddr_to_spim(three_addr_code.code,"Proced2")
	fp.close()
	data=None
    
    
