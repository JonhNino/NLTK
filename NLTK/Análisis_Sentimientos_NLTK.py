import nltk
nltk.download('vader_lexicon')
# Importamos el analizador de sentimientos VADER

from nltk.sentiment import SentimentIntensityAnalyzer

# Inicializamos el analizador de sentimientos VADER
sia = SentimentIntensityAnalyzer()

# Textos de ejemplo
positive_text = "I love this product, it's absolutely amazing!"
negative_text = "I hate this product, it's terrible and disappointing."

# Obtenemos los puntajes de sentimiento para cada texto
positive_score = sia.polarity_scores(positive_text)
negative_score = sia.polarity_scores(negative_text)

print("Puntuación de sentimiento positivo:", positive_score)
print("Puntuación de sentimiento negativo:", negative_score)
