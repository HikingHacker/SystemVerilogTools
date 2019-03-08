# Overview
Accelerates the development of SystemVerilog modules by automating the testbench, runlab and wave file development workflow. This script was developed with the Unversity of Washington curriculum in mind but can be used for most SystemVerilog files.

![alt text](https://i.imgur.com/ciBfiUf.png)

# Guidelines
Sytnax: These scripts make some assumptions about synax of module declarations. Will work on others but the below is reccomended
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

NOTE: Will only append testbenches or create files if they do not exist already. This was enforced to not override user changes to files and stop duplicates on multiple executions of the script.  


# How to use:
1. open terminal and run "git clone https://github.com/HalfDressed/VerilogScripts.git"
2. Move the script into the directory with .sv files you want to run it on.
3. Run the script:

  Terminal: python ./AccelerateSystemVerilogTesting [file1] [file2] .. (if no files listed runs *.sv files)
  
  Executible: Most UW computers do not have python easily available through terminal so must Right click script -> open with - > python (usually located in the install directory of Spyder at C:\ProgramData\Anaconda3\python.exe)
