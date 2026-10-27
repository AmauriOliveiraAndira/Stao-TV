import datetime as dt
import unittest
from unittest.mock import patch
import update_agenda as agenda

class AgendaTests(unittest.TestCase):
    def test_payment_and_declaration_only(self):
        source='''<table><tr><td>2089</td><td>IRPJ</td><td>Lucro presumido</td><td>3º trimestre</td></tr>
        <tr><td>DARF</td><td>DCTFWeb Geral</td><td>Lei</td></tr>
        <tr><td>PJ/PF</td><td>DCTFWeb – Declaração</td><td>Setembro/2026</td><td>IN</td></tr>
        <tr><td>999</td><td>Parcelamento</td><td>Especial</td><td>Mês atual</td></tr></table>'''
        items=agenda.parse_day(source,'2026-10-30','https://www.gov.br/exemplo')
        self.assertEqual(len(items),2)
        self.assertTrue(all(x['date']=='2026-10-30' for x in items))
        self.assertIn('Setembro/2026',items[1]['detail'])

    def test_missing_calendar_fails(self):
        with self.assertRaises(ValueError):
            agenda.collect(dt.date(2026,11,1),lambda url:'<p>Indisponível</p>')

    def test_no_foreign_or_wrong_month_links(self):
        source='''<a href="dia-30-10-2026">Data</a><a href="dia-01-11-2026">Outro mês</a>
        <a href="https://example.com/dia-30-10-2026">Externo</a>'''
        calls=[]
        def reader(url):
            calls.append(url)
            if '/dia-' not in url:return source
            return '<table><tr><td>PJ</td><td>DCTFWeb</td><td>09/2026</td><td>IN</td></tr></table>'
        result=agenda.collect(dt.date(2026,10,27),reader)
        self.assertEqual(len(calls),2)
        self.assertEqual(sum(x['kind'].startswith('Federal') for x in result['items']),1)

    def test_source_failure_keeps_previous_file(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'agenda.json'
            previous='{"checked_on": null,"items":[]}'
            output.write_text(previous)
            with patch.object(agenda,'OUT',output),patch.object(agenda,'collect',side_effect=ValueError('Fonte mudou')):
                with self.assertRaises(ValueError):agenda.main()
            self.assertEqual(output.read_text(),previous)

if __name__=='__main__':unittest.main()
