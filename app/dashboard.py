import streamlit as st
import pandas as pd
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="mysql_db",
        user="admin",
        password="admin123",
        database="inventario_db",
        port=3306
    )

st.title("Dashboard de Inventario Inteligente")

try:
    connection = get_connection()

    query = "SELECT * FROM productos"
    df = pd.read_sql(query, connection)

    st.subheader("Productos Registrados")
    st.dataframe(df)

    st.subheader("Resumen General")

    total_productos = len(df)
    stock_bajo = len(df[df["stock_actual"] <= df["stock_minimo"]])

    st.write(f"Total de productos: {total_productos}")
    st.write(f"Productos con stock bajo: {stock_bajo}")

    st.subheader("Gráfico de Stock")

    st.bar_chart(df.set_index("nombre")["stock_actual"])

    connection.close()

except Exception as e:
    st.error(f"Error: {str(e)}")
