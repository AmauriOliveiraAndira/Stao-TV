import unittest
from update_news import parse_feed, select_items, FEEDS

class NewsTests(unittest.TestCase):
    def test_parse_and_strip_html(self):
        xml=b'''<rss><channel><item><title>Noticia</title><link>https://example.com/1</link><pubDate>Tue, 27 Oct 2026 12:00:00 GMT</pubDate><description>&lt;p&gt;Resumo&lt;/p&gt;</description></item><item><title>Sem data</title></item></channel></rss>'''
        items=parse_feed('Teste',xml)
        self.assertEqual(len(items),1)
        self.assertEqual(items[0]['summary'],'Resumo')
        self.assertEqual(items[0]['date'],'27/10/2026 09:00')

    def test_investing_iso_date_without_description(self):
        xml=b'<rss><channel><item><title>Mercado</title><link>https://br.investing.com/news/1</link><pubDate>2026-10-27 13:47:19</pubDate></item></channel></rss>'
        items=parse_feed('Investing.com Brasil',xml)
        self.assertEqual(len(items),1)
        self.assertEqual(items[0]['summary'],'')
        self.assertIn('horário da fonte',items[0]['date'])

    def test_balance_dedupe_and_age(self):
        now=2_000_000_000
        items=[{'source':source,'title':f'{source}-{i}','timestamp':now-i} for source,_ in FEEDS for i in range(40)]
        items += [{'source':FEEDS[0][0],'title':'Muito antiga','timestamp':now-30*86400},
                  {'source':FEEDS[0][0],'title':'Futura','timestamp':now+86400},items[0]]
        result=select_items(items,now)
        self.assertEqual(len(result),100)
        self.assertEqual(len({x['title'] for x in result}),100)
        counts=[sum(x['source']==source for x in result) for source,_ in FEEDS]
        self.assertLessEqual(max(counts)-min(counts),1)

if __name__=='__main__':unittest.main()
