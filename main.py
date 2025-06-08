import streamlit as st
import pandas as pd
import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
from io import StringIO

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Datos - NumPy & Pandas",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("📊 Aplicación de Análisis de Datos")
st.markdown("### Herramienta interactiva para análisis con NumPy y Pandas")

# Sidebar para navegación
st.sidebar.title("🔧 Herramientas")
option = st.sidebar.selectbox(
    "Selecciona una funcionalidad:",
    ["🏠 Inicio", "📁 Carga de Datos", "🔍 Preparación de Datos", "📋 Selección de Datos", "🔎 Filtrado de Datos", "🧮 Operaciones NumPy"]
)

# Función para cargar datos de ejemplo
@st.cache_data
def load_sample_data():
    """Carga datos de ejemplo para demostración"""
    data = {
        'Nombre': ['Ana', 'Luis', 'Sofía', 'Carlos', 'María', 'Pedro', 'Laura', 'Diego'],
        'Edad': [20, 22, 21, 23, 25, 24, 26, 19],
        'Calificación': [85, 90, 78, 92, 88, 76, 94, 82],
        'Ciudad': ['México', 'Madrid', 'Bogotá', 'Lima', 'Barcelona', 'Buenos Aires', 'Santiago', 'Quito'],
        'Salario': [25000, 30000, 22000, 35000, 28000, 24000, 38000, 21000]
    }
    return pd.DataFrame(data)

# Inicializar session state
if 'df' not in st.session_state:
    st.session_state.df = None

# PÁGINA DE INICIO
if option == "🏠 Inicio":
    st.markdown("""
    ## Bienvenido a la Aplicación de Análisis de Datos
    
    Esta aplicación te permite realizar análisis completos de datos utilizando las bibliotecas **NumPy** y **Pandas** de Python.
    
    ### 🚀 Funcionalidades disponibles:
    
    - **📁 Carga de Datos**: Sube archivos CSV o usa datos de ejem.plo
    - **🔍 Preparación de Datos**: Explora información básica del dataset
    - **📋 Selección de Datos**: Selecciona columnas específicas
    - **🔎 Filtrado de Datos**: Aplica filtros con diferentes condiciones
    - **🧮 Operaciones NumPy**: Realiza operaciones matemáticas avanzadas
    
    ### 📖 Cómo usar:
    1. Comienza cargando tus datos en la sección "Carga de Datos"
    2. Explora la información básica en "Preparación de Datos"
    3. Selecciona y filtra los datos según tus necesidades
    4. Realiza operaciones matemáticas con NumPy
    
    ¡Comienza seleccionando una opción del menú lateral!
    """)
    
    # Mostrar datos de ejemplo
    st.markdown("### 📊 Vista previa de datos de ejemplo:")
    sample_df = load_sample_data()
    st.dataframe(sample_df, use_container_width=True)

# CARGA DE DATOS
elif option == "📁 Carga de Datos":
    st.header("📁 1. Carga de Datos")
    st.markdown("### 1.1 Cargar archivos CSV")
    
    # Opción para usar datos de ejemplo
    if st.button("🎯 Usar datos de ejemplo", type="secondary"):
        st.session_state.df = load_sample_data()
        st.success("✅ Datos de ejemplo cargados correctamente!")
    
    st.markdown("---")
    
    # Carga de archivo CSV
    uploaded_file = st.file_uploader("Sube tu archivo CSV", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Leer el archivo CSV
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.success("✅ Archivo cargado correctamente!")
            
            # Mostrar información básica
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Filas", df.shape[0])
            with col2:
                st.metric("📋 Columnas", df.shape[1])
            with col3:
                st.metric("💾 Tamaño (KB)", round(uploaded_file.size / 1024, 2))
            
        except Exception as e:
            st.error(f"❌ Error al cargar el archivo: {str(e)}")
    
    # Mostrar datos cargados
    if st.session_state.df is not None:
        st.markdown("### 📊 Vista previa de los datos:")
        st.dataframe(st.session_state.df, use_container_width=True)

# PREPARACIÓN DE DATOS
elif option == "🔍 Preparación de Datos":
    st.header("🔍 2. Preparación de Datos")
    
    if st.session_state.df is None:
        st.warning("⚠️ Primero debes cargar datos en la sección 'Carga de Datos'")
        st.stop()
    
    df = st.session_state.df
    
    # 2.1 Primeras N líneas
    st.markdown("### 2.1 Mostrar las primeras N líneas")
    n_head = st.number_input("Número de filas a mostrar (head):", min_value=1, max_value=len(df), value=5)
    st.dataframe(df.head(n_head), use_container_width=True)
    
    # 2.2 Últimas N líneas
    st.markdown("### 2.2 Mostrar las últimas N líneas")
    n_tail = st.number_input("Número de filas a mostrar (tail):", min_value=1, max_value=len(df), value=5)
    st.dataframe(df.tail(n_tail), use_container_width=True)
    
    # 2.3 Información básica
    st.markdown("### 2.3 Información básica del CSV")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Información general:**")
        buffer = StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        st.text(info_str)
    
    with col2:
        st.markdown("**🔍 Tipos de datos:**")
        st.dataframe(df.dtypes.to_frame(name='Tipo de dato'), use_container_width=True)
    
    # 2.4 Lista de columnas
    st.markdown("### 2.4 Lista de Columnas")
    st.write("**Columnas disponibles:**", list(df.columns))
    
    # 2.5 Forma del dataset
    st.markdown("### 2.5 Forma del dataset")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Filas", df.shape[0])
    with col2:
        st.metric("📋 Columnas", df.shape[1])
    with col3:
        st.metric("🔢 Total elementos", df.size)
    
    # 2.6 Descripción estadística
    st.markdown("### 2.6 Descripción estadística del dataset")
    st.dataframe(df.describe(), use_container_width=True)
    
    # Información adicional sobre valores nulos
    st.markdown("### 🔍 Análisis de valores nulos")
    null_info = df.isnull().sum()
    if null_info.sum() > 0:
        st.dataframe(null_info.to_frame(name='Valores nulos'), use_container_width=True)
    else:
        st.success("✅ No hay valores nulos en el dataset")

# SELECCIÓN DE DATOS
elif option == "📋 Selección de Datos":
    st.header("📋 3. Selección de Datos")
    
    if st.session_state.df is None:
        st.warning("⚠️ Primero debes cargar datos en la sección 'Carga de Datos'")
        st.stop()
    
    df = st.session_state.df
    
    # 3.1 Seleccionar 1 columna
    st.markdown("### 3.1 Seleccionar 1 columna")
    single_column = st.selectbox("Selecciona una columna:", df.columns)
    if single_column:
        st.dataframe(df[single_column].to_frame(), use_container_width=True)
        
        # Estadísticas de la columna seleccionada
        if df[single_column].dtype in ['int64', 'float64']:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Media", round(df[single_column].mean(), 2))
            with col2:
                st.metric("📈 Máximo", df[single_column].max())
            with col3:
                st.metric("📉 Mínimo", df[single_column].min())
            with col4:
                st.metric("🎯 Mediana", round(df[single_column].median(), 2))
    
    # 3.2 Seleccionar N columnas
    st.markdown("### 3.2 Seleccionar múltiples columnas")
    multiple_columns = st.multiselect("Selecciona múltiples columnas:", df.columns)
    if multiple_columns:
        selected_df = df[multiple_columns]
        st.dataframe(selected_df, use_container_width=True)
        
        # Botón para descargar selección
        csv = selected_df.to_csv(index=False)
        st.download_button(
            label="📥 Descargar selección como CSV",
            data=csv,
            file_name='seleccion_datos.csv',
            mime='text/csv'
        )

# FILTRADO DE DATOS
elif option == "🔎 Filtrado de Datos":
    st.header("🔎 4. Filtrado de Datos")
    
    if st.session_state.df is None:
        st.warning("⚠️ Primero debes cargar datos en la sección 'Carga de Datos'")
        st.stop()
    
    df = st.session_state.df
    
    st.markdown("### 4.1 Filtrar filas con condiciones")
    
    # Seleccionar columna para filtrar
    filter_column = st.selectbox("Selecciona la columna para filtrar:", df.columns)
    
    if filter_column:
        col_type = df[filter_column].dtype
        
        # Filtros para columnas numéricas
        if col_type in ['int64', 'float64']:
            operator = st.selectbox("Selecciona el operador:", ['>', '<', '>=', '<=', '==', '!='])
            value = st.number_input(f"Valor para comparar con {filter_column}:", 
                                  value=float(df[filter_column].median()))
            
            # Aplicar filtro
            if operator == '>':
                filtered_df = df[df[filter_column] > value]
            elif operator == '<':
                filtered_df = df[df[filter_column] < value]
            elif operator == '>=':
                filtered_df = df[df[filter_column] >= value]
            elif operator == '<=':
                filtered_df = df[df[filter_column] <= value]
            elif operator == '==':
                filtered_df = df[df[filter_column] == value]
            elif operator == '!=':
                filtered_df = df[df[filter_column] != value]
            
        # Filtros para columnas de texto
        else:
            filter_type = st.radio("Tipo de filtro:", ['Contiene texto', 'Igual a', 'Seleccionar valores'])
            
            if filter_type == 'Contiene texto':
                text_value = st.text_input(f"Texto a buscar en {filter_column}:")
                if text_value:
                    filtered_df = df[df[filter_column].str.contains(text_value, case=False, na=False)]
                else:
                    filtered_df = df
                    
            elif filter_type == 'Igual a':
                text_value = st.text_input(f"Valor exacto en {filter_column}:")
                if text_value:
                    filtered_df = df[df[filter_column] == text_value]
                else:
                    filtered_df = df
                    
            else:  # Seleccionar valores
                unique_values = df[filter_column].unique()
                selected_values = st.multiselect(f"Selecciona valores de {filter_column}:", unique_values)
                if selected_values:
                    filtered_df = df[df[filter_column].isin(selected_values)]
                else:
                    filtered_df = df
        
        # Mostrar resultados del filtro
        st.markdown(f"### 📊 Resultados del filtro:")
        st.info(f"Se encontraron {len(filtered_df)} filas de {len(df)} total")
        st.dataframe(filtered_df, use_container_width=True)
        
        # Opción para descargar datos filtrados
        if len(filtered_df) > 0:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar datos filtrados",
                data=csv,
                file_name='datos_filtrados.csv',
                mime='text/csv'
            )

# OPERACIONES NUMPY
elif option == "🧮 Operaciones NumPy":
    st.header("🧮 Operaciones NumPy")
    
    if st.session_state.df is None:
        st.warning("⚠️ Primero debes cargar datos en la sección 'Carga de Datos'")
        st.stop()
    
    df = st.session_state.df
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_columns:
        st.error("❌ No hay columnas numéricas para realizar operaciones NumPy")
        st.stop()
    
    st.markdown("### 🔢 Operaciones disponibles:")
    
    # Seleccionar columnas numéricas
    selected_columns = st.multiselect("Selecciona columnas numéricas:", numeric_columns)
    
    if selected_columns:
        # Convertir a array de NumPy
        np_array = df[selected_columns].values
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Información del Array")
            st.write(f"**Forma (shape):** {np_array.shape}")
            st.write(f"**Dimensiones:** {np_array.ndim}")
            st.write(f"**Tipo de dato:** {np_array.dtype}")
            st.write(f"**Número de elementos:** {np_array.size}")
        
        with col2:
            st.markdown("#### 🧮 Operaciones Básicas")
            st.write(f"**Suma total:** {np.sum(np_array):.2f}")
            st.write(f"**Media:** {np.mean(np_array):.2f}")
            st.write(f"**Máximo:** {np.max(np_array):.2f}")
            st.write(f"**Mínimo:** {np.min(np_array):.2f}")
            st.write(f"**Desviación estándar:** {np.std(np_array):.2f}")
        
        # Operaciones por columna
        st.markdown("#### 📈 Operaciones por columna:")
        operations_df = pd.DataFrame({
            'Columna': selected_columns,
            'Suma': [np.sum(df[col]) for col in selected_columns],
            'Media': [np.mean(df[col]) for col in selected_columns],
            'Máximo': [np.max(df[col]) for col in selected_columns],
            'Mínimo': [np.min(df[col]) for col in selected_columns],
            'Desv. Estándar': [np.std(df[col]) for col in selected_columns]
        })
        st.dataframe(operations_df, use_container_width=True)
        
        # Operaciones entre columnas (si hay al menos 2)
        if len(selected_columns) >= 2:
            st.markdown("#### 🔄 Operaciones entre columnas:")
            col1_op = st.selectbox("Primera columna:", selected_columns)
            col2_op = st.selectbox("Segunda columna:", selected_columns, index=1)
            operation = st.selectbox("Operación:", ['+', '-', '*', '/'])
            
            if col1_op and col2_op:
                if operation == '+':
                    result = df[col1_op] + df[col2_op]
                elif operation == '-':
                    result = df[col1_op] - df[col2_op]
                elif operation == '*':
                    result = df[col1_op] * df[col2_op]
                elif operation == '/':
                    result = df[col1_op] / df[col2_op]
                
                result_df = df[[col1_op, col2_op]].copy()
                result_df[f'{col1_op} {operation} {col2_op}'] = result
                st.dataframe(result_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Puedes navegar entre las diferentes secciones usando el menú lateral.")
st.markdown("📚 Basado en los ejercicios de NumPy y Pandas - Desarrollado con Streamlit")