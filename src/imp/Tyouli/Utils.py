# vr24w32a

backspace = "\b \b"

def printf(*args, **kwargs):
	print(*args, **kwargs, end='')

def print_obj(target, format=False, indent="  ", __level__=0):
	current_indent = indent * __level__
	next_indent = current_indent + indent
	
	def printf_level_0(*args, **kwargs):
		nonlocal __level__
		if __level__ == 0:
			printf(*args, **kwargs)
	
	def printf_format(*args, **kwargs):
		nonlocal format
		if format:
			printf(*args, **kwargs)
	
	if hasattr(target, "__name__"):
		printf(target.__name__)
	printf('{')
	for k, v in target.__dict__.items():
		printf_format('\n' + next_indent)
		printf(f"{k}: ")
		if hasattr(v, "__dict__"):
			print_obj(v, format, indent, __level__ = __level__ + 1)
		else:
			printf(v)
		printf(", ")
	
	if len(target.__dict__) > 0:
		printf(backspace * 2)
	printf_format('\n' + current_indent)
	printf('}')
	printf_level_0('\n')

def add_to_dict(dict, **kwargs):
	if dict is None:
		dict = {}
	dict.update(kwargs)
	return dict

# Test of this function at Programing.Proj. TyBfCompiler
def compile_func(func_src, func_name, globals=None, locals=None):
	rslt_dict = {}
	rslt_dict.update(globals)
	exec(func_src, rslt_dict, locals)
	return rslt_dict[func_name]

