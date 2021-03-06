"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

for priority in range(0,9):
    for days in [-1,0,1,3,8,15,30,60]:
        days = 1 if days == 0 else days+1
        days = days if days > 0 else 0.9
        w = (10-priority) * 1.0/float(days)
        print "%s %s %s" %(priority,days,w)