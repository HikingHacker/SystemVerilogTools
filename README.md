# Overview
These scripts accelerate the development of SystemVerilog modules by automating a majority of the testbench, runlab and wave file development workflow. This script was developed with the Unversity of Washington curriculum (DE1_SoC FPGA Board & ModelSim) in mind but is compatible with any SystemVerilog files that follow the guidelines.

# Guidelines
1. These scripts make strict* assumptions about syntax of module declartions and their file structure. Currently, they have a strict 1 module per file requirement. Each MODULE_NAME module must exist in a file called MODULE_NAME.sv for correct testbench and .do file creation. All manual created testbenches must be named MODULE_NAME_testbench() for correct detection and runlab creation. 

```verilog
  // Suggested Syntax for module and port declartion:
  module NAME (PORT, PORT, PORT, .... ); 
    input logic [3:0] PORT;
    inout logic [9:0] PORT;
    output logic [6:0] PORT, ....;
    .
    . // logic
    .
  endmodule
 
  // Suggested Syntax for module instantiation:
  module NAME (.PORT1(PORTA), .PORT2(PORTB), .... ); 
  
```
2. Only appends testbenches or create .do files if they do not exist already. This was enforced to prevent overriding user changes to files and stop duplicates on multiple executions of the script. If you would like to use the scripts to generate these files please delete the testbench code and do files. 

# How to use:
1. Open Git Bash or Terminal and run "git clone https://github.com/HalfDressed/VerilogScripts.git"
2. Copy the AccelerateSystemVerilogTesting.py script into the directory with .sv files you want to run it on.
3. Run the script using one of the methods below.

```sh
Executible (most UW computers don't have python easily accessible through terminal):
1. Right click script -> open with - > python.exe (usually located in the install directory of Spyder at C:\ProgramData\Anaconda3\)
2. Launch script (will run on every .sv in directory)
```

```sh
Terminal:
1. python ./AccelerateSystemVerilogTesting [file1] [file2] .. (if no parameters given runs on *.sv files in directory)
```

# Example
Directory Prescript:
![alt text](https://i.imgur.com/rSe1bnu.png)

Script Execution:
![alt text](https://i.imgur.com/ECqw6vf.png)

Directory Postscript:
![alt text](https://i.imgur.com/3jQQS84.png)

Example testbench:
![alt text](https://i.imgur.com/e2H4vGM.png)

Example runlab:
![alt text](https://i.imgur.com/OV75BoJ.png)

# TODO list
1. Add automatic variable popluation to wave.do file
2. Improve automated testbench creation for other syntax styles (universality)
3. Allow users to specify files through python script like available through terminal
4. Add more common modelsim install directories to Launch_Modelsim.bat
5. Add config file

