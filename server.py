
#================ Importações ================================
import os  # manipular arquivos
import json  # salvar os dados em formato JSON
from http.server import SimpleHTTPRequestHandler, HTTPServer 
from urllib.parse import parse_qs  # para ler dados enviados por formulários
#=============================================================


class MyHandle(SimpleHTTPRequestHandler): #classe que trata todas as requisições (importante!!!!!!!)
    
    def list_directory(self, path): #usado para listar quando um diretorio é acessado
        try: 
            f = open(os.path.join(path, "index.html"), "r") #tenta abrir um arquivo index.html
            self.send_response(200) #envia um código de ok pro cliente
            self.send_header("Content-type", "text/html") #informa que a resposta é html
            self.end_headers() #finaliza o headers
            self.wfile.write(f.read().encode('utf-8')) #le o arquivo e o escreve em utf-8 pra evitar erros de acento
            f.close() #fecha o arquivo
            return None
        except FileNotFoundError: #se index não existir
            pass #ignora e deixa o metodo cair para o return abaixo
            return super().list_directory(path)

    #============================ login =====================================
    def account_user(self, login, password): #define metodo que verifica credenciais
        logar = "ketyaraujo@gmail.com"
        senha = "123456"
        
        if login == logar and senha == password: #realiza a verificação de email e senha
            return "Usuario logado com sucesso!" #se estiver certo, retorna mensagem de sucesso
        else:
            return "Usuário não existe!"  

    #================================ Inicia método GET ===================================
    def do_GET(self): 
        if self.path == "/login": # se a URL for login
            try: #tente 
                with open(os.path.join(os.getcwd(), "login.html"), encoding='utf-8') as login: 
                    content = login.read() #abrir o login html com utf-8
                    
                self.send_response(200) #se estiver ok
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found") #se não aparecer, dará erro 404
        
        #============ GET CADASTRO ================================  
        elif self.path == "/cadastro": #se a URL for cadastro
            try:
                with open(os.path.join(os.getcwd(), "cadastro.html"), encoding='utf-8') as cadastro: 
                    content = cadastro.read()
                    
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        
        #=================== GET LISTAR FILMES ===========================
        elif self.path == "/listar_filmes": #se a URL for listar_filmes
            
            arquivo = "filmes.json" #nome do arquivo esperado
            if os.path.exists(arquivo): #se o arquivo existe
                with open(arquivo, encoding="utf-8") as listinha: #tenta carregar o json
                    try:
                        filmes = json.load(listinha)
                    except json.JSONDecodeError:
                        filmes = [] 
            else:
                filmes = []
            
            with open (arquivo, "w", encoding="utf-8") as lista:
                json.dump(filmes, lista, indent=4, ensure_ascii=False)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
            
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

        elif self.path == "/send_cadastro":
            
            filme = {
                "nomeFilme": form_data.get("nomeFilme", [""])[0], 
                "atores": form_data.get("atores", [""])[0], 
                "diretor": form_data.get("diretor", [""])[0], 
                "ano": form_data.get("ano", [""])[0], 
                "genero": form_data.get("genero", [""])[0], 
                "produtora": form_data.get("produtora", [""])[0], 
                "sinopse": form_data.get("sinopse", [""])[0], 
            } 
            
            arquivo = "filme.json"
            if os.path.exists(arquivo):
                with open(arquivo, encoding="utf-8") as listinha:
                    try:
                        filmes = json.load(listinha)
                    except json.JSONDecodeError:
                        filmes = []
                filmes.append(filme)
            else:
                filmes = [filme]

            with open(arquivo, "w", encoding="utf-8") as lista:
                json.dump(filmes, lista, indent=4, ensure_ascii=False)
            
            self.send_response(303) 
            self.send_header("Content-type", "application/json") 
            self.end_headers()
            self.wfile()
               
        else: 
            self.send_error(404, "Rota POST não encontrada")

    def _send_html(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))
        
# Inicia o servidor
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server running in http://localhost:8000")
    httpd.serve_forever()

main()