import feedparser
import json
from pathlib import Path

KEYWORDS={
  "trump_ai_deregulation": "trump ai deregulation",
  "ai_case_law": "ai case law",
  "ai_deepfake_scam": "ai deepfake scam"
}
DATA_DIR=Path("data")
DATA_DIR.mkdir(exist_ok=True)

def rss_url(query):
  q=query.replace(" ", "+")
  return(
    f"https://news.google.com/rss/search?"
    f"q={q}&hl=en-US&gl=US&ceid=US:en"
  )

for key, query in KEYWORDS.items():
  file=DATA_DIR/f"{key}.json"

  if file.exists():
    data=json.loads(file.read_text())
    seen={a["url"] for a in data["articles"]}
  else:
    data={
      "label":query.title(),
      "query":query,
      "total":0,
      "articles":[]
    }
    seen=set()

  feed=feedparser.parse(rss_url(query))

  for entry in feed.entries:
    url=entry.link
    if url in seen:
      continue

    data["articles"].append({
      "title":entry.title,
      "url":url,
      "published":entry.get("published", "")
    })
    seen.add(url)
    data["total"]+=1
  
    file.write_text(json.dumps(data,indent=2))
  
