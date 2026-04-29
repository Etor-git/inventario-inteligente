import pandas as pd
from sklearn.linear_model import LinearRegression

def predecir_agotamiento(stock_actual, ventas_semanales):
    try:
        # Datos simples de entrenamiento
        X = pd.DataFrame({
            "ventas_semanales": [5, 10, 15, 20, 25, 30]
        })

        y = pd.DataFrame({
            "semanas_para_agotarse": [20, 10, 7, 5, 4, 3]
        })

        modelo = LinearRegression()
        modelo.fit(X, y)

        prediccion = modelo.predict([[ventas_semanales]])

        semanas = round(float(prediccion[0][0]), 1)

        if semanas < 1:
            semanas = 1

        return semanas

    except Exception as e:
        return str(e)
