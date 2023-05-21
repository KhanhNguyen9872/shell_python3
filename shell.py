import os
import pathlib
import zipfile
import sys
import threading

class Color:
    def blue(): return '\033[94m'
    def green(): return '\033[92m'
    def yellow(): return '\033[93m'
    def red(): return '\033[91m'
    def reset(): return '\033[0m'
    
def fix_arg(arg):
    return arg[1:-1]
    
def _help(arg=""):
    print("""Shell by KhanhNguyen9872

command: ls, cd, rm, mkdir, printf, echo, nohup, python3, unzip, clear, exit
""")
    
def unzip(arg=""):
    arg=fix_arg(arg)
    if arg=="":
        return
    arg=arg.split(" ")
    if "-d" in arg:
        for i in range(len(arg)):
            if arg[i]=="-d":
                try:
                    path=arg[i+1]
                    del arg[i],arg[i+1]
                except IndexError:
                    print("error:  must specify directory to which to extract with -d option")
                    return
                break
    else:
        path="./"
    for i in arg:
        if pathlib.Path(i).is_file():
            with zipfile.ZipFile(i, 'r') as zip_ref:
                zip_ref.extractall(path)
        else:
            print("unzip:  cannot find or open {0}, {0}.zip or {0}.ZIP.".format(i))

def printf(arg=""):
    arg=fix_arg(arg)
    print(arg,end='')

def echo(arg=""):
    arg=fix_arg(arg)
    arg=str(str(arg.replace("\n","\\\n")).replace("\t","\\\t")).replace("\r","\\\r")
    print(arg)
    
def ls(arg=""):
    arg=fix_arg(arg)
    folder=[]
    file=[]
    tmp=""
    count = 0
    for i in os.listdir():
        if pathlib.Path(i).is_file():
            file.append(Color.reset()+i)
        else:
            folder.append(Color.blue()+i)
    syntax="!@#$%^&*()(*&^%$#@!)[];:|><.,/?-=`~+"
    all=str("{0}{2}{1}".format(syntax.join(folder),syntax.join(file),syntax)).split(syntax)
    del folder,file
    for i in all:
        if " " in i:
            i="'{0}'".format(i)
        if count>=3:
            tmp+="\n"
            count=0
        tmp+="{0}\t".format(i)
        count+=1
    
    print("{0}".format(tmp))
    
def cd(arg=""):
    arg=fix_arg(arg)
    if arg=="":
        path=HOME
    elif arg.split(" ")[0] == "..":
        path="/".join("/".join(os.getcwd().split("\\")).split("/")[:-1])
    elif pathlib.Path(arg.split(" ")[0]).is_dir():
        path="{}\\{}".format(os.getcwd(),arg.split(" ")[0])
    elif pathlib.Path(arg.split(" ")[0]).is_file():
        print("-shell: cd: {}: Not a directory".format(arg.split(" ")[0]))
        return
    else:
        print("-shell: cd: {}: No such file or directory".format(arg.split(" ")[0]))
        return
    os.chdir(path)

def clear(arg=""):
    os.system('cls' if os.name == 'nt' else 'clear')
    
def python3(arg=""):
    arg=fix_arg(arg)
    os.system("python {0}".format(arg) if os.name == 'nt' else "python3 {0}".format(arg))
    
def exit(arg=""):
    print("\n")
    sys.exit(0)

def shell():
    print("\n{1}┌──({2}{3}@localhost{1})-[{0}{4}{1}]".format(Color.reset(),Color.green(),Color.blue(),os.getlogin(),"~" if os.getcwd()==os.path.expanduser('~') else os.getcwd()))
    print("└─{1}${0}".format(Color.reset(),Color.blue()),end = ' ')
    cmd=str(input()).split(" ")
    arg=str(' '.join(cmd[1:]))
    try:
        if cmd[0]=="dir" or cmd[0]=="shell" or cmd[0]=="arg":
            int("Khanh")
        globals()[cmd[0]](arg)
    except (ValueError, KeyError, TypeError):
        try:
            os.system("{0} {1}".format(cmd[0],' '.join(arg.split())))
        except FileNotFoundError:
            print("-shell: {0}: command not found".format(cmd[0]))

def main():
    print("\nShell Python3 | KhanhNguyen9872")
    while 1:
        try:
            shell()
        except KeyboardInterrupt:
            print("^C")

if __name__=='__main__':
    HOME=os.path.expanduser('~')
    main()