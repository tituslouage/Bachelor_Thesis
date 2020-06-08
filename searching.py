from search_inverted_index import Search

search = Search('Inverted_index6_2')
terms = ''

while terms != 'exit':
    terms = input('type in search term\n')

    simple_results = search.simple_search(terms)
    post_results = search.search_posts(terms)
    blogger_results = search.search_bloggers(terms)

    relevant = blogger_results[0]

    output = str(len(simple_results)) + ' records found in ' + str(len(post_results)) + ' posts by ' + str(len(blogger_results)) + ' bloggers. Most relevant blogger: \n\tid: ' + str(relevant[0]) + '\n\tgender: ' + str(relevant[1]) + '\n\tage: ' + str(relevant[2]) + '\n\tcompany: ' + str(relevant[3]) + '\n\tastrological sign: ' + str(relevant[4]) + '\n\trecords found: ' + str(relevant[5])

    print(output)
