# Importamos el módulo para parsing de gramática de frases
from nltk import CFG
from nltk.parse import RecursiveDescentParser

# Definimos una gramática de frases simple
grammar = CFG.fromstring("""
    S -> NP VP
    VP -> V NP | V NP PP
    PP -> P NP
    V -> "saw" | "ate"
    NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
    Det -> "a" | "an" | "the" | "my"
    N -> "man" | "dog" | "cat" | "telescope" | "park"
    P -> "in" | "on" | "by" | "with"
""")

# Inicializamos el parser con la gramática
parser = RecursiveDescentParser(grammar)

# Frase de ejemplo para el parsing
sentence = "John saw Mary in the park with a telescope"

# Tokenizamos la frase
tokens = sentence.split()

# Realizamos el parsing y generamos el árbol de parse
for tree in parser.parse(tokens):
    print(tree)
    tree.draw()  # Esto abrirá una ventana con la estructura del árbol visualmente
