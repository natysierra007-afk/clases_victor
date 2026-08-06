# ============================================
# BOT DE VENTAS - Guia de referencia
# Codigo completo hasta donde vamos
# ============================================

import pandas as pd
import glob

# --------------------------------------------
# PARTE 1: Buscar y leer los archivos (YA VISTO)
# --------------------------------------------
archivos_csv = glob.glob("sucursal_*.csv")
archivos_xlsx = glob.glob("sucursal_*.xlsx")

lista_informes = []

for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    lista_informes.append(df)
    print(f"Leido: {archivo} - {len(df)} filas")

for archivo in archivos_xlsx:
    df = pd.read_excel(archivo, engine='openpyxl')
    lista_informes.append(df)
    print(f"Leido: {archivo} - {len(df)} filas")


# --------------------------------------------
# PARTE 2: Consolidar (YA VISTO - primer intento)
# --------------------------------------------
df_consolidado = pd.concat(lista_informes, ignore_index=True)
print(df_consolidado.columns)
# En este punto se ven mas de 7 columnas porque el archivo de
# Bogota usa nombres distintos.


# --------------------------------------------
# PARTE 3: Renombrar columnas (COMPLETADO)
# --------------------------------------------
for i, df in enumerate(lista_informes):
    if 'Fecha_Venta' in df.columns:
        lista_informes[i] = df.rename(columns={
            'Fecha_Venta': 'fecha',
            'Producto': 'producto',
            'Categoria': 'categoria',
            'Cant': 'cantidad',
            'Valor_Unitario': 'precio_unitario',
            'Vendedor': 'vendedor',
            'Pago': 'metodo_pago'
        })

df_consolidado = pd.concat(lista_informes, ignore_index=True)
print(df_consolidado.columns)  # ahora muestra exactamente 7

# --------------------------------------------
# PARTE 4: Limpieza de datos (NUEVO - hoy)
# --------------------------------------------

# 4a. Eliminar filas duplicadas
filas_antes = len(df_consolidado)
df_consolidado = df_consolidado.drop_duplicates()
print(f"Filas antes: {filas_antes} - despues: {len(df_consolidado)}")

# 4b. Explorar valores nulos ANTES de decidir que hacer
print(df_consolidado.isnull().sum())

df_consolidado['metodo_pago'] = df_consolidado['metodo_pago'].fillna('No especificado')

# vendedor: igual, es texto -> etiqueta explicita en vez de adivinar
# quien hizo la venta.
df_consolidado['vendedor'] = df_consolidado['vendedor'].fillna('No especificado')

df_consolidado['precio_unitario'] = df_consolidado['precio_unitario'].fillna(
    df_consolidado['precio_unitario'].median()
)

# Verificacion final: ya no deberia quedar ningun nulo
print(df_consolidado.isnull().sum())


# --------------------------------------------
# PARTE 5: Guardar el resultado
# --------------------------------------------
df_consolidado.to_excel("consolidado_limpio.xlsx", index=False)
print("Archivo guardado")