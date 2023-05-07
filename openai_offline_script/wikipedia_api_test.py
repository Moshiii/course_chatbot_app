import wikipedia


def search_wiki(query):

    result = wikipedia.search(query)
    # print("search term: ",query," list: ",result)
    title=""
    url=""
    summary=""
    references=""

    for x in range(0, len(result)):
        try:
            page = wikipedia.page(result[x])
            title = page.title
            url = page.url
            summary = page.summary
            content = page.content
            references = page.references
            break
        except:
            print("searching title: ",result[x]," no wiki page found, try next one")
    return title, url, summary, references


def search_wiki_first_only(query):

    result = wikipedia.search(query)
    # print("search term: ",query," list: ",result)
    title=""
    url=""
    summary=""
    references=""

    try:
        page = wikipedia.page(result[0])
        title = page.title
        url = page.url
        summary = page.summary
        content = page.content
        references = page.references
    except:
        print("searching title: ",result[0]," no wiki page found, try next one")
        
    return title, url, summary, references