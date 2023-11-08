import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import mysql.connector
from langdetect import detect
import pandas as pd

# Primero, asegúrate de que has descargado los recursos necesarios de NLTK
nltk.download('vader_lexicon')
nltk.download('punkt')

# Configuración para conectarse a la base de datos
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='python'
)

# Crear un analizador de sentimiento
sia = SentimentIntensityAnalyzer()

try:
    cursor = db_connection.cursor(dictionary=True)
    # Seleccionar todos los comentarios
    sql_query = "SELECT * FROM comments;"
    cursor.execute(sql_query)
    comments = cursor.fetchall()

    # Lista para almacenar los resultados
    results = []

    # Procesar cada comentario
    for comment in comments:
        text = comment['comment']
        
        # Detectar el idioma del comentario
        try:
            if detect(text) == 'en':
                # Calcular el puntaje de sentimiento
                sentiment_score = sia.polarity_scores(text)
                
                # Clasificar el sentimiento basado en el puntaje compuesto
                sentiment_class = 'neutral'
                if sentiment_score['compound'] > 0.05:
                    sentiment_class = 'positive'
                elif sentiment_score['compound'] < -0.05:
                    sentiment_class = 'negative'
                
                # Agregar los detalles del comentario a los resultados
                results.append({
                    'comment': text,
                    'comment_length': len(text.split()),  # Longitud del comentario en palabras
                    'comment_id': comment['comment_id'],
                    'author': comment['author'],
                    'likes': comment['likes'],
                    'published_at': comment['published_at'],
                    'neg': sentiment_score['neg'],
                    'neu': sentiment_score['neu'],
                    'pos': sentiment_score['pos'],
                    'compound': sentiment_score['compound'],
                    'sentiment_class': sentiment_class  # Clase de sentimiento
                })
        except Exception as e:
            print(f"Error al detectar el idioma del comentario {comment['comment_id']}: {e}")

finally:
    if db_connection.is_connected():
        cursor.close()
        db_connection.close()

# Guardar los resultados en un archivo CSV
df = pd.DataFrame(results)
df.to_csv('sentiment_analysis_results.csv', index=False)
