import sys
import re

# initalize some constants for the command type
C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABLE = "C_LABLE"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_RETURN = "C_RETURN"
C_CALL = "C_CALL"

def main(vm_name) : 
	ass_name =vm_name.replace(".vm", ".asm")

	#initialize parser and code writer.
	par = Parser(vm_name)
	cwr = CodeWriter(ass_name)

	while True:
		if par.hasMoreCommands() : 
			par.advance()

			if par.commandType() == C_ARITHMETIC:
				cwr.writeArithmetic(par.currentcommand)
			elif par.commandType() == C_PUSH or par.commandType() == C_POP:
				cwr.writePushPop(par.commandType(), par.arg1(), par.arg2())
		else:
			break
	
	cwr.Close()
	print(ass_name + " created")

class Parser():

	def __init__(self,fname):
		self.currentcommand = None
		self.nextcommandindex = 0
		self.commands =[]
		self.arithmetics = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

		with open(fname, 'r') as f:
			lines= f.readlines()
			for ln in lines : 
				if ln.strip() and ln[0:2]!="//" :
					self.commands.append(ln.strip())

	def hasMoreCommands(self):
		return self.nextcommandindex < len(self.commands)
	
	def advance(self):
		#update the current command to next command
		self.currentcommand = self.commands[self.nextcommandindex]
		#progress to next command
		self.nextcommandindex += 1

	def commandType(self):
		if self.currentcommand in self.arithmetics : 
			return C_ARITHMETIC
		elif self.currentcommand.split(' ')[0] == "push":
			return C_PUSH
		elif self.currentcommand.split(' ')[0] == "pop":
			return C_POP
		else:
			return None
	
	def arg1(self):
		parts = self.currentcommand.split(' ')
		if len(parts) > 1 : 
			return parts[1]
		else:
			return parts[0]

	def arg2(self):
		parts = self.currentcommand.split(' ')
		if len(parts) > 2 : 
			return parts[2]
		else:
			return None

class CodeWriter():
	def __init__(self,fname):
		#file name consists of paths seprated by /
		self.name = fname.split('.')[0]
		self.name = self.name.split('/')[-1]
		self.outputf =open(fname, 'w')
		self.outputf =open(fname, 'a')
		self.labelcounter = 0
	
	def writeArithmetic(self, command):
		acode =""
		if command == "add" :
			acode += "@SP\n"
			acode += "AM=M-1\n" #move up the stack pointer
			acode += "D=M\n"
			acode += "A=A-1\n" #move the pointer further up.
			acode += "M=M+D\n"
		elif command == "sub" :
			acode += "@SP\n"
			acode += "AM=M-1\n" #move up the stack pointer
			acode += "D=M\n"
			acode += "A=A-1\n" #move the pointer further up.
			acode += "M=M-D\n"
		elif command == "neg":
			acode += "@SP\n"
			acode += "A=M-1\n"#no need to change stack pointer
			acode += "M=-M\n" 
		elif command == "eq" : 
			acode += "@SP\n"
			acode += "AM=M-1\n" #move up stack pointer, save the address to A register.
			acode += "D=M\n" # get b
			acode += "A=A-1\n" #address of a
			acode += "D=M-D\n" #a-b
			acode += "M=0\n" #assume false
			acode += "@test"+ str(self.labelcounter) +"\n"
			acode += "D;JEQ\n"
			acode += "@continue"+ str(self.labelcounter) +"\n"
			acode += "0;JMP\n"
			acode += "(test" +  str(self.labelcounter) +")\n"
			acode += "@SP\n"
			acode += "A=M-1\n" #address of a
			acode += "M=-1\n"
			acode += "(continue"+ str(self.labelcounter) +")\n"
			self.labelcounter += 1
		elif command == "gt" : 
			acode += "@SP\n"
			acode += "AM=M-1\n" #move up stack pointer
			acode += "D=M\n"
			acode += "A=A-1\n" #address of a
			acode += "D=M-D\n" #a-b
			acode += "M=0\n" #assume false
			acode += "@test"+ str(self.labelcounter) +"\n"
			acode += "D;JGT\n"
			acode += "@continue"+ str(self.labelcounter) +"\n"
			acode += "0;JMP\n"
			acode += "(test" +  str(self.labelcounter) +")\n"
			acode += "@SP\n"
			acode += "A=M-1\n" #address of a
			acode += "M=-1\n"
			acode += "(continue"+ str(self.labelcounter) +")\n"
			self.labelcounter += 1
		elif command == "lt" : 
			acode += "@SP\n"
			acode += "AM=M-1\n" #move up stack pointer
			acode += "D=M\n"
			acode += "A=A-1\n" #address of a
			acode += "D=M-D\n" #a-b
			acode += "M=0\n" #assume false
			acode += "@test"+ str(self.labelcounter) +"\n"
			acode += "D;JLT\n"
			acode += "@continue"+ str(self.labelcounter) +"\n"
			acode += "0;JMP\n"
			acode += "(test" + str(self.labelcounter) +")\n"
			acode += "@SP\n"
			acode += "A=M-1\n" #address of a
			acode += "M=-1\n"
			acode += "(continue"+ str(self.labelcounter) +")\n"
			self.labelcounter += 1
		elif command == "and" : 
			acode += "@SP\n"
			acode += "AM=M-1\n" #move up stack pointer
			acode += "D=M\n"
			acode += "A=A-1\n" #address of a
			acode += "M=D&M\n"
		elif command == "or" : 
			acode += "@SP\n"
			acode += "AM=M-1\n" #move up stack pointer
			acode += "D=M\n"
			acode += "A=A-1\n" #address of a
			acode += "M=D|M\n"
		elif command == "not" : 
			acode += "@SP\n"
			acode += "A=M-1\n" #address of b
			acode += "M=!M\n"

		self.outputf.write(acode)

	def writePushPop(self, command, segment, index):
		acode = ""
		pushcode = ""
		popcode = ""
		#pop code save the memory address to D
		#push code save the memory content to D
		if segment == "constant":
			pushcode += "@"+index+"\n"
			pushcode += "D=A\n"
		elif segment == "local":
			popcode += "@"+index+"\n"
			popcode += "D=A\n"
			popcode += "@LCL\n"
			popcode += "AD=M+D\n" #find the address of memeory
			pushcode += popcode
			pushcode += "D=M\n" #save the content into D register
		elif segment == "argument":
			popcode += "@"+index+"\n"
			popcode += "D=A\n"
			popcode += "@ARG\n"
			popcode += "AD=M+D\n" #find the address of memeory
			pushcode += popcode
			pushcode += "D=M\n" #save the content into D register
		elif segment == "this":
			popcode += "@"+index+"\n"
			popcode += "D=A\n"
			popcode += "@THIS\n"
			popcode += "AD=M+D\n" #find the address of memeory
			pushcode += popcode
			pushcode += "D=M\n" #save the content into D register
		elif segment == "that":
			popcode += "@"+index+"\n"
			popcode += "D=A\n"
			popcode += "@THAT\n"
			popcode += "AD=M+D\n" #find the address of memeory
			pushcode += popcode
			pushcode += "D=M\n" #save the content into D register
		elif segment == "static":
			popcode += "@"+ self.name + "." + index +"\n"
			popcode += "D=A\n"
			pushcode += popcode
			pushcode += "D=M\n" #save the content into D register
		elif segment == "temp":
			popcode += "@"+str(int(index)+5)+"\n"
			popcode += "D=A\n"
			pushcode += popcode
			pushcode += "D=M\n" #save the content into D register
		elif segment == "pointer":
			if index == "0" : 
				popcode += "@THIS\n"
				popcode += "D=A\n"
				pushcode += popcode
				pushcode += "D=M\n" #save the content into D register
			else:
				popcode += "@THAT\n"
				popcode += "D=A\n"
				pushcode += popcode
				pushcode += "D=M\n" #save the content into D register

		if command == C_PUSH:
				acode += pushcode # save memory content to D
				acode += "@SP\n"
				acode += "A=M\n" # save stack address to register A
				acode += "M=D\n"
				acode += "@SP\n"
				acode += "M=M+1\n"
		elif command == C_POP : 
				acode += popcode # save memory address to D
				acode += "@R5\n" # tempo location
				acode += "M=D\n" # save the address
				acode += "@SP\n"
				acode += "AM=M-1\n" #decrease the stack pointer
				acode += "D=M\n" #content of top stack
				acode += "@R5\n"
				acode += "A=M\n"
				acode += "M=D\n"

		self.outputf.write(acode)
		
	def Close(self):
		self.outputf.close()

if __name__ == "__main__":
   main(sys.argv[1])

