create database tienda;
use  tienda;
-- Tabla Cliente
CREATE TABLE Cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido1 VARCHAR(50) NOT NULL,
    direccion VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100)
);

INSERT INTO Cliente (nombre, apellido1, direccion, telefono, email) VALUES
('Juan', 'Pérez', 'Av. Lima 123', '999111222', 'juan.perez@email.com'),
('Ana', 'García', 'Calle Sol 456', '988222333', 'ana.garcia@email.com'),
('Luis', 'Ramírez', 'Jr. Luna 789', '977333444', 'luis.ramirez@email.com');

-- Tabla Producto
CREATE TABLE Producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    marca VARCHAR(50),
    color VARCHAR(30),
    stock INT DEFAULT 0,
    precio_unitario DECIMAL(10,2) NOT NULL
);

INSERT INTO Producto (nombre, marca, color, stock, precio_unitario) VALUES
('Laptop', 'HP', 'Gris', 10, 2500.00),
('Mouse', 'Logitech', 'Negro', 50, 50.00),
('Teclado', 'Genius', 'Blanco', 30, 120.00);

-- Tabla Proveedor
CREATE TABLE Proveedor (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    ruc VARCHAR(20),
    departamento VARCHAR(50),
    ciudad VARCHAR(50)
);

INSERT INTO Proveedor (nombre, direccion, telefono, email, ruc, departamento, ciudad) VALUES
('Distribuidora Perú', 'Av. Comercio 100', '999888777', 'contacto@distribuidoraperu.com', '20123456789', 'Lima', 'Lima'),
('Mayorista S.A.', 'Calle Mayor 200', '988777666', 'ventas@mayorista.com', '20567891234', 'Arequipa', 'Arequipa');

-- Tabla Movimiento
CREATE TABLE Movimiento (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    id_cliente INT NOT NULL,
    fecha DATETIME NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    igv DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    tipo_movimiento VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);

INSERT INTO Movimiento (id_producto, id_cliente, fecha, cantidad, precio_unitario, subtotal, igv, total, tipo_movimiento) VALUES
(1, 1, '2025-08-01 10:00:00', 1, 2500.00, 2500.00, 450.00, 2950.00, 'VENTA'),
(2, 2, '2025-08-02 11:30:00', 2, 50.00, 100.00, 18.00, 118.00, 'VENTA'),
(3, 3, '2025-08-03 09:15:00', 1, 120.00, 120.00, 21.60, 141.60, 'VENTA');

-- Tabla PersonalUsuario
CREATE TABLE PersonalUsuario (
    id_personal INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    cargo VARCHAR(50),
    direccion VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    usuario VARCHAR(50) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    rol VARCHAR(20) NOT NULL,
    estado VARCHAR(20)
);

INSERT INTO PersonalUsuario (nombre, apellido, cargo, direccion, telefono, email, usuario, contrasena, rol, estado) VALUES
('Admin', 'Principal', 'Administrador', 'Av. Central 123', '900111222', 'admin@email.com', 'admin', 'admin123', 'Admin', 'Activo'),
('Vendedor', 'Uno', 'Vendedor', 'Calle Ventas 456', '900222333', 'vendedor@email.com', 'vendedor', 'vendedor123', 'Vendedor', 'Activo');



