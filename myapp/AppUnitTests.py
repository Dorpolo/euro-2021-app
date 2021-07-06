from django.test import TestCase
from models import League


class PostTestCase(TestCase):
    def testPost(self):
        league = League(league_name="TestableLeague", league_owner='Polo', league_owner_id=2)
        self.assertEqual(league.league_name, "TestableLeague")
        self.assertEqual(league.league_owner, "Polo")
        self.assertEqual(league.league_owner_id, 78)