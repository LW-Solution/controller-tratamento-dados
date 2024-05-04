import json
import requests
import schedule
import redis
import time

def conectar():
    r = redis.Redis(
        host='redis-16145.c308.sa-east-1-1.ec2.redns.redis-cloud.com',
        port=16145,
        password='YM2ScUpkcKu2ac8tGrACBxOtjNMzDnXT')
    return r

# Conecte-se ao Redis
r = conectar()

# Exclua todas as chaves do Redis
r.flushdb()

def job():
    # Verifique se há chaves no Redis
    keys = r.keys()
    try:
        if keys:
            # Recupere todos os arquivos JSON
            for key in keys: 
                files = json.loads((r.get(key).decode('utf-8')))
            print(files)
          
            headers = {'Content-Type': 'application/json'}
            url = 'http://localhost:3001/recepcao'
            response = requests.post(url, headers=headers, data=files)

            # Se a resposta for bem-sucedida, exclua as chaves do Redis
            if response.status_code == 200:
                for key in keys:
                    r.delete(key)
            else:
                print('Falha ao enviar arquivos, tentando novamente...')
                print(response.status_code)
                print(response.text)
        else:
            print('Não há dados para enviar')
    except Exception as e:
        print(f'Erro: {e}')

# Agende o trabalho para ser executado a cada 10 segundos
schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
