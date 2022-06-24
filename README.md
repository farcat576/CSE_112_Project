# CSE_112_Project
A custom assembler designed and implemented for a given ISA.

## Team Members
Farhan Ali     (farcat576)      CSE 2021045   
Sahil Saraswat (sahilence)      CSE 2021091   
Anshuman Bunga (AstraTriesGit)  CSE 2021016   

## Assembler
The assembler has been coded in Python.    
The assembler reads the assembly code from a `.txt` file. The assembler then verifies whether the `hlt` statement appears at the end, and whether the number of instructions in the given text file do not exceed the limit supported by the assembler.   
We have implemented a dictionary for matching the assembly instructions with their respective opcodes.   
We then gather all the variables defined at the top of the assembly program and allot them memory addresses as per the Von Neumann computer architecture.   
The instructions are then checked for proper syntax.   
> The `mov` instruction is manually checked for whether it is of register type or immediate value type.   
> The rest of the instructions are checked for their particular syntax as per their type (A, B, C, D, E, F)   
> If the instruction's syntax is correct, we construct the binary command for the instruction as a string and add it to a list of the gathered instructions in machine code.   
> Otherwise, the error message is printed and the assembling process is halted.  


The assembler then writes the final binary machine code in a text file called `binary.txt`.   
This is the output of the assembler.
