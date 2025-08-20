import tkinter as tk
from tkinter import ttk, messagebox
from conexionmysql import conectar_db

def mostrar_proveedores():
    # Conexión a la base de datos para obtener los proveedores
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_proveedor, nombre, direccion, telefono, email, ruc, departamento, ciudad FROM Proveedor")
    proveedores = cursor.fetchall()
    conexion.close()

    # Crear la ventana de proveedores
    ventana_proveedores = tk.Tk()
    ventana_proveedores.title("Proveedores")
    ventana_proveedores.geometry("1028x600")

    # Variables globales
    fila_seleccionada = tk.StringVar()

    # Función para habilitar/deshabilitar cajas de texto
    def habilitar_campos(estado):
        if estado:
            nombre_entry.config(state="normal")
            direccion_entry.config(state="normal")
            telefono_entry.config(state="normal")
            email_entry.config(state="normal")
            ruc_entry.config(state="normal")
            departamento_entry.config(state="normal")
            ciudad_entry.config(state="normal")
            boton_guardar.config(state="normal")
            boton_cancelar.config(state="normal")
        else:
            nombre_entry.config(state="disabled")
            direccion_entry.config(state="disabled")
            telefono_entry.config(state="disabled")
            email_entry.config(state="disabled")
            ruc_entry.config(state="disabled")
            departamento_entry.config(state="disabled")
            ciudad_entry.config(state="disabled")
            boton_guardar.config(state="disabled")
            boton_cancelar.config(state="disabled")

    # Función para limpiar las cajas de texto
    def limpiar_campos():
        nombre_entry.delete(0, tk.END)
        direccion_entry.delete(0, tk.END)
        telefono_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        ruc_entry.delete(0, tk.END)
        departamento_entry.delete(0, tk.END)
        ciudad_entry.delete(0, tk.END)
        fila_seleccionada.set("")  # Limpiar el ID seleccionado

    # Crear contenedor para los botones de acción y formulario
    frame_formulario = tk.Frame(ventana_proveedores)
    frame_formulario.pack(side=tk.LEFT, padx=10, pady=10)

    # Título de formulario
    tk.Label(frame_formulario, text="Formulario de Proveedor", font=("Arial", 12)).pack(pady=5)

    # Campos para ingresar datos del proveedor
    tk.Label(frame_formulario, text="Nombre:").pack()
    nombre_entry = tk.Entry(frame_formulario, width=30, state="disabled")
    nombre_entry.pack(pady=5)

    tk.Label(frame_formulario, text="Dirección:").pack()
    direccion_entry = tk.Entry(frame_formulario, width=30, state="disabled")
    direccion_entry.pack(pady=5)

    tk.Label(frame_formulario, text="Teléfono:").pack()
    telefono_entry = tk.Entry(frame_formulario, width=30, state="disabled")
    telefono_entry.pack(pady=5)

    tk.Label(frame_formulario, text="Email:").pack()
    email_entry = tk.Entry(frame_formulario, width=30, state="disabled")
    email_entry.pack(pady=5)

    tk.Label(frame_formulario, text="RUC:").pack()
    ruc_entry = tk.Entry(frame_formulario, width=30, state="disabled")
    ruc_entry.pack(pady=5)

    tk.Label(frame_formulario, text="Departamento:").pack()
    departamento_entry = tk.Entry(frame_formulario, width=30, state="disabled")
    departamento_entry.pack(pady=5)

    tk.Label(frame_formulario, text="Ciudad:").pack()
    ciudad_entry = tk.Entry(frame_formulario, width=30, state="disabled")
    ciudad_entry.pack(pady=5)

    # Botones de acción
    boton_nuevo = tk.Button(frame_formulario, text="Nuevo", command=lambda: [habilitar_campos(True), limpiar_campos()])
    boton_nuevo.pack(pady=5)

    boton_guardar = tk.Button(frame_formulario, text="Guardar", state="disabled", command=lambda: guardar_o_modificar_proveedor())
    boton_guardar.pack(pady=5)

    boton_eliminar = tk.Button(frame_formulario, text="Eliminar", command=lambda: eliminar_proveedor())
    boton_eliminar.pack(pady=5)

    boton_cancelar = tk.Button(frame_formulario, text="Cancelar", state="disabled", command=lambda: [habilitar_campos(False), limpiar_campos()])
    boton_cancelar.pack(pady=5)

    # Crear contenedor para la tabla
    frame_tabla = tk.Frame(ventana_proveedores)
    frame_tabla.pack(side=tk.RIGHT, padx=10, pady=10)

    # Tabla con Treeview
    tabla = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Dirección", "Teléfono", "Email", "RUC", "Departamento", "Ciudad"), show="headings")
    tabla.pack(expand=True, fill=tk.BOTH)

    # Configurar encabezados
    encabezados = ["ID", "Nombre", "Dirección", "Teléfono", "Email", "RUC", "Departamento", "Ciudad"]
    for col in encabezados:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)

    # Rellenar la tabla con los datos
    for proveedor in proveedores:
        tabla.insert("", tk.END, values=proveedor)

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
            direccion_entry.delete(0, tk.END)
            direccion_entry.insert(0, datos[2])
            telefono_entry.delete(0, tk.END)
            telefono_entry.insert(0, datos[3])
            email_entry.delete(0, tk.END)
            email_entry.insert(0, datos[4])
            ruc_entry.delete(0, tk.END)
            ruc_entry.insert(0, datos[5])
            departamento_entry.delete(0, tk.END)
            departamento_entry.insert(0, datos[6])
            ciudad_entry.delete(0, tk.END)
            ciudad_entry.insert(0, datos[7])

    tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

    # Función para guardar o modificar proveedor
    def guardar_o_modificar_proveedor():
        nombre = nombre_entry.get()
        direccion = direccion_entry.get()
        telefono = telefono_entry.get()
        email = email_entry.get()
        ruc = ruc_entry.get()
        departamento = departamento_entry.get()
        ciudad = ciudad_entry.get()

        if not nombre or not direccion or not telefono or not email or not ruc or not departamento or not ciudad:
            messagebox.showerror("Error", "Todos los campos son requeridos.")
            return

        conexion = conectar_db()
        cursor = conexion.cursor()

        if fila_seleccionada.get():  # Si hay un proveedor seleccionado, se modifica
            cursor.execute(
                "UPDATE Proveedor SET nombre=%s, direccion=%s, telefono=%s, email=%s, ruc=%s, departamento=%s, ciudad=%s WHERE id_proveedor=%s",
                (nombre, direccion, telefono, email, ruc, departamento, ciudad, fila_seleccionada.get())
            )
            mensaje = "Proveedor modificado correctamente."
        else:  # Si no hay proveedor seleccionado, se guarda uno nuevo
            cursor.execute(
                "INSERT INTO Proveedor (nombre, direccion, telefono, email, ruc, departamento, ciudad) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (nombre, direccion, telefono, email, ruc, departamento, ciudad)
            )
            mensaje = "Proveedor agregado correctamente."

        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", mensaje)
        ventana_proveedores.destroy()
        mostrar_proveedores()

    # Función para eliminar proveedor
    def eliminar_proveedor():
        if not fila_seleccionada.get():
            messagebox.showerror("Error", "Seleccione un proveedor para eliminar.")
            return

        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este proveedor?")
        if not confirmacion:
            return

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Proveedor WHERE id_proveedor=%s", (fila_seleccionada.get(),))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
        ventana_proveedores.destroy()
       
