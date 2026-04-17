import sqlite3

def inicializar_banco():
    # ETAPA 1: Conexão
    # Conecta ao banco de dados. Se o arquivo não existir, o Python cria ele na mesma pasta.
    print("Conectando ao banco de dados...")
    conexao = sqlite3.connect('banco_whatsapp.db')
    
    # O cursor é a ferramenta que usamos para enviar os comandos SQL para o banco
    cursor = conexao.cursor()

    # ETAPA 2: Configuração de segurança
    # Por padrão, o SQLite mantém as chaves estrangeiras (Foreign Keys) desativadas. 
    # Precisamos ativar para garantir a integridade entre Clientes e Palavras.
    cursor.execute('PRAGMA foreign_keys = ON;')

    # ETAPA 3: Criar a tabela 'Clientes'
    # Usamos IF NOT EXISTS para evitar erros caso você rode o script duas vezes
    print("Criando tabela 'Clientes'...")
    sql_clientes = """
    CREATE TABLE IF NOT EXISTS Clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT NOT NULL,
        id_grupo_whatsapp TEXT NOT NULL
    );
    """
    cursor.execute(sql_clientes)

    # ETAPA 4: Criar a tabela 'Palavras'
    # Aqui criamos a ligação (Foreign Key) apontando o 'id_cliente' para o 'id' da tabela Clientes
    print("Criando tabela 'Palavras'...")
    sql_palavras = """
    CREATE TABLE IF NOT EXISTS Palavras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        palavra_chave TEXT NOT NULL,
        FOREIGN KEY (id_cliente) REFERENCES Clientes (id) ON DELETE CASCADE
    );
    """
    cursor.execute(sql_palavras)

    # ETAPA 5: Salvar e Fechar
    # O 'commit' é o que efetivamente salva as mudanças no arquivo do banco de dados
    conexao.commit()
    conexao.close()
    print("✅ Banco de dados e tabelas criados com sucesso!")

# Executa a função quando rodamos o arquivo
if __name__ == '__main__':
    inicializar_banco() 