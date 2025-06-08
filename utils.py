import pandas as pd
import io

def cargar_csv(file):
    try:
        df = pd.read_csv(file)
        return df, None
    except Exception as e:
        return None, str(e)

def mostrar_primeras_filas(df, n):
    return df.head(n)

def mostrar_ultimas_filas(df, n):
    return df.tail(n)

def obtener_info_basica_columna_1(df):
    buffer = io.StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()

def obtener_info_basica_columna2(df):
    return df.dtypes.to_frame(name="Tipo de dato")

def obtener_info_estadistica(df):
    return df.describe()

def obtener_columnas(df):
    return df.columns.tolist()

def obtener_forma(df):
    return df.shape

def seleccionar_columnas(df, columnas):
    return df[columnas]

def filtrar_filas_multiples(df, condiciones):
    resultado = df.copy()
    for condicion in condiciones:
        columna, operador, valor = condicion
        if operador == ">":
            resultado = resultado[resultado[columna] > valor]
        elif operador == "<":
            resultado = resultado[resultado[columna] < valor]
        elif operador == "==":
            resultado = resultado[resultado[columna] == valor]
    return resultado
