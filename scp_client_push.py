import sublime
import sublime_plugin
import os
import base64
import datetime
import shutil

class scp_client_push(sublime_plugin.TextCommand):
    server = port = passwd = remote_file = local_file  = ""
    offerServerPort = offerPasswd = offerRemoteFile = ""

    def run(self, edit):
        try:
            defaultValuesForOffer = open("/tmp/scp_config_sublime.txt", "r")
            parseConfig = defaultValuesForOffer.readlines()
            offerServerPort = parseConfig[0].strip()
            offerPasswd = parseConfig[1].strip()
            offerRemoteFile = parseConfig[2].strip()[:parseConfig[2].strip().rindex("/")+1]
            defaultValuesForOffer.close()
        except Exception as e:
            offerServerPort = "192.168.1.125:22"
            offerPasswd = "fedoraarm"
            offerRemoteFile = "/home/sh2/"
        #currentPathToLocalFile = sublime.View.file_name(sublime.Window.active_view(sublime.active_window()))
        #offerRemoteFile = offerRemoteFile + currentPathToLocalFile[currentPathToLocalFile.rindex("/")+1:]
        def on_savePasswd(input_string):
            self.passwd = input_string
            window.show_input_panel("remote_file", offerRemoteFile+currentPathToLocalFile[currentPathToLocalFile.rindex("/")+1:] , on_saveFileSource, on_change, on_cancel)
        def on_saveServerPort(input_string):
            self.server = input_string.split(':')[0]
            self.port = input_string.split(':')[1]
            window.show_input_panel("password", offerPasswd, on_savePasswd, on_change, on_cancel)

        def on_saveFileSource(input_string): 
            #тут перезаписываем данные для следующего предложения 
            self.remote_file = input_string
            
            defaultValuesForOffer = open("/tmp/scp_config_sublime.txt", "w")
            writeOffer = self.server + ":" + self.port + "\n" + self.passwd + "\n" + self.remote_file
            defaultValuesForOffer.write(writeOffer)
            defaultValuesForOffer.close()


            file_name = self.remote_file[self.remote_file.rindex("/")+1:]
            now = datetime.datetime.now()
            name_local_dir = str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) 
            os.mkdir("/tmp/"+name_local_dir) 
            currentPathToLocalFile = sublime.View.file_name(sublime.Window.active_view(sublime.active_window()))
            file_name = self.remote_file[self.remote_file.rindex("/")+1:]
            self.local_file = currentPathToLocalFile
            #делаем копию файла, который писали, в tmp/наша_папка
            stringWithData = self.server + "\n" + self.port + "\n" + self.passwd + "\n" + self.remote_file + "\n" + self.local_file
            
            shutil.copy(currentPathToLocalFile, "/tmp/"+name_local_dir+"/"+file_name)
            localConfig = open("/tmp/"+name_local_dir + "/config_krakozyabala.txt", "w")
            localConfig.write(stringWithData)
            localConfig.close()
            window.open_file('/tmp/'+name_local_dir+"/"+file_name , sublime.ENCODED_POSITION)
            #закончил тут, редачу путь , правильная команда : sshpass  -p '7nGl6SaRF133' scp -P 22 /tmp/logic.xml1111 root@185.154.12.6:/tmp/
            runav = "sshpass -p '"+self.passwd+"' scp -P "+self.port+" /tmp/"+name_local_dir+"/"+ file_name + " root@"+self.server+":"+ self.remote_file
            returnedvalue = os.system(runav)
            if returnedvalue==0 :
                sublime.status_message("File was successfully pushed")
            if returnedvalue==256: 
                sublime.error_message("File wasn't pushed to server or server is down")

        def on_change(input_string):
            pass
        def on_cancel():
            pass
        window = self.view.window()
        def on_done(k):
            print(k)
            if (k==0):
                window.show_input_panel("server:port", offerServerPort, on_saveServerPort, on_change, on_cancel)
        currentPathToLocalFile = sublime.View.file_name(sublime.Window.active_view(sublime.active_window())) #имя локального файла
        localDirName = currentPathToLocalFile[:currentPathToLocalFile.rindex("/")]
        print (localDirName)
        

        try:
            localConfig = open(localDirName+"/config_krakozyabala.txt", "r")
            print(localDirName)
            parseConfig = localConfig.readlines()
            self.server = parseConfig[0].strip()
            self.port = parseConfig[1].strip()
            self.passwd = parseConfig[2].strip()
            self.remote_file = parseConfig[3].strip()
            self.local_file = parseConfig[4].strip()
            localConfig.close()
            #print (self.server, self.port, self.passwd, self.remote_file)
            runav = "sshpass -p '"+self.passwd+"' scp -P "+self.port+" "+sublime.View.file_name(sublime.Window.active_view(sublime.active_window())) + " root@"+self.server+":"+ self.remote_file
            print(runav)
            returnedvalue = os.system(runav)
            if returnedvalue==0 :
                sublime.status_message("File was successfully pushed")
                if self.local_file != "/dev/null" :
                	shutil.copy(sublime.View.file_name(sublime.Window.active_view(sublime.active_window())), self.local_file)
            if returnedvalue==256: 
                sublime.error_message("File wasn't pushed to server or server is down")

        except FileNotFoundError: 
            #sublime.error_message("Config file not found")
            quickDec = ["конфигурационного файла нет. нужно создать? -- да","конфигурационного файла нет. нужно создать? -- нет"]
            window.show_quick_panel(quickDec, on_done, sublime.MONOSPACE_FONT)



        
