import os
import pathlib
import sys
import shutil
import threading
import subprocess
import shlex
import json

class Color:
    def blue(): return '\033[94m'
    def green(): return '\033[92m'
    def yellow(): return '\033[93m'
    def red(): return '\033[91m'
    def reset(): return '\033[0m'

class bin:
    def is_dir(dir): return pathlib.Path(dir).is_dir()
    def is_file(file): return pathlib.Path(file).is_file()
    def touch(file): return pathlib.Patah(file).touch()
    def err(e): print("{}: missing operand".format(e))
    def shell_split(cmd=""):
        if os.name == 'posix': return shlex.split(cmd)
        else:
            if not cmd: return []
            return json.loads(subprocess.check_output('{} {}'.format(subprocess.list2cmdline([sys.executable, '-c', 'import sys, json; print(json.dumps(sys.argv[1:]))']), cmd)).decode())
    def main():
        print("\nShell Python3 | KhanhNguyen9872")
        while 1:
            try:
                bin.shell()
            except KeyboardInterrupt:
                print("^C")
    def shell():
        print("\n{1}┌──({2}{3}@localhost{1})-[{0}{4}{1}]".format(Color.reset(),Color.green(),Color.blue(),os.getlogin(),"~" if os.getcwd()==os.path.expanduser('~') else os.getcwd()))
        print("└─{1}${0}".format(Color.reset(),Color.blue()),end = ' ')
        cmd=bin.shell_split(str(input()))
        try:
            if cmd[0]=="dir":
                int("Khanh")
            globals()[cmd[0]](cmd[1:])
        except (ValueError, KeyError, TypeError):
            try:
                os.system("{0} {1}".format(cmd[0],' '.join(cmd[1:])))
            except FileNotFoundError:
                print("-shell: {0}: command not found".format(cmd[0]))
   
def _help(arg=[]):
    print("""Shell by KhanhNguyen9872

command: ls, cd, rm, mkdir, printf, echo, nohup, python3, unzip, clear, exit
""")
    
def touch(arg=[]):
    if arg==[]:
        bin.err("touch")
    else:
        for i in arg:
            bin.touch(i)
    
def rm(arg=[]):
    if arg==[]:
        bin.err("rm")
        return
    arg=list(set(arg))
    tmp=["-r","-f","-rf"]
    if "-rf" in arg or "-r" in arg:
        is_folder=1
    elif "-f" in arg:
        if "-rf" in arg or "-r" in arg:
            is_folder=1
        else:
            is_folder=0
    else:
        is_folder=0
    for i in tmp:
        while i in arg:
            arg.remove(i)
    for i in arg:
        if bin.is_file(i):
            os.remove(i)
        elif bin.is_dir(i):
            if is_folder==0:
                print("rm: cannot remove '{}': Is a directory".format(i))
            else:
                shutil.rmtree(i)
        else:
            print("rm: cannot remove '{}': No such file or directory".format(i))

def mkdir(arg=[]):
    if arg==[]:
        bin.err("mkdir")
    else:
        is_ignore=0
        if "-p" in arg:
            is_ignore=1
        while "-p" in arg:
            arg.remove("-p")
        for i in arg:
            if bin.is_dir(i):
                if is_ignore==0:
                    print("mkdir: cannot create directory '{}': File exists".format(i))
            elif bin.is_file(i):
                print("mkdir: cannot create directory '{}': File exists".format(i))
            else:
                os.mkdir(i)

def cat(arg=[]):
    if arg==[]:
        while 1:
            try:
                print(str(input()))
            except KeyboardInterrupt:
                print("^C")
                break
    else:
        for i in arg:
            if bin.is_file(i):
                print(open(i,"r").read())
            elif bin.is_dir(i):
                print("cat: '{}': Is a directory".format(i))
            else:
                print("cat: '{}': No such file or directory".format(i))
    
def unzip(arg=[]):
    if arg==[]:
        return
    if "-d" in arg:
        for i in range(len(arg)):
            if arg[i]=="-d":
                try:
                    path=arg[i+1]
                    arg.remove("-d")
                    arg.remove(path)
                except KeyboardInterrupt:
                    print("error:  must specify directory to which to extract with -d option")
                    return
                break
    else:
        path="./"
    for i in arg:
        if bin.is_file(i):
            shutil.unpack_archive(i, path, i.split(".")[-1])
        else:
            print("unzip:  cannot find or open {0}.".format(i))

def zip(arg=[]):
    if arg==[]:
        bin.err("zip")
    elif len(arg)<2:
        print("zip: need two arguments! \"file_name.zip\" and \"path_to_zip\"")
    else:
        if bin.is_file(arg[-2]):
            os.remove(arg[-2])
        if bin.is_dir(arg[-2]):
            arg[-2]=arg[-2]+".zip"
        shutil.make_archive(".".join(arg[-2].split(".")[:-1]), "zip", arg[-1])
        if bin.is_file(arg[-2]):
            print("zip created: {}".format(arg[-2]))
        else:
            print("zip: cannot create '{}'".format(arg[-2]))

def printf(arg=[]):
    print(" ".join(arg),end='')

def echo(arg=[]):
    arg=str(str(" ".join(arg).replace("\n","\\\n")).replace("\t","\\\t")).replace("\r","\\\r")
    print(arg)

def pwd(arg=[]):
    print(os.getcwd())
    
def ls(arg=[]):
    folder=[]
    file=[]
    tmp=""
    count = 0
    for i in os.listdir():
        if bin.is_file(i):
            file.append(Color.reset()+i)
        else:
            folder.append(Color.blue()+i+Color.reset())
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
    
def cd(arg=[]):
    if arg==[]:
        path=HOME
    elif arg[0] == "..":
        path="/".join("/".join(os.getcwd().split("\\")).split("/")[:-1])
    elif bin.is_dir(arg[0]):
        path="{}\\{}".format(os.getcwd(),arg[0])
    elif bin.is_file(arg[0]):
        print("-shell: cd: {}: Not a directory".format(arg[0]))
        return
    else:
        print("-shell: cd: {}: No such file or directory".format(arg[0]))
        return
    os.chdir(path)

def clear(arg=[]):
    os.system('cls' if os.name == 'nt' else 'clear')
    
def python3(arg=[]):
    os.system("python {0}".format(" ".join(arg)) if os.name == 'nt' else "python3 {0}".format(" ".join(arg)))
    
def exit(arg=[]):
    if arg==[]:
        arg=["0"]
    try:
        sys.exit(int(arg[0]))
    except ValueError:
        print("\rshell: exit: {}: numeric argument required".format(arg[0]))

if __name__=='__main__':
    HOME=os.path.expanduser('~')
    bin.main()