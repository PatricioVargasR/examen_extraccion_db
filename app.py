import streamlit as st
import pandas as pd
from utils import *

st.set_page_config(page_title="App de análisis CSV", layout="wide")
st.title("📊 Aplicación Web para Análisis de CSV")

# 1. Carga de datos
st.header("1. Carga de datos")
file = st.file_uploader("Sube un archivo CSV", type=["csv"])

if file:
    df, error = cargar_csv(file)

    if error:
        st.error(f"Error al cargar CSV: {error}")
    else:
        st.success("CSV cargado correctamente")

        # 2. Preparación de datos
        st.header("2. Preparación de datos")

        if st.checkbox("2.1 Mostrar primeras N líneas"):
            n = st.number_input("Número de filas:", min_value=1, value=5)
            st.dataframe(mostrar_primeras_filas(df, n))

        if st.checkbox("2.2 Mostrar últimas N líneas"):
            n = st.number_input("Número de filas (últimas):", min_value=1, value=5, key="ultimas")
            st.dataframe(mostrar_ultimas_filas(df, n))

        if st.checkbox("2.3 Información básica del CSV"):
            col1, col2 = st.columns(2)

            with col1:
                st.text('Información general')
                st.text(obtener_info_basica_columna_1(df))

            with col2:
                st.text('Tipos de datos')
                st.dataframe(obtener_info_basica_columna2(df), use_container_width=True)

        if st.checkbox("2.4 Información estadistica del dataset"):
            st.dataframe(obtener_info_estadistica(df), use_container_width=True)

        if st.checkbox("2.5 Forma del dataset"):
            filas, columnas = obtener_forma(df)
            st.write(f"{filas} filas × {columnas} columnas")

        if st.checkbox("2.6 Lista de columnas"):
            st.write(obtener_columnas(df))

        # 3. Selección de datos
        st.header("3. Selección de datos")

        if st.checkbox("3.1 Seleccionar una columna"):
            col = st.selectbox("Columna:", df.columns)
            st.dataframe(df[[col]])

        if st.checkbox("3.2 Seleccionar múltiples columnas"):
            cols = st.multiselect("Columnas:", df.columns)
            if cols:
                st.dataframe(seleccionar_columnas(df, cols))

        # 4. Filtrado de filas
        st.header("4. Filtrado de filas")

        # if st.checkbox("4.1 Filtrar filas con condición"):

        #     num_cols = df.columns.tolist()
        #     if not num_cols:
        #         st.warning("No hay columnas numéricas disponibles para filtrar.")
        #     else:
        #         col = st.selectbox("Selecciona columna:", num_cols)

        #         if pd.api.types.is_numeric_dtype(df[col]):
        #             operador = st.selectbox("Operador:", [">", "<", "=="])
        #             valor = st.number_input("Valor para filtrar:")
        #         elif pd.api.types.is_string_dtype(df[col]):
        #             valor = st.text_input("Valor para filtrar:")
        #             operador = st.selectbox("Operador:", ["=="])

        #         else:
        #             st.warning("Tipo de dato no soportado para filtrar.")
        #             valor = None

        #         resultado = filtrar_filas(df, col, operador, valor)
        #         st.write(f"{len(resultado)} filas encontradas:")
        #         st.dataframe(resultado)

        if st.checkbox("4.1 Filtrar filas con múltiples condiciones"):

            columnas_disponibles = df.columns.tolist()
            condiciones = []

            st.markdown("### Selecciona y define condiciones de filtro")

            # Selector para columnas a usar en el filtrado
            columnas_a_filtrar = st.multiselect("Selecciona columnas para aplicar filtros:", columnas_disponibles)

            for idx, columna in enumerate(columnas_a_filtrar):
                st.markdown(f"#### Filtro {idx + 1}: `{columna}`")

                if pd.api.types.is_numeric_dtype(df[columna]):
                    operador = st.selectbox(f"Operador para `{columna}`:", [">", "<", "=="], key=f"op_{idx}")
                    valor = st.number_input(f"Valor para `{columna}`:", key=f"val_{idx}")
                elif pd.api.types.is_string_dtype(df[columna]):
                    operador = st.selectbox(f"Operador para `{columna}`:", ["=="], key=f"op_{idx}")
                    valor = st.text_input(f"Valor para `{columna}`:", key=f"val_{idx}")
                else:
                    st.warning(f"Tipo de dato no soportado para la columna `{columna}`.")
                    continue

                condiciones.append((columna, operador, valor))

            if condiciones:
                resultado = filtrar_filas_multiples(df, condiciones)
                st.success(f"{len(resultado)} filas encontradas con los filtros aplicados.")
                st.dataframe(resultado)
            else:
                st.info("Agrega al menos una condición válida para filtrar.")