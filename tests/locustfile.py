from locust import HttpUser, task, between
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
import os


# app_ip = '35.192.180.16'
app_ip = os.environ['app_ip']

class ForumUser(HttpUser):
    # tempo de espera entre as tarefas (em segundos) que neste caso é entre 2 e 5 segundos aleatoriamente
    wait_time = between(2, 5)
    # Lista para armazenar os URLs encontrados
    urls_list = []
    
    def on_start(self):
        self.login()

    # Realiza pedido GET para obter o token CSRF e, em seguida, realiza pedido POST para fazer login
    def login(self):
        response = self.client.get("/login")
        csrftoken = re.search('meta name="csrf-token" content="(.+?)"', response.text).group(1)
        if csrftoken:
            post_data = {'username': "testing", 'password': 'password', "_token": csrftoken }
            with self.client.post('/login', post_data, catch_response=True) as response:
                print("Code: ", response.status_code)


    @task
    # Realiza pedido POST para criar uma thread
    def create_thread(self):
        with self.client.get("/login") as response:
            if response.status_code // 100 == 2:

                csrftoken = re.search('meta name="csrf-token" content="(.+?)"', response.text)
                if csrftoken:
                    headers = {'Content-Type': 'application/json', 'X-CSRF-Token': csrftoken.group(1)}
                    post_data = {
                        "subject": "JSON é Comum",
                        "body": "A maioria das APIs modernas usa JSON (JavaScript Object Notation) como formato de intercâmbio de dados devido à sua simplicidade e facilidade de leitura tanto para humanos quanto para máquinas.",
                        "tags": ["API"]
                    }

                    with self.client.post('/forum/create-thread', json=post_data, catch_response=True, headers=headers) as response:
                        print("Code: ", response.status_code)
                        if response.status_code // 100 == 2:
                            response.success()
                        else:
                            response.failure("Got wrong response code while creating a thread")   
            else:
                response.failure("Got wrong response code while logging in")

    
    @task
    # Realiza pedido POST para logout
    def logout(self):
        with self.client.get("/login") as response:
            if response.status_code // 100 == 2:

                csrftoken = re.search('meta name="csrf-token" content="(.+?)"', response.text)
                if csrftoken:
                    headers = {'Content-Type': 'application/json', 'X-CSRF-Token': csrftoken.group(1)}

                    with self.client.post('/logout', catch_response=True, headers=headers) as response:
                        print("Code: ", response.status_code)
                        if response.status_code // 100 == 2:
                            response.success()
                        else:
                            response.failure("Got wrong response code while creating a thread")
            else:
                response.failure("Got wrong response code while logging in")
    
    @task
    # Realiza pedido GET para obter threads
    def get_threads(self):
        headers = {'Content-Type': 'application/json'}

        response = self.client.get('/forum', headers=headers)

        if response.status_code // 100 == 2:
        
            print(response.status_code)
            if response.status_code // 100 == 2: # Verificar se a solicitação foi bem-sucedida (código de status 2xx)
            
                soup = BeautifulSoup(response.text, 'html.parser')

                links = soup.find_all('a', href=True)
                self.urls_list = []
                # Iterar sobre todos os links e adicionar ao urls_list
                for link in links:
                    absolute_url = urljoin('http://' + app_ip + '/forum/', link['href'])
                    
                    # Verificar se o URL começa com 'http://+ app_ip + /forum/' e não contém '/tags/'
                    if absolute_url.startswith('http://' + app_ip + '/forum/') and '/tags/' not in absolute_url and '/create-thread' not in absolute_url and '/feed' not in absolute_url:
                        self.urls_list.append(absolute_url)
                    
        else:
            response.failure(f"Erro ao obter threads. Código de status: {response.status_code}")

        



    @task
    # Realiza pedido GET para obter detalhes da thread pelo nome
    def get_thread_details_by_name(self):
        headers = {'Content-Type': 'application/json'}

        if self.urls_list:
            count = random.randint(0, len(self.urls_list)-1)
            link = self.urls_list[count]

            name = link[len('http://' + app_ip + '/forum/'):]

            response = self.client.get(f'/forum/{name}', headers=headers)

            if response.status_code // 100 == 2:
                response.success()
        else:
            response.failure(f"Erro ao obter detalhes da thread pelo nome. Código de status: {response.status_code}")

        
        
        
    @task
    # Realiza pedido GET para obter artigos
    def get_articles(self):
        headers = {'Content-Type': 'application/json'}

        response = self.client.get('/articles', headers=headers)

        if response.status_code // 100 == 2:
                response.success()
        else:
            response.failure(f"Erro ao obter artigos. Código de status: {response.status_code}")

