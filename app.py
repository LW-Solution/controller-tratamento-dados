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

    if keys:
        # Recupere todos os arquivos JSON
        files = [json.loads(r.get(key)) for key in keys]
        print(files)

        # Envie os arquivos para a rota especificada
        response = requests.post('http://localhost:3001/recepcao', json=files)

        # Se a resposta for bem-sucedida, exclua as chaves do Redis
        if response.status_code == 200:
            for key in keys:
                r.delete(key)
        else:
            print('Falha ao enviar arquivos, tentando novamente...')
    else:
        print('Não há dados para enviar')

# Agende o trabalho para ser executado a cada 10 segundos
schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)