import unittest
import redis


def conectar():
    r = redis.Redis(
        host='redis-16145.c308.sa-east-1-1.ec2.redns.redis-cloud.com',
        port=16145,
        password='YM2ScUpkcKu2ac8tGrACBxOtjNMzDnXT')
    return r


class TestApp(unittest.TestCase):
    def testandoConexao(self):
        conexaoComBanco = conectar()
        self.assertIsInstance(conexaoComBanco, redis.Redis)
        self.assertTrue(conexaoComBanco.ping(), "Teste de conexao falhou")

if __name__ == '__main__':
    unittest.main