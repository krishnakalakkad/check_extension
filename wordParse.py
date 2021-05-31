from nltk import pos_tag
from nltk.tokenize import WhitespaceTokenizer
import requests
from bs4 import BeautifulSoup



def formSnopesURL(qry, date):
    encoded_qry = qry.replace(" ", "+")

    url = "https://www.snopes.com/?s=" + encoded_qry
    if date == 1:
        url +=  "&orderby=date"
    return url

def formPolitifactURL(qry):
    encoded_qry = qry.replace(" ", "+")
    url = "https://www.politifact.com/search/?q=" + encoded_qry
    return url

#date is int, qry is string
def yieldSnopesResults(qry, date):
    search_page_url = formSnopesURL(qry, date)
    search_request = requests.get(search_page_url)
    data = search_request.text
    search_htmldom = BeautifulSoup(data, "html.parser")
    first_article = search_htmldom.find("a", {"class": "link"})
    article_link = first_article.get('href')
    if article_link[23] == 'f':
        article_request = requests.get(article_link)
        data = article_request.text
        article_htmldom = BeautifulSoup(data, "html.parser")
        title = article_htmldom.select('h1.title')[0].text.strip()
        verdict = (article_htmldom.find("img", {"class" : "figure-image img-responsive img-fluid w-100"}))['alt']
        return (title, article_link, verdict)


def yieldPolitifactResults(qry):
    search_page_url = formPolitifactURL(qry)
    search_request = requests.get(search_page_url)
    search_htmldom = BeautifulSoup(search_request.text, "html.parser")
    first_article = search_htmldom.find("div", {"class": "o-listease__item"})
    fst_art_item = first_article.find("div", {"class": "c-textgroup__title"}).find('a')
    first_article_title = fst_art_item.contents[0]
    first_article_link = "https://www.politifact.com" + fst_art_item['href']
    #first_article_verdict = fst_art_item.find('img')['src']
    return (first_article_title, first_article_link)


"""https://static.politifact.com/CACHE/images/politifact/rulings/tom_ruling_pof/d089e796db6628261f228086d4084fa8.jpg
https://static.politifact.com/CACHE/images/politifact/rulings/meter-false/6078f198eb8fad1b553c23b0d3edc735.jpg
https://static.politifact.com/CACHE/images/politifact/rulings/meter-mostly-false/b7738b2b59177882eb8cbea926ad37ab.jpg
https://static.politifact.com/CACHE/images/politifact/rulings/meter-half-true/b81964349780d58033deb9ef2d1b0dfd.jpg
https://static.politifact.com/CACHE/images/politifact/rulings/meter-mostly-true/eab607507cdade634c07465983bd63d4.jpg
https://static.politifact.com/CACHE/images/politifact/rulings/meter-true/eb3f74da30375e27384812d99e83f2af.jpg"""


def scrapeWebForEachQuery(queries):
    articles_with_verdicts = []
    for qry in queries:
        articles_with_verdicts.append(yieldSnopesResults(qry, 0))

    for qry in queries:
        articles_with_verdicts.append(yieldPolitifactResults(qry))

    return articles_with_verdicts


def formQueries(parsed_words):
    qarr = []
    query = ""
    referred_nouns = "" # this used to refer to the same noun in the case of conjunctions
    new_noun = 1
    verbon = 0

    for i in parsed_words:
        if i[0][0] == '#':
            i = (i[0][1:], i[1])
        try:
            # determine whether word is noun or cardinal digits
            if i[0] == "not":
                query += (" " + i[0])
                continue
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
    if query != "":
        qarr.append(query)
    return qarr

#tweet is going to be a string
def main(tweet):
    #tweet = input("enter tweet here: ")
    tk = WhitespaceTokenizer()
    words = tk.tokenize(tweet)
    words_with_pos = pos_tag(words)
    queries = formQueries(words_with_pos)
    return scrapeWebForEachQuery(queries)


#main("Kamala Harris openly encouraged rioters and directly funded domestic terrorism. She needs to be impeached.")



#if __name__ == "__main__":
#   print(main())
