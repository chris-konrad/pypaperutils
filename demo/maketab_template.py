# -*- coding: utf-8 -*-
"""
Template script for creating LaTeX tables for papers and presentations using a shared config. 

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

import os
import numpy as np
import pandas as pd

from mypyutils.io import read_yaml
from pypaperutils.config import parse_config
from pypaperutils.io import get_default_parser
from pypaperutils.tex import export_as_texcommand, writetex, tex_maketabular, tex_list2tabrow, export_as_texcommand

def main():

    tabkey = 'tab_template'
    
    args = get_default_parser(tabkey).parse_args()
    config = read_yaml(args.config)
    config = parse_config(config, tabkey, presentation=args.presentation)

    # CREATE TABLE -----------------------------------------------------------
    # load some data, then turn in into a table as outlined below. 

    # header
    header = ["some", "column", "names"]
    alignment = "c" * len(header)
    header = tex_list2tabrow(header)

    # body
    body = []
    for i,  in enumerate():
        row = [f"row{i}", f"row{i}", f"row{i}"]
        body.append(row)

        if args.save:
            export_as_texcommand()

    tablines = tex_maketabular(header, alignment, body)
    # --------------------------------------------------------------------------
    if args.save:
        writetex(tablines, config, tabkey)
  
                                      
if __name__ == "__main__":
    main()