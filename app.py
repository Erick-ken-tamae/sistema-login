from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "segredo"

# Criar banco de dados
def criar_banco():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(           
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        senha TEXT
    )
    """)   #criar uma tebela de usuario para cadastrar o email e a senha

    conn.commit()
    conn.close()

criar_banco()


# Página de login
@app.route("/")
def login():
    return render_template("login.html")


# Fazer login
@app.route("/login", methods=["POST"])
def fazer_login():

    usuario = request.form["usuario"]
    senha = request.form["senha"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
 
    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
        (usuario, senha)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        session["usuario"] = usuario
        return redirect("/dashboard")
    else:
        return "Login inválido"


# Página cadastro
@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


# Registrar usuário
@app.route("/registrar", methods=["POST"])
def registrar():

    usuario = request.form["usuario"]
    senha = request.form["senha"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

# verificar se tem @
    if "@" not in usuario:
        return "Email inválido. Precisa ter @"
    
#verifica se o usuario ja existe
    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=?",
        (usuario,)
    )
    user = cursor.fetchone()
    
    if user:
        conn.close()
        return "Usuário já existe"
#cadastrar novo usuario
    cursor.execute(
        "INSERT INTO usuarios (usuario, senha) VALUES (?,?)",  #Esse comando faz o usuario cadastrar(o SENHA e o EMAIL)
        (usuario, senha)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# Dashboard
@app.route("/dashboard")
def dashboard():

    if "usuario" in session:
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
    
        cursor.execute(
        "SELECT id,usuario FROM usuarios"
        )
        usuarios = cursor.fetchall()
        
        quantidade = len(usuarios) #ele lê a quantidade de usuario cadastrado 
        conn.close()
        return render_template(
            "dashboard.html", 
            usuario=session["usuario"],
            usuarios=usuarios,
            quantidade=quantidade)
    else:
        return redirect("/")

#Deletar o usuário
@app.route("/deletar/<int:id>")
def deletar(id):
    conn = sqlite3.connect("database.db") #conecta no database(conecta no banco de dados)
    cursor = conn.cursor()
    

    cursor.execute(     
        "DELETE FROM usuarios WHERE id=?", #comando delete para deletar o email
        (id,)
    )
    
    conn.commit()
    conn.close()   
    return redirect("/dashboard")
# Logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)