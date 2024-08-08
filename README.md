# TyBfCompiler - A Brainfuck Compiler

## Synopsis
TyBfCompiler is a brainfuck compiler implementation in python. It can compile brainfuck source strings/files into python functions/modules, and something more. Details at [How to use -> Functions](#functions)

<br><br>

## How to use
### Functions
After [Setup](#setup), you can use these functions in your own project
* `printable2func`
* `printable2module`
* `module2func`
* `src2printable`
* `src2func`
* `src2module`
* `bfs2src`
* `bfs2printable`
* `bfs2func`
* `bfs2module`

where the references are as below:
| token in function name | refers to |
| :----: | :----: |
| src | raw brainfuck source string |
| bfs | brainfuck source file |
| printable | executable python codes generated from raw brainfuck source string |
| func | executable python function |
| module | compiled TyBf python module |
* You can also `TyBfCompiler.py` to directly compile brainfuck source files into TyBf python modules:
```shell
.\TyBfCompiler.py your_dir_path\your_bfs_file
```
### Setup
* Download the .zip from [Releases](https://github.com/Tyouli/TyBfCompiler/releases)
* Unpack the .zip into your project folder
* Import the module into your project. For example:
```python
from imp.Tyouli import TyBfCompiler
```

<br><br>

## Notes
* This is a project **just for fun**; it is poorly optimized.
### Runtime
* The stack length is set to 128, which can be changed by changing the value of var `CACHE_SIZE` at class `BfRuntime` in file `TyBfCompiler.py`. Note that the actual stack size equals to  `CACHE_SIZE + 1`;
* The value range for a stack slot is $[0, 255]$, which can be changed by changing the value of var `SLOT_MAXV` at class `BfRuntime` in file `TyBfCompiler.py`;
* If you want to change `CACHE_SIZE` and `SLOT_MAXV`, note that the value of them need to be $2^n - 1, n ∈ N^*$;

### Usage
* This project is mainly Procedure Oriented, so you may use the functions like `TyBfCompiler.src2module(",>,[<+>-]<.")` rather than something like `BfSrc(",>,[<+>-]<.").to_TyBfModule()`;
* The functions takes in module_path(like `imp.BfModules.simple_add`) by default. You can use relative module_paths like `...another_proj.src.BfModules.simple_add` free of the limitations in module importing in python (For example, `ImportError: attempted relative import with no known parent package`);
```python
simple_add = TyBfCompiler.bfs2func("imp.BfModules.simple_add")
```
* The module_path would be translated into file_path(like `./imp/Tyouli/simple_add.bfs`) in the functions;
```python
TyBfCompiler.src2module(",>,[<+>-]<.", "imp.BfModules.simple_add")
# The generated module will be at ./imp/BfModules/simple_add (.imp/BfModules/simple_add.pyc)
```
* If you are transforming a brainfuck source file into other types of data, the file_path would be added a default suffix `.bfs`;
```python
simple_add_src = TyBfCompiler.bfs2src("imp.BfModules.simple_add")
# This function will read the content of file ./imp/BfModules/simple_add.bfs
```
* If you want to use other suffix, change the value of `TyBfCompiler.bfs_file_suffix`;
```python
TyBfCompiler.bfs_file_suffix = ".bf"
simple_add_src = TyBfCompiler.bfs2src("imp.BfModules.simple_add")
# This function now will read the content of file ./imp/BfModules/simple_add.bf
```
* If you want to use file_path instead of module_path, use `use_file_path(your_file_path)`. Note that this will change the value of `TyBfCompiler.bfs_file_suffix`;
```python
simple_add_src = TyBfCompiler.bfs2src(use_file_path("./imp/BfModules/simple_add.bf"))
# This will read the content of file ./imp/BfModules/simple_add.bf
simple_mul_src = TyBfCompiler.bfs2src("...basic-bf-modules.simple_mul")
# This will read the content of file .../basic-bf-modules/simple_mul.bf, instead of .../basic-bf-modules/simple_mul.bfs
```
* If you want to reset the suffix, use `reset_bfs_file_suffix()`
```python
simple_add_src = TyBfCompiler.bfs2src(use_file_path("./imp/BfModules/simple_add.bf"))
# This will read ./imp/BfModules/simple_add.bf
TyBfCompiler.reset_bfs_file_suffix()
simple_add_2_src = TyBfCompiler.bfs2src("...basic-bf-modules.simple_mul")
# This now will read .../basic-bf-modules/simple_mul.bfs
```
* The generated TyBf python modules may not be directly imported and used, instead they needs to be loaded using `TyBfCompiler.module2func()`
```python
simple_add = TyBfCompiler.module2func("imp.BfModules.simple_add")
# This loads module imp.BfModules.TyBfModule_simple_add into function simple_add; "TyBfModule_" is a default prefix for generated TyBf python modules.
```
* But actually you can directly use .bfs files as modules
```python
from imp.Tyouli import TyBfCompiler
simple_add = TyBfCompiler.bfs2func("imp.BfModules.simple_add")
# This loads ./imp/BfModules/simple_add.bfs into function simple_add
print(simple_add(92, 47))    # >>> 139
```
