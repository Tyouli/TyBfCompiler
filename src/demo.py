# 240805 St.
# vr24w32c

import os
from functools import wraps

import imp.Tyouli.TyBfCompiler as TyBfCompiler

def print_test_info(func):
	@wraps(func)
	def decorated(*args, **kwargs):
		nonlocal func
		sepline_half = '-' * 20
		print(f"{sepline_half} {func.__name__} {sepline_half}")
		return func(*args, **kwargs)
	
	return decorated

@print_test_info
def tst_basic_1():
	tstfunc = TyBfCompiler.src2func("+++.[-].")
	print("Expected output: (3, 0)")
	print(tstfunc())
	print()

@print_test_info
def tst_add_3digits():
	print("Testing add_3digits...")
	#add_3digits_src = "#e[-]>[-]>[-]>[-]>[-]>#d4[-]>,>,>,>,>,>,>#A[-]->[-]+>[-]>[-]>[-]<<<<"\
	#"[[+]>[[<+>>+<-]>[<+>-]<[<-[<+>-]]<[-<<<<<<<+[->>>>+[<<<<+<+>>>>>-]<<<<<[>>>>>+<<<<<-]+>[<->[-]]"\
	#"<]>>>>>>>>>>>>>+[<+>-[>>]<]<<-]>]>+[>+<-[<<]>]>+[<+>>>+<-]>-[<+>-]<<---]<<<<<<<.>.>.>."
	#add_3digits_printable = TyBfCompiler.src2printable(add_3digits_src)
	#print(add_3digits_printable)
	def get_add_3digits_src():
		f_init = "e[-]>d[-]>c[-]>b[-]>a[-]>d4[-]>d3,>d2,>d1,>d3',>d2',>d1',>A[-]->pd[-]+>B[-]>ph1[-]>ph2[-]<<<<%!"
		f_incr = """[
			->>>>+
			[<<<<+<+>>>>>-]
			<<<<<
			[>>>>>+<<<<<-]
			+>[<->[-]]<
		]"""
		f_movDigit = f"""[
			[<A+>>B+<pd-]>[<pd+>B-]<
			[<-[<+>-]]<
			[
				-<<<<<<<+
				{f_incr}%!
				>>>>>>>>>>>>>(13)+[<+>-[>>]<]at B<<A-
			]>
		]"""
		f_incrDigit = """
			>+[>+<-[<<]>]at A
			>pd+[<A+>>B+<pd-]>B-[<pd+>B-]<<A---(3)
		"""
		f_main = f"""
			{f_init}
			[
				[A+]>
				{f_movDigit}
				{f_incrDigit}
			]
			<<<<<<<d4.>d3.>d2.>d1.!
		"""
		return f_main
	
	add_3digits_src = get_add_3digits_src()
	add_3digits_printable = TyBfCompiler.src2printable(add_3digits_src)
	#print(add_3digits_printable)
	add_3digits = TyBfCompiler.printable2func(add_3digits_printable)
	for input in (
		(0, 0, 1, 0, 0, 1),
		(1, 5, 24, 2, 7, 2)
	):
		print(f"{input} --add_3digits-> ", end="")
		print(f"{add_3digits(*input)}")

_tst_add_params_1 = (
	(23, 47),
	(127, 98)
)
def _print_tst_add_rslt(add_func, tst_params=None):
	if tst_params is None:
		tst_params = _tst_add_params_1
	
	for input in tst_params:
		print(f"{input} --add-> {add_func(*input)}; {input[0]} + {input[1]} = {input[0] + input[1]}")

simpadd_src = ",>,[<+>-]<."
@print_test_info
def tst_add():
	simpadd_printable = TyBfCompiler.src2printable(simpadd_src)
	print(f"{simpadd_printable = }")
	simpadd = TyBfCompiler.printable2func(simpadd_printable)
	
	_print_tst_add_rslt(simpadd)

_tst_compile_params = lambda:...
def _decorate_tst_compile_params(self):
	#self.bfs_folder_path = "../resource/Brainfuck Source Files"
	self.bfs_folder_path = ""
	self.target_name = "add"
	self.target_file_path = os.path.join(self.bfs_folder_path, f"{self.target_name}.bfs")
	self.target_module_path = TyBfCompiler._file_path2module_path(self.target_file_path)
	return self
_tst_compile_params = _decorate_tst_compile_params(_tst_compile_params)

@print_test_info
def tst_compile(params=None):
	if params is None:
		params = _tst_compile_params
	TyBfCompiler.bfs2module(params.target_module_path)

@print_test_info
def tst_load_module(params=None):
	if params is None:
		params = _tst_compile_params
	simpadd = TyBfCompiler.module2func(params.target_module_path)
	_print_tst_add_rslt(simpadd)

def main():
	tst_basic_1()
	tst_add()
	tst_compile()
	tst_load_module()


if __name__ == "__main__":
	main()
