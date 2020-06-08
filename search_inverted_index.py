import sqlite3
from nlp import NLP

class Search:
    def __init__(self, index_table):
        self.index_table = index_table
        self.nlp = NLP()

        self.conn = sqlite3.connect('../database/bloggers.db')
        self.c = self.conn.cursor()

    def clean_terms(self, terms: str) -> list:
        return self.nlp.clean_string(terms)

    def get_or_statements(self, terms: list) -> str:
        return ''.join([' OR word = ?' for term in terms[1:]])

    def search_bloggers(self, terms: str):
        clean_terms = self.clean_terms(terms)
        or_statements = self.get_or_statements(clean_terms)

        self.c.execute('''
        SELECT ie.blogger_id, b.gender, b.age, b.company, b.astrological_sign, count(*) as occurrences
        FROM ''' + self.index_table + ''' as ie    
        LEFT JOIN Blogger as b ON ie.blogger_id = b.id
        WHERE word = ?
        ''' + or_statements + '''
        GROUP BY blogger_id
        ORDER BY occurrences DESC
        ''', clean_terms)

        return self.c.fetchall()

    def search_posts(self, terms: str):
        clean_terms = self.clean_terms(terms)
        or_statements = self.get_or_statements(clean_terms)

        self.c.execute('''
        SELECT ie.blogger_id, p.id, p.creation_date, p.text, count(*) as occurrences
        FROM ''' + self.index_table + ''' as ie    
        LEFT JOIN Post as p ON ie.post_id = p.id
        WHERE word = ?
        ''' + or_statements + '''
        GROUP BY post_id
        ORDER BY occurrences DESC
        ''', clean_terms)

        return self.c.fetchall()

    def simple_search(self, terms: str):
        clean_terms = self.clean_terms(terms)
        or_statements = self.get_or_statements(clean_terms)

        self.c.execute('''
                SELECT *
                FROM ''' + self.index_table + ''' as ie    
                WHERE word = ?
                ''' + or_statements + '''
                ''', clean_terms)

        return self.c.fetchall()
