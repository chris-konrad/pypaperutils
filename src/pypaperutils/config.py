# -*- coding: utf-8 -*-
"""
pypaperutils.config

Parse a config yaml for making paper and presentation figures and tables.

@author: Christoph M. Konrad
"""


import os
from pypaperutils.design import TUDcolors

def merge_config_dicts(dict1, dict2):
    """Merge two config dicts."""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_config_dicts(result[key], value)
            else:
                result[key] = value
        else:
            result[key] = value
    return result


def int_to_word(n):
    if n>14:
        raise NotImplementedError("Numbers larger 14 not supported")
    return ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen'][n]


def parse_config(config, figurekey, presentation=False):
    """ Create a config dictionary fusing the "global_config" and the
    "figure_config" selected by figurekey. Recursively merges subdictionaries. 
    
    If conflicts exist, values from figure_config overwrite the global_config.
    """

    #unpack settings for paper/presentation
    def unpack_doctype(cfg):
        doctypes = ['presentation', 'paper']
        result = {}
        
        for k, v in cfg.items():
            # unpack presentation/paper subconfig and transfer
            if k in doctypes:
                if (presentation and k==doctypes[0]) or (not presentation and k==doctypes[1]):
                    for kk, vv in cfg[k].items():
                        result[kk] = vv
            # transfer 
            else:
                result[k] = v
        return result

    config_global = unpack_doctype(config['global_config'])

    if figurekey in config['figure_config']:
        config_figure = unpack_doctype(config['figure_config'][figurekey])
    else:
        config_figure = {}

    #parse output directory
    subdir_out_floattype = None
    for floattype in config_global['subdir_out_floattype']:
        if floattype in figurekey:
            subdir_out_floattype =  config_global['subdir_out_floattype'][floattype]
            break

    config_figure['subdir_out'] = os.path.join(config_global['subdir_out_doctype'], subdir_out_floattype)
    config_figure['dir_out'] = os.path.join(config_global['dir_out_base'], config_figure['subdir_out'])

    #parse figure size
    new_keys = {}
    for key in config_figure:
        if 'fig_size_relative' in key:
            fig_size_inches = [config_global['textwidth_inches']*config_figure[key][0],
                               config_global['textwidth_inches']*config_figure[key][1]]
            new_keys[key.replace("relative", "inches")] = fig_size_inches
    config_figure = config_figure | new_keys

    if not 'fig_size_inches' in config_figure:
        config_figure['fig_size_inches'] = config_global['fig_size_inches']

    #merge
    config_out = merge_config_dicts(config_global, config_figure)

    #colors
    config_out = parse_colors(config_out)

    return config_out


def modify_config_values(config, func):
    """ Walk through all (nested) values of the config and modify them using func.

    Parameters
    ----------
    config : dict (of dicts)
        Config dictionary to be modified
    func : function
        Modification function with the signature updated_value = func(key, value)

    """
    for k, v in config.items():
        if isinstance(v, dict):
            modify_config_values(v, func)
        else:
            config[k] = func(k, v)


def parse_colors(config):
    """ Convert TUDcolors colorname strings and colordef strings to color tuples 
    """

    def parse_tudcolornames(k, v):
        if 'color' in k:
            if v in TUDcolors.COLORNAMES:
                return TUDcolors().get(v)
        return v
    
    def parse_colordefnames(k, v):
        if ('color' in k) and ('colordef' in v):
            return config[v]
        return v
    
    def parse_tudcolormaps(k, v):
        if ('cmap' in k) and ('colordef' in v):
            return config[v]
        return v

    modify_config_values(config, parse_tudcolormaps)
    modify_config_values(config, parse_tudcolornames)
    modify_config_values(config, parse_colordefnames)

    return config