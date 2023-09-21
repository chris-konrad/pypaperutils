# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 13:13:23 2023

pypaperutils.io

Export and import of figures and other elements

@author: Christoph M. Schmidt
"""

import os
import matplotlib

def export_to_pgf(fig, filename, dirname=None, save=True): 
    """Export a figure to pgf format so that latex may render text by itself.
    

    Parameters
    ----------
    fig : figure
        Figure to be exportet.
    filename : str
        Name of the generated pfg file without ".pgf".
    dirname : str, optional
        Directory where the figure should be saved. If empty, the figure will 
        be saved in the directory of the source file. 
    save : boolean, optional
        Disables saving. The default is True.

    Returns
    -------
    None.

    """
    
    assert matplotlib.get_backend() == 'pgf', f'Set the matplotlib backend \
    to "pgf" before plotting in order to export to .pgf. The current backend \
    is "{matplotlib.get_backend()}".'
    
    if save:
        
        if dirname is not None:
            path = os.path.join(filename, dirname) + '.pgf'
            if not os.path.exists(dirname):
                os.makedirs()  
        else:
            path = filename + '.pgf'
        fig.savefig(path)  
