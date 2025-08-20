import tkinter as tk
from tkinter import ttk, messagebox
from conexionmysql import conectar_db

def mostrar_inventario():
    # Conexión a la base de datos para obtener los productos
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, nombre, marca, color, stock, precio_unitario FROM Producto")
    productos = cursor.fetchall()
    conexion.close()

    # Crear la ventana del inventario
    ventana_inventario = tk.Tk()
    ventana_inventario.title("Inventario")
    ventana_inventario.geometry("800x500")

    # Variables globales
    fila_seleccionada = tk.StringVar()

    # Función para habilitar/deshabilitar cajas de texto
    def habilitar_campos(estado):
        if estado:
            nombre_entry.config(state="normal")
            marca_entry.config(state="normal")
            color_entry.config(state="normal")
            stock_entry.config(state="normal")
            precio_entry.config(state="normal")
            boton_guardar.config(state="normal")
            boton_cancelar.config(state="normal")
        else:
            nombre_entry.config(state="disabled")
            marca_entry.config(state="disabled")
            color_entry.config(state="disabled")
            stock_entry.config(state="disabled")
            precio_entry.config(state="disabled")
            boton_guardar.config(state="disabled")
            boton_cancelar.config(state="disabled")

    # Función para limpiar las cajas de texto
    def limpiar_campos():
        nombre_entry.delete(0, tk.END)
        marca_entry.delete(0, tk.END)
        color_entry.delete(0, tk.END)
        stock_entry.delete(0, tk.END)
        precio_entry.delete(0, tk.END)
        fila_seleccionada.set("")  # Limpiar el ID seleccionado

    # Crear contenedor para los botones de acción y formulario
    frame_formulario = tk.Frame(ventana_inventario)
    frame_formulario.pack(side=tk.LEFT, padx=10, pady=10)

    # Título de formulario
    tk.Label(frame_formulario, text="Formulario de Producto", font=("Arial", 12)).pack(pady=5)

    # Campos para ingresar datos del producto
    tk.Label(frame_formulario, text="Nombre:").pack()
    nombre_entry = tk.Entry(frame_formulario, width=30, state="disabled")
    nombre_entry.pack(pady=5)

    tk.Label(frame_formulario, text="Marca:").pack()
    marca_entry = tk.Entry(frame_formulario, width=30, state="disabled")
    marca_entry.pack(pady=5)

    tk.Label(frame_formulario, text="Color:").pack()
    color_entry = tk.Entry(frame_formulario, width=30, state="disabled")
    color_entry.pack(pady=5)

    tk.Label(frame_formulario, text="Stock:").pack()
    stock_entry = tk.Entry(frame_formulario, width=30, state="disabled")
    stock_entry.pack(pady=5)

    tk.Label(frame_formulario, text="Precio:").pack()
    precio_entry = tk.Entry(frame_formulario, width=30, state="disabled")
    precio_entry.pack(pady=5)

    # Botones de acción
    boton_nuevo = tk.Button(frame_formulario, text="Nuevo", command=lambda: [habilitar_campos(True), limpiar_campos()])
    boton_nuevo.pack(pady=5)

    boton_guardar = tk.Button(frame_formulario, text="Guardar", state="disabled", command=lambda: guardar_o_modificar_producto())
    boton_guardar.pack(pady=5)

    boton_eliminar = tk.Button(frame_formulario, text="Eliminar", command=lambda: eliminar_producto())
    boton_eliminar.pack(pady=5)

    boton_cancelar = tk.Button(frame_formulario, text="Cancelar", state="disabled", command=lambda: [habilitar_campos(False), limpiar_campos()])
    boton_cancelar.pack(pady=5)

    # Crear contenedor para la tabla
    frame_tabla = tk.Frame(ventana_inventario)
    frame_tabla.pack(side=tk.RIGHT, padx=10, pady=10)

    # Tabla con Treeview
    tabla = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Marca", "Color", "Stock", "Precio"), show="headings")
    tabla.pack(expand=True, fill=tk.BOTH)

    # Configurar encabezados
    encabezados = ["ID", "Nombre", "Marca", "Color", "Stock", "Precio"]
    for col in encabezados:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)

    # Rellenar la tabla con los datos
    for producto in productos:
        tabla.insert("", tk.END, values=producto)

    # Detectar selección de fila
    def seleccionar_fila(event):
        item = tabla.selection()
        if item:
            datos = tabla.item(item, "values")
            fila_seleccionada.set(datos[0])  # Guardar ID seleccionado
            habilitar_campos(True)
            # Llenar los campos del formulario con los datos de la fila seleccionada
            nombre_entry.delete(0, tk.END)
            nombre_entry.insert(0, datos[1])
            marca_entry.delete(0, tk.END)
            marca_entry.insert(0, datos[2])
            color_entry.delete(0, tk.END)
            color_entry.insert(0, datos[3])
            stock_entry.delete(0, tk.END)
            stock_entry.insert(0, datos[4])
            precio_entry.delete(0, tk.END)
            precio_entry.insert(0, datos[5])

    tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

    # Función para guardar o modificar producto
    def guardar_o_modificar_producto():
        nombre = nombre_entry.get()
        marca = marca_entry.get()
        color = color_entry.get()
        stock = stock_entry.get()
        precio = precio_entry.get()

        if not nombre or not marca or not color or not stock or not precio:
            messagebox.showerror("Error", "Todos los campos son requeridos.")
            return

        conexion = conectar_db()
        cursor = conexion.cursor()

        if fila_seleccionada.get():  # Si hay un producto seleccionado, se modifica
            cursor.execute(
                "UPDATE Producto SET nombre=%s, marca=%s, color=%s, stock=%s, precio_unitario=%s WHERE id_producto=%s",
                (nombre, marca, color, stock, precio, fila_seleccionada.get())
            )
            mensaje = "Producto modificado correctamente."
        else:  # Si no hay producto seleccionado, se guarda uno nuevo
            cursor.execute(
                "INSERT INTO Producto (nombre, marca, color, stock, precio_unitario) VALUES (%s, %s, %s, %s, %s)",
                (nombre, marca, color, stock, precio)
            )
            mensaje = "Producto agregado correctamente."

        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", mensaje)
        ventana_inventario.destroy()
        mostrar_inventario()

    # Función para eliminar producto
    def eliminar_producto():
        if not fila_seleccionada.get():
            messagebox.showerror("Error", "Seleccione un producto para eliminar.")
            return

        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este producto?")
        if not confirmacion:
            return

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Producto WHERE id_producto=%s", (fila_seleccionada.get(),))
        cursor.execute("DELETE FROM movimiento WHERE id_movimiento = %s", (fila_seleccionada.get(),))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        ventana_inventario.destroy()
      