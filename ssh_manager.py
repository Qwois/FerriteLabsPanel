import paramiko

class SSHClient:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ssh_client = None

    def connect(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(self.hostname, username=self.username, password=self.password)

    def disconnect(self):
        if self.ssh_client:
            self.ssh_client.close()

    def list_directory(self, path):
        stdin, stdout, stderr = self.ssh_client.exec_command(f'ls -l {path}')
        return stdout.read().decode('utf-8').splitlines()

    def navigate_directory(self, path):
        return self.list_directory(path)

    def read_file(self, file_path):
        stdin, stdout, stderr = self.ssh_client.exec_command(f'cat {file_path}')
        return stdout.read().decode('utf-8')
