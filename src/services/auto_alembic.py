import subprocess

class Automatic_Alembic():
    
    def automatic_migrate(self):
        resp = self.__cmd('alembic check')
        if 'FAILED: Target database is not up to date.' in resp:
            return self.__cmd('alembic upgrade head')
        else:
            return resp
    def stamp_head(self):
        return self.__cmd('alembic stamp head')
    
    def __cmd(self, command:str):
        str_arguments = ""
        CMD = command
        p = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        str_arguments = p.stdout.read()
        try:
            str_arguments = f"{str_arguments.decode('ascii')}\n"
        except:
            str_arguments = f"{str_arguments.decode('utf-8')}\n"
        
        return str_arguments