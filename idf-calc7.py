import sqlite3
import math


def log(number):
    return math.log10(number)


# create connection
conn = sqlite3.connect('../database/bloggers.db')
# save log function in database
conn.create_function('log', 1, log)
conn.commit()
c = conn.cursor()

print('Getting index size')
c.execute('''
SELECT count(*)
FROM Inverted_index7
''')

index_size = c.fetchone()[0]

print('Getting word size')
c.execute('''
SELECT count(*)
FROM Word
''')

word_size = c.fetchone()[0]

for i in range(word_size):
    print('calculating IDF', i)
    c.execute('''
    UPDATE Word7
    SET idf = (
        SELECT log(? * 1.0 / count(*))
        FROM Inverted_index7 as ie
        WHERE id = ie.word_id
    )
    WHERE id = ?
    ''', (index_size, i))

    print('calculating TF-IDF', i)
    c.execute('''
    UPDATE Inverted_index7
    SET tfidf = (
        Inverted_index7.tf
        * (
        SELECT idf
        FROM Word7 as w
        WHERE Inverted_index7.word_id = w.id
        )
    )
    WHERE word_id = ?
    ''', (i,))

    print('committing changes...')
    conn.commit()

conn.close()