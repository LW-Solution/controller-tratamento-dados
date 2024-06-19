import unittest
import redis


def conectar():
    r = redis.Redis(
        host='redis-16145.c308.sa-east-1-1.ec2.redns.redis-cloud.com',
        port=16145,
        password='YM2ScUpkcKu2ac8tGrACBxOtjNMzDnXT')
    return r


class TestApp(unittest.TestCase):
    def testandoGetNoBanco(self):
        conexaoComBanco = conectar()
        itemsBuscados = conexaoComBanco.get("4022D87402B8")
        self.assertIsNone(itemsBuscados)
        print("Teste de get no banco")