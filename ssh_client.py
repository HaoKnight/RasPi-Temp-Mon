import paramiko


class SSHClient:
    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        self.ssh.connect(self.ip, username=self.user, password=self.password)

    def get_temperature(self):
        stdin, stdout, stderr = self.ssh.exec_command('vcgencmd measure_temp')
        temperature = stdout.readlines()[0].strip()
        return temperature

    def close(self):
        self.ssh.close()
