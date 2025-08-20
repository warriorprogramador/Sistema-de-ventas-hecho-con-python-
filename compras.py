import tkinter as tk
from tkinter import ttk, messagebox
from conexionmysql import conectar_db
from decimal import Decimal


def mostrar_carrito():
    # Conexión a la base de datos
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, nombre, precio_unitario FROM Producto WHERE stock > 0")
    productos = cursor.fetchall()
    conexion.close()

    carrito = []

    def agregar_al_carrito():
        # Obtener el producto seleccionado y la cantidad
        producto_seleccionado = combo_productos.get()
        cantidad = entry_cantidad.get()

        if not producto_seleccionado or not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Seleccione un producto y una cantidad válida.")
            return

        cantidad = int(cantidad)
        id_producto, nombre, precio_unitario = next(p for p in productos if p[1] == producto_seleccionado)
        
        # Verificar si el producto ya está en el carrito
        for item in carrito:
            if item['id_producto'] == id_producto:
                item['cantidad'] += cantidad
                item['subtotal'] = item['cantidad'] * item['precio_unitario']
                actualizar_carrito()
                return

        # Agregar nuevo producto al carrito
        carrito.append({
            'id_producto': id_producto,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'subtotal': cantidad * precio_unitario
        })
        actualizar_carrito()

    def actualizar_carrito():
        # Limpiar la tabla del carrito
        for row in tabla_carrito.get_children():
            tabla_carrito.delete(row)

        # Llenar la tabla con los datos del carrito
        for item in carrito:
            tabla_carrito.insert("", tk.END, values=(item['nombre'], item['cantidad'], item['precio_unitario'], item['subtotal']))

    def generar_compra():
        # Obtener datos del cliente
        nombre = entry_nombre.get()
        apellidos = entry_apellidos.get()
        telefono = entry_telefono.get()
        direccion = entry_direccion.get()
        email = entry_email.get()

        if not nombre or not apellidos or not telefono or not direccion:
            messagebox.showerror("Error", "Por favor, complete todos los datos obligatorios del cliente.")
            return

        # Insertar datos del cliente en la tabla Cliente
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO Cliente (nombre, apellido1, direccion, telefono, email) VALUES (%s, %s, %s, %s, %s)",
            (nombre, apellidos, direccion, telefono, email)
        )
        id_cliente = cursor.lastrowid

        # Insertar detalles de la compra en Movimiento y actualizar el stock
        for item in carrito:
            subtotal = item['subtotal']
            igv = subtotal * Decimal('0.18')  # Convertir el 0.18 a Decimal
            total = subtotal + igv

            cursor.execute(
                "INSERT INTO Movimiento (id_producto, id_cliente, fecha, cantidad, precio_unitario, subtotal, igv, total, tipo_movimiento) "
                "VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s, 'VENTA')",
                (item['id_producto'], id_cliente, item['cantidad'], item['precio_unitario'], subtotal, igv, total)
            )

            # Actualizar el stock de los productos
            cantidad_comprada = item['cantidad']  # Cantidad comprada por el cliente
            cursor.execute(
                "UPDATE Producto SET stock = stock - %s WHERE id_producto = %s",
                (cantidad_comprada, item['id_producto'])
            )

        # Confirmar la transacción y cerrar la conexión
        conexion.commit()
        conexion.close()

        # Mostrar mensaje de éxito y cerrar la ventana
        messagebox.showinfo("Éxito", "Compra generada con éxito.")
        ventana_ventas.destroy()

    # Crear ventana para el carrito de compras
    ventana_ventas = tk.Tk()
    ventana_ventas.title("Carrito de Compras")
    ventana_ventas.geometry("700x650")

    # Sección: Selección de productos
    frame_productos = tk.Frame(ventana_ventas)
    frame_productos.pack(pady=10)

    tk.Label(frame_productos, text="Seleccione un producto:").grid(row=0, column=0, padx=5, pady=5)
    combo_productos = ttk.Combobox(frame_productos, values=[p[1] for p in productos], state="readonly", width=40)
    combo_productos.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_productos, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
    entry_cantidad = tk.Entry(frame_productos, width=10)
    entry_cantidad.grid(row=1, column=1, padx=5, pady=5)

    tk.Button(frame_productos, text="Agregar al Carrito", command=agregar_al_carrito).grid(row=2, column=0, columnspan=2, pady=10)

    # Sección: Carrito de compras
    frame_carrito = tk.Frame(ventana_ventas)
    frame_carrito.pack(pady=10)

    tk.Label(frame_carrito, text="Carrito de Compras").pack()
    columnas = ("Producto", "Cantidad", "Precio Unitario", "Subtotal")
    tabla_carrito = ttk.Treeview(frame_carrito, columns=columnas, show="headings", height=10)
    tabla_carrito.pack()

    for col in columnas:
        tabla_carrito.heading(col, text=col)
        tabla_carrito.column(col, width=150)

    # Sección: Datos del cliente
    frame_cliente = tk.Frame(ventana_ventas)
    frame_cliente.pack(pady=20)

    tk.Label(frame_cliente, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = tk.Entry(frame_cliente, width=30)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_cliente, text="Apellidos:").grid(row=1, column=0, padx=5, pady=5)
    entry_apellidos = tk.Entry(frame_cliente, width=30)
    entry_apellidos.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_cliente, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
    entry_telefono = tk.Entry(frame_cliente, width=30)
    entry_telefono.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_cliente, text="Dirección:").grid(row=3, column=0, padx=5, pady=5)
    entry_direccion = tk.Entry(frame_cliente, width=30)
    entry_direccion.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(frame_cliente, text="Email (opcional):").grid(row=4, column=0, padx=5, pady=5)
    entry_email = tk.Entry(frame_cliente, width=30)
    entry_email.grid(row=4, column=1, padx=5, pady=5)

    # Botón para generar compra
    tk.Button(ventana_ventas, text="Generar Compra", command=generar_compra).pack(pady=10)

    ventana_ventas.mainloop()

