import os

import oracledb


def escapar(valor) -> str:
    """Escapa aspas simples para uso em SQL montado por concatenação."""
    return str(valor).replace("'", "''")


class OracleQueries:
    """Módulo de conexão com o Oracle.

    Credenciais vêm de variáveis de ambiente (não deixe senha no código):
        ORACLE_USER, ORACLE_PASSWORD e ORACLE_DSN (padrão: localhost:1521/XEPDB1)
    """

    def __init__(self):
        self.user = os.getenv("ORACLE_USER", "")
        self.password = os.getenv("ORACLE_PASSWORD", "")
        self.dsn = os.getenv("ORACLE_DSN", "localhost:1521/XEPDB1")
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = oracledb.connect(user=self.user, password=self.password, dsn=self.dsn)
        self.cursor = self.conn.cursor()
        return self

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def query(self, sql: str) -> list:
        """Executa um SELECT e devolve uma lista de dicionários (chaves em minúsculo)."""
        self.cursor.execute(sql)
        colunas = [c[0].lower() for c in self.cursor.description]
        return [dict(zip(colunas, linha)) for linha in self.cursor.fetchall()]

    def write(self, sql: str):
        """Executa um INSERT, UPDATE ou DELETE e confirma (commit)."""
        self.write_many([sql])

    def write_many(self, comandos: list):
        """Executa vários comandos na mesma transação: ou todos funcionam, ou nenhum."""
        try:
            for comando in comandos:
                self.cursor.execute(comando)
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
