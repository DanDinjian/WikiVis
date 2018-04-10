import requests
import pickle

WIKI_GRAPH = {}
WIKI_TITLES = "data/english-wiki-titles"
WIKI_LINKS_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=links&pllimit=max&format=json&redirects=true&titles="

def formWikiGraphFromTitles():
    with open(WIKI_TITLES, 'r') as f:
        for title in f.readlines():
            title = title[:-1]
            WIKI_GRAPH[title] = []
    with open("data/wiki-graph.pickle", "wb") as fp:
        pickle.dump(WIKI_GRAPH, fp)
        #    links = getLinks(title)
        #    print(links)
        #    WIKI_GRAPH[title] = links

def getLinks(title):
    links = []
    url = WIKI_LINKS_URL + title
    data = requests.get(url).json()
    try:
        redirects = data["query"]["redirects"]
    except:
        print(title, " - does not redirect to a different page")
        try:
            pageid = list(data["query"]["pages"])[0]
            links_as_dictlist = data["query"]["pages"][pageid]["links"]
            for d in links_as_dictlist:
                links.append(d['title'])
        except:
            print(title, ' -- failed to load data -- ', data)
    return links

def addLinksToGraph():
    for key in WIKI_GRAPH.keys():
        WIKI_GRAPH[key] = getLinks(key)
        print(WIKI_GRAPH[key])

# By representing each page as a 24 bit vector (2^24 is about 17M) I can create encodings for the titles


if __name__ == "__main__":
    try:
        with open("data/wiki-graph.pickle", "rb") as data:
            WIKI_GRAPH = pickle.load(data)
            print('... ... ...loaded graph data')
    except:
        print('... ... ...failed to load graph')
    if len(WIKI_GRAPH) < 100:
        print('... ... ...reloading graph titles')
        formWikiGraphFromTitles()
    print('... ... ...adding links to graph')
    addLinksToGraph()

    # formWikiGraphFromTitles()
    # with open("data/wiki-graph.pickle", "wb") as fp:
    #     pickle.dump(WIKI_GRAPH, fp)
    #     i += 100
    #     print("finished: ", i)