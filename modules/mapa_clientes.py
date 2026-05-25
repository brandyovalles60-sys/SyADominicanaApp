import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
from database.conexion import conectar
from modules.auditoria import registrar_accion
from streamlit_js_eval import get_geolocation


def cargar_clientes_mapa():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT nombre, latitud, longitud
        FROM clientes
        WHERE latitud IS NOT NULL
          AND longitud IS NOT NULL
    """)

    datos = cursor.fetchall()

    df = pd.DataFrame(datos, columns=["nombre", "lat", "lon"])

    if not df.empty:
        df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
        df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
        df = df.dropna(subset=["lat", "lon"])

    return df


@st.cache_data(ttl=900)
def buscar_restaurantes(lat, lon, radio):
    query = f"""
    [out:json][timeout:25];
    (
        node["amenity"~"restaurant|bar|cafe|fast_food"](around:{radio},{lat},{lon});
        way["amenity"~"restaurant|bar|cafe|fast_food"](around:{radio},{lat},{lon});
        relation["amenity"~"restaurant|bar|cafe|fast_food"](around:{radio},{lat},{lon});
    );
    out center;
    """

    url = "https://overpass-api.de/api/interpreter"

    try:
        headers = {
            "User-Agent": "SyA-Dominicana-App/1.0",
            "Accept": "application/json"
        }

        response = requests.post(
            url,
            data={"data": query},
            headers=headers,
            timeout=25
        )

        if response.status_code != 200:
            st.error(f"Error API Overpass. Código: {response.status_code}")
            st.code(response.text[:500])
            return pd.DataFrame(columns=["nombre", "lat", "lon"])

        data = response.json()

    except Exception as e:
        st.error(f"Error conectando con Overpass API: {e}")

    restaurantes = []

    for r in data.get("elements", []):
        tags = r.get("tags", {})
        nombre = tags.get("name", "Restaurante sin nombre")

        if "lat" in r and "lon" in r:
            lat_r = r["lat"]
            lon_r = r["lon"]
        elif "center" in r:
            lat_r = r["center"]["lat"]
            lon_r = r["center"]["lon"]
        else:
            continue

        restaurantes.append({
            "nombre": nombre,
            "lat": lat_r,
            "lon": lon_r
        })

    df = pd.DataFrame(restaurantes)

    if not df.empty:
        df = df.drop_duplicates(subset=["nombre", "lat", "lon"])

    return df


def pagina_mapa():

    st.title("🗺️ Mapa Comercial de Clientes")
    st.write("Explora clientes actuales y restaurantes potenciales cerca de zonas comerciales.")

    st.markdown("""
    <style>
    .map-card {
        background: rgba(17,24,39,0.92);
        border: 1px solid rgba(220,38,38,0.35);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 0 20px rgba(220,38,38,0.18);
        animation: fadeIn .5s ease-in-out;
    }
    .map-title {
        color: white;
        font-size: 22px;
        font-weight: 900;
    }
    .map-text {
        color: #d1d5db;
        font-size: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    ciudades = {
        "Santo Domingo": (18.4861, -69.9312),
        "Santiago": (19.4517, -70.6970),
        "Punta Cana": (18.5601, -68.3725),
        "La Romana": (18.4273, -68.9728),
        "San Pedro de Macorís": (18.4539, -69.3086),
        "Puerto Plata": (19.7902, -70.6884),
        "La Vega": (19.2230, -70.5290),
        "San Cristóbal": (18.4167, -70.1000),
        "Bonao": (18.9369, -70.4092),
        "Baní": (18.2796, -70.3319)
    }


    st.subheader("📍 Ubicación automática")

    ubicacion = get_geolocation(component_key="ubicacion_actual_mapa")

    usar_mi_ubicacion = st.toggle(
        "Usar mi ubicación actual",
        value=True,
        key="toggle_ubicacion_mapa"
    )

    if usar_mi_ubicacion and ubicacion and "coords" in ubicacion:

        lat_base = ubicacion["coords"]["latitude"]
        lon_base = ubicacion["coords"]["longitude"]

        ciudad = "Mi ubicación actual"

        seleccion_radio = st.selectbox(
            "Radio de búsqueda",
            ["1 km", "3 km", "5 km", "10 km"],
            index=1,
            key="radio_ubicacion_actual"
        )

    else:

        st.info("Permite acceso a ubicación o selecciona ciudad manual.")

        col_a, col_b = st.columns(2)

        with col_a:
            ciudad = st.selectbox(
                "Seleccionar zona comercial",
                list(ciudades.keys()),
                key="ciudad_manual_mapa"
            )

        with col_b:
            seleccion_radio = st.selectbox(
                "Radio de búsqueda",
                ["1 km", "3 km", "5 km", "10 km"],
                index=1
            )

        lat_base, lon_base = ciudades[ciudad]

    

    

    

    opciones_radio = {
        "1 km": 1000,
        "3 km": 3000,
        "5 km": 5000,
        "10 km": 10000
    }

    
    radio = opciones_radio[seleccion_radio]

    clientes = cargar_clientes_mapa()

    with st.spinner("Buscando restaurantes potenciales..."):
        restaurantes = buscar_restaurantes(lat_base, lon_base, radio)
        st.caption(f"📍 Buscando desde: lat {lat_base}, lon {lon_base} | Radio: {radio} metros")
        st.caption(f"🍽️ Resultados encontrados: {len(restaurantes)}")

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Clientes actuales", len(clientes))
    col2.metric("🍽️ Potenciales encontrados", len(restaurantes))
    col3.metric("📍 Zona", ciudad)

    st.divider()

    if clientes.empty and restaurantes.empty:

        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #78350f, #111827);
            border: 1px solid rgba(245,158,11,0.45);
            border-radius: 18px;
            padding: 22px;
            margin-top: 20px;
            box-shadow: 0 0 22px rgba(245,158,11,0.18);
        ">
            <h3 style="color:white;">🟡 Sin resultados en esta búsqueda</h3>
            <p style="color:#fde68a;">
                No encontramos restaurantes cercanos en esta zona o la API tardó demasiado.
            </p>
            <p style="color:#d1d5db;">
                Prueba con otro radio, otra ciudad o vuelve a intentar en unos segundos.
            </p>
        </div>
        """, unsafe_allow_html=True)

        return

    clientes_mapa = clientes.copy()
    clientes_mapa["tipo"] = "Cliente actual"

    restaurantes_mapa = restaurantes.copy()
    restaurantes_mapa["tipo"] = "Potencial"

    mapa_df = pd.concat([clientes_mapa, restaurantes_mapa], ignore_index=True)

    color_exp = """
    tipo == 'Cliente actual' ? [34, 197, 94, 180] : [220, 38, 38, 170]
    """

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=mapa_df,
        get_position='[lon, lat]',
        get_color=color_exp,
        get_radius=70,
        pickable=True,
        auto_highlight=True
    )

    view_state = pdk.ViewState(
        latitude=lat_base,
        longitude=lon_base,
        zoom=12,
        pitch=0
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                "html": "<b>{nombre}</b><br/>Tipo: {tipo}",
                "style": {"backgroundColor": "#111827", "color": "white"}
            },
            map_style=None
        ),
        use_container_width=True
    )

    st.divider()

    st.subheader("🍽️ Restaurantes potenciales")

    if restaurantes.empty:
        st.info("No se encontraron restaurantes potenciales en esta zona.")
        return

    seleccion = st.selectbox(
        "Seleccionar restaurante potencial",
        restaurantes["nombre"].tolist(),
        key="select_restaurante_potencial"
    )

    rest = restaurantes[restaurantes["nombre"] == seleccion].iloc[0]

    lat_rest = rest["lat"]
    lon_rest = rest["lon"]

    st.markdown(f"""
    <div class="map-card">
        <div class="map-title">🍽️ {rest['nombre']}</div>
        <div class="map-text">Latitud: {lat_rest}</div>
        <div class="map-text">Longitud: {lon_rest}</div>
        <div class="map-text">Zona: {ciudad}</div>
    </div>
    """, unsafe_allow_html=True)

    link_maps = f"https://www.google.com/maps?q={lat_rest},{lon_rest}"
    link_imagen = f"https://www.google.com/search?tbm=isch&q={str(rest['nombre']).replace(' ', '+')}"

    colx, coly = st.columns(2)

    with colx:
        st.link_button("📍 Abrir en Google Maps", link_maps, width="stretch")

    with coly:
        st.link_button("🖼️ Ver imágenes", link_imagen, width="stretch")

    telefono = st.text_input("Teléfono del restaurante potencial")

    if st.button("💾 Guardar como cliente potencial", width="stretch"):

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO clientes_potenciales
            (nombre, telefono, latitud, longitud)
            VALUES (%s,%s,%s,%s)
        """, (
            rest["nombre"],
            telefono,
            lat_rest,
            lon_rest
        ))

        conexion.commit()

        registrar_accion(
            "Mapa",
            "Guardar cliente potencial",
            f"Restaurante: {rest['nombre']} | Zona: {ciudad}"
        )

        st.success("Cliente potencial guardado correctamente.")
        st.rerun()