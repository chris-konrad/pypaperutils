# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 13:13:23 2023

pypaperutils.io

Export and import of figures and other elements

@author: Christoph M. Konrad
"""

import os
import matplotlib
import datetime
from pathlib import Path
from argparse import ArgumentParser

def get_default_parser(figkey):
    """A default parser for scripts that make figures/tables with the parameters
        config : str
            Path to the config.yaml
        save : bool
            If true, save output.
        presentation : bool
            If true, use presentation settings (instead of paper settings)
        interactive : bool
            If true, block execution at the end of scripts to inspect figures. 
    """
    parser = ArgumentParser(prog = f"Make the float {figkey}.")
    parser.add_argument("-c", "--config", required = True, type = str, help="Filepath to the figure config file 'fig_config.yaml'")
    parser.add_argument("-s", "--save", action='store_true', help="Save the generated figure to disk. Set the output directory in the config file.")
    parser.add_argument("-p", "--presentation", action="store_true", help="Create figures for presentation using the corresponding definitions in the config.")
    parser.add_argument("-i", "--interactive", action="store_true", help="Block execution at the end of the script to inspect figure.")
    
    return parser

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
    if save:    
        assert matplotlib.get_backend() == 'pgf', f'Set the matplotlib \
        backend to "pgf" before plotting in order to export to .pgf. The \
        current backend is "{matplotlib.get_backend()}".'
        
        if dirname is not None:
            path = os.path.join(dirname,filename) + '.pgf'
            if not os.path.exists(dirname):
                os.makedirs()  
        else:
            path = filename + '.pgf'
        fig.savefig(path)  


def savefig(fig, config, figure_name, figsize=None, metadata={}, verbose=True):
    """Save a matplotlib figure.
    
    Parameters
    ----------

    fig : Figure
        The figure to save.
    config : dict
        A config-dictionary. Requires the following fields:
            fig_ftype : The file type to save as. Typically .png
            dir_out : The directory to save at.
            fig_dpi : Dots Per Inch
            fig_size_inches : The figure size in inches. 
            file_metadata : Default metadata for each output file. 
                Automatically gets timestamp and scriptname that saves the figure. 
    figsize : list
        The figure size (size_x, size_y) in inches. 
    metadata : dict
        Additional metadate for this file. 
    verbose : bool
        Verbose output
    """
    if figsize is None:
        figsize = config['fig_size_inches']    

    filepath = os.path.join(config['dir_out'], f"{figure_name}{config['fig_ftype']}")
    file_exists = os.path.isfile(filepath)

    fig.set_size_inches(figsize[0], figsize[1])
    fig.savefig(filepath, dpi=config['fig_dpi'], metadata=make_filemetadata(config['file_metadata'] | metadata))

    if verbose:
        if file_exists:
            print(f"Overwrote existing '{filepath}'.")
        else:
            print(f"Wrote '{filepath}'.")


def make_filemetadata(metadata):
    """Create a fileheader dictionary with the fields 'Creation Time', and 'Created By'."""
    metadata_ = {"Creation Time": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                 "Created By": Path(sys.argv[0]).name} 
    metadata_ = metadata_ | metadata
    return metadata_


def make_fileheader(filename, metadata={}, comment="%"):
    """Make a fileheader string in comments given a metadata dictionary. Uses 
    'comment' as symbol to mark the comment (default is '%' for .tex files)"""
    header = [f"{comment} {filename}\n"]
    header += [f"{comment} "+"-"*len(filename)+"\n"]
    for key, val in make_filemetadata(metadata).items():
        header.append(f"{comment} {key.capitalize()}:   {val}\n")
    return header
