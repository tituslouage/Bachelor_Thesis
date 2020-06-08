from bs4 import BeautifulSoup as bs
import sqlite3
from os import listdir

# make connection
conn = sqlite3.connect('../database/bloggers.db')
c = conn.cursor()

# drop tables
c.execute("DROP TABLE IF EXISTS Blogger")

c.execute("DROP TABLE iF EXISTS Post")

conn.commit()

# create tables
c.execute('''
CREATE TABLE Blogger (
	id INTEGER PRIMARY KEY,
	gender TEXT,
	age INTEGER,
	company TEXT,
	astrological_sign TEXT)
''')

c.execute('''
CREATE TABLE Post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    creation_date TEXT,
    blogger_id INTEGER,
    FOREIGN KEY(blogger_id) REFERENCES Blogger(id))
''')

# save changes to db
conn.commit()


# get all file names in folder data
# file name structure = id.gender.age.company.astrological_sign.xml
files = listdir('data')

bloggers = []
posts = []

file_blogger_id = 0
file_gender = 1
file_age = 2
file_company = 3
file_astrological_sign = 4

for file_name in files:
    split_file_name = file_name.split('.')

    blogger_id = split_file_name[file_blogger_id]
    gender = split_file_name[file_gender]
    age = split_file_name[file_age]
    company = split_file_name[file_company]
    astrological_sign = split_file_name[file_astrological_sign]

    # save blogger in tuple
    blogger = (blogger_id, gender, age, company, astrological_sign)

    # add blogger to bloggers list
    bloggers.append(blogger)

    # open file
    with open('data/' + file_name, encoding='ansi') as file:
        # read file content
        content = file.readlines()
        # convert list to string
        content = ''.join(content)

        # define language
        bs_content = bs(content, 'lxml')
        # the dates are stored in <date> tags
        xml_dates = bs_content.find_all('date')
        # the posts are stored in <post> tags
        xml_posts = bs_content.find_all('post')

        for index, xml_post in enumerate(xml_posts):
            post_text = xml_post.text.strip()
            post_date = xml_dates[index].text.strip()

            # save post in tuple
            post = (post_text, post_date, blogger_id)

            # save post in posts list
            posts.append(post)

# insert bloggers into database
c.executemany('INSERT INTO Blogger VALUES (?, ?, ?, ?, ?)', bloggers)

# insert posts into database
c.executemany('INSERT INTO Post (text, creation_date, blogger_id) VALUES (?, ?, ?)', posts)

# save to db and close connection
conn.commit()
conn.close()
