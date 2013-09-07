import numpy as np
import pdb


def sort_array_of_ints(array):
    """
    Return sorted array of integers.
     
    The array has to be composed as follows:
    - 2D, first column is the ID, just to keep reference to the original rows
    - All subsequent columns are the values (higher is better)
    - we only sort using the values columns
    
    Returns an array with the indices of the rows on the front
    """
    
    # first, sort the array.
    # recipe taken from http://stackoverflow.com/questions/2828059/sorting-arrays-in-numpy-by-column
    nb_cols = array.shape[-1]
    view = ','.join(nb_cols*['i8'])
    order_list = ['f'+str(i) for i in range(1,nb_cols)]
    return np.sort(array.view(view), order=order_list, axis=0).view(np.int)


def pareto(sorted_array):
    """
    Return pareto front of a sorted array.
     
    The array has to be composed as follows:
    - 2D, first column is the ID, just to keep reference to the original rows
    - All subsequent columns are the values (higher is better)
    - The array is sorted according to the values, row by row. Lowest values first. 
    
    Returns an array with selection of rows that that are non-dominated by any other row.
    """
    #pdb.set_trace()
    # The last row is the first point on the front
    front = sorted_array[-1,:].reshape(1,sorted_array.shape[-1])
    # Loop through array, from one but last to first row
    for index in sorted(range(sorted_array.shape[0]-1), reverse=True):
        keep = False
        # compare this row with last row in the list of fronts
        keep = np.any(sorted_array[index,1:] > front[-1,1:]) or \
               np.all(sorted_array[index,1:] == front[-1,1:]) # also keep the row if it's identical
        if keep:
            front = np.row_stack((front, sorted_array[index,:]))
    
        
    return front

