import os
import subprocess


class Handler():
    def handle(self):
        pass


class PythonHandler(Handler):
    def __init__(self, file_path):
        self.file_path = file_path
        self.result = None
        self.nextCheck = None

    def handle(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                if line.__contains__("__main__") or line.__contains__("def"):
                    result = "python"
                    return result
        self.nextCheck.handle()


class KotlinHandler(Handler):
    def __init__(self, file_path):
        self.file_path = file_path
        self.result = None ;
        self.nextCheck = None

    def handle(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                if line.__contains__("fun") or line.__contains__("!!") or line.__contains__(".."):
                    print("The content is Kotlin")
                    result = "kotlin"
                    return result
        self.nextCheck.handle()


class JavaHandler(Handler):
    def __init__(self, file_path):
        self.file_path = file_path
        self.result = None;
        self.nextCheck = None

    def handle(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                if line.__contains__("java") or line.__contains__("public static void main"):
                    print("The content is Java")
                    result = "java"
                    return result
        self.nextCheck.handle()


class BashHandler(Handler):
    def __init__(self, file_path):
        self.file_path = file_path
        self.result = None;
        self.nextCheck = None

    def handle(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                if line.__contains__("bash"):
                    print("The content is Bash")
                    result = "bash"
                    return result


class UnknownHandler(Handler):
    def __init__(self, file_path):
        self.file_path = file_path
        self.result = None;
        self.nextCheck = None

    def handle(self):
        print("Unknown programming language")
        result = "unknown"
        return result


class Command():
    def execute(self, file_path):
        pass


class ExecutePython(Command):
    def __init__(self, file_path):
        self.file_path = file_path

    def execute(self):
        output = subprocess.check_output(["python3", self.file_path])
        print("output:", output)
        return None


class ExecuteKotlin(Command):
    def __init__(self, file_path):
        self.file_path = file_path

    def execute(self):
        output = subprocess.run(["kotlinc", self.file_path])
        print("output:", output)
        return None


class ExecuteJava(Command):
    def __init__(self, file_path):
        self.file_path = file_path

    def execute(self):
        output = subprocess.check_output(["java", self.file_path])
        print("output", output.returncode)
        return None


class ExecuteBash(Command):
    def __init__(self, file_path):
        self.file_path = file_path

    def execute(self):
        output = subprocess.run(["bash", self.file_path])
        print("output", output)
        return None

class ExecuteHandler():
    def __init__(self, file_path, commandType):
        ex = Command()

        if ex == "python":
            ex = ExecutePython()
            ex.execute(file_path)
        if ex == "kotlin":
            ex = ExecuteKotlin()
            ex.execute(file_path)

        if ex == "java":
            ex = ExecuteJava()
            ex.execute(file_path)

        if ex == "bash":
            ex = ExecuteBash()
            ex.execute(file_path)
        else:
            print("Can't be executed")


if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(ROOT_DIR, '/text.txt')

    handlerPython = PythonHandler(file_path)
    handlerKotlin = KotlinHandler(file_path)
    handlerJava = JavaHandler(file_path)
    handlerBash = BashHandler(file_path)
    unknown = UnknownHandler(file_path)

    handlerPython.nextCheck = handlerKotlin
    handlerKotlin.nextCheck = handlerJava
    handlerJava.nextCheck = handlerBash
    handlerBash.nextCheck = unknown

    commandType = handlerPython.handle()

    execute = ExecuteHandler(file_path, commandType)


