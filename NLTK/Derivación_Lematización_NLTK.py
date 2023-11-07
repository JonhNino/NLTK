import nltk

# Descarga del paquete wordnet
nltk.download('wordnet')
# Importamos los módulos necesarios
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Inicializamos el stemmer y el lematizador
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Una lista de palabras para demostrar la derivación y lematización
words = ["running", "jumps", "easily", "bigger"]

# Aplicamos stemming y lemmatization
stemmed_words = [stemmer.stem(word) for word in words]
lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

print("Palabras originales:", words)
print("Después de la derivación:", stemmed_words)
print("Después de la lematización:", lemmatized_words)
