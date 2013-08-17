# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 22:34:19 2013

@author: roel
"""

import unittest
import peppov
from collections import OrderedDict
import pdb

#class PortfolioTest(unittest.TestCase):
class PortfolioTest():
    
    def setUp(self):
        self.p1 = peppov.Project(projectnumber=1, name="eerste project", tags=['huis', 'familie', 'persoonlijk'], fun=5, plieslies=3)
        self.p2 = peppov.Project(projectnumber=2, name="2e project", tags=['huis', 'familie', 'spel'], fun=4, plieslies=3)
    
        self.pf = peppov.Portfolio()
        self.pf.projects=OrderedDict([(1,self.p1),(2,self.p2)])
        
    def test_filter_projects(self):
        """Filtering with tags to be included"""
        
        #pdb.set_trace()        
        self.assertEqual(self.pf.selection, {})
        
        self.pf.filter_projects(incl=['spel'])
        self.assertEqual(len(self.pf.selection), 1)
        self.assertListEqual(self.pf.selection[2].tags, ['huis', 'familie', 'spel'])
        print 'test'
        
    def manual_test_filter_projects(self):
        """Filtering with a single tag to be included"""
        
        #pdb.set_trace() 7
        assert self.pf.selection == {}
        self.pf.filter_projects(incl=['spel'])
        
        assert len(self.pf.selection) == 1
        assert self.pf.selection[2].tags == ['huis', 'familie', 'spel']
        
        print '.'
        
    def manual_test_filter_projects2(self):
        """Filtering with multiple tags to be included"""
        
        #pdb.set_trace() 7
        assert self.pf.selection == {}
        self.pf.filter_projects(incl=['spel', 'huis'])
        
        assert len(self.pf.selection) == 1
        assert self.pf.selection[2].tags == ['huis', 'familie', 'spel']
        
        print '.'

if __name__ == '__main__':
#    unittest.main()
    print 'Unittest is not working in Canopy.  Trying to circumvent the problems manually.'
    
    pftest = PortfolioTest()
    pftest.setUp()
    pftest.manual_test_filter_projects()
    pftest.setUp()
    pftest.manual_test_filter_projects2()
    
    
    print 'All tests successful!'
    
    
    
    
#    suite1 = unittest.TestLoader().loadTestsFromTestCase(PortfolioTest)
#    alltests = unittest.TestSuite([suite1])
#    
#    selection = unittest.TestSuite()
#    selection.addTest(PortfolioTest('test_filter_projects'))
    #selection.addTest(GreyBoxTest('test_wrongOrder'))
        
    
#    unittest.TextTestRunner(verbosity=3, failfast=False).run(alltests)