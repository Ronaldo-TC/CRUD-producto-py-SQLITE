from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Inicializar la base de datos


def init_db():
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()

# Ruta para la página principal (lista de productos)


@app.route('/')
def index():
    conn = sqlite3.connect('almacen.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

# Ruta para crear un nuevo producto


@app.route('/crear', methods=['POST'])
def crear():
    descripcion = request.form['descripcion']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO producto (descripcion, cantidad, precio) VALUES (?, ?, ?)",
                   (descripcion, cantidad, precio))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Ruta para editar un producto existente


@app.route('/editar/<int:id>')
def editar(id):
    conn = sqlite3.connect('almacen.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template('editar.html', producto=producto)

# Ruta para guardar los cambios de un producto editado


@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    descripcion = request.form['descripcion']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE producto SET descripcion = ?, cantidad = ?, precio = ? WHERE id = ?",
                   (descripcion, cantidad, precio, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Ruta para eliminar un producto


@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM producto WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
