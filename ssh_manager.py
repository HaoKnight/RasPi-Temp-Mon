import paramiko

class SSHManager:
    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password
        self.ssh = paramiko.SSHClient() # 创建 SSHClient 实例
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # 设置自动添加主机密钥的策略
        try:
            self.ssh.connect(ip, username=user, password=password) # 连接到树莓派
        except paramiko.AuthenticationException:
            print("Authentication failed") # 认证失败，打印错误信息
        except paramiko.SSHException as e:
            print("SSH error:", str(e)) # SSH 连接错误，打印错误信息

    def get_temperature(self):
        try:
            stdin, stdout, stderr = self.ssh.exec_command('vcgencmd measure_temp') # 执行获取温度命令
            temperature = stdout.readlines()[0].strip() # 从输出中获取温度数据
            return temperature
        except paramiko.SSHException as e:
            print("SSH error:", str(e)) # SSH 连接错误，打印错误信息

    def close(self):
        self.ssh.close() # 关闭 SSH 连接
