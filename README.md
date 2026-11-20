# Normas de Áreas Verdes del Perú (Streamlit)

Buscador de normas peruanas sobre áreas verdes, parques, arbolado y espacios públicos.
Filtra por tema, tipo de norma y "solo verificadas", y enlaza a la fuente oficial.

## Ejecutar en tu computadora

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Publicar en Streamlit Community Cloud

1. Sube **los archivos sueltos** (no el .zip) a la raíz de tu repositorio de GitHub:
   `streamlit_app.py`, `buscador.py`, `requirements.txt`, `data/normas.json`, etc.
2. En https://share.streamlit.io elige **Create app**.
3. Completa:
   - **Repository:** `tu-usuario/nombre-del-repo` (sin `.zip`)
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
4. Pulsa **Deploy**.

## Estructura

```
streamlit_app.py       Interfaz
buscador.py            Lógica de búsqueda
data/normas.json       Base de datos de normas
tests/test_buscador.py Pruebas (python tests/test_buscador.py)
requirements.txt       Dependencias
```

## Agregar o corregir normas

Edita `data/normas.json` y agrega un objeto con los mismos campos que los existentes
(`id`, `temas`, `tipo`, `numero`, `titulo`, `resumen`, `fecha`, `entidad`, `estado`,
`verificado`, `url`, `palabras`). Temas válidos: `espacios`, `planificacion`, `diseno`, `municipal`.
Luego ejecuta `python tests/test_buscador.py`.

## Importante

- La base es una **selección**, no un compendio completo; las ordenanzas municipales varían por distrito.
- Las normas con "Confirmar vigencia" se cargaron por conocimiento general: verifícalas antes de citarlas.
- Este proyecto no constituye asesoría legal.

## Licencia

MIT (ver `LICENSE`).
