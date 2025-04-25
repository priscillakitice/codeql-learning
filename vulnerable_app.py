from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Criar uma conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar a tabela de usuários
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializar o banco de dados
init_db()

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Vulnerabilidade: SQL Injection
    # O usuário pode inserir SQL malicioso no campo username
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    conn = get_db_connection()
    user = conn.execute(query, (username, password)).fetchone()
    conn.close()
    
    if user:
        return "Login bem-sucedido!"
    else:
        return "Login falhou!"

if __name__ == '__main__':
    app.run(debug=True) 