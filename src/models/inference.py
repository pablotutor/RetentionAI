import joblib
import pandas as pd
import numpy as np
import os

# Ruta al modelo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'churn_pipeline.joblib')

class ModelLoader:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            print(f"✅ Modelo cargado desde: {MODEL_PATH}")
        else:
            raise FileNotFoundError(f"❌ No se encuentra el modelo en {MODEL_PATH}")
        
    def get_feature_importance(self):
        """
        Extrae los coeficientes del modelo para explicar qué variables pesan más.
        """
        if not self.model:
            self.load_model()

        try:
            # 1. Acceder a los pasos del Pipeline
            # Asumimos que tu pipeline tiene pasos llamados 'preprocessor' y 'classifier'
            # (Es el estándar si usaste ColumnTransformer y LogisticRegression en un Pipeline)
            classifier = self.model.named_steps['classifier']
            preprocessor = self.model.named_steps['preprocessor']

            # 2. Obtener los nombres de las features tras el OneHotEncoding
            # Esto es necesario porque 'Department' se convierte en 'Department_Sales', etc.
            feature_names = preprocessor.get_feature_names_out()

            # 3. Obtener los coeficientes (pesos)
            # LogisticRegression devuelve una matriz de forma (1, n_features), cogemos la primera fila
            coefficients = classifier.coef_[0]

            # 4. Crear DataFrame
            df_imp = pd.DataFrame({
                'Variable': feature_names,
                'Peso': coefficients
            })

            # 5. Calcular impacto absoluto para ordenar
            df_imp['AbsPeso'] = df_imp['Peso'].abs()
            
            # 6. Devolver el Top 10 ordenado
            return df_imp.sort_values(by='AbsPeso', ascending=False).head(10)

        except Exception as e:
            print(f"Error extrayendo importancia: {e}")
            # Si falla (ej: el modelo no es lineal o el pipeline es distinto), devolvemos vacío
            return pd.DataFrame()
        

    def predict(self, input_data: dict):
        if not self.model:
            self.load_model()
            
        # 1. Convertir diccionario a DataFrame
        df_input = pd.DataFrame([input_data])
        
        # ---------------------------------------------------------
        # 🚨 CORRECCIÓN DE TIPOS (CRÍTICO)
        # ---------------------------------------------------------
        
        # A. La variable traicionera: StockOptionLevel debe ser STRING
        # Aunque sea un número (0,1,2), el modelo la aprendió como categoría "0", "1"...
        if 'StockOptionLevel' in df_input.columns:
            df_input['StockOptionLevel'] = df_input['StockOptionLevel'].astype(str)
            
        # B. Asegurar que las numéricas sean float (por seguridad)
        # Esto evita problemas con np.log1p si llegan como strings
        numeric_cols_to_log = ['MonthlyIncome', 'DistanceFromHome']
        for col in numeric_cols_to_log:
            df_input[col] = df_input[col].astype(float)

        # ---------------------------------------------------------
        # 🧪 FEATURE ENGINEERING
        # ---------------------------------------------------------
        
        # C. Aplicar Logaritmos (Feature Engineering del Notebook)
        df_input['Log_MonthlyIncome'] = np.log1p(df_input['MonthlyIncome'])
        df_input['Log_DistanceFromHome'] = np.log1p(df_input['DistanceFromHome'])
        
        # D. (Opcional) Borrar columnas originales si quieres limpiar, 
        # aunque sklearn suele ignorarlas si no están en su lista.
        # df_input.drop(columns=['MonthlyIncome', 'DistanceFromHome'], inplace=True)

        # ---------------------------------------------------------
        
        try:
            # 2. Predecir
            prediction = self.model.predict(df_input)[0]
            probability = self.model.predict_proba(df_input)[0][1]
            
            return {
                "prediction": int(prediction),
                "probability": float(probability),
                "label": "Se va (Churn)" if prediction == 1 else "Se queda (Retained)"
            }
        except Exception as e:
            # Tip: Imprime los tipos de datos para depurar si vuelve a fallar
            print("Tipos de datos actuales:\n", df_input.dtypes)
            raise ValueError(f"Error en inferencia: {str(e)}")

model_service = ModelLoader()