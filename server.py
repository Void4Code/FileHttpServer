import socket
import threading

port = 8080
host = ''

class httpFileServer:
    def __init__(self):
        #Doing the TCP default connection on port 8080
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as tcp_connection:
            tcp_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            tcp_connection.bind((host,port))
            tcp_connection.listen(4096)
            print("Sucess! Listening to port:",port)

            #Getting all connections
            while True:
                con, addr = tcp_connection.accept()
                users = threading.Thread(target = self.fileDownload, args=(con,))
                users.start()

            tcp_connection.close()

    
    def fileDownload(self, con):
        try:
            info = con.recv(2048).decode('utf-8')
            if not info:
                con.close()
                return
                
            #Gets the filename to download
            filename  = info.split()[1]
            con.sendall(bytes(f"\nHTTP/1.1 200 ok\nContent-Disposition: attachment; filename={filename[1:]}\n\n",'utf-8'))
                
            #Open and send file
            with open(filename[1:], "rb") as f:
                con.sendfile(f)
            con.close()
            
        except(IOError):
            print(info)

