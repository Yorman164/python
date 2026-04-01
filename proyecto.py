import tkinter as tk
from tkinter import messagebox

# ---------------- CLASE PRODUCTO ----------------
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


# ---------------- CLASE INVENTARIO ----------------
class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def obtener_productos(self):
        return self.productos


# ---------------- CLASE CARRITO ----------------
class Carrito:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def calcular_total(self):
        return sum(p.precio for p in self.productos)

    def vaciar(self):
        self.productos.clear()


# ---------------- CLASE INTERFAZ ----------------
class CajeroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cajero de Supermercado")

        self.inventario = Inventario()
        self.carrito = Carrito()

        self.crear_interfaz()

    # ----------- INTERFAZ -----------
    def crear_interfaz(self):

        # --- FORMULARIO ---
        tk.Label(self.root, text="Nombre del producto").pack()
        self.entry_nombre = tk.Entry(self.root)
        self.entry_nombre.pack()

        tk.Label(self.root, text="Precio").pack()
        self.entry_precio = tk.Entry(self.root)
        self.entry_precio.pack()

        tk.Button(self.root, text="Agregar al inventario", command=self.agregar_producto).pack(pady=5)

        # --- LISTA ---
        tk.Label(self.root, text="Inventario").pack()
        self.lista = tk.Listbox(self.root)
        self.lista.pack()

        # --- BOTONES ---
        tk.Button(self.root, text="Agregar al carrito", command=self.agregar_al_carrito).pack()
        tk.Button(self.root, text="Mostrar total", command=self.mostrar_total).pack()
        tk.Button(self.root, text="Vaciar carrito", command=self.vaciar_carrito).pack()

        # --- FACTURA ---
        self.texto = tk.Text(self.root, height=10, width=40)
        self.texto.pack()

    # ----------- LÓGICA -----------
    def agregar_producto(self):
        nombre = self.entry_nombre.get()
        precio = self.entry_precio.get()

        if not nombre or not precio:
            messagebox.showwarning("Error", "Complete todos los campos")
            return

        try:
            precio = float(precio)
        except:
            messagebox.showerror("Error", "Precio inválido")
            return

        producto = Producto(nombre, precio)
        self.inventario.agregar_producto(producto)

        self.actualizar_lista()

        self.entry_nombre.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)

    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        for producto in self.inventario.obtener_productos():
            self.lista.insert(tk.END, str(producto))

    def agregar_al_carrito(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showwarning("Error", "Seleccione un producto")
            return

        producto = self.inventario.obtener_productos()[seleccion[0]]
        self.carrito.agregar_producto(producto)

        self.texto.insert(tk.END, f"{producto}\n")

    def mostrar_total(self):
        total = self.carrito.calcular_total()
        self.texto.insert(tk.END, f"\nTOTAL: ${total}\n\n")

    def vaciar_carrito(self):
        self.carrito.vaciar()
        self.texto.delete(1.0, tk.END)
        messagebox.showinfo("Info", "Carrito vacío")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CajeroApp(root)
    root.mainloop()
