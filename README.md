# CSE_112_Project
A custom assembler designed and implemented for a given ISA.

## Team Members
Farhan Ali     (farcat576)      CSE 2021045   
Sahil Saraswat (sahilence)      CSE 2021091   
Anshuman Bunga (AstraTriesGit)  CSE 2021016   

## Assembler
The assembler has been coded in Python.    
The assemble reads assembly code from the standard console. All the lines of the assembly code are read before it is processed. The final code is then submitted with the `Ctrl + D` key. Empty lines in the assembly code have been ignored.     

The assembler uses dictionaries for error messages and opcode mapping. The error dictionary is used with a general error printing function, that prints the error message, the line where the error occured and halts the assembling process.      
The assembler has functions to create the binary code for the assembly instruction, as well as separate functions to check the syntax of the assembly instruction based on their type (A, B, C, D, E, F.)     
The assembler also has helper functions for the syntax verifying functions for registers, labels, variables, immediate values and illegal use of the special FLAGS register.     

The inputted assembly code is first parsed through using the `parse()` function.     
> This function returns mappings for variables `var_dict`, labels `label_dict` and the final opcode dictionary `op_dict`.     
> This function checks for `hlt` statements, variable space, length of input assembly code, re-initialisations and general syntax.     

The `process()` function converts the parsed data into the final assembled binary code into a list `L`.      
> The `mov` instruction is manually checked as it has two possible types (register type or immediate value type.)     
> The rest of the instructions are checked for their particular syntax as per their type (A, B, C, D, E, F) and their corresponding binary code is generated to appended to `L`.     

The final binary code is then printed from `L` to the console.     
This is the output of the assembler.
