// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// A Loop to Detect keyboard Input.
@SCREEN
D=A
@screen
M=D

(LOOP)
@KBD
D=M
@BLACK
D;JNE
@WHITE
D;JEQ

(BLACK)
@8191
D=A
@rows
M=D
(BLACKLOOP)
//check all rows is drawn.
@rows
D=M
@LOOP // if rows are cleared jump back to the loop. 
D;JLT
@screen
D=M
@rows
D=D+M // screen base row + current rownumber
A=D //assign the row number to address a.
M=-1 // black the screen.
@rows // one row is done, thus minus one.
M = M - 1
@BLACKLOOP
0;JMP

(WHITE)
@8191
D=A
@rows
M=D
(WHITELOOP)
//check all rows is drawn.
@rows
D=M
@LOOP // if rows are cleared jump back to the loop. 
D;JLT
@screen
D=M
@rows
D=D+M // screen base row + current rownumber
A=D //assign the row number to address a.
M=0 // white the screen.
@rows // one row is done, thus minus one.
M = M - 1
@WHITELOOP
0;JMP
