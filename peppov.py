# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 21:42:12 2013

@author: roel
"""


from traits.api import HasTraits,Int,Float,Str,Property,Range,Array
from traitsui.api import View,Item,Label,ListStrEditor,UItem,Group
from traitsui.menu import OKButton, CancelButton,RevertButton
from chaco.chaco_plot_editor import ChacoPlotItem
from numpy import array,poly1d,arange,linspace
from collections import OrderedDict

class Person(HasTraits):
   name = Str
   age = Int
   height = Float
   weight = Float

   bmi = Property(Float,depends_on=["height","weight"])

   view = View(
               Item("height",label = "Height / m"),
               Item("weight",label = "Weight / kg"),
               Item("bmi"),
               buttons=[RevertButton,OKButton,CancelButton],
              )

   def _get_bmi(self):
      return self.weight/self.height**2

#p = Person(name="Billy",age=18,height=2.,weight=90)
#p.configure_traits()
#
#print p.name,p.age.p.height,p.weight


class PlotterApplication(HasTraits):
   c0 = Range(-5.,5.)
   c1 = Range(-5.,5.)
   c2 = Range(-5.,5.)

   xdata = Array
   ydata = Property(Array,depends_on=["c0","c1","c2"])

   #Set the coeffients to 0 as default
   def _c0_default(self): return 0.
   def _c1_default(self): return 0.
   def _c2_default(self): return 0.

   def _xdata_default(self): return linspace(-10,10,100)

   def _get_ydata(self):
      poly = poly1d([self.c2,self.c1,self.c0])
      return poly(self.xdata)

   traits_view = View(
                  ChacoPlotItem("xdata","ydata", y_bounds=(-10.,10.),y_auto=False,resizable=True,show_label=False,x_label="x",y_label="y",title=""),
                  Item('c0'),
                  Item('c1'),
                  Item('c2'),
                  resizable = True,
                  width=900, height=800,
                  title="Plot App"
                     )

import random

from traits.api import HasTraits, List, Str, Button
from traitsui.api import ListStrEditor, View, UItem


class Demo(HasTraits):

    my_list = List(Str)

    add = Button("ADD")
    clear = Button("CLEAR")

    traits_view = \
        View(
            UItem('my_list', editor=ListStrEditor(auto_add=False)),
            UItem('add'),
            UItem('clear'),
        )

    def _my_list_default(self):
        return ['Item1', 'Item2']

    def _add_fired(self):
        new_item = "Item%d" % random.randint(3, 999)
        self.my_list.append(new_item)

    def _clear_fired(self):
        self.my_list = []


class Project(HasTraits):
    """Class for a single project"""
    
    number = Int
    name = Str
    comment = Str
    tags = List(Str, label='all tags')
    singletag = Str(desc='Tag to be added or removed', label='tag')
    fun = Range(0,5)
    dringendheid = Range(0,5)
    belang = Range(0,5)
    goeiedaad = Range(0,5)
    plieslies = Range(0,5)
    
    add = Button('Add tag')
    remove = Button('Remove tag')
    
    view_tabs = View(Group(
                        Item('number'),
                        Item(name='name'),
                        Item(name='comment'),
                        Item('tags', editor=ListStrEditor(auto_add=True)),
                        Item('singletag'),
                        UItem('add'),
                        UItem('remove'),
                        label='tags'),
                    Group(Item('fun'),
                        Item('dringendheid'),
                        Item('belang'),
                        Item('goeiedaad'),
                        Item('plieslies'),
                        label='categories')
                       
                       )
                       
    view_all = View(    Item('number'),
                        Item(name='name'),
                        Item(name='comment'),
                        Item('tags', editor=ListStrEditor(auto_add=True)),
                        Item('singletag'),
                        UItem('add'),
                        UItem('remove'),
                        Item('fun'),
                        Item('dringendheid'),
                        Item('belang'),
                        Item('goeiedaad'),
                        Item('plieslies'),
                        
                       
                       )

    def __init__(self, projectnumber, **kwargs):
        """Create a project with projectnumber and optional kwargs"""
        
        self.number = projectnumber

        for k,v in kwargs.items():
            setattr(self, k, v)
    
    def _add_fired(self):
        self.tags.append(self.singletag)
        
    def _remove_fired(self):
        self.tags.remove(self.singletag)
        
    def has_tag(self, tag):
        return tag in self.tags


class Portfolio(HasTraits):
    """Class to manage and analyse a portfolio of projects"""
    
    projects = OrderedDict()  # int:Project pairs
    selection = OrderedDict() # selection of projects, based on tags
    
    fun = Property(Array, depends_on = "selection")
    def _get_fun(self):
        if self.selection.keys()==[]:
            self.selection = self.projects
        return [p.fun for p in self.selection.values()] 
    
    dringendheid = Range(0,5)
    belang = Range(0,5)
    goeiedaad = Range(0,5)
    plieslies = Range(0,5)
    
    
    
    
    def _get_new_projectnumber(self):
        try:
            return 1+sorted(self.projects.keys())[-1]
        except:
            return 1
               
    def add_project(self):
        """Add a project to the dictionary of projects"""
        projectnumber = self._get_new_projectnumber()
        p = Project(projectnumber=projectnumber)
        p.configure_traits(view='view_all')
        self.projects[projectnumber] = p
        
    def filter_projects(self, incl=[], excl=[]):
        """Filter projects and update self.selection"""
        selection=self.projects
        for id, project in self.projects.items():
            keep = True
            for tag in incl:
                if project.has_tag(tag):
                    pass
                else:
                    keep = False
                    break
            for tag in excl:
                if project.has_tag(tag):
                    keep = False
                    break
                else:
                    pass
            if keep:
                selection[id]=project
                
        self.selection = selection
        
    def __str__(self):
        try:
            return "This portfolio has {} project(s).".format(len(self.projects))
        except TypeError:
            return "This portfolio has no projects."
                
            
                
        
        
    


if __name__ == "__main__":
#   p = PlotterApplication()
#   p.configure_traits()

    #demo = Demo()
    #demo.configure_traits()
    
    p1 = Project(projectnumber=1, name="eerste project", tags=['huis', 'familie', 'persoonlijk'], fun=5, plieslies=3)
    p2 = Project(projectnumber=2, name="2e project", tags=['huis', 'familie', 'spel'], fun=4, plieslies=3)
    #p.configure_traits()
    pf = Portfolio()
    pf.projects=OrderedDict([(1,p1),(2,p2)])