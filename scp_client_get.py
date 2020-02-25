import sublime
import sublime_plugin
import os
import base64
import datetime

class scp_client_get(sublime_plugin.TextCommand):
    server = port = passwd = remote_file = local_file = ""
    offerServerPort = offerPasswd = offerRemoteFile = ""
    
    def run(self, edit):
        try:
            defaultValuesForOffer = open("/tmp/scp_config_sublime.txt", "r")
            parseConfig = defaultValuesForOffer.readlines()
            offerServerPort = parseConfig[0].strip()
            offerPasswd = parseConfig[1].strip()
            offerRemoteFile = parseConfig[2].strip()
            defaultValuesForOffer.close()
        except Exception as e:
            offerServerPort = "192.168.1.125:22"
            offerPasswd = "fedoraarm"
            offerRemoteFile = "/home/sh2/logic.xml"
        def on_savePasswd(input_string):
            self.passwd = input_string
            window.show_input_panel("remote_file", offerRemoteFile, on_saveFileSource, on_change, on_cancel)
        def on_saveServerPort(input_string):
            self.server = input_string.split(':')[0]
            self.port = input_string.split(':')[1]
            window.show_input_panel("password", offerPasswd, on_savePasswd, on_change, on_cancel)
        def on_change(input_string):
            pass
        def on_cancel():
            pass
        window = self.view.window()
        # начинается макаронный ввод данных
        window.show_input_panel("server:port", offerServerPort, on_saveServerPort, on_change, on_cancel)

        #конец макаронного ввода, продолжаем работать в функции on_saveFileSource
        def on_saveFileSource(input_string):
            #тут перезаписываем данные для следующего предложения 
            self.remote_file = input_string

            defaultValuesForOffer = open("/tmp/scp_config_sublime.txt", "w")
            writeOffer = self.server + ":" + self.port + "\n" + self.passwd + "\n" + self.remote_file
            defaultValuesForOffer.write(writeOffer)
            defaultValuesForOffer.close()


            #тут качаем файл в папку tmp/локальное_время и создаем конфиг для последующей загрузки этого же файла на сервер
            file_name = self.remote_file[self.remote_file.rindex("/")+1:]
            stringWithData = self.server + "\n" + self.port + "\n" + self.passwd + "\n" + self.remote_file + "\n/dev/null" 
            now = datetime.datetime.now()
            name_local_dir = str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) 
            os.mkdir("/tmp/"+name_local_dir) 
            localConfig = open("/tmp/"+name_local_dir + "/config_krakozyabala.txt", "w")
            localConfig.write(stringWithData)
            localConfig.close()
            runav = "sshpass -p '"+self.passwd+"' scp -P "+self.port+" root@"+self.server+":"+ self.remote_file+" /tmp/"+name_local_dir 
            # после scp  в предыдущей команде указывается источник, а потом куда положить
            returnedvalue = os.system(runav)
            if returnedvalue==0 :
                window.open_file('/tmp/'+name_local_dir+"/"+file_name , sublime.ENCODED_POSITION)
            if returnedvalue==256: 
                sublime.error_message("File not found on server or server is down")