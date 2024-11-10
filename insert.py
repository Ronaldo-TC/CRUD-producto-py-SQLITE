import sqlite3

conn = sqlite3.connect('almacen.db')
cursor = conn.cursor()

# Crear la tabla "productos"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        precio REAL NOT NULL
    )
''')

# Insertar 5 productos de ejemplo
productos = [
    ('Producto 1', 'Descripción del producto 1', 15.50),
    ('Producto 2', 'Descripción del producto 2', 8.75),
    ('Producto 3', 'Descripción del producto 3', 12.00),
    ('Producto 4', 'Descripción del producto 4', 10.00),
    ('Producto 5', 'Descripción del producto 5', 14.00)
]
cursor.executemany(
    "INSERT INTO productos (nombre, descripcion, precio) VALUES (?, ?, ?)", productos)

conn.commit()
conn.close()
