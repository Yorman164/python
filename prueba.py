import tkinter as tk
from tkinter import messagebox
import sqlite3

conexion = sqlite3.connect("tienda.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT,
precio REAL,
stock INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas(
id INTEGER PRIMARY KEY AUTOINCREMENT,
producto TEXT,
cantidad INTEGER,
total REAL
)
""")

conexion.commit()

# ---------------- FUNCIONES ----------------

def agregar_producto():
    nombre = entry_nombre.get()
    precio = entry_precio.get()
    stock = entry_stock.get()

    if nombre == "" or precio == "" or stock == "":
        messagebox.showwarning("Error","Complete todos los campos")
        return

    cursor.execute("INSERT INTO productos(nombre,precio,stock) VALUES(?,?,?)",
                   (nombre,precio,stock))
    conexion.commit()

    messagebox.showinfo("Éxito","Producto agregado")

    entry_nombre.delete(0,tk.END)
    entry_precio.delete(0,tk.END)
    entry_stock.delete(0,tk.END)

    mostrar_productos()


def mostrar_productos():

    lista_productos.delete(0,tk.END)

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    for producto in productos:
        texto = f"ID:{producto[0]}  {producto[1]}  Precio:{producto[2]}  Stock:{producto[3]}"
        lista_productos.insert(tk.END,texto)


def registrar_venta():

    id_producto = entry_idventa.get()
    cantidad = entry_cantidad.get()

    if id_producto == "" or cantidad == "":
        messagebox.showwarning("Error","Ingrese datos")
        return

    cursor.execute("SELECT * FROM productos WHERE id=?", (id_producto,))
    producto = cursor.fetchone()

    if producto is None:
        messagebox.showerror("Error","Producto no existe")
        return

    nombre = producto[1]
    precio = producto[2]
    stock = producto[3]

    cantidad = int(cantidad)

    if cantidad > stock:
        messagebox.showerror("Error","Stock insuficiente")
        return

    total = precio * cantidad
    nuevo_stock = stock - cantidad

    cursor.execute("UPDATE productos SET stock=? WHERE id=?",(nuevo_stock,id_producto))
    cursor.execute("INSERT INTO ventas(producto,cantidad,total) VALUES(?,?,?)",
                   (nombre,cantidad,total))

    conexion.commit()

    messagebox.showinfo("Venta realizada",f"Total: ${total}")

    entry_idventa.delete(0,tk.END)
    entry_cantidad.delete(0,tk.END)

    mostrar_productos()


def ver_ventas():

    ventana_ventas = tk.Toplevel()
    ventana_ventas.title("Historial de Ventas")
    ventana_ventas.geometry("400x300")

    lista = tk.Listbox(ventana_ventas,width=50)
    lista.pack(pady=20)

    cursor.execute("SELECT * FROM ventas")
    ventas = cursor.fetchall()

    for venta in ventas:
        texto = f"Venta {venta[0]}  Producto:{venta[1]}  Cantidad:{venta[2]}  Total:${venta[3]}"
        lista.insert(tk.END,texto)


# ---------------- INTERFAZ ----------------

ventana = tk.Tk()
ventana.title("Sistema de Ventas")
ventana.geometry("600x500")

titulo = tk.Label(ventana,text="SISTEMA DE VENTAS",font=("Arial",20))
titulo.pack(pady=10)

# -------- PRODUCTOS --------

frame_productos = tk.LabelFrame(ventana,text="Agregar Producto")
frame_productos.pack(pady=10)

tk.Label(frame_productos,text="Nombre").grid(row=0,column=0)
tk.Label(frame_productos,text="Precio").grid(row=1,column=0)
tk.Label(frame_productos,text="Stock").grid(row=2,column=0)

entry_nombre = tk.Entry(frame_productos)
entry_precio = tk.Entry(frame_productos)
entry_stock = tk.Entry(frame_productos)

entry_nombre.grid(row=0,column=1)
entry_precio.grid(row=1,column=1)
entry_stock.grid(row=2,column=1)

btn_agregar = tk.Button(frame_productos,text="Agregar Producto",command=agregar_producto)
btn_agregar.grid(row=3,columnspan=2,pady=5)

# -------- LISTA PRODUCTOS --------

lista_productos = tk.Listbox(ventana,width=70)
lista_productos.pack(pady=10)

btn_actualizar = tk.Button(ventana,text="Actualizar Lista",command=mostrar_productos)
btn_actualizar.pack()

# -------- VENTAS --------

frame_ventas = tk.LabelFrame(ventana,text="Registrar Venta")
frame_ventas.pack(pady=10)

tk.Label(frame_ventas,text="ID Producto").grid(row=0,column=0)
tk.Label(frame_ventas,text="Cantidad").grid(row=1,column=0)

entry_idventa = tk.Entry(frame_ventas)
entry_cantidad = tk.Entry(frame_ventas)

entry_idventa.grid(row=0,column=1)
entry_cantidad.grid(row=1,column=1)

btn_vender = tk.Button(frame_ventas,text="Registrar Venta",command=registrar_venta)
btn_vender.grid(row=2,columnspan=2,pady=5)

# -------- VER VENTAS --------

btn_verventas = tk.Button(ventana,text="Ver Historial de Ventas",command=ver_ventas)
btn_verventas.pack(pady=10)

mostrar_productos()

ventana.mainloop()

