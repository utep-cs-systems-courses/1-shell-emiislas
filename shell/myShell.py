import os, sys, re

pipe()

#fork()

dup()

#execve()

#wait()

open()

close()

chdir()



def execute():
    pid = os.getpid()
    os.write(1, ("about to fork(pid:%d)\n" % pid).encode))
    rc = os.fork()

    if (rc < 0): #fail
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif (rc == 0): #child
        os.write(1, ("I am child. My pid==%d. Parent's pid=%d\n" % (os.getpid(), pid)).encode())
        args = ["wc", "p3-exec.py"]
        for dir in re.split(":", os.environ['PATH']):
            program = "%s%s" % (dir, args[0])
            os.write(1, ("Child: tryinng to exec %s\n" % program).encode())
            try:
                os.execve(program, args, os.environ)
            except FileNotFoundError:
                pass

	time.sleep(1)
        os.write(1, "Child: could not exec 0\n".encode())
	sys.exit(0)

    else: #parent forked
	
        os.write(1, ("I am parent. My pid=%d. Child's pid=%d\n" % (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, "Parent: Child %d termiinated with exit code %d\n" % childPiidCode).encode())

def main():
    
    while (True):
        command = input("$")
        if (command == "exit"):
            sys.exit(0)
        elif(command == "cd"):
            cd_instruction()

        else:
            print("Instruction not found")

            




