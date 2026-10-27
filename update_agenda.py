#!/usr/bin/env python3
"""Coleta vencimentos publicados pela RFB; não calcula prazos por recorrência."""
import datetime as dt
import json
import re
import unicodedata
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'agenda.json'
REFERENCE = 'https://www.contabilizei.com.br/contabilidade-online/agenda-tributaria/'
MONTHS = ('Janeiro Fevereiro Março Abril Maio Junho Julho Agosto Setembro Outubro Novembro Dezembro').split()

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.links, self.rows, self.row, self.cell = [], [], None, None
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs).get('href', ''))
        elif tag == 'tr':
            self.row = []
        elif tag in ('td', 'th') and self.row is not None:
            self.cell = []
    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)
    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            self.row.append(' '.join(' '.join(self.cell).split()))
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'STAO-TV/1.0', 'Accept': 'text/html'})
    with urllib.request.urlopen(req, timeout=35) as response:
        return response.read(4_000_000).decode('utf-8')

def normal(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if not unicodedata.combining(c)).lower()

# Escopo de rotina contábil: não inclui todos os códigos de receita da RFB.
TAXES = {'irpj', 'csll', 'pis/pasep', 'cofins', 'ipi', 'simples nacional', 'inss', 'irrf'}
DECLARATIONS = ('dctfweb', 'efd', 'esocial', 'pgdas', 'defis', 'dasn', 'ecd', 'ecf', 'dme', 'doi', 'decripto')

def parse_day(source, date, url):
    page = Page(source)
    if not page.rows:
        raise ValueError('Tabela ausente: ' + url)
    items = []
    for row in page.rows:
        if len(row) != 4:
            continue
        code, group, description, period = row
        if normal(group) in TAXES:
            items.append({'date': date, 'name': group + ' • ' + description,
                          'detail': 'Apuração: ' + period + ' • código ' + code,
                          'kind': 'Federal • conforme enquadramento', 'source': url})
        elif any(normal(group).startswith(prefix) for prefix in DECLARATIONS):
            items.append({'date': date, 'name': group, 'detail': 'Referência: ' + description,
                          'kind': 'Federal • contribuintes obrigados', 'source': url})
    return items

def collect(today, reader=fetch):
    month = f'{today:%Y-%m}'
    index = f'https://www.gov.br/receitafederal/pt-br/assuntos/agenda-tributaria/{today.year}/{MONTHS[today.month-1]}'
    page = Page(reader(index))
    days = {}
    for href in page.links:
        url = urljoin(index + '/', href).split('#')[0].split('?')[0].rstrip('/')
        match = re.search(r'/dia-(\d{2})-(\d{2})-(\d{4})$', url)
        if not match or urlparse(url).netloc != 'www.gov.br':
            continue
        day, mon, year = map(int, match.groups())
        date = dt.date(year, mon, day)
        if date.strftime('%Y-%m') == month:
            days[url] = date.isoformat()
    if not days:
        raise ValueError('Calendário do mês ainda indisponível ou formato alterado')
    # Qualquer falha aborta o arquivo todo, preservando a última coleta completa.
    items = []
    for url, date in sorted(days.items()):
        items.extend(parse_day(reader(url), date, url))
    if not items:
        raise ValueError('Nenhuma obrigação reconhecida; conferir o formato da fonte')
    state = ROOT / 'agenda_estadual.json'
    if state.exists():
        # Apenas datas estaduais explicitamente validadas; nunca repetir no mês seguinte.
        for item in json.loads(state.read_text(encoding='utf-8')).get('items', []):
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}', item.get('date', '')) and item['date'].startswith(month):
                items.append(item)
    unique = {(x['date'], x['name'], x['detail']): x for x in items}
    return {'month': month, 'checked_on': today.isoformat(),
            'reference': REFERENCE, 'source': index,
            'items': sorted(unique.values(), key=lambda x: (x['date'], x['name'], x['detail']))}

def main():
    today = dt.datetime.now(ZoneInfo('America/Sao_Paulo')).date()
    if OUT.exists():
        previous = json.loads(OUT.read_text(encoding='utf-8'))
        if previous.get('checked_on') == today.isoformat():
            print('Agenda já consultada hoje.')
            return
    data = collect(today)
    temp = OUT.with_suffix('.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(OUT)
    print(f"Agenda {data['month']}: {len(data['items'])} vencimentos publicados.")

if __name__ == '__main__':
    main()
