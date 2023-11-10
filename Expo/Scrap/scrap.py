import googleapiclient.discovery
import mysql.connector
from datetime import datetime

# Configura tus credenciales y parámetros de conexión aquí
api_key = 'AIzaSyCndpl4zIQwjH78HblXumy-UwIet5WOESA'
video_id = 'AjzMrDla0OA'
mysql_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'python'
}
# Inicia la API de YouTube
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

# Recupera todos los comentarios del video manejando la paginación
def get_all_comments(video_id):
    comments = []
    page_token = None
    while True:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,  # Puedes ajustar esto hasta un máximo de 100
            pageToken=page_token,
            textFormat='plainText'
        ).execute()

        for item in response['items']:
            comment_snippet = item['snippet']['topLevelComment']['snippet']
            comment = comment_snippet['textDisplay']
            author = comment_snippet['authorDisplayName']
            likes = comment_snippet['likeCount']
            comment_id = item['snippet']['topLevelComment']['id']
            published_at = datetime.strptime(comment_snippet['publishedAt'], '%Y-%m-%dT%H:%M:%S%z')
            comments.append((author, comment, likes, comment_id, published_at))

        # Si no hay un nextPageToken, hemos llegado al final de los comentarios
        page_token = response.get('nextPageToken')
        if not page_token:
            break

    return comments

# Conecta a MySQL y almacena los comentarios
def store_comments(comments):
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()
    
    # Inserta los datos en la tabla de comentarios
    insert_stmt = (
        "INSERT INTO comments (author, comment, likes, comment_id, published_at) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    for comment_data in comments:
        try:
            cursor.execute(insert_stmt, comment_data)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    connection.commit()
    cursor.close()
    connection.close()

# Ejecuta el script
comments = get_all_comments(video_id)
store_comments(comments)