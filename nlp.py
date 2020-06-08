import re
from collections import Counter
from nltk.tokenize import TweetTokenizer
from stop_words import get_stop_words
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

class NLP:
    def __init__(self):
        self.tokenizer = TweetTokenizer()
        self.stop_words = set(stopwords.words('english')).union(set(get_stop_words('en')))
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = SnowballStemmer('english')

    def clean_string(self, text: str) -> list:
        text = self.to_lowercase(text)
        tokens = self.tokenize(text)
        tokens = [c_token for c_token in (self.remove_non_alphanumerics(token) for token in tokens if token not in self.stop_words) if c_token != '' and c_token not in self.stop_words]
        tokens = [self.stem(token) for token in tokens]
        return tokens

    def clean_string_and_add_tf(self, text: str) -> list:
        tokens = self.clean_string(text)
        tokens_len = len(tokens)
        tokens = Counter(tokens).items()
        tokens = [(word, tf / tokens_len) for word, tf in tokens]
        return tokens

    def lemma(self, word: str) -> str:
        return self.lemmatizer.lemmatize(word)

    def stem(self, word: str) -> str:
        return self.stemmer.stem(word)

    def tokenize(self, text: str) -> list:
        return self.tokenizer.tokenize(text)

    def to_lowercase(self, text: str) -> str:
        return text.lower()

    def remove_non_alphanumerics(self, text: str) -> str:
        return re.sub('\W', '', text)
