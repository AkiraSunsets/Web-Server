'''

#=========================criando um servidor============================

from http.server import SimpleHTTPRequestHandler, HTTPServer #importa biblioteca para logar o server

#definindo a porta
port = 8000

#definindo o gerenciador/manipulador de requisições
handler = SimpleHTTPRequestHandler

#criar a instancia do servidor
server = HTTPServer(("localhost", port), handler)

#imprimindo uma mensagem de ok
print(f"Server Initiated in http://localhost:{port}")

server.serve_forever()

#====================================================================
'''

#segundo servidor

import os #manipular arquivos
from http.server import SimpleHTTPRequestHandler, HTTPServer

class MyHandle (SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f = open(os.path.join(path, "index.html"), "r")
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close()
            return None
        except FileNotFoundError:
            pass
            return super().list_directory(path)
        
    def do_GET(self):
           
            if self.path == "/login":
                try:
                    with open(os.path.join(os.getcwd(), "login.html"), encoding='utf-8') as login: 
                        content = login.read()
                        
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(content.encode("utf-8"))
                except FileNotFoundError:
                    self.send_error(404, "File Not Found")
                
            elif self.path == "/cadastro":
                try:
                    with open(os.path.join(os.getcwd(), "cadastro.html"), encoding='utf-8') as cadastro: 
                        content = cadastro.read()
                        
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(content.encode("utf-8"))
                except FileNotFoundError:
                    self.send_error(404, "File Not Found")
            
            elif self.path == "/listar_filmes":
                try:
                    with open(os.path.join(os.getcwd(), "listar_filmes.html"), encoding='utf-8') as listarfilmes: 
                        content = listarfilmes.read()
                        
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(content.encode("utf-8"))
                except FileNotFoundError:
                    self.send_error(404, "File Not Found")
            else:
                super().do_GET()          
        
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server running in http://localhost:8000")
    httpd.serve_forever()
main()
