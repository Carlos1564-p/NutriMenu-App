import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página web
st.set_page_config(
    page_title="NutriMenu - Venezuela",
    page_icon="🥗",
    layout="centered"
)

# --- BASES DE DATOS EN MEMORIA (SIMULANDO BACKEND) ---
if 'menu_db' not in st.session_state:
    st.session_state.menu_db = {
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

if 'order_queue' not in st.session_state:
    st.session_state.order_queue = [
        {"id": "ORD-101", "estado": "Distrito Capital", "patologia": "Enfermedad Renal Crónica", "plato": "Crema de Calabacín (Bajo Potasio)", "prioridad": 1, "prioridad_txt": "ALTA (Renal)", "hora": "14:15", "cliente": "María Pérez"}
    ]

if 'restaurants_db' not in st.session_state:
    st.session_state.restaurants_db = [
        {"nombre": "NutriKitchen Chacao", "estado": "Distrito Capital", "especialidad": "Renal y Diabetes", "contacto": "0414-1112233"},
        {"nombre": "Vida Sana El Viñedo", "estado": "Carabobo", "especialidad": "Hipertensión y Sin Gluten", "contacto": "0412-4445566"}
    ]

# --- ENCABEZADO ---
st.title("🥗 NutriMenu Venezuela")
st.markdown("*Alimentación Médica Especializada y Terapéutica a Domicilio*")
st.divider()

# Menú de Navegación Lateral (Sidebar)
menu_opcion = st.sidebar.radio("Navegación", ["🛒 Menú de Pacientes", "👨‍🍳 Panel de Cocina (Prioridades)", "🏪 Afiliar Restaurante"])

# ==================== VISTA 1: PACIENTES / PEDIDOS ====================
if menu_opcion == "🛒 Menú de Pacientes":
    st.subheader("Selecciona tu Condición o Patología")
    patologia_sel = st.selectbox("Patología:", list(st.session_state.menu_db.keys()))

    st.markdown("### Platillos Disponibles")
    platos = st.session_state.menu_db[patologia_sel]

    for i, plato in enumerate(platos):
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{plato['nombre']}**")
                st.caption(plato['desc'])
                st.markdown(f"Precio: **${plato['precio']:.2f}**")
            with col2:
                if st.button("Pedir", key=f"btn_{patologia_sel}_{i}"):
                    st.session_state.plato_seleccionado = plato
                    st.session_state.patologia_seleccionada = patologia_sel

    # Sección de Checkout si seleccionó un plato
    if 'plato_seleccionado' in st.session_state:
        st.divider()
        st.markdown(f"### 📋 Configurar Entrega para: *{st.session_state.plato_seleccionado['nombre']}*")
        
        with st.form("checkout_form"):
            estado = st.selectbox("Estado en Venezuela:", ["Distrito Capital", "Carabobo", "Zulia", "Lara", "Miranda", "Anzoátegui"])
            direccion = st.text_input("Dirección de Destino:", "Av. Francisco de Miranda, Torre...")
            delivery = st.selectbox("Opción de Envío:", ["Delivery Motorizado (Express) - $2.50", "Retiro en Dark Kitchen - $0.00"])
            sugerencia = st.text_input("Sugerencias especiales (opcional):", "Ej: Sin cebolla, extra sellado.")
            
            metodo_pago = st.selectbox("Método de Pago:", ["Pago Móvil (Banesco/Mercantil)", "Zelle", "Binance Pay (USDT)"])
            referencia = st.text_input("Número de Referencia del Pago:")
            
            submitted = st.form_submit_button("Confirmar Pedido")
            if submitted:
                if not referencia or not direccion:
                    st.error("Por favor, completa la dirección y el número de referencia del pago.")
                else:
                    prio = 1 if "Renal" in st.session_state.patologia_seleccionada else 2
                    prio_txt = "ALTA (Renal)" if prio == 1 else "MEDIA"
                    
                    nueva_orden = {
                        "id": f"ORD-{pd.np.random.randint(100, 999)}" if hasattr(pd, 'np') else f"ORD-{datetime.now().microsecond % 900 + 100}",
                        "estado": estado,
                        "patologia": st.session_state.patologia_seleccionada,
                        "plato": st.session_state.plato_seleccionado['nombre'],
                        "prioridad": prio,
                        "prioridad_txt": prio_txt,
                        "hora": datetime.now().strftime("%H:%M"),
                        "cliente": "Cliente Web"
                    }
                    st.session_state.order_queue.append(nueva_orden)
                    st.success("¡Pedido registrado con éxito! Enviado a cocina y logística.")
                    del st.session_state.plato_seleccionado

# ==================== VISTA 2: PANEL DE COCINA ====================
elif menu_opcion == "👨‍🍳 Panel de Cocina (Prioridades)":
    st.subheader("Panel Operativo para Dark Kitchens")
    st.markdown("Órdenes ordenadas automáticamente por **rigor clínico (prioridad)** y hora de llegada:")

    if not st.session_state.order_queue:
        st.info("No hay pedidos pendientes en la cola.")
    else:
        # Ordenar cola por prioridad numérica ascendente
        cola_ordenada = sorted(st.session_state.order_queue, key=lambda x: (x['prioridad'], x['hora']))

        for orden in cola_ordenada:
            if orden['prioridad'] == 1:
                st.error(f"🔴 **[{orden['id']}] Prioridad: {orden['prioridad_txt']}** | Estado: {orden['estado']} ({orden['hora']})\n\n**Plato:** {orden['plato']} | *Patología: {orden['patologia']}*")
            else:
                st.warning(f"🟡 **[{orden['id']}] Prioridad: {orden['prioridad_txt']}** | Estado: {orden['estado']} ({orden['hora']})\n\n**Plato:** {orden['plato']} | *Patología: {orden['patologia']}*")

# ==================== VISTA 3: AFILIACIÓN DE RESTAURANTES ====================
elif menu_opcion == "🏪 Afiliar Restaurante":
    st.subheader("Red de Cocinas y Restaurantes Aliados")
    st.markdown("Registra tu local especializado para formar parte de la red de despacho terapéutico.")

    with st.form("afiliacion_form"):
        nombre_local = st.text_input("Nombre del Local / Dark Kitchen:")
        estado_local = st.selectbox("Estado:", ["Distrito Capital", "Carabobo", "Zulia", "Lara", "Miranda", "Anzoátegui"])
        especialidad = st.text_input("Especialidades Médicas Cubiertas:", "Ej: Diabetes, Renal, Hipertensión")
        contacto = st.text_input("Teléfono de Contacto / WhatsApp:")
        
        submit_afiliacion = st.form_submit_button("Registrar Local")
        if submit_afiliacion:
            if not nombre_local or not contacto:
                st.error("Debes ingresar el nombre del local y el teléfono.")
            else:
                st.session_state.restaurants_db.append({
                    "nombre": nombre_local, 
                    "estado": estado_local, 
                    "especialidad": especialidad, 
                    "contacto": contacto
                })
                st.success(f"¡Restaurante '{nombre_local}' afiliado con éxito!")

    st.divider()
    st.markdown("### 📋 Restaurantes Activos en la Red")
    for r in st.session_state.restaurants_db:
        st.info(f"📍 **{r['nombre']}** ({r['estado']}) — *Especialidad:* {r['especialidad']} | *Contacto:* {r['contacto']}")