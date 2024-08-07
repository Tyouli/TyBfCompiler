# 240805 St.
# vr24w32b

import os
from queue import Queue
from py_compile import compile as compile_py

if __name__ == "__main__":
	from Utils import compile_func
else:
	from .Utils import compile_func

INNER_FUNC_NAME = "bf_func"
INNER_FUNC_RUNTIME_PARAM_NAME = "__runtime_cls__"
MODULE_DEFAULT_PREFIX = "TyBfModule_"

class BfRuntime:
	CACHE_SIZE = 127		# Needs to be 2 ** n - 1, n ∈ N; actural size = CACHE_SIZE + 1
	SLOT_MAXV = 255		# Needs to be 2 ** n - 1, n ∈ N
	
	def __init__(self, *args):
		self.cache = [0] * (self.CACHE_SIZE + 1)
		self.ptr = 0
		self.params = Queue()
		for arg in args:
			self.params.put(arg)
		self.output_lst = []
	
	def add(self, v=1):
		self.cache[self.ptr] += v
		self.cache[self.ptr] &= self.SLOT_MAXV
		return self
	
	def sub(self, v=1):
		return self.add(-v)
	
	def movr(self, rpt=1):
		self.ptr += rpt
		self.ptr &= self.CACHE_SIZE
		return self
	
	def movl(self, rpt=1):
		return self.movr(-rpt)
	
	def get_crtv(self):
		return self.cache[self.ptr]
	
	def input(self):
		self.cache[self.ptr] = self.params.get()
		#print(f"input: cache[{self.ptr}]:={self.cache[self.ptr]}")
		return self
	
	def output(self):
		self.output_lst.append(self.get_crtv())
		return self
	
	def get_output(self):
		return tuple(self.output_lst)
	
	def print_cache(self):
		print(self.cache)
		return self

def _post_decoration(func):
	func.__kwdefaults__.update({INNER_FUNC_RUNTIME_PARAM_NAME:BfRuntime})
	return func

def compile_src2printable(src:str):
	crt_indent = 0
	ptr = 0
	crtc = src[ptr]
	INDENT = "    "
	
	def add_line(line:str):
		nonlocal rslt_func_str
		rslt_func_str += INDENT * crt_indent + line + '\n'
	
	rslt_func_str = ""
	add_line(f"def {INNER_FUNC_NAME}(*args, {INNER_FUNC_RUNTIME_PARAM_NAME}=None):")
	crt_indent += 1
	add_line(f"if {INNER_FUNC_RUNTIME_PARAM_NAME} is None:")
	add_line(f"\t{INNER_FUNC_RUNTIME_PARAM_NAME} = BfRuntime")
	add_line(f"_ = {INNER_FUNC_RUNTIME_PARAM_NAME}(*args)")
	
	
	def get_next_char():
		nonlocal ptr
		ptr += 1
		if ptr >= len(src):
			return None
		return src[ptr]
	
	while ptr < len(src):
		if crtc in "+-<>":
			# Get target_char and target_char_number
			targetc = crtc
			targetcn = 1
			crtc = get_next_char()
			while crtc == targetc:
				targetcn += 1
				crtc = get_next_char()
			
			# Apply targetc and targetcn
			method_to_call = None
			if targetc == '+':
				method_to_call = "add"
			elif targetc == '-':
				method_to_call = "sub"
			elif targetc == '<':
				method_to_call = "movl"
			elif targetc == '>':
				method_to_call = "movr"
			add_line(f"_.{method_to_call}({targetcn})")
			continue
		
		if crtc == ',':
			add_line(f"_.input()")
		elif crtc == '.':
			add_line(f"_.output()")
		elif crtc == '!':
			add_line(f"_.print_cache()")
		elif crtc == '%':
			# Single char comment
			get_next_char()
		elif crtc == '#':
			# Multichar comment
			while crtc != '#':
				crtc = get_next_char()
		elif crtc == '[':
			add_line(f"while _.get_crtv() != 0:")
			crt_indent += 1
		elif crtc == ']':
			crt_indent -= 1
		
		crtc = get_next_char()
	
	add_line("return _.get_output()")
	
	#print(rslt_func_str)
	return rslt_func_str

def compile_printable2func(printable:str):
	return _post_decoration(compile_func(printable, INNER_FUNC_NAME, {"BfRuntime": BfRuntime}))

def compile_src2func(src:str):
	return compile_printable2func(compile_src2printable(src))

def compile_file2module(src_file_path:str):
	src_file_path_split = os.path.splitext(src_file_path)[0]	# Remove the suffix
	src_file_path_split = os.path.split(src_file_path_split)	# Result: (dir, file_name)
	temp_py_src_file_path = os.path.join(src_file_path_split[0], f"{MODULE_DEFAULT_PREFIX}{src_file_path_split[1]}.py")
	if os.path.exists(temp_py_src_file_path):
		user_choice = input(f"The temp file {temp_py_src_file_path} already exists and will be replaced. Do you want to continue? (y/n)")
		if user_choice != 'y':
			return
	
	src = None
	with open(src_file_path, 'r') as file:
		src = file.read()
	
	with open(temp_py_src_file_path, 'w') as file:
		file.write(compile_src2printable(src))
	
	target_pyc_file_path = f"{temp_py_src_file_path}c"
	compile_py(temp_py_src_file_path, cfile=target_pyc_file_path)
	
	os.remove(temp_py_src_file_path)

def load_module2func(module_path:str):
	# split module_dir and module_name
	module_dir = ""
	module_name = None
	if module_path.find('.') == -1:
		module_name = module_path
	else:
		module_dir, module_name = module_path.rsplit(sep='.', maxsplit=1)
		module_dir += "."
	
	_globals = {}
	exec(f"from {module_dir}{MODULE_DEFAULT_PREFIX}{module_name} import {INNER_FUNC_NAME}", _globals)
	return _post_decoration(_globals[INNER_FUNC_NAME])
	

def main():
	from sys import argv
	
	USAGE_TIP = "Usage:"\
						"\t.\\TyBfCompiler.py [|the Brainfuck source file you want to compile|]"
	try:
		compile_file2module(argv[1])
	#except FileNotFoundError:
		#just raise it
	except IndexError:
		print(USAGE_TIP)

if __name__ == "__main__":
	main()

