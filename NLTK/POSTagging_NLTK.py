import nltk

# Descarga del paquete averaged_perceptron_tagger
nltk.download('averaged_perceptron_tagger')
# Importamos el etiquetador POS
from nltk import pos_tag

# Importamos la función de tokenización de palabras
from nltk.tokenize import word_tokenize

# Definimos un texto de ejemplo
text_example = "The quick brown fox jumps over the lazy dog"

# Tokenizamos el texto en palabras
words = word_tokenize(text_example)

# Aplicamos POS Tagging a las palabras tokenizadas
tagged_words = pos_tag(words)

# Mostramos las palabras con sus etiquetas POS
print("Etiquetado POS:", tagged_words)
