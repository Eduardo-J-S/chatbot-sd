import nltk
import numpy as np

# nltk.download('punkt')  # Descomente se necessário

from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def tokenize(sentence):
    """
    Tokeniza uma sentença em palavras.

    Parâmetros:
    - sentence: A sentença a ser tokenizada.

    Retorna:
    - Uma lista de palavras tokenizadas.
    """
    return nltk.word_tokenize(sentence)

def stem(word):
    """
    Aplica stemming a uma palavra.

    Parâmetros:
    - word: A palavra a ser stemizada.

    Retorna:
    - A palavra após aplicar stemming.
    """
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    """
    Gera um vetor de representação de saco de palavras para uma sentença.

    Parâmetros:
    - tokenized_sentence: A sentença tokenizada.
    - all_words: Lista de todas as palavras únicas no conjunto de dados.

    Retorna:
    - Um vetor de representação de saco de palavras.
    """
    tokenized_sentence = [stem(w) for w in tokenized_sentence]

    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0

    return bag
