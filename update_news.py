#!/usr/bin/env python3
"""Coleta manchetes e excertos de feeds públicos para a TV STAO."""
import datetime as dt
import email.utils
import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from zoneinfo import ZoneInfo

FEEDS = [
    ('BBC News Brasil', 'https://feeds.bbci.co.uk/portuguese/rss.xml'),
    ('Portal Contábeis', 'https://www.contabeis.com.br/rss/conteudo/'),
    ('Conselho Federal de Contabilidade', 'https://cfc.org.br/feed/'),
    ('Brasil de Fato', 'https://www.brasildefato.com.br/feed/'),
    ('Investing.com Brasil', 'https://br.investing.com/rss/news.rss'),
    ('Jovem Pan', 'https://jovempan.com.br/feed'),
]
OUT = Path(__file__).parent / 'news.json'
MAX_AGE = 14 * 86400

def plain(text):
    text = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', ' ', text or '', flags=re.S | re.I)
    text = re.sub(r'<[^>]*>', ' ', text)
    return re.sub(r'\s+', ' ', html.unescape(text)).strip()

def parse_feed(source, data):
    root = ET.fromstring(data)
    output = []
    for item in root.findall('.//item')[:100]:
        get = lambda tag: (item.findtext(tag) or '').strip()
        title, link = plain(get('title')), get('link')
        try:
            raw_date = get('pubDate')
            try:
                published = email.utils.parsedate_to_datetime(raw_date)
            except (ValueError, TypeError):
                published = dt.datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
            naive_date = published.tzinfo is None
            if published.tzinfo is None:
                published = published.replace(tzinfo=dt.timezone.utc)
            timestamp = published.timestamp()
        except (ValueError, TypeError, OverflowError):
            continue  # Não exibir uma manchete sem saber a data de publicação.
        if title and link.startswith(('https://', 'http://')):
            summary = plain(get('description'))
            if len(summary) > 280:
                summary = summary[:277].rsplit(' ', 1)[0] + '…'
            output.append({'source': source, 'title': title, 'summary': summary,
                           'date': (published.strftime('%d/%m/%Y %H:%M') + ' (horário da fonte)' if naive_date else published.astimezone(ZoneInfo('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M')),
                           'link': link, 'timestamp': timestamp})
    return output

def read_feed(source, url):
    request = urllib.request.Request(url, headers={
        'User-Agent': 'STAO-Painel/1.0 (+https://github.com/AmauriOliveiraAndira/Stao-TV)',
        'Accept': 'application/rss+xml,application/xml,text/xml'})
    with urllib.request.urlopen(request, timeout=25) as response:
        return parse_feed(source, response.read(3_000_000))

def select_items(items, now, limit=100):
    # Alternar as fontes para que uma redação com mais publicações não elimine as demais.
    queues = {source: [] for source, _ in FEEDS}
    for item in sorted(items, key=lambda x: x.get('timestamp', 0), reverse=True):
        timestamp = item.get('timestamp', 0)
        if item.get('source') in queues and now - MAX_AGE <= timestamp <= now + 3600:
            queues[item['source']].append(item)
    seen, output = set(), []
    while len(output) < limit and any(queues.values()):
        for queue in queues.values():
            while queue:
                item = queue.pop(0)
                key = plain(item['title']).casefold()
                if key in seen:
                    continue
                seen.add(key)
                output.append(item)
                break
            if len(output) == limit:
                break
    return output

def main():
    previous = []
    if OUT.exists():
        try:
            previous = json.loads(OUT.read_text(encoding='utf-8')).get('items', [])
        except (ValueError, OSError):
            pass
    items, statuses = [], []
    now = dt.datetime.now(dt.timezone.utc)
    for source, url in FEEDS:
        try:
            result = read_feed(source, url)
            if not result:
                raise ValueError('Feed sem itens válidos')
            items.extend(result)
            statuses.append({'source': source, 'ok': True, 'count': len(result)})
            print(source, len(result))
        except Exception as error:
            print('Feed indisponível:', source, str(error))
            items.extend(item for item in previous if item.get('source') == source)
            statuses.append({'source': source, 'ok': False})
    # Acumular notícias ainda recentes entre coletas, inclusive de feeds curtos.
    clean = select_items(items + previous, now.timestamp())
    # Mesmo sem notícias recentes, registrar lista vazia para remover manchetes vencidas.
    data = {'updated_at': now.isoformat(), 'sources': statuses, 'items': clean}
    temporary = OUT.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(OUT)

if __name__ == '__main__':
    main()
