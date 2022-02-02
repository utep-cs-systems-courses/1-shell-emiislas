import os, sys, re

pipe()

fork()

dup()

execve()

wait()

open()

close()

chdir()

pid = os.getpid()

def fork(pid):
    os.write(1, ("about to fork(pid:%d)\n" % pid).encode))
    rc = os.fork()
    
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:
        os.write(1, ("I am child. My pid==%d. Parent's pid=%d\n" % (os.getpid(), pid)).encode())
    else:
        os.write(1, ("I am parent. My pid=%d. Child's pid=%d\n" % (pid, rc)).encode())


