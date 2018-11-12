import sys
from py2diagrams.executors.class_diagrams import execute as execute_class_diagrams

args = sys.argv
num_args = len(args) - 1
if num_args < 1:
    print("Help text TBD")
    exit(0)

cmd = args[1]

if cmd == "class-diagram":
    if num_args < 2:
        print("usage: python3 main.py class-diagram <base_path>")
        exit(1)
    base_dir = args[2]
    print("@startuml")
    execute_class_diagrams(base_dir)
    print("@enduml")

else:
    print("Unsupported command {}".format(cmd))
