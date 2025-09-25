import os  # manipular arquivos
import json  # salvar os dados em formato JSON
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs  # para ler dados enviados por formulários

class MyHandle(SimpleHTTPRequestHandler):
    
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

    def account_user(self, login, password):
        logar = "ketyaraujo@gmail.com"
        senha = "123456"
        
        if login == logar and senha == password:
            return "Usuario logado com sucesso!"
        else:
            return "Usuário não existe!" 

    def register_movie(self, data):
        movie = {
            "nome": data.get("nomeFilme", [""])[0],  # serve para pegar os dados enviados via POST, transforma tudo em um dicionário
            "atores": data.get("atores", [""])[0],
            "diretor": data.get("diretor", [""])[0],
            "ano": data.get("ano", [""])[0],
            "genero": data.get("genero", [""])[0],
            "produtora": data.get("produtora", [""])[0],
            "sinopse": data.get("sinopse", [""])[0],
        }
        
        # salvar arquivo filmes.txt em formato JSON
        with open("filmes.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(movie, ensure_ascii=False) + "\n")
        
        return f"Filme '{movie['nome']}' cadastrado com sucesso!"

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
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        form_data = parse_qs(body)

        if self.path == '/send_login':
            login = form_data.get('email', [""])[0]
            password = form_data.get('password', [""])[0]
            logou = self.account_user(login, password)
            print('Data Form:')
            print('Email:', form_data.get('email', [""])[0])
            print('Password:', form_data.get('password', [""])[0])

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(logou.encode('utf-8'))

        elif self.path == '/send_cadastro':
            print("Data Form Cadastro Filme: ")
            for key, value in form_data.items():
                print(f"{key}: {value}")
            
            resposta = self.register_movie(form_data)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(resposta.encode('utf-8'))

        else:
            super(MyHandle, self).do_POST()

# Inicia o servidor
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server running in http://localhost:8000")
    httpd.serve_forever()

main()
