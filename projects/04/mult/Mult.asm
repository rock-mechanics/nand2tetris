// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
// Set realr0 to r0
@R0
D=M
@realr0
M=D
// Set realr1 to r1
@R1
D=M
@realr1
M=D
// Set sum to zero
@sum
M=0
// Set r2 to zero, I think it is not neccessary, but it is in the test scripts.
@R2
M=0

// Check if r0 is positve.
// If not, flip the sign of realr0 and realr1
@realr0
D=M
@FLIPSIGN
D;JLT

// Start the loop
(LOOP)
// Check realr0 if zero then, jumps to conclusion.
@realr0
D=M
@FINAL
D;JEQ 
// IF realr0 is not zero, then add realr1 to sum.
@realr1
D=M
@sum
M=D+M 
// realr0 should minus one.
@realr0
M=M-1
// go back to loop.
@LOOP
0;JMP

(FLIPSIGN) // flip the sign, so realr0 is always positive.
@realr0
D=M
M=-D
@realr1
D=M
M=-D
@LOOP
0;JMP 

(FINAL)
@sum
D=M
@R2
M=D

(END) //infinite loop to end
@END
0;JMP
