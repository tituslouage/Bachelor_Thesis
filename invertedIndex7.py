import sqlite3
from nlp import NLP

# create connection
conn = sqlite3.connect('../database/bloggers.db')
c = conn.cursor()

table_name = 'Inverted_index7'

c.execute('DROP TABLE IF EXISTS Word7')
c.execute('DROP TABLE IF EXISTS ' + table_name)

# creating word table
c.execute('''
CREATE TABLE Word7 (
    id INTEGER PRIMARY KEY,
    word TEXT NOT NULL,
    idf REAL NOT NULL DEFAULT 0
)
''')

# create Inverted_index table
c.execute('''
CREATE TABLE ''' + table_name + ''' (
    blogger_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,
    tf REAL NOT NULL,
    tfidf REAL NOT NULL DEFAULT 0,
    PRIMARY KEY (blogger_id, post_id, word_id)
    FOREIGN KEY(blogger_id) REFERENCES Blogger(id)
    FOREIGN KEY(post_id) REFERENCES Post(id)
)
''')
# save changes to db
conn.commit()

# create nlp instance
nlp = NLP()

# get all posts
c.execute('SELECT * FROM Post')
all_posts = c.fetchall()

# replace with id
words = {}

def replace_token_w_id(tokens):
    res = []
    for word, tf in tokens:
        if word not in words:
            words[word] = len(words)
        res.append((words[word], tf))
    return res

increment = 50000

start = 0
end = increment

while start < len(all_posts):
    indexed_data = []

    print(start, ' -> ', end)

    for post_id, text, creation_date, blogger_id in all_posts[start:end]:
        clean_tokens = nlp.clean_string_and_add_tf(text)
        clean_tokens = replace_token_w_id(clean_tokens)
        # rest of the code #
        # for each word in the post add a tuple with blogger id, post id, word position in the post and the word to indexed_data
        indexed_data.extend([(blogger_id, post_id, word, tf) for word, tf in clean_tokens])

    print('saving...')
    c.executemany('''
    INSERT INTO ''' + table_name + ''' (blogger_id, post_id, word_id, tf)
    VALUES (?, ?, ?, ?)
    ''', indexed_data)

    start += increment
    if end + increment > len(all_posts):
        end = len(all_posts)
    else:
        end += increment

print('saving words...')
c.executemany('''
INSERT INTO Word7 (word, id)
VALUES (?, ?)
''', words.items())

print('closing connection...')
conn.commit()
# close connection
conn.close()
