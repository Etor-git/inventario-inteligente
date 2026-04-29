# ============================================================
# Sistema de Inventario Inteligente
# Aplicación web Flask para gestionar productos con predicción
# de agotamiento de stock usando un modelo de ML.
# ============================================================

from flask import Flask, request
from database import get_connection
from ml_model import predecir_agotamiento

app = Flask(__name__)


# ------------------------------------------------------------
# RUTA PRINCIPAL
# ------------------------------------------------------------

@app.route("/")
def home():
    """Página de inicio con enlace al formulario de registro."""
    return """
    <h1>Sistema de Inventario Inteligente</h1>
    <a href='/formulario'>Ir a registrar producto</a>
    """


# ------------------------------------------------------------
# REGISTRO DE PRODUCTOS
# ------------------------------------------------------------

@app.route("/formulario")
def formulario():
    """Muestra el formulario HTML para registrar un nuevo producto."""
    return """
    <h2>Registrar Producto</h2>

    <form action="/agregar_producto" method="POST">
        <label>Nombre:</label><br>
        <input type="text" name="nombre"><br><br>

        <label>Categoría:</label><br>
        <input type="text" name="categoria"><br><br>

        <label>Stock actual:</label><br>
        <input type="number" name="stock_actual"><br><br>

        <label>Stock mínimo:</label><br>
        <input type="number" name="stock_minimo"><br><br>

        <label>Precio:</label><br>
        <input type="number" step="0.01" name="precio"><br><br>

        <button type="submit">Guardar Producto</button>
    </form>
    """


@app.route("/agregar_producto", methods=["POST"])
def agregar_producto():
    """
    Recibe los datos del formulario y los inserta en la base de datos.
    Retorna confirmación o mensaje de error.
    """
    try:
        # Obtener datos enviados desde el formulario
        nombre       = request.form["nombre"]
        categoria    = request.form["categoria"]
        stock_actual = request.form["stock_actual"]
        stock_minimo = request.form["stock_minimo"]
        precio       = request.form["precio"]

        # Conectar a la base de datos e insertar el nuevo producto
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO productos (nombre, categoria, stock_actual, stock_minimo, precio)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (nombre, categoria, stock_actual, stock_minimo, precio)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return """
        <h2>Producto agregado correctamente</h2>
        <a href="/formulario">Agregar otro producto</a>
        """

    except Exception as e:
        return f"Error: {str(e)}"


# ------------------------------------------------------------
# VISUALIZACIÓN DE PRODUCTOS
# ------------------------------------------------------------

@app.route("/productos")
def ver_productos():
    """
    Consulta todos los productos en la base de datos y los
    muestra en una tabla HTML con opciones de editar y eliminar.
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        cursor.close()
        connection.close()

        # Encabezado de la tabla
        html = """
        <h2>Lista de Productos</h2>
        <table border="1" cellpadding="10">
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Categoría</th>
                <th>Stock Actual</th>
                <th>Stock Mínimo</th>
                <th>Precio</th>
                <th>Acciones</th>
            </tr>
        """

        # Filas de la tabla: una por cada producto
        for producto in productos:
            html += f"""
            <tr>
                <td>{producto[0]}</td>
                <td>{producto[1]}</td>
                <td>{producto[2]}</td>
                <td>{producto[3]}</td>
                <td>{producto[4]}</td>
                <td>${producto[5]}</td>
                <td>
                    <a href="/editar_producto/{producto[0]}">Editar</a>
                    &nbsp;|&nbsp;
                    <a href="/eliminar_producto/{producto[0]}">Eliminar</a>
                </td>
            </tr>
            """

        html += "</table><br><a href='/'>Volver al inicio</a>"
        return html

    except Exception as e:
        return f"Error: {str(e)}"


# ------------------------------------------------------------
# ELIMINACIÓN DE PRODUCTOS
# ------------------------------------------------------------

@app.route("/eliminar_producto/<int:id>")
def eliminar_producto(id):
    """
    Elimina un producto de la base de datos según su ID.
    Recibe el ID como parámetro en la URL.
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = "DELETE FROM productos WHERE id = %s"
        cursor.execute(query, (id,))
        connection.commit()

        cursor.close()
        connection.close()

        return f"""
        <h2>Producto con ID {id} eliminado correctamente</h2>
        <a href="/productos">Volver a productos</a>
        """

    except Exception as e:
        return f"Error: {str(e)}"


# ------------------------------------------------------------
# EDICIÓN DE PRODUCTOS
# ------------------------------------------------------------

@app.route("/editar_producto/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    """
    GET:  Muestra el formulario pre-rellenado con los datos actuales del producto.
    POST: Recibe los datos modificados y actualiza el registro en la base de datos.
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()

        if request.method == "POST":
            # Obtener datos actualizados desde el formulario
            nombre       = request.form["nombre"]
            categoria    = request.form["categoria"]
            stock_actual = request.form["stock_actual"]
            stock_minimo = request.form["stock_minimo"]
            precio       = request.form["precio"]

            query = """
                UPDATE productos
                SET nombre=%s, categoria=%s, stock_actual=%s,
                    stock_minimo=%s, precio=%s
                WHERE id=%s
            """
            values = (nombre, categoria, stock_actual, stock_minimo, precio, id)

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            return f"""
            <h2>Producto actualizado correctamente</h2>
            <a href="/productos">Volver a productos</a>
            """

        # GET: cargar datos actuales del producto para pre-rellenar el formulario
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
        producto = cursor.fetchone()

        cursor.close()
        connection.close()

        return f"""
        <h2>Editar Producto</h2>

        <form method="POST">
            <label>Nombre:</label><br>
            <input type="text" name="nombre" value="{producto[1]}"><br><br>

            <label>Categoría:</label><br>
            <input type="text" name="categoria" value="{producto[2]}"><br><br>

            <label>Stock actual:</label><br>
            <input type="number" name="stock_actual" value="{producto[3]}"><br><br>

            <label>Stock mínimo:</label><br>
            <input type="number" name="stock_minimo" value="{producto[4]}"><br><br>

            <label>Precio:</label><br>
            <input type="number" step="0.01" name="precio" value="{producto[5]}"><br><br>

            <button type="submit">Actualizar Producto</button>
        </form>
        """

    except Exception as e:
        return f"Error: {str(e)}"


# ------------------------------------------------------------
# PREDICCIÓN DE AGOTAMIENTO
# ------------------------------------------------------------

@app.route("/prediccion")
def prediccion():
    """
    Usa el modelo de ML para estimar en cuántas semanas se agotará
    el stock de un producto dado el stock actual y las ventas semanales.
    """
    # Valores de ejemplo (en una versión real vendrían de la BD o de la URL)
    stock_actual      = 30
    ventas_semanales  = 10

    # Llamada al modelo predictivo
    semanas = predecir_agotamiento(stock_actual, ventas_semanales)

    return f"""
    <h2>Predicción de Inventario</h2>

    <p>Stock actual: {stock_actual}</p>
    <p>Ventas semanales promedio: {ventas_semanales}</p>
    <h3>Se agotará en aproximadamente {semanas} semanas</h3>

    <a href="/">Volver al inicio</a>
    """


# ------------------------------------------------------------
# PUNTO DE ENTRADA
# ------------------------------------------------------------

if __name__ == "__main__":
    # Ejecutar el servidor en todas las interfaces de red, puerto 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
