from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ... (código para inicializar la base de datos) ...


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/productos")
def productos():
    conn = sqlite3.connect("almacen.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template("productos/index.html", productos=productos)


@app.route("/productos/create")
def productos_create():
    return render_template('productos/create.html')


@app.route("/productos/create/save", methods=['POST'])
def productos_save():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = float(request.form['precio'])

    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO productos (nombre, descripcion, precio) VALUES (?, ?, ?)",
                   (nombre, descripcion, precio))

    conn.commit()
    conn.close()
    return redirect('/productos')


@app.route("/productos/edit/<int:id>")
def productos_edit(id):
    conn = sqlite3.connect("almacen.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template("productos/edit.html", producto=producto)


@app.route("/productos/update", methods=['POST'])
def productos_update():
    id = request.form['id']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = float(request.form['precio'])

    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE productos SET nombre=?, descripcion=?, precio=? WHERE id=?",
                   (nombre, descripcion, precio, id))

    conn.commit()
    conn.close()
    return redirect("/productos")


@app.route("/productos/delete/<int:id>")
def productos_delete(id):
    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/productos')


if __name__ == "__main__":
    app.run(debug=True)
