import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
from database.conexion import conectar


st.write("🚨 ESTE ES EL ARCHIVO REAL 🚨")
st.write("MAPA BUENO")






def pagina_mapa():
   
    st.write("🔥 ESTE ES EL MAPA NUEVO 🔥")
    conexion = conectar()
    cursor = conexion.cursor()

    # -----------------------------
    # CLIENTES EXISTENTES
    # -----------------------------
    cursor.execute("""
    SELECT nombre, latitud, longitud 
    FROM clientes
    WHERE latitud IS NOT NULL
    """)

    datos = cursor.fetchall()

    clientes = pd.DataFrame(datos, columns=[
        "nombre",
        "lat",
        "lon"
    ])
    # -----------------------------
    # TITULO
    # -----------------------------
    st.title("🗺️ Mapa Comercial de Clientes")
    st.info("Explora restaurantes cercanos y conviértelos en clientes 🚀")

    st.write("Encuentra clientes y nuevos restaurantes cercanos.")

    # -----------------------------
    # CIUDADES
    # -----------------------------
    ciudades = {
        "Santo Domingo": (18.4861, -69.9312),
        "Santiago": (19.4517, -70.6970),
        "Punta Cana": (18.5601, -68.3725),
        "La Romana": (18.4273, -68.9728),
        "San Pedro de Macoris": (18.4539, -69.3086),
        "Puerto Plata": (19.7902, -70.6884),
        "La Vega": (19.2230, -70.5290),
        "San Cristobal": (18.4167, -70.1000),
        "Bonao": (18.9369, -70.4092),
        "Bani": (18.2796, -70.3319)
    }

    ciudad = st.selectbox(
        "Seleccionar ciudad",
        list(ciudades.keys())
    )

    lat_base, lon_base = ciudades[ciudad]

    # -----------------------------
    # RADIO BUSQUEDA
    # -----------------------------
    opciones_radio = {
        "1 km": 1000,
        "3 km": 3000,
        "5 km": 5000,
        "10 km": 10000
    }

    seleccion_radio = st.selectbox(
        "Buscar restaurantes en un radio de:",
        list(opciones_radio.keys())
    )

    radio = opciones_radio[seleccion_radio]

    # -----------------------------
    # BUSCAR RESTAURANTES
    # -----------------------------
    @st.cache_data(ttl=600)
    def buscar_restaurantes(lat, lon, radio):

        query = f"""
        [out:json];
        node["amenity"="restaurant"](around:{radio},{lat},{lon});
        out body;
        """

        url = "https://overpass-api.de/api/interpreter"

        try:

            response = requests.post(url, data=query, timeout=20)

            if response.status_code != 200:
                return pd.DataFrame(columns=["nombre","lat","lon"])

            data = response.json()

        except Exception as e:
            st.error(f"Error conectando API: {e}")
            return pd.DataFrame(columns=["nombre","lat","lon"])

        restaurantes = []

        for r in data.get("elements", []):
            restaurantes.append({
                "nombre": r.get("tags", {}).get("name","Restaurante"),
                "lat": r["lat"],
                "lon": r["lon"]
            })

        return pd.DataFrame(restaurantes)

    # -----------------------------
    # BUSCAR RESTAURANTES
    # -----------------------------
    with st.spinner("Buscando restaurantes cercanos..."):
        restaurantes = buscar_restaurantes(lat_base, lon_base, radio)

        st.write("DEBUG RESTAURANTES:", restaurantes)

    if restaurantes.empty:
        restaurantes = pd.DataFrame([
            {"nombre": "Zona seleccionada", "lat": lat_base, "lon": lon_base}
        ])
        

    # -----------------------------
    # MAPA
    # -----------------------------

    if clientes.empty:
        clientes = pd.DataFrame(columns=["nombre", "lat", "lon"])

    layer_clientes = pdk.Layer(
        "ScatterplotLayer",
        data=clientes,
        get_position='[lon, lat]',
        get_color='[0,200,0,160]',
        get_radius=120,
        pickable=True,
    )

    layer_restaurantes = pdk.Layer(
        "ScatterplotLayer",
        data=restaurantes,
        get_position='[lon, lat]',
        get_color='[200,0,0,160]',
        get_radius=100,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=lat_base,
        longitude=lon_base,
        zoom=13
    )

    layers = [layer_restaurantes]

    if not clientes.empty:
        layers.append(layer_clientes)

    if clientes.empty and restaurantes.empty:
        restaurantes = pd.DataFrame([
            {"nombre": "Punto inicial", "lat": lat_base, "lon": lon_base}
        ])

    st.pydeck_chart(pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={"text": "{nombre}"}
    ))

    if clientes.empty and restaurantes.empty:
        st.warning("No hay datos aún. Intenta cambiar la ciudad o el radio.")
    # -----------------------------
    # LISTA RESTAURANTES
    # -----------------------------
    st.subheader("🍽️ Restaurantes encontrados")
    st.success("Selecciona un restaurante y revisa su ubicación e imágenes antes de guardarlo")

    if not restaurantes.empty:

        seleccion = st.selectbox(
            "Seleccionar restaurante",
            restaurantes["nombre"]
        )

        rest = restaurantes[restaurantes["nombre"] == seleccion].iloc[0]

        lat_rest = rest["lat"]
        lon_rest = rest["lon"]

        link_maps = f"https://www.google.com/maps?q={lat_rest},{lon_rest}"

        st.link_button("📍 Abrir en Google Maps", link_maps)

        nombre_rest = rest["nombre"]
        st.image(f"https://source.unsplash.com/400x300/?restaurant,{nombre_rest}")

        link_imagen = f"https://www.google.com/search?tbm=isch&q={nombre_rest.replace(' ', '+')}"

        st.markdown(f"🖼️ **Ver imágenes del restaurante:** [Buscar en Google]({link_imagen})")

        st.divider()
        st.subheader(f"📍 {nombre_rest}")

        telefono = st.text_input("Teléfono del restaurante")

        if st.button("Guardar como cliente potencial"):

            

            cursor.execute("""
            INSERT INTO clientes_potenciales
            (nombre, telefono, latitud, longitud)
            VALUES (%s,%s,%s,%s)
            """,(
                seleccion,
                telefono,
                rest["lat"],
                rest["lon"]
            ))

            conexion.commit()

            st.success("Cliente potencial guardado")

    else:

        st.info("No se encontraron restaurantes cercanos")


