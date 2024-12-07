import requests

def fn():
    api_key = '4c59710cd0c34893a0d8036a27c4c091'
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    # newsh = ""
    newsd ={}
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        
        for article in articles:
            title = article.get('title', 'No Title')
            link = article.get('url', 'No Link')
            # print(f"Headline: {title}\n")
            newsd.setdefault(title,link)

    else:
        print("Failed to fetch news:", response.status_code)
    # print(newsd)
    newsh = newsd.keys()
    newslist = list(newsh)
    # newslist = [[x] for x in newslist]
    return newslist[:5]
        


if __name__ == "__main__":
    fn()
