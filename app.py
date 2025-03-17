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

    if not all([titulo, categoria, autor, imagem_url]):
        return jsonify({'erro':'todos os campos são obrigatórios'}), 400
    
    with sqlite3.connect('database.db') as conn:
        conn.execute(f"""  INSERT INTO livros (titulo, categoria, autor, imagem_url) values (?,?,?,?)""",(titulo,categoria,autor,imagem_url))
        
        conn.commit()

        return jsonify({'mensagem': 'livros cadastrados com sucesso'}), 201

@app.route('/livros', methods=['GET'])
def listar_livros():
    with sqlite3.connect('database.db') as conn:
        livros = conn.execute("SELECT * FROM livros").fetchall()
    
    livros_formatados =[]
    
    for livro in livros:
        dicionario_livros ={
            'id':livro[0],
            'titulo':livro[1],
            'categoria':livro[2],
            'autor':livro[3],
            'imagem_url':livro[4]
        }
        livros_formatados.append(dicionario_livros)
    return jsonify(livros_formatados)
if __name__ == "__main__":
    app.run(debug=True)