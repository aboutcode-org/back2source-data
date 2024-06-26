import requests
from purldb_toolkit.purlcli import d2d


from_to_urls = []
with open("pairs.csv", "r") as f:
    for line in f:
        from_to = line.strip().split(",")
        from_to_urls.append({"to": from_to[0], "from": from_to[1]})

for from_to_url in from_to_urls:
    from_url = from_to_url["from"]
    to_url = from_to_url["to"]
    
    try:
        r = requests.head(from_url, timeout=30)
    except:
        continue
    from_size = r.headers.get('content-length')
    from_size = int(from_size) if from_size else None

    if from_size and from_size > 10000000:
        continue

    try:
        r = requests.head(from_url, timeout=30)
    except:
        continue
    to_size = r.headers.get('content-length')
    to_size = int(to_size) if to_size else None

    if to_size and to_size > 10000000:
        continue
    try:
        d2d(
        purls=[
            from_url, to_url
        ], 
        output=f"{from_to_url['from'].split('/')[-1]}-{from_to_url['to'].split('/')[-1]}.txt", 
        purldb_api_url=None, 
        matchcode_api_url="http://127.0.0.1:8002/api/"
        )
    except:
        continue
