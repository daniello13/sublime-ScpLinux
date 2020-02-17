import sublime
import sublime_plugin
import os
#import paramiko
import base64

class scp_client(sublime_plugin.TextCommand):
    server = port = passwd = file_source = ""
    
    def run(self, edit):
        #def createSSHClient(server, port, user, password):
        #    client = paramiko.SSHClient()
        #    client.load_system_host_keys()
        #    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #    client.connect(server, port, user, password)
        #    return client
        def on_savePasswd(input_string):
            self.passwd = input_string
            window.show_input_panel("file_source", "/home/sh2/logic.xml", on_saveFileSource, on_change, on_cancel)
        def on_saveServerPort(input_string):
            self.server = input_string.split(':')[0]
            self.port = input_string.split(':')[1]
            window.show_input_panel("password", "fedoraarm", on_savePasswd, on_change, on_cancel)
        def on_change(input_string):
            pass
        def on_cancel():
            pass
        window = self.view.window()
        # начинается макаронный ввод данных
        window.show_input_panel("server:port", "192.168.1.125:22", on_saveServerPort, on_change, on_cancel)

        #конец макаронного ввода, продолжаем работать в функции on_saveFileSource
        def on_saveFileSource(input_string):
            self.file_source = input_string
            print(self.server, self.port, self.passwd, self.file_source)
            #cmd_get="python3 scp_get.py " +  self.server + " " + self.port + " " +  self.passwd + " " + self.file_source
            #print(cmd_get)
            #tmp=os.system(cmd_get)
            #print(tmp)
            runav = "cat /etc/*release >> /tmp/1.txt" #тут будет так: sshpass -p 'password' scp file.tar.gz root@xxx.xxx.xxx.194:/backup
            # после scp  в предыдущей команде указывается источник, а потом куда положить
            returnedvalue = os.system(runav)
            print (returnedvalue)

            #ssh = createSSHClient(self.server, self.port, "root", self.passwd)
            #with SCPClient(ssh.get_transport()) as scp:
            #    scp.get(self.file_source, local_path='/tmp/')
            #    print("OK")
