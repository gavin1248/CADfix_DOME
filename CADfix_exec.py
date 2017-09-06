import os
import ctypes
import shutil

# save local dir
local_directory = os.getcwd()
local_directory = local_directory + "\\"
print local_directory

# parse input params and put in object called 'inputs'
with open('in.txt') as f:
    lines = f.readlines()

    inputs = {}

    for line in lines:
        kv = line.rstrip().split("=")
        key = kv.pop(0).strip()
        value = "=".join(kv).strip()
        inputs[key] = value

# download the input file to the local dir
# import filemanagement
# Note that first DOME variable is called inputFile
# !!! Problem, how do I get the original file name or more importantly the extension
input_file = "input.stl"
filemanagement.download_data(inputs["inputFile"], input_file)


# Grab credentials
# !!! Where does the JSON that this uses come from?
creds = filemanagement.get_credentials()
print "Got S3 creds....\n"

# Open out.txt for writing for DOME
target = open("out.txt", 'w')
print "Open out.txt"

# Running CADfix
from subprocess import call
# CADfix executable location
# Remember to escape the extra quotes for command line
CADfix_loc = "\"c:\\Program Files (x86)\\CADfix 11\\bin\\runcadfconsole.exe\""
# Wizard file, for example to_jt.cwc
wiz_file = "to_" + inputs["convertTo"] + ".cwc"
print CADfix_loc + " -wait -BATCH -config " + wiz_file + " " + input_file
# This command looks like 
# "c:\Program Files (x86)\CADfix 11\bin\runcadfconsole.exe" -wait -BATCH -config wizard.cwc file.stp
call(CADfix_loc + " -wait -BATCH -config " + wiz_file + " " + input_file, shell=False)

# Create output file name
input_noext = os.path.splitext(input_file)[0]
output_file = input_noext + "_cf." + inputs["convertTo"]

# Upload and get url
output_url = upload_file(output_file, creds)

# Write out to out.txt then close
target.write("outputFile = " + output_url)
target.close()