from nltk import pos_tag
from nltk.tokenize import WhitespaceTokenizer


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
    return queries


#if __name__ == "__main__":
#   print(main())
