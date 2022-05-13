import os, sys, time, re

def executeHelper(cmd):
    for dir in re.split(":", os.environ['PATH']):
            program = "%s/%s" % (dir, cmd[0])
           # os.write(1, ("Child: trying to exec %s\n" % program).encode())
            try:
                os.execve(program, cmd, os.environ)
            except FileNotFoundError:
                pass

    os.write(1, "Child: could not exec 0\n".encode())
    sys.exit(0)

def execute(cmd):#Executes commands through execve
    pid = os.getpid() #gets pid to keep track
    rc = os.fork() #forks
  
    if (rc < 0): #if fork fails
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    if (rc == 0): #child
       # os.write(1, ("I am child. My pid==%d. Parent's pid=%d\n" % (os.getpid(), pid)).encode())
       executeHelper(cmd)
        

    else: #parent forked
	
       # os.write(1, ("I am parent. My pid=%d. Child's pid=%d\n" % (pid, rc)).encode())
       childPidCode = os.wait()#waiting for child
       # os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())

def pipe(cmd):
    pr, pw = os.pipe() # pipe read and pipe write
    rcp = os.fork()
    if rcp < 0:
        sys.exit(1)
    if rcp == 0:
        os.close(1) #close fd output (redirect)
        os.dup(pw) #dup of fd
        os.set_inheritable(1, True) 

        for i in (pr, pw): #i is fd
            os.close(i)

        leftcmd = cmd[:cmd.index("|")] # save left command
        executeHelper(leftcmd)
        #os.write(2, ("%s: Command not found\n" %cmd[0]).encode())        
        #sys.exit(1)

    elif rcp > 0:
        #fork another process (execute in child only)
        #pr, pw = os.pipe() # pipe read and pipe write
        rcp = os.fork()
        if rcp < 0:
            sys.exit(1)
        if rcp == 0:
            os.close(0) #parent close fd
            os.dup(pr) 
            os.set_inheritable(0, True)
	
            for i in (pr, pw):
               os.close(i)

            rightcmd = cmd[cmd.index("|")+1:] #right command
            executeHelper(rightcmd)
	        #os.write(2, ("%s: Command not found\n" %cmd[0]).encode())
	        #sys.exit(1)
            
        elif rcp > 0:
           childPidCode = os.wait()
     


def redir(cmd):
    os.close(1)
    os.open(cmd[cmd.index('>')+1], os.O_CREAT | os.O_WRONLY); #create file or open
    os.set_inheritable(1, True)
    cmd.remove(cmd[cmd.index('>')+1])
    cmd.remove('>')
    executeHelper(cmd)


def chdir(path):

    try:
        os.chdir(path)
    except FileNotFoundError:
        os.write(1, ("Invalid Destination %d\n").encode())



def main():
 
    while (True):
        current = os.getcwd()
        command = input(current + "$ ")
        cmd = command.split(' ')
        if (cmd[0] == "exit"):
            sys.exit(0)

        elif(cmd[0] == "cd"):
            chdir(cmd[1])

        elif ('|' in cmd):
            pipe(cmd)

        elif('>' in cmd):
            redir(cmd)

        else:
            #execute any other command
            execute(cmd)

            

main()




