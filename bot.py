# ============================================
# BOT DE VENTAS - Guia de referencia
# Codigo completo hasta donde vamos
# ============================================

import matplotlib.pyplot as plt
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
    df = pd.read_excel(archivo, engine="openpyxl")
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
    if "Fecha_Venta" in df.columns:
        lista_informes[i] = df.rename(columns={
            "Fecha_Venta": "fecha",
            "Producto": "producto",
            "Categoria": "categoria",
            "Cant": "cantidad",
            "Valor_Unitario": "precio_unitario",
            "Vendedor": "vendedor",
            "Pago": "metodo_pago"
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

df_consolidado["metodo_pago"] = df_consolidado["metodo_pago"].fillna("No especificado")

# vendedor: igual, es texto -> etiqueta explicita en vez de adivinar
# quien hizo la venta.
df_consolidado["vendedor"] = df_consolidado["vendedor"].fillna("No especificado")

df_consolidado["precio_unitario"] = df_consolidado["precio_unitario"].fillna(
    df_consolidado["precio_unitario"].median()
)

# Verificacion final: ya no deberia quedar ningun nulo
print(df_consolidado.isnull().sum())


# --------------------------------------------
# PARTE 5: Guardar el resultado
# --------------------------------------------
df_consolidado.to_excel("consolidado_limpio.xlsx", index=False)
print("Archivo guardado")

# ============================================
# ANÁLISIS DE NEGOCIO - Bot de Ventas
# (continúa después de tu código de lectura, 
# consolidación y limpieza ya hecho)
# ============================================

# --------------------------------------------
# PREGUNTA 1: ¿Cuánto vendió cada categoría en total?
# (EJEMPLO RESUELTO)
# --------------------------------------------
ventas_categoria = df_consolidado.groupby("categoria")["precio_unitario"].sum()
print(ventas_categoria)

ventas_categoria.plot(kind="bar", title="Ventas por Categoria")
plt.ticklabel_format(style="plain", axis="y")
plt.ylabel("Ventas totales ($)")
plt.xlabel("Categoría")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("grafico_categoria.png")
plt.show()


# --------------------------------------------
# PREGUNTA 2: ¿Qué porcentaje de las ventas representa 
# cada vendedor?
# --------------------------------------------
# Paso 1: agrupen por vendedor y sumen precio_unitario
# Paso 2: impriman el resultado
# Paso 3: hagan un gráfico de torta (pie) con porcentajes
# Paso 4: guarden como "grafico_vendedor.png"
# Paso 1 y 2: agrupar por vendedor y sumar precio_unitario
ventas_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum().reset_index()
print(ventas_vendedor)

plt.figure(figsize=(6, 6))
plt.pie(ventas_vendedor['precio_unitario'], labels=ventas_vendedor['vendedor'],
        autopct='%1.1f%%', startangle=90)
plt.title('Distribución de ventas por vendedor')
plt.axis('equal')
plt.tight_layout()
plt.savefig("grafico_vendedor.png")
plt.show()

# --------------------------------------------
# PREGUNTA 3: ¿Cuál es el producto que más se vende?
# --------------------------------------------
# Paso 1: investiguen la función value_counts()
# Paso 2: apliquenla a la columna producto
# Paso 3: impriman el resultado

datos_productos = df_consolidado["producto"].value_counts()
print(datos_productos)





# --------------------------------------------
# PREGUNTA 4: ¿Cómo se distribuyen las ventas según 
# el método de pago?
# --------------------------------------------
# Paso 1: agrupen por metodo_pago y sumen precio_unitario
# Paso 2: impriman el resultado
# Paso 3: hagan el gráfico que consideren más apropiado
# Paso 4: guarden como "grafico_metodo_pago.png"

grafico_metodo_pago = df_consolidado.groupby("metodo_pago")["precio_unitario"].sum()
print(grafico_metodo_pago)

grafico_metodo_pago.plot(kind="bar", title="metoodos de pago por precio unitario")
plt.ticklabel_format(style="plain", axis="y")
plt.ylabel("metodo pago")
plt.xlabel("precio unitario")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("grafico_metodo_pago.png")
plt.show()



# --------------------------------------------
# RETO OPCIONAL - Para quien termine las 4 preguntas
# PREGUNTA 5: ¿Cuál es el día de la semana con más ventas?
# --------------------------------------------
# Paso 1: investiguen pd.to_datetime() para convertir la columna 
# fecha a formato de fecha real
# Paso 2: investiguen .dt.day_name() para extraer el día de la semana
# Paso 3: agrupen por ese nuevo dato y sumen las ventas