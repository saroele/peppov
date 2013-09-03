# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 21:42:12 2013

@author: roel
"""


from traits.api import HasTraits,Int,Float,Str,Property,Range,Array,Dict,List,Button
from traitsui.api import View,Item,Label,ListStrEditor,UItem,Group,ListEditor,CSVListEditor
from traitsui.menu import OKButton, CancelButton,RevertButton
from chaco.chaco_plot_editor import ChacoPlotItem
from numpy import array,poly1d,arange,linspace
from collections import OrderedDict
import pdb
import numpy as np



class Project(HasTraits):
    """Class for a single project"""
    
    projectnumber = Int
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
                        Item('projectnumber'),
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
                       
    view_all = View(    Item('projectnumber'),
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
        
        self.projectnumber = projectnumber

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
    
    all_tags = [] #list of possible tags for the Projects
    all_properties = [] #list of all properties (values between 0 and 5)    
    current_project = Int(default_value=1)   
    projects = List(Project)  # 
    selection = List(Project) # selection of projects, based on tags
    repr_projects = Property(List, depends_on = 'projects')    
    repr_selection = Property(List, depends_on = 'selection')
    
    to_plot_x = Str()
    to_plot_y = Str()
    x = Property(Array, depends_on=['to_plot_x', 'property_values'])
    y = Property(Array, depends_on=['to_plot_y', 'property_values'])
    
    #dictionary of property values, property:list of values
    property_values = Property(Dict, depends_on = "selection")  
    
    tags_to_include = List(Str)
    tags_to_exclude = List(Str)
    button_add = Button("Add project")
    button_edit = Button("Edit project")
    button_filter = Button("Filter projects")    
    
    def _get_property_values(self):
        property_values = {}
        for prop in self.all_properties:
            property_values[prop] = [getattr(project, prop) for project in self.selection]
        return property_values            
        
    def _get_repr_projects(self):
        return [str(p.projectnumber) + ' - ' + p.name for p in self.projects]
        
    def _get_repr_selection(self):
        return [str(p.projectnumber) + ' - ' + p.name for p in self.selection]
        
    def _get_x(self):
        return np.ndarray(self.property_values.get(self.to_plot_x, np.zeros(len(self.selection))))
        
    def _get_y(self):
        return np.ndarray(self.property_values.get(self.to_plot_y, np.zeros(len(self.selection))))
    
    view = View(
                Item('repr_projects', label='Projects',editor=ListStrEditor(editable=False)),
                UItem('button_add'),
                Item('current_project', label='Project to edit'),
                UItem('button_edit'),                
                Item('tags_to_include', editor=CSVListEditor()),
                Item('tags_to_exclude', editor=CSVListEditor()),
                UItem('button_filter'),
                Item('repr_selection', label='Selection of projects', editor=ListStrEditor(editable=False)),
                ChacoPlotItem("x","y", type='scatter',
                                y_bounds=(0.,6.),y_auto=False,
                                x_bounds=(0.,6.),x_auto=False,
                                resizable=True, show_label=False,
                                x_label=to_plot_x.value, y_label=to_plot_y.value, title=""),
                resizable=True
                )
    
    
    def _get_new_projectnumber(self):
        return 1 + self.projects[-1].projectnumber
        
               
    def add_project(self):
        """Add a project to the dictionary of projects"""
        projectnumber = self._get_new_projectnumber()
        p = Project(projectnumber=projectnumber)
        p.configure_traits(view='view_all')
        self.projects.append(p)
        
    def edit_project(self, projectnumber):
        """Edit a project"""
        
        for project in self.projects:
            if project.projectnumber == projectnumber:
                project.configure_traits(view='view_all')
                break
        self.filter_projects(incl=['tagthatdoesnotexist'])
        self.filter_projects(incl=self.tags_to_include, excl=self.tags_to_exclude) 
        
        
    def filter_projects(self, incl=[], excl=[]):
        """Filter projects and update self.selection"""
        
        selection=[]
        for project in self.projects:
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
                selection.append(project)
                
        self.selection = selection
        
    def __str__(self):
        try:
            return "This portfolio has {} project(s).".format(len(self.projects))
        except TypeError:
            return "This portfolio has no projects."
                
            
    def _button_add_fired(self):
        self.add_project()
        
    def _button_edit_fired(self):
        self.edit_project(self.current_project)
        #self._get_belang()
        #self._get_fun()        

    def _button_filter_fired(self):
        self.filter_projects(incl=self.tags_to_include, excl=self.tags_to_exclude)            
        
        
    


if __name__ == "__main__":
#   p = PlotterApplication()
#   p.configure_traits()

    #demo = Demo()
    #demo.configure_traits()
    
    p1 = Project(projectnumber=1, name="eerste project", tags=['huis', 'familie', 'persoonlijk'], fun=5, belang=4, plieslies=3)
    p2 = Project(projectnumber=2, name="2e project", tags=['huis', 'familie', 'spel'], fun=4, belang=4, plieslies=3)
    #p.configure_traits()
    pf = Portfolio()
    pf.all_tags = ['huis', 'familie', 'persoonlijk', 'spel']
    pf.all_properties = ['fun', 'belang', 'plieslies']
    pf.projects=[p1,p2]