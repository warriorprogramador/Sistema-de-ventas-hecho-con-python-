import tkinter as tk
from tkinter import ttk
from conexionmysql import conectar_db

def mostrar_clientes():
    # Conexión a la base de datos
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # Obtener los clientes y sus compras, incluyendo apellido y correo
    cursor.execute("""
        SELECT 
            m.id_movimiento AS id_movimiento, 
            p.nombre AS producto, 
            c.nombre AS nombre_cliente, 
            c.apellido1 AS apellido_cliente,
            c.email AS correo,
            m.cantidad AS cantidad, 
            m.precio_unitario AS precio_unitario, 
            m.subtotal AS subtotal, 
            m.igv AS igv, 
            m.total AS total, 
            m.fecha AS fecha
        FROM Movimiento m
        JOIN Producto p ON m.id_producto = p.id_producto
        JOIN Cliente c ON m.id_cliente = c.id_cliente
        WHERE m.tipo_movimiento = 'VENTA'
        ORDER BY m.fecha ASC; -- Ordenar por fecha de la compra (puedes cambiar el criterio)
    """)
    clientes = cursor.fetchall()
    conexion.close()

    # Crear ventana
    ventana_clientes = tk.Tk()
    ventana_clientes.title("Clientes y Compras")
    ventana_clientes.geometry("1000x400")

    # Tabla de clientes y compras
    columnas = ("ID Movimiento", "Producto", "Nombre", "Apellido", "Correo", "Cantidad", 
                "Precio Unitario", "Total a cancelar")
    tabla_clientes = ttk.Treeview(ventana_clientes, columns=columnas, show="headings", height=20)
    tabla_clientes.pack(pady=20)

    # Configurar encabezados de las columnas
    for col in columnas:
        tabla_clientes.heading(col, text=col)
        tabla_clientes.column(col, width=120, anchor="center")

    # Insertar los datos en la tabla
    for cliente in clientes:
        tabla_clientes.insert("", tk.END, values=cliente)

    ventana_clientes.mainloop()

if __name__ == "__main__":
    mostrar_clientes()
