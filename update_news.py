#!/usr/bin/env python3
"""Atualização gratuita de manchetes para GitHub Pages, sem chaves de API."""
import datetime,email.utils,html,json,re,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
FEEDS=[('Agência Brasil • Economia','https://agenciabrasil.ebc.com.br/rss/economia/feed.xml'),('Agência Brasil • Últimas','https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml')]
OUT=Path(__file__).parent/'news.json'
def plain(t):
 t=re.sub(r'<[^>]*>',' ',t or '')
 return re.sub(r'\s+',' ',html.unescape(t)).strip()
def read_feed(source,url):
 req=urllib.request.Request(url,headers={'User-Agent':'STAO-Painel/1.0 (+https://github.com/amaurioliveiraandira/Stao-TV)','Accept':'application/rss+xml,application/xml,text/xml'})
 with urllib.request.urlopen(req,timeout=22) as r: data=r.read(2500000)
 root=ET.fromstring(data); output=[]
 for it in root.findall('.//item')[:30]:
  get=lambda tag: (it.findtext(tag) or '').strip()
  title=plain(get('title'));summary=plain(get('description'))[:380];pub=get('pubDate')
  try:dt=email.utils.parsedate_to_datetime(pub);date=dt.strftime('%d/%m/%Y %H:%M');ts=dt.timestamp()
  except Exception: date='';ts=0
  if title:output.append({'source':source,'title':title,'summary':summary,'date':date,'link':get('link'),'timestamp':ts})
 return output
items=[]
for source,url in FEEDS:
 try:
  result=read_feed(source,url);print(source,len(result));items+=result
 except Exception as e:print('Feed indisponível:',source,str(e))
seen=set();clean=[]
for it in sorted(items,key=lambda x:x['timestamp'],reverse=True):
 k=it['title'].lower()
 if k not in seen: seen.add(k);clean.append(it)
if clean:
 OUT.write_text(json.dumps({'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'items':clean[:30]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
else:
 print('Nenhum feed respondeu: mantendo arquivo anterior para evitar perda de conteúdo.')
