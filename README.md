# TyBfCompiler - A Brainfuck Compiler

## Synopsis
TyBfCompiler is a brainfuck compiler implementation in python. It can compile brainfuck source strings into python functions and brainfuck source files into python modules

## Examples
Compile from string:
```python
from imp.Tyouli import TyBfCompiler

simple_add = TyBfCompiler.compile_src2func(",>,[<+>-]<.")
print(simple_add(25, 47))    # >>> 72
```

Compile from brainfuck source file:
```python
from imp.Tyouli import TyBfCompiler

# Compile into module
# Assuming that the target file already exists
TyBfCompiler.compile_file2module("./bf/simple_add.bfs") 

# Load from module
simple_add = TyBfCompiler.load_module2func("bf.simple_add")

# Run the function
print(simple_add(43, 70))    # >>> 113
```

## How to use
### Setup
* Download the .zip from [Releases](https://github.com/Tyouli/TyBfCompiler/releases)
* Unpack the .zip into your project folder
* import the module. For example:
```python
from imp.Tyouli import TyBfCompiler
```
### Functions
* `compile_src2printable`
* `compile_printable2func`
* `compile_src2func`: Compile brainfuck source string into python function
* `compile_file2module`: Compile brainfuck source file into python module
* `load_module2func`: Load compiled TyBf module into python function
* You can also `TyBfCompiler.py` to directly compile brainfuck source files:
```shell
.\TyBfCompiler.py your_dir_path\your_bfs_file
```

## Notes
* This is a project **just for fun**;
* The stack length is set to 128, which can be changed by changing the value of var `CACHE_SIZE` at class `BfRuntime` in file `TyBfCompiler.py`. Note that the actual stack size equals to  `CACHE_SIZE + 1`;
* The value range for a stack slot is $[0, 255]$, which can be changed by changing the value of var `SLOT_MAXV` at class `BfRuntime` in file `TyBfCompiler.py`;
* If you want to change `CACHE_SIZE` and `SLOT_MAXV`, note that the value of them need to be $2^n - 1, n ∈ N^*$. 
