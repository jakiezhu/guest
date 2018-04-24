from django.test import TestCase
from sign.models import Event, Guest


class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=2, name="一加6发布会", status=True, limit=200,
                             address='深圳大广场', start_time="2018-05-12 12:12:12")
        Guest.objects.create(id=8, event_id=2, realname='Alen', phone="19000020008",
                             email="10008@qq.com", sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='一加6发布会')
        self.assertEqual(result.address, '深圳大广场')
        self.assertTrue(result.status)

    def test_gust_models(self):
        result = Guest.objects.get(phone='19000020008')
        self.assertEqual(result.realname, 'Alen')
        self.assertFalse(result.sign)
