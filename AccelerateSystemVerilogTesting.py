#!/usr/bin/env python

import re
import sys
import glob
import os.path

# Accelerates the development of SystemVerilog modules by automating
# the testbench, runlab and wave file development workflow.

# Please help grow this project by contributing to to github at:
# https://github.com/HalfDressed/VerilogScripts


__author__ = "Allen Putich"
__copyright__ = "Copyright 2019"
__credits__ = ["Allen Putich", "Scott Hauck"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Allen Putich"
__email__ = "allen.putich@gmail.com"
__status__ = "BETA"

debug = 0;

def debugPrint(obj):
    if debug:
        print(str(obj))


def getFileNameWithoutExtension(filename):
    return re.match("^([^.]+)", filename).group()


def getModuleDeclarations(filename):
    modules = []
    with open(filename, 'r') as f:
        for line in f:
            if 'module' in line:
                words = line.split()
                for index in range(len(words)):
                    if 'module' and not 'endmodule' in words[index]:
                        module_name = words[index + 1]
                        modules.append(re.sub('[();;]', '', module_name))
                        break
    return list(set(modules))


parameterTestbenchConversion =	{
  "input": "",
  "output": "",
  "inout logic": "tri"
}


# Returns ports for FIRST module declared in file. Requires following format for correct processing.

# module name (port1, port2...portn);
# input/output/inout .....
# endmoule

# TODO: correct sytnax so end of line character is proper. possibliy replace commas with ; if necessary.
def getModulePorts(filename):
    parameters = []
    with open(filename, 'r') as f:
        for line in f:
            if 'input' in line:
                parameters.append((re.sub('input', '', line)).strip('\n'))
            if 'output' in line:
                parameters.append((re.sub('output', '', line)).strip('\n'))
            if 'inout' in line:
                parameters.append((re.sub('inout logic', 'tri', line)).strip('\n'))
            if 'endmodule' in line:
                break
    return list(set(parameters))


# TODO: Returns ports for specific module in file with legal SystemVerilog Syntax.
def getSpecificModulePorts(filename, module):
    print("getModuleParameters_fancy")
    parameters = []
    parameter = ""
    f = open(filename, 'r')
    lines = f.readlines()
    for line_number in range(len(lines)):
        print("getModuleParameters_fancy")


# Returns all submodules used in file that are declared in current directory
def getModuleExplictSubmodules(filename, module_list):
    submodules = []
    with open(filename, 'r') as file:
        for line in file:
            for word in line.split():
                if word in module_list:
                    submodules.append(word)
    return list(set(submodules))


# TODO: Recursively get all required submodules. Currently breaks at depth of 3.
# Returns all submodules and their submodules used in file that are declared in current directory
def getModuleImplictSubmodules(filename):
    all_submodules = []
    module_dictonary = createModuleDictionary()
    submodules = module_dictonary[getFileNameWithoutExtension(filename)]
    for module in submodules:
        for m in module_dictonary[module]:
            all_submodules.append(m)
    return list(set(all_submodules))


# Returns all names of modules in current directory.
def getAllModulesInCurrentDirectory():
    declarations = []
    for filename in glob.glob('*.sv'):
        declarations.append(getFileNameWithoutExtension(filename))
    return declarations


def hasTestbench(filename, module):
    testbenchName = module + "_testbench()"
    with open(filename, 'r') as f:
        for line in f:
            if testbenchName in line:
                return True
    return False


def createTestbench(filename, module):
    if hasTestbench(filename, module):
        printErrorMessage(module + "_testbench")
    else:
        printSuccessMessage(filename)
        f = open(filename, "a+")
        f.write("\n\n")
        f.write("/*\n")
        f.write("module " + module + "_testbench();\n")
        for parameter in getModulePorts(filename):
            f.write("\t" + parameter.strip() + "\n")
        f.write(createTestbenchClock())
        f.write("\n\t" + module + " dut (.*); // \".*\" Implicitly connects all ports "
                                  "to variables with matching names\n")
        f.write("\n\tinitial begin\n")
        f.write("\n\t\trepeat (10) @(posedge clk);")
        f.write("\n\t\t$stop; // End simulation")
        f.write("\n\tend")
        f.write("\nendmodule")
        f.write("\n*/")

        f.close()


# Returns dictionary with keys of every SystemVerilog module and their required submodules
def createModuleDictionary():
    modules_with_submodules = {}
    module_list = getAllModulesInCurrentDirectory()
    for filename in glob.glob('*.sv'):
        modules_with_submodules[getFileNameWithoutExtension(filename)] = getModuleExplictSubmodules(filename, module_list)
    return modules_with_submodules


def hasFile(filename):
    return os.path.isfile(filename)


def createProgramDE1SoCFile():
    filename = "ProgramTheDE1_SoC.cdf"
    if hasFile(filename):
        printErrorMessage(filename)
    else:
        printSuccessMessage(filename)
        f = open(filename, "w")
        contents = ("/* Quartus Prime Version 17.0.0 Build 595 04/25/2017 SJ Lite Edition */\n"
                    "JedecChain;\n"
                    "\tFileRevision(JESD32A);\n"
                    "\tDefaultMfr(6E);\n"
                    "\n"
                    "\tP ActionCode(Ign)\n"
                    "\t\tDevice PartName(SOCVHPS) MfrSpec(OpMask(0));\n"
                    "P ActionCode(Cfg)\n"
                    "\t\tDevice PartName(5CSEMA5F31) Path(\"./output_files/\") File(\"DE1_SoC.sof\") MfrSpec(OpMask(1));\n"
                    "\n"
                    "ChainEnd;\n"
                    "\n"
                    "AlteraBegin;\n"
                    "\tChainType(JTAG);\n"
                    "AlteraEnd;\n")
        f.write(contents)
        f.close()
        addFileToProject("DE1_SoC.qos", "CDF_FILE", "ProgramTheDE1_SoC.cdf")


def createLaunchModelSimFile():
    filename = "Launch_ModelSim.bat"
    if hasFile(filename):
        printErrorMessage("Launch_ModelSim.bat")
    else:
        printSuccessMessage("Launch_ModelSim.bat (ensure correct installation path)")
        f = open(filename, "w")
        contents = "C:\intelFPGA\\17.0\modelsim_ase\win32aloem\modelsim.exe\n C:\intelFPGA_lite\\17.0\modelsim_ase\win32aloem\modelsim.exe"
        f.write(contents)
        f.close()


#set_global_assignment -name CDF_FILE ProgramTheDE1_SoC.cdf
#set_global_assignment -name SOURCE_FILE Launch_ModelSim.bat


def addFileToProject(filename, type, target):
    contents = "set_global_assignment -name " + type + " " + filename
    f = open(target, "a+")
    f.write(contents)
    f.close()


def createRunlabFileVlogs(modules):
    result = ""
    for module in modules:
        result = result + "vlog \"./" + module + ".sv\"\n"
    return result


def createRunlabFile(module):
    filename = "runlab_" + module + ".do"
    if hasFile(filename):
        printErrorMessage(filename)
    else:
        printSuccessMessage(filename)
        f = open(filename, "w")
        submodules = getModuleImplictSubmodules(module + ".sv")
        vlog = createRunlabFileVlogs(submodules)
        f.write("# File generated using scripted created by Allen Putich."
                "# "
                "# Runlab format was adopted from Scott Hauck UW EE 271 course files.\n"
                "# Create work library\n"
                "vlib work\n"
                "\n"
                "# Compile Verilog\n"
                "#     All Verilog files that are part of this design should have\n"
                "#     their own \"vlog\" line below.\n"
                + vlog +
                "\n"
                "# Call vsim to invoke simulator\n"
                "#     Make sure the last item on the line is the name of the\n"
                "#     testbench module you want to execute.\n"
                "vsim -voptargs=\"+acc\" -t 1ps -lib work " + module + "_testbench\n" +
                "\n"
                "# Source the wave do file\n"
                "#     This should be the file that sets up the signal window for\n"
                "#     the module you are testing.\n"
                "do " + module + "_wave.do\n" +
                "\n"
                "# Set the window types\n"
                "view wave \n"
                "view structure\n"
                "view signals\n"
                "\n"
                "# Run the simulation\n"
                "run -all\n"
                "\n"
                "\n"
                "# END")
        f.close()


def createWaveFile(module):
    filename = module + "_wave.do"
    if hasFile(filename):
        printErrorMessage(filename)
    else:
        printSuccessMessage(filename)
        f = open(filename, "w")


def createTestingSuite(filename):
    print("Target file: " + filename)
    filenamePrefix = getFileNameWithoutExtension(filename)
    createTestbench(filename, filenamePrefix)
    createWaveFile(filenamePrefix)
    createRunlabFile(filenamePrefix)


def printScriptHeader():
    print(" ------------------------------------------------------------ ")
    print("|    Accelerated SystemVerilog Simulation by Allen Putich    |")
    print("|       https://github.com/HalfDressed/VerilogScripts        |")
    print(" ------------------------------------------------------------ ")

def createTestbenchClock():
    clockInstantiation = ("\n\t// Set up the clock."
                          "\n\tparameter PERIOD = 100; // period = length of clock"
                          "\n\tinitial begin"
                          "\n\t\tclk <= 0;"
                          "\n\t\tforever #(PERIOD/2) clk = ~clk;"
                          "\n\tend\n")

    return clockInstantiation

def createWorkFlowScripts():
    print ("Create workflow scripts:")
    createProgramDE1SoCFile()
    createLaunchModelSimFile()


def printAndReturn(message):
    print(message)
    return message


def printTargetMessage(name):
    message = "Targeting file: \t" + name
    return printAndReturn(message)


def printErrorMessage(name):
    message = "\tAborted: " + name + " already exists"
    return printAndReturn(message)


def printSuccessMessage(name):
    message = "\tSuccess: " + name + " was created"
    return printAndReturn(message)


def printContributeMessage ():
    print("Thanks for using this script :)")


#MAIN ------------------------------------------------------------------------
printScriptHeader()
createWorkFlowScripts()
# Process all arguments given to script OR every .sv file in directory
if (len(sys.argv) > 1):
    for arg in range(len(sys.argv)):
        if arg is not 0:
            createTestingSuite(sys.argv[arg])
else:
    for file in glob.glob('*.sv'):
        createTestingSuite(file)
print("") # additional line for spacing
input('Press ENTER to exit...')
