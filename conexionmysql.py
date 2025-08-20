import mysql.connector
def conectar_db():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",       # Usuario de la base de datos por defecto es root
        password="aqui va la contraseña",       # Contraseña de tu Mysql Workbench o servidor MySQL
        port=3306,         # Puerto por defecto de MySQL es 3306
        database="tienda"   # Nombre de la base de datos a la que te quieres conectar
    )
    return conexion
