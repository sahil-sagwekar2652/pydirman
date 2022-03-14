#!/bin/python3



        #######    ##       ##   ##########     ########   #######    ##        ###         ###         ###     ##
        ##    ##    ##     ##    ##      ###       ##      ##    ##   ####     ####        ## ##        ####    ##
        ##    ##     ##  ##      ##       ##       ##      ##    ##   ## ##   ## ##       ##   ##       ## ##   ##
        #######        ##        ##       ##       ##      #######    ##   ###   ##      ##     ##      ##  ##  ##
        ##             ##        ##       ##       ##      ## ##      ##         ##     ###########     ##   ## ##
        ##             ##        ##      ###       ##      ##  ##     ##         ##    ##         ##    ##    ####
        ##             ##        ##########     ########   ##   ###   ##         ##   ##           ##   ##     ###


import os
import sys
import readline
import subprocess as sp
from time import sleep
from termcolor import colored, cprint

## GLOBAL VARS USED... PLEASE DON'T HATE ME, I AM AN IDIOT.

global profile, CONFIG, CUR_DIR, LS_DIR, CUR_PATH, CUR_FILE, SEARCH_DIR, SYS_DIR, TempC, TempCpp, TempHTML, COL, browser
TempC= "#include <stdio.h>\n#include <stdlib.h>\n\nint main(){\n\n\treturn 0;\n}"
TempCpp= "#include <iostream>\n\nusing namespace std;\nint main(){\n\n\treturn 0;\n}"
TempHTML= '<!DOCTYPE html>\n<html lang="en">\n\t<head>\n\t\t<meta charset="UTF-8">\n\t\t<meta name="viewport" content="width=device-width,initial-scale=1.0>"\n\t\t<title></title>\n\t</head>\n\t<body>\n\n\t</body>\n</html>'
COL, LINE = os.get_terminal_size()
CONFIG= "/.pydirman.config"
NANORC="/etc/nanorc"
profile= ""

try:
    with open(CONFIG, "x") as f:
        pass
except:
    pass

def green(text):

    return colored(text, "green")

def log(cmd, ctx):

    global CONFIG

    with open(CONFIG, "a") as f:
        f.write("[{}] {}\n".format(ctx, cmd))

def load(ctx):

    global CONFIG

    with open(CONFIG, "r") as f:
        lines= f.readlines()

    for line in lines:
        context= line.split(" ")[0][1:-1]
        if context == ctx:
            return " ".join(line.split(" ")[1:]).rstrip("\n")

    return ""

def custom(fp):

    global profile
    os.system("clear")
    cmd= input("Get Profile? [New/Load/{press Enter to skip}] ")
    if cmd.lower() == "n":
        context= input("Enter Profile Context: ")
        profile= input("Enter Profile: ")
        log(profile, context)
        print("Successfully Saved Custom Profile `{}`\n".format(context))

    elif cmd.lower() == "l":
        print_profiles()
        context= input("Enter Profile Context: ")
        try:
            profile= load(context)
            print("Successfully Loaded Custom Profile `{}`\n".format(context))

        except:
            print("No Profile Found with name `{}`\n".format(context))

    elif cmd.lower() is None:
        profile= ""

    else:
        print("Invalid Command: `{}`".format(cmd))

SYS_DIR = []
for directory in os.listdir("/"):
    SYS_DIR.append(directory)

if len(sys.argv) > 1:
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        cprint("\nPython Directory Management", "red", attrs=['bold', 'underline'])
        cprint("Usage: pydirman [directory]", "blue", attrs=['bold'])
        cprint("if no arg is specified, current working directory will be specified by default.\n", "blue", attrs=['bold'])
        cprint("-h/--help flag for this help menu\n", "blue", attrs=['bold'])
        sys.exit()
    else:
        try:
            os.chdir(sys.argv[1])
        except NotADirectoryError:
            cprint("\nEnter a Directory path only!!", "red", attrs=['bold'])
            sys.exit(1)
        except FileNotFoundError:
            cprint("Directory does not exist!!\n", "red", attrs=['bold'])
            sys.exit(0)

elif len(sys.argv) == 1:
    CUR_DIR = os.getcwd()

CUR_DIR = os.getcwd()
LS_DIR = sorted(os.listdir())
CUR_PATH = os.path.abspath(CUR_DIR)

def convert_bytes(size):
    for ext in ['bytes', 'KB', 'MB', 'GB']:
        if size < 1024:
            return "{} {}".format(round(size, 2), ext)
        else:
            size/= 1024

def __hex(fp):
    with open(fp, "rb") as file:
        content= file.read()

    hexd= content.hex(sep= ' ')
    print("\n"+ colored(hexd, "blue") +"\n")

def print_profiles():

    global CONFIG, profile, COL

    with open(CONFIG, "r") as f:
        data= f.readlines()

    print("-"*COL)
    for line in data:
        context= line.split(" ")[0]
        profile= " ".join(line.split(" ")[1:]).rstrip("\n")

        print("CONTEXT{}: `{}`".format(context, profile))

    print("-"*COL)

def test(file, cc=""):

    global COL, browser, CONFIG, profile
    __file = file.split(".")
    try:
        filename, file_type = __file
    except:
        filename= __file[0]

    command = str(input("Enter command [exit|test|nano|clear|hex] "))
    if command.startswith("t"):
        args= " ".join(command.split(" ")[1:])

        print("="*COL)
        if profile != "":
            print("profile: {}".format(cc))
        else:
            print("No profiles detected!")

        print("-"*COL)

        if file_type == 'py':
            os.system("python3 {} {}".format(file, args).rstrip())

        elif file_type == 'c':
            os.system("gcc {} {} -o {}.out && ./{}.out {}".format(file, cc, filename, filename, args).rstrip())

        elif file_type == 'cpp':
            os.system("g++ {} {} -o {}.out && ./{}.out {}".format(file, cc, filename, filename, args).rstrip())

        elif file_type == 'asm':
            os.system("sudo nasm -f elf64 {} && sudo ld -o {}.out {}.o && sudo ./{}.out".format(file, filename, filename, filename))

        elif file_type == 'js':
            os.system("node {} {}".format(file, args).rstrip())

        elif file_type == 'java':
            os.system("javac -Xlint:unchecked {} && java {} {}".format(file, filename, args).strip())

        elif file_type == 'out' or file_type == 'sh':
            try:
                os.system("./{} {}".format(file, args).rstrip())
            except:
                os.system("chmod +x {}".format(file))

        elif file_type == 'class':
            os.system("java {} {}".format(filename, args).rstrip())

        elif file_type == 'html':
            os.system("python3 -m http.server 8080 --directory {}".format(CUR_DIR))

        print()
        print("="*COL)
        test(file, cc)

    elif command.lower() == "n":
        os.system("sudo nano {}".format(file))
        test(file, cc)

    elif command.lower() == "c":
        COL= os.get_terminal_size()[0]
        os.system("clear")
        print("FILE -> {}\n".format(file))
        test(file, cc)

    elif command.lower() == "h":
        __hex(file)
        test(file, cc)

    elif command.lower() == "e":
        os.system("clear")
        __display()
        __chdir(os.getcwd())

    elif command.lower() == "cc":
        os.system("sudo nano /.pydirman.config")
        print_profiles()
        profile= load(input("Enter Profile Context: "))
        test(file, profile)

    elif command.lower() == "gc":
        print("-"*COL)
        if (cc != ""):
            print("profile: {}".format(cc))
        else:
            print("No profiles detected.\n")

        print("-"*COL)
        test(file, cc)

    elif command.lower() == "rc":
        print("-"*COL)
        print("Removing context... `{}`\n".format(cc))
        print("-"*COL)
        test(file)

    else:
        print("please enter a valid command")
        test(file, cc)

def __display():

    global COL

    COL= os.get_terminal_size()[0]
    TAB= round((0.6*COL))
    CUR_DIR = os.getcwd()
    LS_DIR = sorted(os.listdir())
    CUR_PATH = os.path.abspath(CUR_DIR)

    print(colored("\nPYTHON DIRECTORY MANAGEMENT\n", "red", attrs=['underline', 'bold']))
    gi= green(" | ")
    print(colored("Directory", "yellow") + gi + colored("File", "white") + gi + colored("Error", "red"))
    print(green("="*COL))
    fc = 0
    dc = 0
    misc= 0
    counter = 0
    total_size = 0
    for index,FI_FO in enumerate(LS_DIR):
        gin= green("[{}] ".format(index))
        counter += 1
        if os.path.isfile(FI_FO):
            fc += 1
            name_length= len(str(counter))+ 3+ len(FI_FO)
            GAP= TAB-name_length
            file_size= convert_bytes(os.path.getsize(FI_FO))
            total_size+= os.path.getsize(FI_FO)
            print(gin + colored("{}".format(str(FI_FO)), "white") + colored("-"*GAP +"{}".format(file_size), "blue"))

        elif os.path.isdir(FI_FO):
            dc += 1
            print(gin + colored("{}/".format(str(FI_FO)), "yellow"))

        else:
            print(gin + colored("{}".format(str(FI_FO)), "red"))
            misc += 1

    print(green("="*COL))
    fcounter = colored("{}".format(fc), "white", attrs=['bold'])
    dcounter = colored("{}".format(dc), "yellow", attrs=['bold'])
    c = colored("{}".format(counter), "green", attrs=['bold'])
    m = colored("{}".format(misc), "red", attrs=['bold'])
    print("TOTAL FILES/DIRECTORIES: {} ({}/{}/{})".format(c, fcounter, dcounter, m))
    print("YOUR CURRENT LOCATION: "+ colored("{}".format(CUR_PATH), "green", attrs=['bold']))
    print("TOTAL SIZE HERE(files): "+ colored("{}".format(convert_bytes(total_size)), "green", attrs=['bold']))
    print(green("="*COL))
    print("[help] = "+ colored("[?]", 'red'))

def parse_cmd(ss, lsd):

    cc = ss.split()
    res = []
    for index, obj in enumerate(cc):

        try:
            eoc = obj.index("^")
        except:
            eoc = None

        if obj.startswith("$"):

            if "^" in obj:
                ref = "'{}'{}".format(str(lsd.index(obj[1:eoc])), obj[eoc +1:])

                try:
                    ref = eval(ref)
                except:
                    print("An error has occured parsing the command: `{}`".format(ref))

            else:
                ref = str(lsd.index(obj[1:]))

        elif obj.startswith("&"):

            if "^" in obj:
                ref = "'{}'{}".format(str(lsd[int(obj[1:eoc])]), obj[eoc +1:])

                try:
                    ref = eval(ref)
                except:
                    print("An error has occured parsing the command: `{}`".format(ref))

            else:
                ref = str(lsd[int(obj[1:])])

        else:
            ref = obj

        if not isinstance(ref, str):
            print("An generic error has occured parsing the command...")
            return None

        res.append(ref)

    return " ".join(res)

def __chdir(CUR_DIR):

    global TempC, TempCpp, TempHTML, COL
    CUR_DIR = os.getcwd()
    LS_DIR = sorted(os.listdir())
    SEARCH_DIR = []
    for item in LS_DIR:
        SEARCH_DIR.append(str(item.lower()))
    SOURCE_FILE_PATH = os.path.abspath(sys.argv[0])

    __all__ = [
    '?', 'help', 'editsource', 'usb', 'open'
    'goto', 'previous', 'search',
    'update', 'terminal', 'exit', 'clear',
    'newfile', 'deletefile', 'searchfile',
    'makedir', 'removedir', 'test'
    ]

    try:
        com = str(input(colored("\npydirman", "blue", attrs=['underline']) +colored(">", "blue"))).strip()
        if com.startswith("g"): #  GOTO COMMAND

            com = parse_cmd(com, LS_DIR)
            print("[COM] {}".format(com))
            try:
                if len(os.listdir(os.getcwd()))==1:
                    ask= "0"
                else:
                    if len(com.strip())==1:
                        print("I need a index here to work!")
                        __chdir(CUR_DIR)
                    else:
                        ask= com.split(" ")[1]

                if ask.isdigit():
                    ask= eval(ask)

                    try:
                        if os.path.isdir(str(LS_DIR[ask])):
                            os.system("clear")
                            os.chdir(str(LS_DIR[ask]))
                            __display()
                            __chdir(LS_DIR[ask])

                        elif os.path.isfile(str(LS_DIR[ask])):
                            rp = colored('[p]', 'red')
                            rc = colored('[c]', 'red')
                            re = colored('[e]', 'red')
                            porr = str(input(colored("FILE=[{}]\n".format(str(LS_DIR[ask])), "white")+"{}rint/{}ancel/{}xit: ".format(rp,rc,re)))
                            CUR_FILE = str(LS_DIR[ask])

                            if porr.lower() == "p":
                                print(colored("\n" +"="*((COL-5)//2) +"START"+ "="*((COL-5)//2) +"\n", "red"))
                                os.system("reader.out {}".format(CUR_FILE))
                                print(colored("\n" +"="*((COL-3)//2) +"END"+ "="*((COL-3)//2)+ "\n", "red"))
                                __chdir(os.getcwd())

                            elif porr.lower() == "c":
                                __chdir(os.getcwd())

                            elif porr.lower() == "e":
                                sys.exit(0)

                            else:
                                print("Enter a valid command")
                                __chdir(os.getcwd())

                    except IndexError:
                        print("oops, you entered a wrong number.")
                        __chdir(os.getcwd())

                elif ask.isalpha():
                    print("Please enter index of the file :[")
                    print("[HINT] if you can't find the index then you can find it by typing [s] ;]")
                    __chdir(os.getcwd())

                else:
                    print("wait what?, what is this: {}".format(" ".join(com.split(" ")[1:])))
                    __chdir(os.getcwd())

            except PermissionError:
                cprint("\nThis directory is off limits!! Are you root?? I don't think so. BACK OFF!\n".upper(), "red", attrs=['bold'])
                sleep(2)
                __chdir(os.getcwd())

        elif com.lower() == "e": #  EXIT COMMAND
            print(colored("See you soon!\n", "white"))
            sys.exit(0)

        elif com.lower() == "console": #  PYTHON CONSOLE
            os.system("clear")
            sp.run("python3")
            __display()
            __chdir(CUR_DIR)

        elif com.lower() == "o": #  OPEN-IN-GUI COMMAND

            edited = 0
            char_set = "!@#$%^&*()"
            path = CUR_DIR
            for i, j in enumerate(path):
                if j in char_set:
                    path = path[:i+edited] + "\\" + path[i+edited:]
                    edited += 1

            print("[PATH]: {}".format(path))
            os.system("nautilus {}".format(path))
            __chdir(CUR_DIR)

        elif com.lower() == "u": #  USB COMMAND
            try:
                CUR_DIR= "/media/{}".format(os.environ["SUDO_USER"])
            except KeyError:
                CUR_DIR= "/media/{}".format(os.environ["USER"])

            os.system("clear")
            os.chdir(CUR_DIR)
            __display()
            __chdir(CUR_DIR)

        elif com.lower() == "ed": # SOURCE CODE ACCESS
            os.system("sudo nano {} ".format(SOURCE_FILE_PATH))
            __chdir(os.getcwd())

        elif com.lower() == "edn": # SOURCE CODE ACCESS
            os.system("sudo nano {} ".format(NANORC))
            __chdir(os.getcwd())

        elif com.lower() == "c": #  CLEAR/REFRESH COMMAND
            os.system("clear")
            __display()
            __chdir(CUR_DIR)

        elif com.startswith("test"): #  CODE-TESTING COMMAND
            CUR_DIR = os.getcwd()
            LS_DIR = sorted(os.listdir())

            if len(com) == 4:
                print("I am hungry! Feed me indices.")
                __chdir(CUR_DIR)
            else:
                try:
                    com = parse_cmd(com, LS_DIR)
                    global profile
                    file_index = int(com[5:])
                    file = LS_DIR[file_index]
                    ext= file.split(".")[1]
                    CUSTOMISABLE= ["c", "cpp"]

                    if os.path.isfile(file):

                        if ext in CUSTOMISABLE:
                            custom(file)

                        os.system("clear")
                        print("FILE -> {}\n".format(file))
                        test(file, profile)

                    elif os.path.isdir(file):
                        print("Enter index of files only !!")
                        __chdir(CUR_DIR)

                except IndexError:
                    print("Index {} not found".format(file_index))
                    __chdir(CUR_DIR)

                except ValueError:
                    print("Please enter a index!!")
                    __chdir(CUR_DIR)

        elif (com.lower() == "?")or(com.lower() == "h"): #  HELP COMMAND
            print("\n[help]      = "+ colored("[?/h]", 'red') +"elp-"+ colored("[ed]", 'red') +"itsource")
            print("[walker]    = "+ colored("[g]", 'red') +"oto-" +colored("[p]", 'red') +"revious-"+ colored("[s]", 'red') +"earch")
            print("[utility]   = "+ colored("[c]", 'red') +"lear-"+ colored("[t]", 'red') +"erminal-" +colored("[e]", 'red')+ "xit-" +colored("[c]", 'red') +"lear")
            print("[writer]    = "+ colored("[n]", 'red') +"ewfile-" +colored("[d]", 'red') +"eletefile")
            print("[folder]    = "+ colored("[m]", 'red') +"akedir-" +colored("[r]", 'red') +"emovedir")
            print("[misc]      = "+ colored("[u]", 'red') +"sb-"+ colored("[o]", 'red') +"pen")
            __chdir(CUR_DIR)

        elif com.lower() == "p": #  PREVIOUS COMMAND
            os.system("clear")
            os.chdir("..")
            if os.getcwd() == CUR_DIR:
                cprint("\nEnd of the line, buddy!", "blue", attrs=['bold'])
                __chdir(CUR_DIR)
            else:
                CUR_DIR = os.getcwd()
                __display()
                __chdir(CUR_DIR)

        elif com.startswith("s "): #  SEARCH COMMAND
            args= com.split()
            search = args[1]
            try:
                con= args[2]
            except:
                con= "-a"
            objects= []
            for object in LS_DIR:
                if search in object:
                    if con == "-a":
                        objects.append((object, LS_DIR.index(object)))
                    elif con == "-f":
                        if os.path.isfile(object):
                            objects.append((object, LS_DIR.index(object)))
                    elif con == "-d":
                        if os.path.isdir(object):
                            objects.append((object, LS_DIR.index(object)))
                    else:
                        print("Wrong argument: `{}`".format(con))
                        print("\n[-a] for all(by default).\n[-f] for files only.\n[-d] for directory only.\n")
                        break

            if len(objects) > 0:
                print("-"*COL)
                print(colored(f"OBJECTS SEARCHED: {len(LS_DIR)}, OBJECTS FOUND: {len(objects)}", "red", attrs=["bold"]))
                print("-"*COL)

                for object in objects:
                    if os.path.isfile(object[0]):
                        print("[{}] ".format(object[1]) + colored("{}".format(object[0]), "white"))
                    elif os.path.isdir(object[0]):
                        print("[{}] ".format(object[1]) + colored("{}/".format(object[0]), "yellow"))
                print("-"*COL)

            else:
                print("`{}` not found!!!".format(args[:]))
            __chdir(CUR_DIR)

        elif com.startswith("t "): #  TERMINAL COMMAND
            com = parse_cmd(com, LS_DIR)
            if com is not None:
                cmd= com[2:]
                cmd_args= cmd.split(" ")
                print("-"*COL + "\nExecuting [{}]...\n".format(colored(cmd, "green")) + "-"*COL)
                os.system(cmd)
                print("-"*COL)

            __chdir(CUR_DIR)

        elif com.lower() == "n": #  NEW-FILE COMMAND
            try:
                filename = str(input("Enter file name [create]: "))
                os.system("touch {}".format(filename))
                file_name ,file_ext = filename.split('.')
                TempJava= "public class "+ file_name +" {\n\n\tpublic static void main(String[] args){\n\n\n\t}\n\n}\n"
                ns= "__"+ file_name.upper() +"_H"
                TempHPP= "#ifndef {}\n#define {}\n\n\n".format(ns, ns) + "class "+ file_name +" {\n\n};\n\n#endif"

                if file_ext == 'c':
                    with open(filename, "w") as f:
                        f.write(TempC)

                elif file_ext == 'cpp':
                    with open(filename, "w") as f:
                        f.write(TempCpp)

                elif file_ext == 'java':
                    with open(filename, "w") as f:
                        f.write(TempJava)

                elif file_ext == 'hpp':
                    with open(filename, "w") as f:
                        f.write(TempHPP)

                elif file_ext == 'html':
                    with open(filename, "w") as f:
                        f.write(TempHTML)

                os.system("sudo chmod 777 {}".format(filename))

            except:
                print("File not created")

            os.system("clear")
            __display()
            __chdir(CUR_DIR)

        elif com.lower() == "d": #  DELETE-FILE COMMAND
            print("="*COL)
            counter = 0
            for index,FI_FO in enumerate(LS_DIR):
                if os.path.isfile(FI_FO):
                    print("[{}] ".format(index) + colored("{}".format(FI_FO), "white")) #color for file instance
                    counter += 1

            print("="*COL)
            try:
                delfileindex = int(input("Enter file index [delete]: "))
                delfile = LS_DIR[delfileindex]
                os.system("sudo rm {}".format(delfile))
            except KeyboardInterrupt:
                print("File not deleted")
            except ValueError:
                print("Enter Correctly")
            except IndexError:
                print("Enter Correctly")

            __chdir(os.getcwd())

        elif com.startswith("m "): #  NEW-DIRECTORY COMMAND
            try:
                dirname_mk = com.split(" ")[1]
                os.system("mkdir {}".format(dirname_mk))
            except KeyboardInterrupt:
                print("Directory not created!")

            os.system("clear")
            __display()
            __chdir(os.getcwd)

        elif com.lower() == "r": #  DELETE-DIRECTORY COMMAND
            print("="*COL)
            counter = 0
            for index,FI_FO in enumerate(LS_DIR):

                if os.path.isdir(FI_FO):
                    print("[{}] ".format(index) + colored("{}/".format(FI_FO), "yellow")) #color for directory
                    counter += 1
            print("="*COL)
            try:
                dirname_rm = str(input("Enter directory name: ")).strip()
                if dirname_rm in SYS_DIR:
                    print("You just tried to delete a system folder!!")
                    __chdir(os.getcwd())
                os.system("rmdir {}".format(dirname_rm))
            except KeyboardInterrupt:
                print("Directory not deleted")
            except ValueError:
                print("Enter Correctly")
            except IndexError:
                print("Enter Correctly")

            os.system("clear")
            __display()
            __chdir(os.getcwd())

        elif com.lower() in __all__:
            print("\nplease enter the the first letter [{}] only".format(com.lower()[0]))
            __chdir(os.getcwd())

        else:
           print("\nEnter a valid command!")
           __chdir(os.getcwd())

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected..Press e for exit")
        __chdir(os.getcwd)

__display()
__chdir(CUR_DIR)
