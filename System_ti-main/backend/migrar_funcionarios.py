import sqlite3

# Caminho do banco de dados SQLite
DB_PATH = 'system_ti.db'  # ajuste se necessário

# Conexão com o banco
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# 1. Obter estrutura da tabela original
cursor.execute('PRAGMA table_info(funcionarios)')
table_info = cursor.fetchall()

# 2. Montar lista de colunas e tipos, exceto setor_id
columns = []
columns_types = []
for col in table_info:
    if col[1] != 'setor_id':
        columns.append(col[1])
        # col[2] = tipo, col[3] = NOT NULL, col[5] = PK
        col_def = f"{col[1]} {col[2]}"
        if col[3]:
            col_def += " NOT NULL"
        # Corrige PK para manter apenas no campo id
        if col[5] and col[1] == 'id':
            col_def += " PRIMARY KEY AUTOINCREMENT"
        columns_types.append(col_def)

columns_str = ', '.join(columns)
columns_types_str = ',\n    '.join(columns_types)

# 3. Exportar dados
cursor.execute(f'SELECT {columns_str} FROM funcionarios')
funcionarios_data = cursor.fetchall()

# 4. Excluir tabela antiga
cursor.execute('DROP TABLE funcionarios')

# 5. Criar nova tabela com os mesmos campos (exceto setor_id)
cursor.execute(f'''
CREATE TABLE funcionarios (
    {columns_types_str}
)
''')

# 6. Reimportar dados
placeholders = ', '.join(['?'] * len(columns))
cursor.executemany(
    f'INSERT INTO funcionarios ({columns_str}) VALUES ({placeholders})',
    funcionarios_data
)

conn.commit()
conn.close()

print('Migração concluída: setor_id removido da tabela funcionarios.')
