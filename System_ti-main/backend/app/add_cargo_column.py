import sqlite3

conn = sqlite3.connect('../system_ti.db')
cursor = conn.cursor()
cursor.execute('ALTER TABLE funcionarios ADD COLUMN cargo TEXT;')
conn.commit()
conn.close()
print('Coluna cargo adicionada com sucesso!')