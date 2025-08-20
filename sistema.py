import tkinter as tk
from PIL import Image, ImageTk  # Importa PIL para manejar imágenes
from inventario import mostrar_inventario  # Importa la función del archivo inventario
from proveedores import mostrar_proveedores
from compras import mostrar_carrito
from clientes import mostrar_clientes
class Sistema:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Ventas")
        self.ventana.geometry("800x500")
        self.crear_interface()
        self.ventana.resizable(False, False)  # Desactiva el cambio de tamaño


    def crear_interface(self):
        # Crear un marco para el logo (izquierda)
        frame_imagen = tk.Frame(self.ventana)
        frame_imagen.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

        # Cargar el logo
        logo = Image.open("C:/Users/USUARIO/Desktop/SISTEMA DE VENTAS/imagenes/images.png")  # Ruta del logo
        logo_tk = ImageTk.PhotoImage(logo)
        label_logo = tk.Label(frame_imagen, image=logo_tk)
        label_logo.image = logo_tk  # Mantener una referencia para evitar que la imagen se elimine
        label_logo.grid(row=0, column=0)

        # Crear un marco para los botones a la derecha
        frame_botones = tk.Frame(self.ventana)
        frame_botones.grid(row=0, column=1, padx=20, pady=10, sticky="n")

        # Cargar imágenes para los botones con PIL y redimensionarlas
        self.imagen_inventario = Image.open("C:/Users/USUARIO/Desktop/SISTEMA DE VENTAS/imagenes/Featured-Como-hacer-correctamente-un-inventario.jpg")
        self.imagen_inventario = self.imagen_inventario.resize((150, 150))  # Redimensionar
        self.imagen_inventario_tk = ImageTk.PhotoImage(self.imagen_inventario)

        self.imagen_clientes = Image.open("C:/Users/USUARIO/Desktop/SISTEMA DE VENTAS/imagenes/Compras-en-supermercado.jpg")
        self.imagen_clientes= self.imagen_clientes.resize((150, 150))  # Redimensionar
        self.imagen_clientes_tk = ImageTk.PhotoImage(self.imagen_clientes)

        self.imagen_carrito = Image.open("C:/Users/USUARIO/Desktop/SISTEMA DE VENTAS/imagenes/depositphotos_143047667-stock-illustration-shopping-cart-sign-vector-red.jpg")
        self.imagen_carrito = self.imagen_carrito.resize((150, 150))  # Redimensionar
        self.imagen_carrito_tk = ImageTk.PhotoImage(self.imagen_carrito)

        self.imagen_proveedores = Image.open("C:/Users/USUARIO/Desktop/SISTEMA DE VENTAS/imagenes/Proveedores-828x548.jpg")
        self.imagen_proveedores = self.imagen_proveedores.resize((150, 150))  # Redimensionar
        self.imagen_proveedores_tk = ImageTk.PhotoImage(self.imagen_proveedores)

        # Crear una grilla de 2x2 para las imágenes y sus nombres
        frame_imagenes = tk.Frame(self.ventana)
        frame_imagenes.grid(row=1, column=1, padx=20, pady=10)

        # Colocar las imágenes en el grid con sus nombres debajo
        boton_inventario = tk.Button(frame_imagenes, image=self.imagen_inventario_tk, command=self.mostrar_inventario)
        boton_inventario.grid(row=0, column=0, padx=10, pady=10)
        tk.Label(frame_imagenes, text="Inventario").grid(row=1, column=0, pady=5)

        boton_compras = tk.Button(frame_imagenes, image=self.imagen_clientes_tk, command=self.mostrar_clientes)
        boton_compras.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(frame_imagenes, text="Clientes").grid(row=1, column=1, pady=5)

        boton_carrito = tk.Button(frame_imagenes, image=self.imagen_carrito_tk, command=self.mostrar_carrito)

        boton_carrito.grid(row=2, column=0, padx=10, pady=10)
        tk.Label(frame_imagenes, text="Carrito").grid(row=3, column=0, pady=5)

        boton_proveedores = tk.Button(frame_imagenes, image=self.imagen_proveedores_tk, command=self.mostrar_proveedores)
        boton_proveedores.grid(row=2, column=1, padx=10, pady=10)
        tk.Label(frame_imagenes, text="Proveedores").grid(row=3, column=1, pady=5)

    def mostrar_inventario(self):
        # Aquí llamas la función mostrar_inventario que importaste
        mostrar_inventario()

    def mostrar_clientes(self):
       mostrar_clientes()

    def mostrar_carrito(self):
        # Llamada correcta al método de la clase
        mostrar_carrito()


    def mostrar_proveedores(self):
       mostrar_proveedores()

    def run(self):
        self.ventana.mainloop()


