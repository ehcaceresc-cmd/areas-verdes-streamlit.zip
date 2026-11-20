import streamlit as st

from buscador import TEMAS, buscar, cargar_normas

st.set_page_config(page_title="Normas de Áreas Verdes del Perú", page_icon="🌳", layout="centered")


@st.cache_data
def normas_cargadas():
    return cargar_normas()


def formatear_fecha(f):
    meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    partes = str(f).split("-")
    try:
        if len(partes) == 3:
            return f"{int(partes[2])} {meses[int(partes[1]) - 1]} {partes[0]}"
        if len(partes) == 2:
            return f"{meses[int(partes[1]) - 1]} {partes[0]}"
    except (ValueError, IndexError):
        pass
    return str(f)


NORMAS = normas_cargadas()

st.title("🌳 Normas de áreas verdes del Perú")
st.caption("Leyes, reglamentos, guías y ordenanzas sobre parques, arbolado y espacios públicos.")

texto = st.text_input(
    "Buscar",
    placeholder="Ej.: áreas verdes, parques, arbolado, habilitación urbana, 31199…",
)

col1, col2 = st.columns(2)
with col1:
    tema_sel = st.selectbox(
        "Tema",
        options=[""] + list(TEMAS),
        format_func=lambda k: "Todos" if k == "" else TEMAS[k],
    )
with col2:
    tipos = sorted({n["tipo"] for n in NORMAS})
    tipo_sel = st.selectbox("Tipo de norma", options=[""] + tipos, format_func=lambda t: t or "Todos")

solo_ver = st.checkbox("Solo normas verificadas con fuente oficial")

resultados = buscar(
    NORMAS,
    texto=texto,
    tema=tema_sel or None,
    tipo=tipo_sel or None,
    solo_verificadas=solo_ver,
)

st.write(f"**{len(resultados)}** {'norma encontrada' if len(resultados) == 1 else 'normas encontradas'}")

if not resultados:
    st.info("No se encontraron normas. Prueba con otras palabras o quita algún filtro.")

for n in resultados:
    with st.container(border=True):
        etiquetas = " · ".join(TEMAS[t] for t in n["temas"])
        sello = "✅ Verificada" if n.get("verificado") else "⚠️ Confirmar vigencia"
        st.caption(f"{etiquetas}  |  {sello}")
        st.subheader(n["titulo"])
        st.caption(f"{n['tipo']} N.° {n['numero']} · {formatear_fecha(n['fecha'])} · {n['entidad']}")
        st.write(n["resumen"])
        st.link_button("Ver norma en la fuente oficial", n["url"])

st.divider()
st.caption(
    "Esta base es orientativa y no incluye todas las ordenanzas municipales. Las normas pueden modificarse "
    "o derogarse: confirma siempre el texto vigente en El Peruano o gob.pe. No constituye asesoría legal."
)
