import subprocess
import queue

#se citeste o comanda unix care se  imparta la |  si foloseste pipe-ul din subprocessing a.i. comanda din stanga sa fie input la comanda din dreapta

def execute(q):
    first_cmd = subprocess.run(q.get(), stdout=subprocess.PIPE, text=True, shell=True)
    data = first_cmd.stdout
    while not q.empty():
        cmd = subprocess.run(q.get(), stdout=subprocess.PIPE, text=True, input=data, shell=True)
        data = cmd.stdout
    print(data)


def process(command):
    x = command.split(" | ")
    q = queue.Queue()
    for cmd in x:
        q.put(cmd)

    execute(q)


if __name__ == '__main__':
    command = "ls -la | cat"
    process(command)
