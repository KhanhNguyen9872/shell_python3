import os
import pathlib
import sys
import shutil
import threading
import subprocess
import shlex
import json
import stat
import requests

__import__('urllib3').disable_warnings(__import__('urllib3').exceptions.InsecureRequestWarning)

class Color:
    def blue(): return '\033[94m'
    def green(): return '\033[92m'
    def yellow(): return '\033[93m'
    def red(): return '\033[91m'
    def reset(): return '\033[0m'
    def bg_green(i=""): return '\x1b[6;30;42m' + str(i) + '\x1b[0m'

class bin:
    def unlink(file): os.unlink(file)
    def fwrite(file, data="", t="w"): open(file, t).write(data)
    def get_pyver(): return str(".".join(sys.version.split(" ")[0].split(".")[:-1]))
    def get(link): return requests.get(link, headers={'user-agent' : 'curl/9.9.99'}, verify=False).text
    def is_dir(dir): return pathlib.Path(dir).is_dir()
    def is_file(file): return pathlib.Path(file).is_file()
    def touch(file): return pathlib.Path(file).touch()
    def err(e): print("{}: missing operand".format(e))
    def title(): os.system("title Shell") if os.name == 'nt' else os.system("")
    def owner_group(file):
        if os.name == 'nt':
            return ""
        return "{}\t{}".format(pathlib.Path(file).owner(),pathlib.Path(file).group())
    def shell_split(cmd=""):
        if os.name == 'posix': return shlex.split(cmd)
        else:
            if not cmd: return []
            return json.loads(subprocess.check_output('{} {}'.format(subprocess.list2cmdline([sys.executable, '-c', 'import sys, json; print(json.dumps(sys.argv[1:]))']), cmd)).decode())
    def chmod(file,chmod_per=9999,is_chmod=1):
        if bin.is_file(file) and bin.is_dir(file):
            print("chmod: cannot access '{}': No such file or directory".format(file))
        elif is_chmod == 0:
            return eval("stat.filemode({})".format(oct(os.stat(file).st_mode)))
        elif chmod_per == 9999:
            print("chmod: missing operand after '{}'".format(file))
        elif len(chmod_per)>3 or len([str(char) for char in str(chmod_per) if int(char)<=7]) != 3:
            print("chmod: invalid mode: '{}'".format(chmod_per))
            return
        os.chmod(str(file),int(chmod_per))
    def main():
        bin.title()
        print("\nShell Python3 | KhanhNguyen9872")
        while 1:
            try:
                bin.shell()
            except KeyboardInterrupt:
                print("^C")
    def shell():
        try:
            user = os.getlogin() if os.name == 'nt' else os.environ['USER']
        except KeyError:
            user = subprocess.getoutput('whoami')
        print("\n{1}┌──({2}{3}@localhost{1})-[{0}{4}{1}]".format(Color.reset(),Color.green(),Color.blue(),user,"~" if os.getcwd()==os.path.expanduser('~') else os.getcwd()))
        print("└─{1}${0}".format(Color.reset(),Color.blue()),end = ' ')
        cmd=bin.shell_split(str(input()))
        try:
            if cmd[0]=="dir":
                int("Khanh")
            globals()[cmd[0]](cmd)
        except (ValueError, KeyError, TypeError):
        #except KeyboardInterrupt:
            try:
                os.system("{0} {1}".format(cmd[0],' '.join(cmd[1:])))
            except FileNotFoundError:
                print("-shell: {0}: command not found".format(cmd[0]))
        except IndexError:
            return
   
def _help(arg=[]):
    print("""Shell by KhanhNguyen9872

command: ls, cd, touch, rm, mkdir, cat, chmod, printf, echo, pwd, python3, unzip, zip, clear, exit
tool_dec_py: dump_marshal, cv_marshalpyc, kramer_deobf, specter_deobf, berserker_deobf, hyperion_deobf
""")

def dump_marshal(arg=[]):
    print("Loading dump_marshal....")
    bin.fwrite('dump_marshal.py', bin.get('https://raw.githubusercontent.com/KhanhNguyen9872/dump_marshal_py/main/py{}/dump_marshal.py'.format(bin.get_pyver())))
    os.system('{} dump_marshal.py'.format(sys.executable))

def cv_marshalpyc(arg=[]):
    print("Loading cv_marshalpyc....")
    bin.fwrite('cv_marshalpyc.py', bin.get('https://raw.githubusercontent.com/KhanhNguyen9872/Convert_Marshal-PYC/main/cv_marshal_pyc-py{}.py'.format("".join(bin.get_pyver().split(".")))))
    os.system('{} cv_marshalpyc.py'.format(sys.executable))

def specter_deobf(arg=[]):
    kramer_deobf(arg)

def berserker_deobf(arg=[]):
    kramer_deobf(arg)

def kramer_deobf(arg=[]):
    try: 
        txt = arg[0]
    except IndexError:
        txt = 'kramer_deobf'
    print("Loading {}....".format(txt))
    bin.fwrite('kramer_deobf.py', bin.get('https://raw.githubusercontent.com/KhanhNguyen9872/kramer-specter_deobf/main/kramer-specter-deobf_py{}.py'.format("".join(bin.get_pyver().split(".")))))
    os.system('{} kramer_deobf.py'.format(sys.executable))

def hyperion_deobf(arg=[]):
    print("Loading hyperion_deobf....")
    bin.fwrite('hyperion_deobf.py', bin.get('https://raw.githubusercontent.com/KhanhNguyen9872/hyperion_deobfuscate/main/hyperion-deobf_py{}.py'.format("".join(bin.get_pyver().split(".")))))
    os.system('{} hyperion_deobf.py'.format(sys.executable))

def chmod(arg=[]):
    if len(arg) == 1:
        bin.err("chmod")
    elif len(arg)<2:
        print("chmod: missing operand after '{}'".format(arg[1]))
    else:
        bin.chmod(arg[2], arg[1])

def touch(arg=[]):
    if len(arg) == 1:
        bin.err("touch")
    else:
        for i in arg:
            bin.touch(i)
    
def rm(arg=[]):
    if len(arg) == 1:
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
    if len(arg) == 1:
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
    if len(arg) == 1:
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
    if len(arg) == 1:
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
    if len(arg) == 1:
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
    file=[]
    tmp=""
    tmp1=[]
    count = 0
    try:
        for i in os.listdir():
            if bin.is_file(i):
                if "x" in bin.chmod(i,9999,0):
                    j=Color.green()+i
                else:
                    j=Color.reset()+i
                file.append(j)
            elif bin.is_dir(i):
                if "x" in bin.chmod(i,9999,0):
                    j=Color.bg_green(i)
                else:
                    j=Color.blue()+i+Color.reset()
                file.append(j)
            else:
                continue
            if "-l" in arg:
                tmp += "{0}\t{1}\t{2}\n".format(bin.chmod(i,9999,0),bin.owner_group(i),file[-1])
    except PermissionError:
        print("ls: can't open '{0}': Permission denied".format(os.getcwd()))
        return
    
    if "-l" not in arg:
        for i in file:
            if " " in i:
                i="'{0}'".format(i)
            if count>=3:
                tmp+="\n"
                count=0
            tmp+="{0}\t".format(i)
            count+=1
    
    print("{0}".format(tmp))
    
def cd(arg=[]):
    if len(arg) == 1:
        path=HOME
    elif arg[1] == "..":
        path="/".join("/".join(os.getcwd().split("\\")).split("/")[:-1])
        if path=="" and os.name != 'nt':
            path = "/"
        elif path[-1] == ':' and os.name == 'nt':
            path += "\\"
    elif bin.is_dir(os.getcwd()+"\\"+arg[1]):
        path="{}\\{}".format(os.getcwd(),arg[1])
    elif bin.is_dir(arg[1]):
        path=arg[1]
    elif bin.is_file(arg[1]):
        print("-shell: cd: {}: Not a directory".format(arg[1]))
        return
    else:
        print("-shell: cd: {}: No such file or directory".format(arg[1]))
        return
    os.chdir(path)

def clear(arg=[]):
    os.system('cls' if os.name == 'nt' else 'clear')
    
def python3(arg=[]):
    os.system("python {0}".format(" ".join(arg)) if os.name == 'nt' else "python3 {0}".format(" ".join(arg)))
    
def exit(arg=[]):
    if arg[0]=="exit":
        arg=["exit", "0"]
    try:
        sys.exit(int(arg[1]))
    except ValueError:
        print("\rshell: exit: {}: numeric argument required".format(arg[1]))

if __name__=='__main__':
    HOME=os.path.expanduser('~')
    bin.main()
