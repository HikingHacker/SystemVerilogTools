Accelerates the development of SystemVerilog modules by automating the testbench, runlab and wave file development workflow. This script was developed with the Unversity of Washington curriculum in mind but can be used for most SystemVerilog files.

![alt text](https://i.imgur.com/ciBfiUf.png)

NOTE: Will only append testbenches or create files if they do not exist already. This was enforced to not override user changes to files and stop duplicates on multiple executions of the script.  

How to use:
1. Terminal: python ./AccelerateSystemVerilogTesting [file1] [file2] .. (if no files listed runs *.sv files)
2. Run as: Most UW computers do not have python easily available through terminal so must Right click script -> open with - > python (usually located in the install directory of Spyder at C:\ProgramData\Anaconda3\python.exe)
