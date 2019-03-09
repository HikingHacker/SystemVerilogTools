# Overview
Accelerates the development of SystemVerilog modules by automating the testbench, runlab and wave file development workflow. This script was developed with the Unversity of Washington curriculum in mind but can be used for most SystemVerilog files.

![alt text](https://i.imgur.com/ciBfiUf.png)

# Guidelines
Sytnax: These scripts make some assumptions about synax of module declarations. Will work on other styles but the below is recommend for the best experience. Other styles could require minimal editing of generated files to work or completely fail. 

```verilog
  module NAME(PORT, PORT, PORT, .... ); 
    output logic [6:0] PORT, ....;
    input logic [3:0] PORT;
    input logic [9:0] PORT;
    tri logic [9:0] Port;
    .
    .
    .
  endmodule 
```

# Notes
1. The script currently has strict 1 module per file requirement. Each MODULE_NAME must exist in a file called MODULE_NAME.sv for the testbench and .do file creation to work properly. Testbenches must be named MODULE_NAME_testbench() for proper dection and runlab execution.
2. Will only append testbenches or create files if they do not exist already. This was enforced to not override user changes to files and stop duplicates on multiple executions of the script.  

# How to use:
1. open terminal and run "git clone https://github.com/HalfDressed/VerilogScripts.git"
2. Move the script into the directory with .sv files you want to run it on.
3. Run the script:

```sh
Terminal:
1. mv ./AccelerateSystemVerilogTesting [working directory]
2. python ./AccelerateSystemVerilogTesting [file1] [file2] .. (if no parameters given runs on *.sv files in directory)
```
  
```sh
1. Executible (most UW computers don't have python easily accessible through terminal):
2. Move file to working directory.
3. Right click script -> open with - > python (usually located in the install directory of Spyder at C:\ProgramData\Anaconda3\python.exe)
```
