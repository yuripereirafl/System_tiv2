import sqlite3

conn = sqlite3.connect('../system_ti.db')
cursor = conn.cursor()

print('Tabelas no banco:')
for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    print(row[0])

print('\nEstrutura de cada tabela:')
tables = [row[0] for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")]
for table in tables:
    print(f'\nTabela: {table}')
    for col in cursor.execute(f'PRAGMA table_info({table});'):
        print(col)

conn.close()
