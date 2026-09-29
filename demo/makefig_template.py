# -*- coding: utf-8 -*-
"""
Template script for creating figures for papers and presentations using a shared config. 

Requires mypyutils (https://github.com/chris-konrad/mypyutils)

Usage
-----
python makefig_template.py -c config.yaml [--save] [--presentation] [--interactive]
 
Options
-------
    -c, --config    
        Path to the figure configuration file (required). See demo/config.yaml for an example. 
    -s, --save 
        Save output to disk.
    -p, --presentation 
        Use presentation settings from config.yaml instead of paper settings. 
    -i, --interactive 
        Keep figures open for inspection.

@author: Christoph M. Konrad
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pypaperutils.design import config_matplotlib_for_latex, TUDcolors
from mypyutils.io import read_yaml
from pypaperutils.config import parse_config
from pypaperutils.io import savefig, get_default_parser
from pypaperutils.tex import export_as_texcommand

tudcolors=TUDcolors()

def main():

    figkey = 'fig_template'
    
    args = get_default_parser(figkey).parse_args()
    config = read_yaml(args.config)
    config = parse_config(config, figkey, presentation=args.presentation)
    
    config_matplotlib_for_latex(save=args.save,
                                 font_size_small=config['fig_fontsizes'][0], 
                                font_size_normal=config['fig_fontsizes'][1], 
                                output_type=config["fig_ftype"])

    # CREATE FIGURE -----------------------------------------------------------
    # Load data and create figure here. Use config[figkey] to acess style 
    # definitions for this figure. 
    fig = ...
    

    # EXPORT VALUES -----------------------------------------------------------
    # Some values visible in the figure may be convenient as tex-commands 
    # because one may want to talk about them in the body of the paper. 
    export_as_texcommand(key, value, config)

    # -------------------------------------------------------------------------
    if args.save:
        savefig(fig, config, figkey)

    if args.interactive:
        plt.show(block=True)
    else:
        plt.close("all")
  
                                      
if __name__ == "__main__":
    main()