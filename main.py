from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from sistema import Sistema  # llamamos al archivo sistema.py
from conexionmysql import conectar_db  # llamamos al archivo conexionmysql.py
from inventario import mostrar_inventario  # llamamos al archivo inventario.py

def validar_login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    rol = combo_rol.get()

    try:
        # Establece la conexión
        conexion = conectar_db()
        cursor = conexion.cursor()

        # Consulta SQL para verificar el usuario, contraseña y rol
        query = """
        SELECT * FROM PersonalUsuario WHERE usuario = %s AND rol = %s;
        """
        cursor.execute(query, (usuario, rol))
        usuario_encontrado = cursor.fetchone()  # Trae el primer resultado encontrado

        # Validación de usuario, rol y contraseña
        if usuario_encontrado:
            id_personal, nombre, apellido, cargo, direccion, telefono, email, usuario_db, contrasena_db, rol_db, estado = usuario_encontrado
            if contraseña == contrasena_db:
                messagebox.showinfo("Login exitoso", f"¡Bienvenido {nombre} al sistema!")
                ventana.destroy()  # Cierra la ventana de login antes de abrir la siguiente ventana
                sistema = Sistema()  # Crea la instancia de la clase Sistema
                sistema.run()  # Inicia el bucle de la ventana del sistema
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
        else:
            messagebox.showerror("Error", "Usuario o rol incorrectos")
        conexion.close()  # Cerrar la conexión después de la consulta
    except Exception as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")

# Función para la recuperación de la contraseña
def recuperar_contraseña():
    def verificar_respuesta():
        usuario = entry_usuario.get()  # Obtén el usuario ingresado
        respuesta = entry_respuesta.get().lower()

        try:
            # Establecer la conexión a la base de datos
            conexion = conectar_db()
            cursor = conexion.cursor()

            # Consulta SQL para buscar el usuario por nombre
            query = "SELECT * FROM PersonalUsuario WHERE usuario = %s"
            cursor.execute(query, (usuario,))
            usuario_encontrado = cursor.fetchone()

            if usuario_encontrado:
                # Verificación de la respuesta
                if respuesta == "mi gato":  # Respuesta correcta
                    messagebox.showinfo("Recuperación exitosa", "Puedes cambiar tu contraseña ahora.")
                    ventana_recuperacion.destroy()  # Cierra la ventana de recuperación
                    cambiar_contraseña(usuario)  # Llama a la función para cambiar la contraseña
                else:
                    messagebox.showerror("Error", "Respuesta incorrecta. Intenta nuevamente.")
            else:
                messagebox.showerror("Error", "Usuario no encontrado.")
            conexion.close()  # Cerrar la conexión después de la consulta
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")

    def cambiar_contraseña(usuario):
        def actualizar_contraseña():
            nueva_contraseña = entry_nueva_contraseña.get()
            if nueva_contraseña:
                try:
                    # Actualizar contraseña en la base de datos
                    conexion = conectar_db()
                    cursor = conexion.cursor()
                    query = "UPDATE PersonalUsuario SET contrasena = %s WHERE usuario = %s;"
                    cursor.execute(query, (nueva_contraseña, usuario))
                    conexion.commit()
                    messagebox.showinfo("Contraseña actualizada", "Tu contraseña ha sido actualizada exitosamente.")
                    ventana_actualizar.destroy()
                    conexion.close()
                except Exception as e:
                    messagebox.showerror("Error de conexión", f"No se pudo actualizar la contraseña: {e}")

        ventana_actualizar = tk.Toplevel(ventana)
        ventana_actualizar.title("Actualizar Contraseña")
        ventana_actualizar.geometry("400x300")

        tk.Label(ventana_actualizar, text="Nueva Contraseña:", font=("Arial", 12)).pack(pady=20)
        entry_nueva_contraseña = tk.Entry(ventana_actualizar, font=("Arial", 12))
        entry_nueva_contraseña.pack(pady=10)

        boton_actualizar = tk.Button(ventana_actualizar, text="Actualizar Contraseña", command=actualizar_contraseña, font=("Arial", 12), bg="#4CAF50", fg="white")
        boton_actualizar.pack(pady=20)

    ventana_recuperacion = tk.Toplevel(ventana)
    ventana_recuperacion.title("Recuperación de Contraseña")
    ventana_recuperacion.geometry("400x300")

    tk.Label(ventana_recuperacion, text="¿Cuál es el nombre de tu mascota?", font=("Arial", 12)).pack(pady=20)
    entry_respuesta = tk.Entry(ventana_recuperacion, font=("Arial", 12))
    entry_respuesta.pack(pady=10)
    boton_verificar = tk.Button(ventana_recuperacion, text="Verificar", command=verificar_respuesta, font=("Arial", 12), bg="#4CAF50", fg="white")
    boton_verificar.pack(pady=20)

# Ventana principal
ventana = tk.Tk()
ventana.title("Login - Sistema de Ventas")
ventana.geometry("800x500")
ventana.resizable(False, False)  # Desactiva el cambio de tamaño

# Centrar ventana
ancho_ventana = 700
alto_ventana = 500
pantalla_ancho = ventana.winfo_screenwidth()
pantalla_alto = ventana.winfo_screenheight()
x = (pantalla_ancho - ancho_ventana) // 2
y = (pantalla_alto - alto_ventana) // 2
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

# Frame principal para la imagen y el login
frame_principal = tk.Frame(ventana)
frame_principal.pack(fill=tk.BOTH, expand=True)

# Intenta cargar la imagen
try:
    imagen_fondo = Image.open("C:/Users/USUARIO/Desktop/SISTEMA DE VENTAS/imagenes/depositphotos_143047667-stock-illustration-shopping-cart-sign-vector-red.jpg")
    imagen_fondo = imagen_fondo.resize((150, 150))  # Redimensionar la imagen
    imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)
    print("Imagen cargada correctamente")
except Exception as e:
    print(f"No se pudo cargar la imagen: {e}")

# Frame para centrar los elementos a la derecha
frame_login = tk.Frame(frame_principal, padx=20, pady=20)
frame_login.pack(side=tk.RIGHT, fill=tk.Y, padx=50)  # Coloca el frame de login con más margen a la derecha

# Frame para la imagen (a la izquierda)
frame_imagen = tk.Frame(frame_principal)
frame_imagen.pack(side=tk.LEFT, padx=50)  # Coloca el frame de la imagen a la izquierda

# Etiqueta para mostrar la imagen
label_imagen = tk.Label(frame_imagen, image=imagen_fondo_tk)
label_imagen.pack(pady=20)

# Etiqueta y entrada para el usuario
tk.Label(frame_login, text="Usuario:", font=("Arial", 14)).pack(pady=(30, 5))  # Etiqueta más abajo
entry_usuario = tk.Entry(frame_login, font=("Arial", 14))
entry_usuario.pack(pady=5)

# Etiqueta y entrada para el rol
tk.Label(frame_login, text="Rol:", font=("Arial", 14)).pack(pady=20)
combo_rol = ttk.Combobox(frame_login, values=["Admin", "Vendedor"], font=("Arial", 14))
combo_rol.pack(pady=5)
combo_rol.set("Admin")  # Establecer un valor por defecto

# Etiqueta y entrada para la contraseña
tk.Label(frame_login, text="Contraseña:", font=("Arial", 14)).pack(pady=20)  # Más espaciado
entry_contraseña = tk.Entry(frame_login, font=("Arial", 14), show="*")
entry_contraseña.pack(pady=5)

# Botón de login
boton_login = tk.Button(frame_login, text="Ingresar", font=("Arial", 14), command=validar_login, bg="#4CAF50", fg="white")
boton_login.pack(pady=30)

# Enlace para recuperar contraseña
recuperar_contraseña_label = tk.Label(frame_login, text="¿Olvidaste tu contraseña?", font=("Arial", 12), fg="blue", cursor="hand2")
recuperar_contraseña_label.pack()
recuperar_contraseña_label.bind("<Button-1>", lambda e: recuperar_contraseña())

ventana.mainloop()
