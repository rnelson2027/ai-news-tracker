import feedparser
import json
from pathlib import Path

#keywords used in the rss earch terms
KEYWORDS={
  "trump_ai_deregulation": "trump ai deregulation",
  "ai_case_law": "ai case law",
  "ai_deepfake_scam": "ai deepfake scam"
}
DATA_DIR=Path("data")
DATA_DIR.mkdir(exist_ok=True)

#create the string that is the search querrey by appenidng terms
def rss_url(query):
  q=query.replace(" ", "+")
  return(
    f"https://news.google.com/rss/search?"
    f"q={q}&hl=en-US&gl=US&ceid=US:en"
  )

#for each key word, get the expected file path
for key, query in KEYWORDS.items():
  file=DATA_DIR/f"{key}.json"

  #if the file exists, skip already known articles
  if file.exists():
    data=json.loads(file.read_text())
    seen={a["url"] for a in data["articles"]}
  #otherwise create the .json file  
  else:
    data={
      "label":query.title(),
      "query":query,
      "total":0,
      "articles":[]
    }
    seen=set()

  #create the rss feed scrape
  feed=feedparser.parse(rss_url(query))

  #for each article, if the article has been seen, skip to the next
  for entry in feed.entries:
    url=entry.link
    if url in seen:
      continue

    #create the article in the .json file with this format
    data["articles"].append({
      "title":entry.title,
      "url":url,
      "published":entry.get("published", "")
    })
    #add article to seen
    seen.add(url)
    data["total"]+=1
  
    file.write_text(json.dumps(data,indent=2))
  
