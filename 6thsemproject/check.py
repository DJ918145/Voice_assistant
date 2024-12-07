from youtube_search import YoutubeSearch
import webbrowser as wb
def song(query):
    query.split()
    ans = ""
    for i in range(len(query)):
        if query[i]=='play' or query[i]=='search':
            query = query[i:]
    for i in query:
        ans = ans + query
            
    results = YoutubeSearch(ans, max_results=10).to_dict()
    url = results[0]['id']
    url = "https://www.youtube.com/watch?v="+url
    wb.open(url)

query = "Hey jarvis can you please search python playlist"
song(query)
