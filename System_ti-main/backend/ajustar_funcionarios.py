import sqlite3

DB_PATH = 'system_ti.db'
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Adiciona os campos ausentes na tabela funcionarios
try:
    cursor.execute("ALTER TABLE funcionarios ADD COLUMN sobrenome TEXT")
except sqlite3.OperationalError:
    print("Campo 'sobrenome' já existe.")

try:
    cursor.execute("ALTER TABLE funcionarios ADD COLUMN celular TEXT")
except sqlite3.OperationalError:
    print("Campo 'celular' já existe.")

try:
    cursor.execute("ALTER TABLE funcionarios ADD COLUMN grupo_email TEXT")
except sqlite3.OperationalError:
    print("Campo 'grupo_email' já existe.")

conn.commit()
conn.close()
print('Campos sobrenome e celular adicionados na tabela funcionarios.')
print("Campo grupo_email adicionado na tabela funcionarios.")
