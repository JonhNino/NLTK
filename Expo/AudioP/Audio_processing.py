import speech_recognition as sr
import spacy
import mysql.connector

# Cargar el modelo de lenguaje en español para spacy
nlp = spacy.load('es_core_news_sm')

# Descripciones de etiquetas POS en español para spacy
tag_descriptions = {
    'ADJ': 'adjetivo',
    'ADP': 'adposición',
    'ADV': 'adverbio',
    'AUX': 'auxiliar',
    'CONJ': 'conjunción',
    'CCONJ': 'conjunción coordinada',
    'DET': 'determinante',
    'INTJ': 'interjección',
    'NOUN': 'sustantivo',
    'NUM': 'numeral',
    'PART': 'partícula',
    'PRON': 'pronombre',
    'PROPN': 'sustantivo propio',
    'PUNCT': 'puntuación',
    'SCONJ': 'conjunción subordinada',
    'SYM': 'símbolo',
    'VERB': 'verbo',
    'X': 'otro',
    'SPACE': 'espacio',
}

# Intentar establecer la conexión a la base de datos MySQL
try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python"
    )
    cursor = db_connection.cursor()
except Error as err:
    print(f"Error al conectar a MySQL: {err}")
    cursor = None

# Función para transcribir audio a texto
def transcribe_audio(audio_file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='es-ES')
            return text
    except (sr.UnknownValueError, sr.RequestError) as e:
        print(f"Error al transcribir el audio: {e}")
        return ""

# Función para tokenizar el texto, hacer POS tagging y almacenar los tokens en MySQL
def tokenize_and_store(text):
    if text and cursor and nlp:  # Verificar que el texto no esté vacío, que exista una conexión de cursor y que nlp esté cargado
        doc = nlp(text)
        for sent in doc.sents:
            cursor.execute("INSERT INTO sentences (content) VALUES (%s)", (sent.text,))
        for token in doc:
            description = tag_descriptions.get(token.pos_, 'Etiqueta desconocida')
            cursor.execute("INSERT INTO words (content, pos_tag, description) VALUES (%s, %s, %s)", (token.text, token.pos_, description))
        db_connection.commit()

# Ruta al archivo de audio, actualizada con la ruta correcta
audio_file_path = 'C:\\Users\\LENOVO\\Desktop\\Espe\\Modulo 4\\Exposicion\\output.wav'

# Ejecutar el proceso de transcripción y almacenamiento
if cursor and nlp:
    try:
        transcribed_text = transcribe_audio(audio_file_path)
        tokenize_and_store(transcribed_text)
    finally:
        cursor.close()
        db_connection.close()
    print("El proceso de transcripción y almacenamiento ha terminado.")
else:
    print("No se pudo establecer la conexión con la base de datos o cargar el modelo de lenguaje.")
