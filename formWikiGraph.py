import requests
import pickle

WIKI_GRAPH = {}
WIKI_TITLES = "data/english-wiki-titles"
WIKI_LINKS_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=links&pllimit=max&format=json&titles="

def formWikiGraph():
    with open(WIKI_TITLES, 'r') as f:
        #for title in f.readlines()[i:i+10]:
        for title in f.readlines():#[i:i+100]:
            title = title[:-1]
        #    print(title)
        #    links = getLinks(title)
        #    print(links)
        #    WIKI_GRAPH[title] = links
            WIKI_GRAPH[title] = []

def getLinks(title):
    links = []
    url = WIKI_LINKS_URL + title
    data = requests.get(url).json()
    if "query" in data.keys():
        if "pages" in data["query"].keys():
            pageid = list(data["query"]["pages"])[0]
            if "links" in data["query"]["pages"][pageid].keys():
                links_as_dictlist = data["query"]["pages"][pageid]["links"]
                for d in links_as_dictlist:
                    links.append(d['title'])
    return links

# By representing each page as a 24 bit vector (2^24 is about 17M) I can create encodings for the titles


if __name__ == "__main__":
    formWikiGraph()
    #  i = 0
    # while i < 1000000:
    #     formWikiGraph(i)
    with open("data/wiki-graph.pickle", "wb") as fp:
        pickle.dump(WIKI_GRAPH, fp)
    #     i += 100
    #     print("finished: ", i)