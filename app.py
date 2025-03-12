from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS livros(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     titulo TEXT NOT NULL,
                     categoria TEXT NOT NULL,
                     autor TEXT NOT NULL,
                     imagem_url TEXT NOT NULL
                     )""")
        print("banco de dados inicializado")

init_db()

### print(__name__)

@app.route('/')
def homepage():
    return '<h2>Bom Diaaaaaaaa!</h2>'

@app.route('/doar', methods=['POST'])
def doar():
    dados = request.get_json()

    titulo = dados.get('titulo')
    categoria = dados.get('categoria')
    autor = dados.get('autor')
    imagem_url = dados.get('imagem_url')

    if not titulo or not categoria or not autor or not imagem_url:
        return jsonify({'erro':'todos os campos são obrigatórios'}), 400
    
    with sqlite3.connect('database.db') as conn:
        conn.execute(f"""  INSERT INTO livros (titulo, categoria, autor, imagem_url) values 
                           ('{titulo},{categoria},{autor},{imagem_url}') """)
        
        conn.commit()

        return jsonify({'mensagem': 'livros cadastrados com sucesso'}), 201

if __name__ == "__main__":
    app.run(debug=True)