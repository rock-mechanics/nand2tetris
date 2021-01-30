import sys
import re

# initalize some constants for the command type
C_ARITHMETIC="C_ARITHMETIC"
C_PUSH="C_PUSH"
C_POP="C_POP"
C_LABLE="C_LABLE"
C_GOTO="C_GOTO"
C_IF="C_IF"
C_FUNCTION="C_FUNCTION"
C_RETURN="C_RETURN"
C_CALL="C_CALL"

def main(vm_name) : 
	ass_name =vm_name.replace(".vm", ".asm")

	#initialize parser and code writer.
	par = Parser(vm_name)
	while True:
		if par.hasMoreCommands() : 
			par.advance()
			print(par.commandType() + " : " + par.currentcommand)
			print("arg 1 : " + par.arg1())
			print("arg 2 : " + str(par.arg2()))
		else:
			break


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
		self.outputf =open(fname, 'r')
		self.outputf =open(fname, 'a')
	
	def writeArithmetic(command):
		acode =""
		if command == "add" :
			acode += "@SP\n"
			acode += "M=M-1\n"
			acode += "A=M\n"
			acode += "D=M\n"
			acode += "A=A-1\n"
			acode += "D=D+M\n"
			acode += "@SP\n"
			acode += "A=M-1\n"
			acode += "M=D\n"
		elif command == "sub" :
			acode += "@SP\n"
			acode += "M=M-1\n"
			acode += "A=M\n"
			acode += "D=-M\n" #only difference with add
			acode += "A=A-1\n"
			acode += "D=D+M\n"
			acode += "@SP\n"
			acode += "A=M-1\n"
			acode += "M=D\n"
		elif command == "neg":
			acode += "@SP\n"
			acode += "A=M-1\n"#no need to change stack pointer
			acode += "M=-M\n" 
		else:

if __name__ == "__main__":
   main(sys.argv[1])

