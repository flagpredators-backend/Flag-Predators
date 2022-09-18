from cgitb import strong
import httpx, requests, shutil
import xmltodict
import json, os, glob
from bs4 import BeautifulSoup as bs
import re


folder = r"./assets/img/uCTFs"
temp = os.path.join(folder, r'tmp')
files = glob.glob(os.path.join(temp, "*"))
for f in files:
    os.remove(f)
    
client = httpx.Client()

rssUrl = "https://ctftime.org/event/list/upcoming/rss/"
rssfile = 'upcomingCTFsRSS.json'
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
}

data = xmltodict.parse(client.get(
    rssUrl, 
    follow_redirects=True,
    headers=headers
    ).content
)['rss']['channel']['item']

'''
#saving json data to a file (another approach)

with open(rssfile, 'w', encoding='utf-8') as file:
    json.dump(
        xmltodict.parse(client.get(
                    rssUrl, 
                    follow_redirects=True,
                    headers=headers
                ).content
        ), file, ensure_ascii=False, indent=2
    )

with open(rssfile, 'r') as file:
    data = json.load(file)['rss']['channel']['item']
'''

modified = list()

for instance in (data):

    storage = dict()
    
    if float(instance['weight']) == 0.0 or instance['location'] != None:
        continue

    storage['title'] = instance['title']
    storage['url'] = instance['url']
    html = client.get(
        instance['link'],
        headers=headers
    ).content

    soup = bs(html, 'lxml')
    desc = soup.find('div', attrs={'id': 'id_description'})
    if desc != None:
        summary = str(desc.find('p')).replace("<p>", "").replace("</p>", "")
        tmp = re.compile(r'<[^>]+>').sub('', summary)
        storage['description'] = tmp if len(tmp) <= 200 else f"{tmp.split('.')[0]}."
    else:
        storage['description'] = f"{instance['title']} is a jeopardy-style CTF hosted by {json.loads(instance['organizers'])[0]['name']}"
    
    
    imgfile = os.path.join(folder, "ctftime.jpg")
    link = instance['logo_url']

    if link != None:
        
        url = f"https://ctftime.org{link}"
        res = requests.get(url, stream=True, headers=headers)
        if res.status_code == 200:
            imgfile = f"{os.path.join(temp, instance['ctf_name'])}.{link.split('.')[1]}"
            with open(imgfile,'wb') as fptr:
                shutil.copyfileobj(res.raw, fptr)

    storage['logo_path'] = imgfile
    modified.append(storage)

with open(rssfile, 'w', encoding='utf-8') as file:
    json.dump(modified, file, ensure_ascii=False, indent=2)

