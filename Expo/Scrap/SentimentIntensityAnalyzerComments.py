import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pymysql
from langdetect import detect
import pandas as pd

# Primero, asegúrate de que has descargado los recursos necesarios de NLTK
nltk.download('vader_lexicon')
nltk.download('punkt')

# Configuración para conectarse a la base de datos
# Deberías reemplazar 'your_database' con el nombre de tu base de datos,
# y proporcionar el usuario y contraseña correctos.
db_connection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                database='python',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

# Crear un analizador de sentimiento
sia = SentimentIntensityAnalyzer()

try:
    with db_connection.cursor() as cursor:
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
                    # Agregar los detalles del comentario a los resultados
                    results.append({
                        'comments': comment['comment'],
                        'comment_id': comment['comment_id'],
                        'author': comment['author'],
                        'likes': comment['likes'],
                        'published_at': comment['published_at'],
                        'sentiment': sentiment_score # Podrías usar 'compound' para un resumen general del sentimiento
                    })
            except Exception as e:
                print(f"Error al detectar el idioma del comentario {comment['comment_id']}: {e}")

finally:
    db_connection.close()

# Guardar los resultados en un archivo CSV
df = pd.DataFrame(results)
df.to_csv('sentiment_analysis_results.csv', index=False)