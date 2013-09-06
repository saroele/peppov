# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 21:42:12 2013

@author: roel
"""


from traits.api import HasTraits,Int,Bool,Float,Str,Property,Range,Array,Dict,List,Button
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
    
    fun = Range(0,5)
    dringendheid = Range(0,5)
    belang = Range(0,5)
    goeiedaad = Range(0,5)
    plieslies = Range(0,5)
    
                           
    view_all = View(    Item('projectnumber'),
                        Item(name='name'),
                        Item(name='comment'),
                        Item('tags', editor=CSVListEditor()),
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
    
    def has_tag(self, tag):
        return tag in self.tags
        



class Portfolio(HasTraits):
    """Class to manage and analyse a portfolio of projects"""
    
    
    all_properties = ['fun','belang','dringendheid','goeiedaad','plieslies'] #list of all properties (values between 0 and 5)    
    current_project = Int(default_value=1)   
    projects = List(Project)  # 
    selection = Property(List(Project), depends_on = ['projects', 'tags_to_include', 'tags_to_exclude']) # selection of projects, based on tags
    repr_projects = Property(List, depends_on = 'projects')    
    repr_selection = Property(List, depends_on = 'selection')
    
    #dictionary of property values, property:list of values
    property_values = Property(Dict, depends_on = "selection")  
    
    tags_to_include = List(Str)
    tags_to_exclude = List(Str)
    button_add = Button("Add project")
    button_edit = Button("Edit project")
       
    
    # Analysis
    to_plot_x = Str()
    to_plot_y = Str()
    x = Property(Array, depends_on=['to_plot_x', 'property_values'])
    y = Property(Array, depends_on=['to_plot_y', 'property_values'])
    # sliders for the analysis    
    fun = Range(0,5,1)
    dringendheid = Range(0,5,1)
    belang = Range(0,5,1)
    goeiedaad = Range(0,5,1)
    plieslies = Range(0,5,1) 
    
    priority_projects = Property(List, depends_on = all_properties + ['selection', 'priority_quadr'])
    priority_quadr = Bool
    
    
    def _get_property_values(self):
        property_values = {}
        for prop in self.all_properties:
            property_values[prop] = [getattr(project, prop) for project in self.selection]
        return property_values            
        
    def _get_repr_projects(self):
        return [str(p.projectnumber) + ' - ' + p.name for p in self.projects]
        
    def _get_selection(self):
        self.filter_projects(incl=self.tags_to_include, excl=self.tags_to_exclude)
        return self._selection
    
    def _get_repr_selection(self):
        return [str(p.projectnumber) + ' - ' + p.name for p in self.selection]
        
    def _get_x(self):
        return np.array(self.property_values.get(self.to_plot_x, np.zeros(len(self.selection))))
        
    def _get_y(self):
        return np.array(self.property_values.get(self.to_plot_y, np.zeros(len(self.selection))))
    
    view = View(
                Group(
                    Item('repr_projects', label='Projects',editor=ListStrEditor(editable=False)),
                    UItem('button_add'),
                    Item('current_project', label='Project to edit'),
                    UItem('button_edit'),                
                    Item('tags_to_include', editor=CSVListEditor()),
                    Item('tags_to_exclude', editor=CSVListEditor()),
                    Item('repr_selection', label='Selection of projects', editor=ListStrEditor(editable=False)),
                    label='Projects'),
                Group(
                    Item('to_plot_x'),
                    Item('to_plot_y'),
                    ChacoPlotItem("x","y", type='scatter',
                                    y_bounds=(0.,6.),y_auto=False,
                                    x_bounds=(0.,6.),x_auto=False,
                                    resizable=True, show_label=False,
                                    x_label=to_plot_x.value, y_label=to_plot_y.value, title=""),
                    label='Analysis'),
                Group(
                    Item('fun'),
                    Item('dringendheid'),
                    Item('belang'),
                    Item('goeiedaad'),
                    Item('plieslies'),
                    Item('priority_quadr', label = 'Kwadratisch algoritme'),
                    Item('priority_projects', label='Priority projects',editor=ListStrEditor(editable=False)),
                    label='Priorities'),
                resizable=True
                )
    
    
    def _get_priority_projects(self):
        """Sort the projects based on their properties and the sensitivities
        for each priority"""
        
        #pdb.set_trace()        
        priority = np.zeros(len(self.selection))
        for prop in self.all_properties:
            #multiply the array of values with the weight, add to previous result
#            print 'first operand = ', getattr(self, prop)             
#            print 'type of first operand', type(getattr(self, prop))  
#            print 'second operand = ', self.property_values[prop]
#            print 'type of second operand', type(self.property_values[prop])
            if self.priority_quadr:
                priority += getattr(self, prop) * np.array(self.property_values[prop])**2
            else:
                priority += getattr(self, prop) * np.array(self.property_values[prop])
            
        sorted_projects = sorted(zip(priority, self.selection), reverse=True)
        return [str(project.projectnumber) + ' - ' + project.name + \
            ' - (priority = {})'.format(p) for (p, project) in sorted_projects]


    
    def _get_new_projectnumber(self):
        try:
            return 1 + self.projects[-1].projectnumber
        except:
            return 1
               
    def add_project_GUI(self):
        """Add a project to the list of projects and open GUI"""
        projectnumber = self._get_new_projectnumber()
        p = Project(projectnumber=projectnumber)
        p.configure_traits(view='view_all')
        self.projects.append(p)
        
    def add_project(self, **kwargs):
        """Add a project to the dictionary of projects with **kwargs"""
        projectnumber = self._get_new_projectnumber()
        p = Project(projectnumber=projectnumber, **kwargs)
        
        self.projects.append(p)

        
    def edit_project(self, projectnumber):
        """Edit a project"""
        
        for project in self.projects:
            if project.projectnumber == projectnumber:
                project.configure_traits(view='view_all')
                break

    
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
                
        self._selection = selection
        
    def __str__(self):
        try:
            return "This portfolio has {} project(s).".format(len(self.projects))
        except TypeError:
            return "This portfolio has no projects."
                
            
    def _button_add_fired(self):
        self.add_project_GUI()
        
    def _button_edit_fired(self):
        self.edit_project(self.current_project)
          
        
    def read_csv(self, filename):
        """Read projects from a csv file"""
        
        import pandas as pd
        df = pd.read_csv(filename, sep='\t')
        for id, project in df.iterrows():
            kwargs = project.to_dict()
            try:
                kwargs['tags'] = kwargs['tags'].split(',')
            except:
                kwargs['tags'] = []
            if type(kwargs['comment']) is not str:
                kwargs['comment'] = ''
            self.add_project(**kwargs)
            
    def save_csv(self, filename):
        
        f = open(filename, 'w')
        # write the header
        columns = ['name','fun','belang','dringendheid','goeiedaad','plieslies','tags','comment']
        f.write('\t'.join(columns))
        f.write('\n')
        
        # write the lines, one per project
        for project in self.projects:
            line = '\t'.join([str(getattr(project, c)) for c in \
                ['name','fun','belang','dringendheid','goeiedaad','plieslies']])
            line += '\t'
            line += ','.join(getattr(project, 'tags'))
            line += '\t' + project.comment
            line += '\n'
            f.write(line)
        f.close()
    

if __name__ == "__main__":

    
    pf = Portfolio()
    pf.read_csv('MyProjectPortfolio.peppov')
    pf.configure_traits()
    