import nltk

# Descarga del paquete punkt
nltk.download('punkt')
# Importamos las funciones de tokenización
from nltk.tokenize import sent_tokenize, word_tokenize

# Definimos un texto de ejemplo
text_example = "Hello there, how are you? Weather is awesome. Its raining here now."

# Realizamos la tokenización por oraciones
sentences = sent_tokenize(text_example)

# Realizamos la tokenización por palabras
words = word_tokenize(text_example)

# Imprimimos los resultados
print("Tokenización de oraciones:", sentences)
print("Tokenización de palabras:", words)
