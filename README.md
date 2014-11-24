				Ada Compiler v3 
				  GROUP 12  
			Ashudeep Singh	10162
			Chandra Prakash 10209
			Deepak Pathak	10222
			Kaustubh Tapi	10346
-------------------------------------------------------------------------------------------------------	

VERY IMPORTANT -
1. To Run any test file, 'the location of the test file' must be changed in the "main_script.py" file.  
2. Currently for any test program the name of main procedure in the Ada program must be "Proced2" .
3. Run the main_script.py file with the location set to the folder which contains 1 file that is to be tested.
4. Spim_Code.asm is generated in the "Final_Code" folder.
5. This program can be run on mips architecture
	(We have tested it on Mars4.3 mips simulator)
	
-----------------------------------------------------------------------------------------------------		
FEATURES OF COMPILER-
1. expression
2. for loop
3. while loop
4. if else
5. arithmetic and relational operators
6. 1 and multi dimensional arrays
7. procedures and recursive procedures(call by value and call by reference)
8. Simple package structure.
9. error handling
10. generation of three address code and assembly code
-----------------------------------------------------------------------------
Important files and folders-
1. ada_compiler_source.py 			- Contains the lexer and parser phase of our compiler
									  Takes 
									  
2. globalitems.py				- Contains global variables and structures used

3. main_script.py					- 
										Main script file that runs and compiles the "Ada file" and           generates the three address code
										
4. spim_code_gen.py				- Converts the three address code to mips assembly program

5. symbol_table.py				- Symbol Table, Environment and their functions defined in this file

6. three_addr_generator.py			- Contains Functions that help in three address code generation

7. Output_3addr.txt				- Contains the three address code for test file

8. recordtype.py				- Standard Python file included to use python records

9. Spim_Code.asm				- Contains the mips assembly code for the test program

10. final_examples-
	Contains the test program that we have run.
	a. 1_for.ada 		- 		contains a basic for loop that prints numbers from 1 to 4
						(For loop and printing integers implemented)
						
	b. 2_twofives_proc_while.ada    - 	tries to express every number as 2*x+ 5*y
						(procedure calling , while loop , if else implemented)
						
	c. 3_sort_insertion_array_for_expr.ada- iterative program to sort array.
						(multiple for loop implemented)
						
	d. 4_2-darray.ada		- 	Creates a two dimensional array and assigns value to thme and prints them.
						(2- dimensional array implemented)
						
	e. 5_pythagorus_nestedfor_proc.ada -	 Checks for all pythagorean triplets b/w 1 and 20
							(Nested for loops upto 3 level)
							
	f. 6_2refvar.ada  - 			Swaps 2 numbers
						( Demonstrates call by value and call by reference (with multiple outputs) in ada)
						
	g. 7_fact_recursion.ada - 		Calculates and Prints the Factorial of 6
						(Demonstrates Recursion)
	h. 8_evenodd_mutualrecursion.ada - 	Checks whether a number is odd or even.
						(Demonstrates mutual recursion)
						
	i. 9_primes_nestedproc.ada	-	Prints prime numbers b/w  2 to 100
						(For loop and nesting of procedures implemented)
						
	j. 10_package.ada		- 	Simple package structure implemented
						(Procedure defined in package called in the same file)
						
	j. error_1.ada			-	Demonstrates error(type error during assignment)
	

------------------------------------------------------------------------------------------------------


