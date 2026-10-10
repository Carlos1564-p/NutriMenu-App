import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime

# --- BASES DE DATOS EN MEMORIA (SIMULANDO BACKEND) ---

MENU_DATABASE = {
    "Diabetes Tipo 2": [
        {"nombre": "Bowl de Quinua y Pechuga al Limón", "precio": 6.50, "desc": "Bajo índice glucémico, rico en fibra."},
        {"nombre": "Salmón al Horno con Vegetales al Vapor", "precio": 8.00, "desc": "Sin azúcares añadidos, alto en Omega-3."},
        {"nombre": "Pechuga de Pollo en Reducción de Balsámico", "precio": 7.00, "desc": "Acompañada de espárragos y brócoli."},
        {"nombre": "Hamburguesa de Lentejas sin Pan", "precio": 6.00, "desc": "Base de ensalada verde y aderezo de aguacate."},
        {"nombre": "Filet de Merluza a la Plancha", "precio": 7.50, "desc": "Con puré de coliflor cremoso sin mantequilla."},
        {"nombre": "Wrap de Lechuga con Atún y Vegetales", "precio": 5.80, "desc": "Proteína magra, cero carbohidratos refinados."}
    ],
    "Enfermedad Renal Crónica": [
        {"nombre": "Crema de Calabacín (Bajo Potasio)", "precio": 5.00, "desc": "Control riguroso de sodio, fósforo y potasio."},
        {"nombre": "Pollo Acorazonado con Arroz Blanco Tierno", "precio": 6.00, "desc": "Proteína de alto valor biológico ajustada."},
        {"nombre": "Tortilla de Claras con Zanahoria Rallada", "precio": 4.50, "desc": "Bajo fósforo, ideal para cenas ligeras."},
        {"nombre": "Filet de Pollo Hervido con Arroz y Chayota", "precio": 6.20, "desc": "Preparación limpia sin condimentos ricos en potasio."},
        {"nombre": "Arroz Caldoso con Pechuga Desmenuzada", "precio": 5.50, "desc": "Fácil digestión y control estricto de electrolitos."},
        {"nombre": "Pastel de Arroz Blanco con Pavo Magro", "precio": 6.80, "desc": "Bajo contenido mineral y proteico controlado."}
    ],
    "Hipertensión Severa": [
        {"nombre": "Ensalada Mediterránea de Oliva", "precio": 5.50, "desc": "Cero sodio añadido, aderezo cardioprotector."},
        {"nombre": "Pavo a las Finas Hierbas con Camote", "precio": 7.00, "desc": "Rico en magnesio y potasio equilibrado."},
        {"nombre": "Lomo de Cerdo Magro al Horno", "precio": 7.50, "desc": "Especias naturales sin sal, con vegetales asados."},
        {"nombre": "Bowl de Arroz Integral y Salteado de Pavo", "precio": 6.80, "desc": "Bajo en sodio, endulzado con hierbas frescas."},
        {"nombre": "Crema suave de Auyama sin Sal", "precio": 5.00, "desc": "Suave al paladar, rica en antioxidantes naturales."},
        {"nombre": "Pescado Blanco al Horno con Limón y Eneldo", "precio": 7.20, "desc": "Cardioprotector, cero sodio agregado."}
    ],
    "Celiaquía / Sin Gluten": [
        {"nombre": "Pasta de Garbanzos con Pesto de Albahaca", "precio": 6.80, "desc": "100% Libre de gluten certificado."},
        {"nombre": "Milanesa de Pollo con Harina de Yuca", "precio": 6.20, "desc": "Crujiente, libre de contaminación cruzada."},
        {"nombre": "Pizza casera con Base de Yuca y Vegetales", "precio": 7.50, "desc": "Queso bajo en grasa y masa libre de trigo."},
        {"nombre": "Risotto de Hongos Portobello", "precio": 8.00, "desc": "Arroz arborio certificado sin gluten."},
        {"nombre": "Bowl de Pollo, Aguacate y Arroz", "precio": 6.50, "desc": "Ingredientes naturales seguros para celíacos."},
        {"nombre": "Croquetas de Yuca y Carne Desmechada", "precio": 5.90, "desc": "Horneadas, sin reboques de trigo tradicional."}
    ]
}

# Cola global de pedidos para cocinas (Prioridad: 1=Alta/Renal, 2=Media, 3=Baja)
ORDER_QUEUE = [
    {"id": "ORD-101", "estado": "Distrito Capital", "patologia": "Enfermedad Renal Crónica", "plato": "Crema de Calabacín (Bajo Potasio)", "prioridad": 1, "prioridad_txt": "ALTA (Renal)", "hora": "14:15", "cliente": "María Pérez"},
    {"id": "ORD-102", "estado": "Carabobo", "patologia": "Diabetes Tipo 2", "plato": "Bowl de Quinua y Pechuga al Limón", "prioridad": 2, "prioridad_txt": "MEDIA", "hora": "14:20", "cliente": "Carlos Gómez"}
]

# Base de datos de restaurantes afiliados por estado
RESTAURANTS_DB = [
    {"nombre": "NutriKitchen Chacao", "estado": "Distrito Capital", "especialidad": "Renal y Diabetes", "contacto": "0414-1112233"},
    {"nombre": "Vida Sana El Viñedo", "estado": "Carabobo", "especialidad": "Hipertensión y Sin Gluten", "contacto": "0412-4445566"},
    {"nombre": "SaludExpress 5 de Julio", "estado": "Zulia", "especialidad": "General Terapéutica", "contacto": "0424-7778899"}
]


class NutriMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NutriMenu App - Ecosistema Venezuela")
        self.root.geometry("460x780")
        self.root.configure(bg="#F4F6F5")

        # Encabezado con botones de navegación superior
        header_frame = tk.Frame(root, bg="#2E7D32", height=80)
        header_frame.pack(fill="x")
        
        lbl_title = tk.Label(header_frame, text="NutriMenu Manager", font=("Helvetica", 14, "bold"), fg="white", bg="#2E7D32")
        lbl_title.pack(pady=4)

        nav_frame = tk.Frame(header_frame, bg="#2E7D32")
        nav_frame.pack(pady=2)

        tk.Button(nav_frame, text="🛒 Menú Pacientes", bg="#1B5E20", fg="white", font=("Helvetica", 8, "bold"), bd=0, padx=6, pady=2, command=self.mostrar_vista_clientes).pack(side="left", padx=3)
        tk.Button(nav_frame, text="👨‍🍳 Cocina / Pedidos", bg="#1B5E20", fg="white", font=("Helvetica", 8, "bold"), bd=0, padx=6, pady=2, command=self.mostrar_vista_cocina).pack(side="left", padx=3)
        tk.Button(nav_frame, text="🏪 Afiliar Local", bg="#1B5E20", fg="white", font=("Helvetica", 8, "bold"), bd=0, padx=6, pady=2, command=self.mostrar_vista_afiliacion).pack(side="left", padx=3)

        # Contenedor dinámico principal
        self.main_container = tk.Frame(root, bg="#F4F6F5")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.mostrar_vista_clientes()

    def limpiar_contenedor(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # ==================== VISTA 1: CLIENTES / MENÚ ====================
    def mostrar_vista_clientes(self):
        self.limpiar_contenedor()

        tk.Label(self.main_container, text="Seleccione su Patología:", font=("Helvetica", 10, "bold"), bg="#F4F6F5", anchor="w").pack(fill="x")
        
        self.patologia_var = tk.StringVar(value="Diabetes Tipo 2")
        combo = ttk.Combobox(self.main_container, textvariable=self.patologia_var, values=list(MENU_DATABASE.keys()), state="readonly", font=("Helvetica", 10))
        combo.pack(fill="x", pady=5)
        combo.bind("<<ComboboxSelected>>", self.actualizar_menu)

        # Contenedor con Scroll para los platos
        container_scroll = tk.Frame(self.main_container, bg="#F4F6F5")
        container_scroll.pack(fill="both", expand=True, pady=5)

        self.canvas = tk.Canvas(container_scroll, bg="#F4F6F5", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container_scroll, orient="vertical", command=self.canvas.yview)
        self.canvas_frame = tk.Frame(self.canvas, bg="#F4F6F5")

        self.canvas_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.actualizar_menu()

    def actualizar_menu(self, event=None):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        patologia = self.patologia_var.get()
        platos = MENU_DATABASE.get(patologia, [])

        for plato in platos:
            card = tk.Frame(self.canvas_frame, bg="white", bd=1, relief="solid", padx=10, pady=8)
            card.pack(fill="x", pady=5, ipadx=5)

            tk.Label(card, text=plato['nombre'], font=("Helvetica", 10, "bold"), fg="#333333", bg="white").pack(anchor="w")
            tk.Label(card, text=f"Precio: ${plato['precio']:.2f}", font=("Helvetica", 9, "bold"), fg="#2E7D32", bg="white").pack(anchor="w")
            tk.Label(card, text=plato['desc'], font=("Helvetica", 8), fg="#666666", bg="white", wraplength=380, justify="left").pack(anchor="w", pady=2)

            btn_pedir = tk.Button(card, text="Pedir y Configurar Entrega", bg="#0288D1", fg="white", font=("Helvetica", 8, "bold"), bd=0, padx=8, pady=4, command=lambda p=plato, pat=patologia: self.abrir_checkout(p, pat))
            btn_pedir.pack(anchor="e", pady=2)

    def abrir_checkout(self, plato, patologia):
        top = tk.Toplevel(self.root)
        top.title("Checkout y Delivery")
        top.geometry("380x640")
        top.configure(bg="#F4F6F5")

        tk.Label(top, text=f"Pedido: {plato['nombre']}\nPatología: {patologia}", font=("Helvetica", 10, "bold"), bg="#F4F6F5", justify="center").pack(pady=10)
        
        tk.Label(top, text="Estado de Destino:", font=("Helvetica", 9, "bold"), bg="#F4F6F5").pack(anchor="w", padx=20)
        estado_combo = ttk.Combobox(top, values=["Distrito Capital", "Carabobo", "Zulia", "Lara", "Miranda", "Anzoátegui"], state="readonly")
        estado_combo.set("Distrito Capital")
        estado_combo.pack(fill="x", padx=20, pady=5)

        tk.Label(top, text="Dirección Específica:", font=("Helvetica", 9, "bold"), bg="#F4F6F5").pack(anchor="w", padx=20)
        dir_entry = tk.Entry(top, font=("Helvetica", 9))
        dir_entry.pack(fill="x", padx=20, pady=5)
        dir_entry.insert(0, "Av. Francisco de Miranda...")

        tk.Label(top, text="Opción de Envío:", font=("Helvetica", 9, "bold"), bg="#F4F6F5").pack(anchor="w", padx=20, pady=(5, 0))
        delivery_options = {"Delivery Motorizado (Express) - $2.50": 2.50, "Retiro en Dark Kitchen - $0.00": 0.00}
        delivery_combo = ttk.Combobox(top, values=list(delivery_options.keys()), state="readonly")
        delivery_combo.set("Delivery Motorizado (Express) - $2.50")
        delivery_combo.pack(fill="x", padx=20, pady=5)

        tk.Label(top, text="Método de Pago:", font=("Helvetica", 9, "bold"), bg="#F4F6F5").pack(anchor="w", padx=20, pady=(5, 0))
        metodo_combo = ttk.Combobox(top, values=["Pago Móvil (Banesco/Mercantil)", "Zelle", "Binance Pay"], state="readonly")
        metodo_combo.set("Pago Móvil (Banesco/Mercantil)")
        metodo_combo.pack(fill="x", padx=20, pady=5)

        tk.Label(top, text="Nro. Referencia / Comprobante:", font=("Helvetica", 9, "bold"), bg="#F4F6F5").pack(anchor="w", padx=20)
        ref_entry = tk.Entry(top, font=("Helvetica", 10))
        ref_entry.pack(fill="x", padx=20, pady=5)

        def procesar():
            ref = ref_entry.get().strip()
            if not ref:
                messagebox.showerror("Error", "Ingrese el número de referencia del pago.", parent=top)
                return
            
            # Determinar prioridad clínica (Renal = Prioridad 1 más alta, resto = 2)
            prio = 1 if "Renal" in patologia else 2
            prio_txt = "ALTA (Renal)" if prio == 1 else "MEDIA"
            
            nueva_orden = {
                "id": f"ORD-{random.randint(103, 999)}",
                "estado": estado_combo.get(),
                "patologia": patologia,
                "plato": plato['nombre'],
                "prioridad": prio,
                "prioridad_txt": prio_txt,
                "hora": datetime.now().strftime("%H:%M"),
                "cliente": "Cliente App"
            }
            ORDER_QUEUE.append(nueva_orden)

            messagebox.showinfo("¡Pedido Exitoso!", f"Registrado correctamente.\nAsignado a cocina en {estado_combo.get()}.\nPrioridad: {prio_txt}", parent=top)
            top.destroy()

        tk.Button(top, text="Confirmar y Enviar a Cocina", bg="#388E3C", fg="white", font=("Helvetica", 10, "bold"), bd=0, pady=8, command=procesar).pack(fill="x", padx=20, pady=15)

    # ==================== VISTA 2: PANEL DE COCINAS Y PRIORIDADES ====================
    def mostrar_vista_cocina(self):
        self.limpiar_contenedor()

        tk.Label(self.main_container, text="Panel de Cocinas: Órdenes por Prioridad y Tiempo", font=("Helvetica", 11, "bold"), fg="#2E7D32", bg="#F4F6F5").pack(anchor="w", pady=5)
        tk.Label(self.main_container, text="Ordenado por rigor clínico y hora de recepción:", font=("Helvetica", 8), fg="#666", bg="#F4F6F5").pack(anchor="w")

        # Contenedor con scroll para la cola de órdenes
        frame_cola = tk.Frame(self.main_container, bg="#F4F6F5")
        frame_cola.pack(fill="both", expand=True, pady=5)

        # Ordenar cola por prioridad numérica ascendente (1 primero) y luego por hora
        cola_ordenada = sorted(ORDER_QUEUE, key=lambda x: (x['prioridad'], x['hora']))

        for orden in cola_ordenada:
            color_fondo = "#FFEBEE" if orden['prioridad'] == 1 else "white" # Rojo claro si es alta prioridad renal
            card = tk.Frame(frame_cola, bg=color_fondo, bd=1, relief="solid", padx=10, pady=8)
            card.pack(fill="x", pady=5)

            tk.Label(card, text=f"[{orden['id']}] - Estado: {orden['estado']} ({orden['hora']})", font=("Helvetica", 9, "bold"), bg=color_fondo).pack(anchor="w")
            tk.Label(card, text=f"Plato: {orden['plato']}", font=("Helvetica", 9), bg=color_fondo).pack(anchor="w")
            tk.Label(card, text=f"Prioridad: {orden['prioridad_txt']} | Patología: {orden['patologia']}", font=("Helvetica", 8, "italic"), fg="#C62828" if orden['prioridad']==1 else "#333", bg=color_fondo).pack(anchor="w")

    # ==================== VISTA 3: AFILIACIÓN DE RESTAURANTES ====================
    def mostrar_vista_afiliacion(self):
        self.limpiar_contenedor()

        tk.Label(self.main_container, text="Afiliación de Restaurantes Saludables", font=("Helvetica", 11, "bold"), fg="#2E7D32", bg="#F4F6F5").pack(anchor="w", pady=5)
        
        tk.Label(self.main_container, text="Nombre del Local / Dark Kitchen:", font=("Helvetica", 9, "bold"), bg="#F4F6F5").pack(anchor="w", pady=(5, 0))
        nombre_entry = tk.Entry(self.main_container, font=("Helvetica", 9))
        nombre_entry.pack(fill="x", pady=2)

        tk.Label(self.main_container, text="Estado de Ubicación:", font=("Helvetica", 9, "bold"), bg="#F4F6F5").pack(anchor="w", pady=(5, 0))
        estado_af_combo = ttk.Combobox(self.main_container, values=["Distrito Capital", "Carabobo", "Zulia", "Lara", "Miranda", "Anzoátegui"], state="readonly")
        estado_af_combo.set("Distrito Capital")
        estado_af_combo.pack(fill="x", pady=2)

        tk.Label(self.main_container, text="Especialidad Dietoterapéutica:", font=("Helvetica", 9, "bold"), bg="#F4F6F5").pack(anchor="w", pady=(5, 0))
        esp_entry = tk.Entry(self.main_container, font=("Helvetica", 9))
        esp_entry.pack(fill="x", pady=2)
        esp_entry.insert(0, "Ej: Diabetes, Renal, Hipertensión")

        tk.Label(self.main_container, text="Teléfono / Contacto:", font=("Helvetica", 9, "bold"), bg="#F4F6F5").pack(anchor="w", pady=(5, 0))
        tel_entry = tk.Entry(self.main_container, font=("Helvetica", 9))
        tel_entry.pack(fill="x", pady=2)

        def registrar_local():
            nom = nombre_entry.get().strip()
            est = estado_af_combo.get().strip()
            esp = esp_entry.get().strip()
            tel = tel_entry.get().strip()

            if not nom or not tel:
                messagebox.showerror("Error", "Debe rellenar el nombre y el teléfono de contacto.")
                return

            RESTAURANTS_DB.append({"nombre": nom, "estado": est, "especialidad": esp, "contacto": tel})
            messagebox.showinfo("¡Afiliación Exitosa!", f"El restaurante '{nom}' en {est} ha sido registrado en la red de cocinas aliadas.")
            self.mostrar_vista_clientes()

        tk.Button(self.main_container, text="Registrar Restaurante Aliado", bg="#388E3C", fg="white", font=("Helvetica", 10, "bold"), bd=0, pady=8, command=registrar_local).pack(fill="x", pady=20)

        # Mostrar lista actual de afiliados
        tk.Label(self.main_container, text="Red Actual de Cocinas Afiliadas:", font=("Helvetica", 9, "bold"), bg="#F4F6F5").pack(anchor="w", pady=(10, 2))
        for r in RESTAURANTS_DB:
            lbl = tk.Label(self.main_container, text=f"• {r['nombre']} ({r['estado']}) - {r['especialidad']}", font=("Helvetica", 8), bg="white", anchor="w", padx=5, pady=3)
            lbl.pack(fill="x", pady=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = NutriMenuApp(root)
    root.mainloop()