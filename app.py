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
    try:
        # Verifique se há chaves no Redis
        keys = r.keys()
        if keys:
            for key in keys:
                # Recupere os dados em JSON do Redis
                json_data = r.get(key)
                if json_data:
                    files = json_data.decode("utf-8").replace("'", '"').strip('"')
                    files = json.loads(files)
                    print("Dados recuperados do Redis:")
                    print(files)

                    # Enviar os dados para o servidor HTTP
                    headers = {'Content-Type': 'application/json'}
                    url = 'http://host.docker.internal:3001/recepcao'
                    response = requests.post(url, headers=headers, json=files)

                    # Verificar resposta do servidor HTTP
                    if response.status_code == 200:
                        print('Dados enviados com sucesso.')
                        # Se a resposta for bem-sucedida, exclua a chave do Redis
                        r.delete(key)
                    else:
                        print('Falha ao enviar dados para o servidor.')
                        print(response.status_code)
                        print(response.text)
        else:
            print('Não há dados para enviar.')
    except Exception as e:
        print(f'Erro: {e}')

# Agende o trabalho para ser executado a cada 10 segundos
schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
