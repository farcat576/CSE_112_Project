# CSE_112_Project
A custom assembler designed and implemented for a given ISA.

## Team Members
Farhan Ali     (farcat576)      CSE 2021045   
Sahil Saraswat (sahilence)      CSE 2021091   
Anshuman Bunga (AstraTriesGit)  CSE 2021016   

## Assembler (Q1)                     
The assembler has been coded in Python.    
The assemble reads assembly code from the standard console. All the lines of the assembly code are read before it is processed. The final code is then submitted with the `Ctrl + D` key. Empty lines in the assembly code have been ignored.     

The assembler uses dictionaries for error messages and opcode mapping. The error dictionary is used with a general error printing function, that prints the error message, the line where the error occured and halts the assembling process.      
The assembler has functions to create the binary code for the assembly instruction, as well as separate functions to check the syntax of the assembly instruction based on their type (A, B, C, D, E, F.)     
The assembler also has helper functions for the syntax verifying functions for registers, labels, variables, immediate values and illegal use of the special FLAGS register.     

The inputted assembly code is first parsed through using the `parse()` function.     
> This function returns mappings for variables `var_dict`, labels `label_dict` and the final opcode dictionary `op_dict`.     
> This function checks for `hlt` statements, variable space, length of input assembly code, re-initialisations and general syntax of labels and variables.     

The `process()` function converts the parsed data into the final assembled binary code into a list `L`.      
> The `mov` instruction is manually checked as it has two possible types (register type or immediate value type.)     
> The rest of the instructions are checked for their particular syntax as per their type (A, B, C, D, E, F) and their corresponding binary code is generated to appended to `L`. If an error is found, the assembling process is halted and the error is printed on the console.      

The final binary code is then printed from the list `L` to the console.     
This is the output of the assembler.        

## Simulator (Q2)           
The simulator has been coded in Python.           
The program equivalent for the memory is a _list_ `MEM` of 256 strings, all set to `'0000000000000000'` by default. The program counter has been represented by an _integer_ `PC` and the register file is represented as a _dictionary_ `RF` with the register names as the keys, which store the values of the registers, with the exception of the FLAGS register, which stores a string.          
The simulator reads binary machine code from the standard console. The instructions are then stored in the memory through the function `fix_mem()`, called after the input is taken.            
Instructions are then executed line by line with the `exec()` function called on the entire memory with a while loop which runs until the machine code equivalent of `hlt` is reached.             

The `exec()` function determines the type of the instruction with the help of `opcode`, an opcode mapping. Once the type of the instruction has been determined, the instruction is interpreted as an object of its type.         
> We have defined classes for every type of instruction (A, B, C, D, E, F) and during the initialisation of the instruction object, the exact command and its arguments are determined. The requested command is then directly executed by making a call to its respective method within the class.                     


After a line is fully executed, the program counter and the values stored in the registers are printed on the standard console with the `line_output()` function. All the values are printed in binary.           
When the `hlt` statement is reached, the entire state of the program's memory is printed out on the console by calling the `mem_dump()` function.         


This is the output of the simulator.                  

## Floating Point Arithmetic Support (Q3)             
We have extended the functionality of the assembler and simulator by supporting the addition and subtraction of floating point numbers, as well as the storing of a float value in a register.                
> In the assembler, we have updated the error dictionary to include possible errors in the syntax for floating point numbers. Helper functions `bin_to_float()`, `float_to_bin()` and `float_check()` have been implemented to ensure the proper implementation of flop arithmetic.                      
> In the simulator, `addf()`, `subtractf()` have been included in Class A methods, while `movif()` is implemented as a method in Class B.                       

## Memory Access Trace (Q4)                 
We have created a function `plot_graph()` which plots the memory location accessed to the cycle number in which it was accessed due to the `ld` and `st` instructions. A global variable `cycle` was created for this purpose.              
The graphs are plotted using the `matplotlib` module.           
> The X-axis marks the cycle number while the Y-axis marks the memory location accessed at that cycle number.                       

## Memory Mumbo Jumbo (Q5)                    



