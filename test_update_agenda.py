import datetime as dt
import unittest
import update_agenda as agenda

class AgendaTests(unittest.TestCase):
    def test_first_business_after_holiday(self):
        excluded=agenda.holidays(2026,{})
        self.assertEqual(agenda.business_day(2026,11,1,excluded),dt.date(2026,11,3))
        self.assertEqual(agenda.business_day(2026,11,5,excluded),dt.date(2026,11,9))
        self.assertEqual(agenda.business_day(2026,11,12,excluded),dt.date(2026,11,18))
    def test_local_holiday(self):
        excluded=agenda.holidays(2026,{'extra_holidays':['2026-11-03']})
        self.assertEqual(agenda.business_day(2026,11,1,excluded),dt.date(2026,11,4))
    def test_payment_adjustment(self):
        excluded=agenda.holidays(2026,{})
        rule={'rule':'calendar','day':20,'adjust':'after'}
        self.assertEqual(agenda.due_date(2026,11,rule,excluded),dt.date(2026,11,23))
        rule['adjust']='before'
        self.assertEqual(agenda.due_date(2026,11,rule,excluded),dt.date(2026,11,19))
        rule['adjust']='none'
        self.assertEqual(agenda.due_date(2026,11,rule,excluded),dt.date(2026,11,20))
    def test_all_internal_and_year_rollover(self):
        result=agenda.collect(dt.date(2026,12,29))
        internal=[x for x in result['items'] if x['kind']=='Escritório']
        self.assertEqual(len(internal),18)
        self.assertTrue(any(x['date']=='2027-01-04' for x in internal))
    def test_specific_date_and_disabled_rule(self):
        config={'source':'Contabilizei','calendar_note':'teste','rules':[{'enabled':False}],
                'dated_items':[{'date':'2026-11-10','name':'Reunião'}]}
        self.assertEqual(len(agenda.collect(dt.date(2026,11,1),config)['items']),1)

if __name__=='__main__':unittest.main()
