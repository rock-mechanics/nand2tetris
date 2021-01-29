import sys
import re

#main takes in assembly code file
#output the binary code file named xxx.hack

def main(acode) : 
	fname = acode.replace(".asm", ".hack")
	#rewrite the output file
	outf = open(fname, 'w')
	outf = open(fname, 'a')

	#initialize symbol table, parser, variable table, translator.
	table = symbol_table()
	par = parser()
	vtable = table.pvarmap
	trans =translator()

	#first walk through
	#record all the labels.
	with open(acode, 'r') as f:
		lines = f.readlines()
		linecounter = -1
		for line in lines:
			if parser.is_command(line):
				linecounter+= 1
			elif parser.is_label(line):
				label = par.parse_label(line)
				vtable[label] = linecounter + 1

	with open(acode, 'r') as f:
		lines= f.readlines()
		for line in lines:
			#ignore non commands
			if parser.is_command(line):
				if parser.is_a_instruction(line):
					print(line.strip() + " is a instruction")
					instruction = par.parse_a_instruction(line.strip())
					print("parsed instruction : " + instruction)
					bcode = trans.translate_a_instruction(instruction, vtable)
					outf.write("0" + bcode + "\n")
				else:
					print(line.strip() + " is c instruction\n")
					dest = par.parse_dest(line)
					opts = par.parse_opts(line)
					jump = par.parse_jump(line)
					bcode="111"
					bcode += trans.translate_c_cmps(opts, table)
					bcode += trans.translate_c_dest(dest, table)
					bcode += trans.translate_c_jump(jump, table)
					outf.write(bcode + "\n")
	outf.close()

class parser():

	def is_label(line):
		if not line.strip():
			return False
		elif line.strip()[0]!="(":
			return False
		else:
			return True

	def is_command(line):
		if not line.strip():
			return False
		elif line.strip()[0:2]=="//":
			return False
		elif line.strip()[0]=="(":
			return False
		else:
			return True

	def is_a_instruction(line):
		if line.strip()[0] == "@" : 
			return True 
		else:
			return False

	def parse_label(self, line):
		return line.strip()[1:-1]

	def parse_a_instruction(self, line):
		parts = line[1:].split("//")
		parts = [ x.strip() for x in parts ]
		return parts[0]

	def parse_dest(self,line):
		parts = line.split("//")
		parts = parts[0].split("=")
		if len(parts) == 1 : 
			return "null"
		else:
			return parts[0].strip()

	def parse_opts(self,line):
		parts = line.split("//")
		parts = parts[0].split(";")
		parts = parts[0].split("=")
		if len(parts) == 1 : 
			return parts[0].strip()
		else:
			return parts[1].strip()

	def parse_jump(self,line):
		parts = line.split("//")
		parts = parts[0].split(";")
		if len(parts) == 1 : 
			return "null"
		else:
			return parts[1].strip()

class translator(): 

	def __init__(self):
		#variable memory address starts from 16
		self.variable_counter = 16

	def translate_a_instruction(self, part,vtable):
		if part in vtable:
			return format(int(vtable[part]), 'b').zfill(15) 
		elif not part.isnumeric():
			# it is confirmed not in vtable
			vtable[part] = self.variable_counter
			self.variable_counter += 1
			return format(int(vtable[part]), 'b').zfill(15)
		else:
			return format(int(part), 'b').zfill(15) 

	def translate_c_dest(self, part,table):
		if part in table.destmap:
			return table.destmap[part]
		else:
			print(part+" is not found")
			return False
	def translate_c_cmps(self, part,table):
		if part in table.optsmap:
			return table.optsmap[part]
		else:
			print(part+" is not found")
			return False
	def translate_c_jump(self, part,table):
		if part in table.jumpmap:
			return table.jumpmap[part]
		else:
			print(part+" is not found")
			return False

class symbol_table() : 
	def __init__(self):
		self.destmap = self.load_db("destmap.db")
		self.optsmap = self.load_db("optsmap.db")
		self.jumpmap = self.load_db("jumpmap.db")
		self.pvarmap = self.load_db("pvarmap.db")
	
	# turn a f to dictonary for inital setup.
	def load_db(self,filename):
		mapsdict = {}
		with open(filename, 'r') as f:
			lines= f.readlines()
			for line in lines:
				if line : 
					data = line.split(",")
					mapsdict[data[0].strip()] = data[1].strip()
		return mapsdict

if __name__ == "__main__":
   main(sys.argv[1])

