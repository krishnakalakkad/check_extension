from nltk import pos_tag
from nltk.tokenize import WhitespaceTokenizer
import requests
from bs4 import BeautifulSoup

def formURL(qry):
    encoded_qry = parse.urlencode(qry)
    url = "https://www.snopes.com/?s=" + encoded_qry + "&orderby=date"
    return url

def scrapeForEachQuery(queries):
    """for qry in queries:
        url = formURL(qry)
        print(url)"""
    r = requests.get("https://www.snopes.com/?s=kamala+harris+purse&orderby=date")
    data = r.text
    source = BeautifulSoup(data, "html.parser")
    first_article = source.find("a", {"class": "link"})
    return first_article.get('href')


def formQueries(parsed_words):
    qarr = []
    query = ""
    referred_nouns = "" # this used to refer to the same noun in the case of conjunctions
    new_noun = 1
    verbon = 0

    for i in parsed_words:
        try:
            # determine whether word is noun or cardinal digits
            if i[1][0] == "N" or i[1] == "CD":
                if new_noun == 0:
                    query += (" " + i[0])
                    if (verbon == 0):
                        referred_nouns += (" " + i[0])
                else:
                    query = i[0]
                    referred_nouns = query
                    new_noun = 0
            if i[1][0] == "V":
                query += (" " + i[0])
                verbon = 1
            if i[1] == "JJ":
                query += (" " + i[0])
            if i[1] == "CC":
                qarr.append(query)
                query = referred_nouns
                verbon == 0
            if i[0][-1] == '.' or i[0][-1] == "!" or i[0][-1] == "?":
                query = query.replace(i[0][-1], "")
                new_noun == 1
                qarr.append(query)
                query = ""
        except IndexError:
            continue
    return qarr

#tweet is going to be a string
def main(tweet):
    #tweet = input("enter tweet here: ")
    tk = WhitespaceTokenizer()
    words = tk.tokenize(tweet)
    words_with_pos = pos_tag(words)
    queries = formQueries(words_with_pos)
    return scrapeForEachQuery(queries)


main("Kamala Harris openly encouraged rioters and directly funded domestic terrorism. She needs to be impeached.")



#if __name__ == "__main__":
#   print(main())
