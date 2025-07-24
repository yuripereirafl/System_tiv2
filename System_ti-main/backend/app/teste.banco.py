import sqlite3

class BancoConsulta:
    def __init__(self, db_path='../system_ti.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def listar_tabelas(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = self.cursor.fetchall()
        print('Tabelas encontradas:')
        for tabela in tabelas:
            print('-', tabela[0])

    def listar_usuarios(self):
        try:
            self.cursor.execute("SELECT * FROM usuarios;")
            usuarios = self.cursor.fetchall()
            print('Usuários:')
            for usuario in usuarios:
                print(usuario)
        except Exception as e:
            print('Erro ao consultar tabela usuarios:', e)

    def fechar(self):
        self.conn.close()

if __name__ == '__main__':
    banco = BancoConsulta()
    banco.listar_tabelas()
    banco.listar_usuarios()
    banco.fechar()
