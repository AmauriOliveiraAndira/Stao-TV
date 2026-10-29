#!/usr/bin/env python3
"""Agenda resumida e editável de pagamentos e rotinas internas STAO."""
import calendar
import datetime as dt
import hashlib
import json
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'agenda.json'
CONFIG = ROOT / 'agenda_regras.json'
# Feriados nacionais de data fixa; feriados locais/religiosos e dias de fechamento
# do escritório podem ser acrescentados pelo responsável em extra_holidays.
NATIONAL_DAYS = ('01-01','04-21','05-01','09-07','10-12','11-02','11-15','11-20','12-25')

def holidays(year, config):
    result = {f'{year}-{day}' for day in NATIONAL_DAYS}
    for value in config.get('extra_holidays', []):
        date = dt.date.fromisoformat(value)
        if date.year == year:
            result.add(date.isoformat())
    return result

def is_business(date, excluded):
    return date.weekday() < 5 and date.isoformat() not in excluded

def business_day(year, month, number, excluded):
    if not 1 <= number <= 23:
        raise ValueError('Número de dia útil inválido')
    count = 0
    for day in range(1, calendar.monthrange(year, month)[1]+1):
        date = dt.date(year, month, day)
        if is_business(date, excluded):
            count += 1
            if count == number:
                return date
    raise ValueError('O mês não possui esse número de dias úteis')

def due_date(year, month, rule, excluded):
    mode = rule['rule']
    if mode == 'business':
        return business_day(year, month, int(rule['day']), excluded)
    if mode == 'last_business':
        date = dt.date(year, month, calendar.monthrange(year, month)[1])
        adjust = 'before'
    elif mode == 'calendar':
        date = dt.date(year, month, int(rule['day']))
        adjust = rule.get('adjust', 'none')
    else:
        raise ValueError('Regra desconhecida: ' + mode)
    if adjust not in ('none','before','after'):
        raise ValueError('Ajuste de data desconhecido')
    if adjust != 'none':
        step = dt.timedelta(days=1 if adjust == 'after' else -1)
        while not is_business(date, excluded):
            date += step
    return date

def collect(today, config=None):
    config = config if config is not None else json.loads(CONFIG.read_text(encoding='utf-8'))
    year, month = today.year, today.month
    excluded = holidays(year, config) | holidays(year-1, config) | holidays(year+1, config)
    items = []
    # Mês atual e próximo: permite mostrar as primeiras rotinas do mês seguinte.
    for offset in (0, 1):
        y, m = (year+1, 1) if month+offset == 13 else (year, month+offset)
        for row in config['rules']:
            if not row.get('enabled', True) or m not in row.get('months', list(range(1,13))):
                continue
            date = due_date(y, m, row, excluded)
            internal = row['kind'] == 'Escritório'
            items.append({'date': date.isoformat(), 'name': row['name'],
                          'kind': row['kind'], 'detail': row.get('detail',''),
                          'source': 'Rotina interna STAO' if internal else config['source']})
    for row in config.get('dated_items', []):
        dt.date.fromisoformat(row['date'])
        items.append({'date':row['date'],'name':row['name'],
                      'kind':row.get('kind','Escritório'),'detail':row.get('detail',''),
                      'source':row.get('source','Tabela STAO')})
    return {'month':f'{year:04}-{month:02}', 'checked_on':today.isoformat(),
            'source':config['source'], 'calendar_note':config['calendar_note'],
            'config_hash':hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest(),
            'items':sorted(items,key=lambda x:(x['date'],x['kind']!='Escritório',x['name']))}

def main():
    today = dt.datetime.now(ZoneInfo('America/Sao_Paulo')).date()
    data = collect(today)
    temporary = OUT.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
    temporary.replace(OUT)
    print(f"Agenda resumida: {len(data['items'])} registros, mês atual e próximo.")

if __name__ == '__main__':
    main()
