# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:50:26 2023

pypaperutils.design

colors and other design elements

@author: Christoph M. Konrad
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap, ListedColormap


def config_matplotlib_for_latex(
    save=True,
    font_family="serif",
    font_size_normal=10,
    font_size_small=8,
    output_type=".pgf",
):
    """Presets of matplotlib for beautiul latex plots"""

    if output_type[0] != ".":
        output_type = "." + output_type

    if save and output_type == ".pgf":
        matplotlib.use("pgf")
    else:
        matplotlib.use("Qt5Agg")

    matplotlib.rcParams.update(
        {
            "text.usetex": True,
            "font.family": "serif",
            "axes.labelsize": font_size_small,
            "axes.titlesize": font_size_normal,
            "font.size": font_size_normal,
            "legend.fontsize": font_size_normal,
            "xtick.labelsize": font_size_small,
            "ytick.labelsize": font_size_small,
        }
    )


def figure_for_latex(height, width=18.47987):
    """Creates a figure with a given hight and width in cm
    and constrained layout.

    Parameters
    ----------
    height : float,
        Figure height in cm.
    width : float, optional
        Figure width in cm. Default is 18.47987 for a typical A4 textwidth.

    Returns
    -------
    figure
        Matplotlib figure handle.
    """
    cm = 1 / 2.54
    return plt.figure(layout="constrained", figsize=(width * cm, height * cm))


class TUDcolors:
    """Colors of the TU Delft corporate image as of 20-09-2023.

    https://www.tudelft.nl/huisstijl/bouwstenen/kleur

    """

    PALETTE = (
        (0, 166, 214),  # Cyaan
        (12, 35, 64),  # Donkerblauw
        (0, 184, 200),  # Turkoois
        (0, 118, 194),  # Blauw
        (111, 29, 119),  # Paars
        (239, 96, 163),  # Roze
        (165, 0, 52),  # Framboos
        (224, 60, 49),  # Rood
        (237, 104, 66),  # Oranje
        (255, 184, 28),  # Geel
        (108, 194, 74),  # Lichtgroen
        (0, 155, 119),
    )  # Donkergroen

    COLORNAMES = (
        "cyaan",
        "donkerblauw",
        "turkoois",
        "blauw",
        "paars",
        "roze",
        "framboos",
        "rood",
        "oranje",
        "geel",
        "lichtgroen",
        "donkergroen",
    )

    def __init__(self):
        self.colors = dict(zip(self.COLORNAMES, self.PALETTE))
        self.colornames = self.COLORNAMES
        self.palette = self.PALETTE

    def get(self, colors, dtype="float"):
        """Get a color by name or index.

        0 - "cyaan"
        1 - "donkerblauw"
        2 - "turkoois"
        3 - "blauw"
        4 - "paars"
        5 - "roze",
        6 - "framboos"
        7 - "rood"
        8 - "oranje"
        9 - "geel"
        10 - "lichtgroen"
        11 - "donkergroen"


        Parameters
        ----------
        color : int, str, or list thereof
            Identifiers of the color. May be a string with the color name or
            the color id.
        dtype : str, default = "float"
            Return colors as floats in [0,1] ("float") or integers in [0,255]
            ("int")

        Returns
        -------
        RGB color triplets.

        """
        if not dtype in ("float", "int"):
            raise ValueError(
                f"The parameter dtype has to be either 'float' \
                             or 'int', instead it was '{dtype}'."
            )

        if not isinstance(colors, list) and not isinstance(colors, tuple):
            colors = (colors,)
            islist = False
        else:
            islist = True

        rgbtriplets = []

        if isinstance(colors[0], str):
            for name in colors:
                val = np.array(self.colors[name])
                if dtype == "float":
                    val = val.astype(float) / 255
                rgbtriplets.append(val)

        elif isinstance(colors[0], int):
            for i in colors:
                val = np.array(self.palette[i])
                if dtype == "float":
                    val = val.astype(float) / 255
                rgbtriplets.append(val)

        if not islist:
            rgbtriplets = rgbtriplets[0]

        return rgbtriplets

    def colormap(self, name="line-plot-colors"):
        """
        Return different color maps made of colors from the TU Delft color
        scheme. 
        
        **Available colormaps:**
        
        - Continous maps
            - "blue-to-yellow": A smooth gradient from dark blue over green to 
                                yellow.
            - "blue-to-red": A smooth gradient from blue over pink to red. 
            - "red-blue-red": A smooth gradient from blue over pink to red and back
            - "colorwheel" : A colorful gradient for cirular color maps
            - color_name : A smooth gradient from white to the color indicated by the name. Must be any of COLORNAMES
        - Discrete maps
            - "line-plot-colors": A selection of 11 colors for line plots, 
                                  roughly following the matplotlib default
                                  color scheme. 

        Parameters
        ----------
        name : str, optional
            Name of the colormap. Must be from the above list. 
            The default is "line-plot-colors".

        Returns
        -------
        cmp : matplotlib.colors.Colormap
            The requested colormap.
        """
        
        colormap_names = [
            "blue-to-yellow", "line-plot-colors", "blue-to-red", "red-blue-red", "colorwheel"
        ] +  list(self.COLORNAMES)

        assert (
            name in colormap_names
        ), f'The parameter "name" has to be any of\
             {colormap_names}, instead it was "{name}".'

        if name == "blue-to-yellow":
            cmp = LinearSegmentedColormap.from_list(
                "blue-to-yellow",
                (
                    self.get("donkerblauw"),
                    self.get("blauw"),
                    self.get("donkergroen"),
                    self.get("lichtgroen"),
                    self.get("geel"),
                ),
            )

        if name == "blue-to-red":
            cmp = LinearSegmentedColormap.from_list(
                "blue-to-red",
                (
                    self.get("blauw"),
                    self.get("roze"),
                    self.get("rood"),
                ),
            )

        if name == "red-blue-red":
            cmp = LinearSegmentedColormap.from_list(
                "red-blue-red",
                (
                    self.get("rood"),
                    self.get("roze"),
                    self.get("blauw"),
                    self.get("donkerblauw"),
                    self.get("blauw"),
                    self.get("roze"),
                    self.get("rood"),
                ),
            )
        if name == "colorwheel":
            cmp = LinearSegmentedColormap.from_list(
                "colorwheel",
                (
                    self.get("blauw"),
                    self.get("roze"),
                    self.get("rood"),
                    self.get("oranje"),
                    self.get("geel"),
                    self.get("lichtgroen"),
                    self.get("cyaan"),
                    self.get("blauw"),
                ),
            )

        if name in self.COLORNAMES:
            cmp = LinearSegmentedColormap.from_list(
                name, 
                (
                    [1,1,1],
                    self.get(name),
                    [0,0,0]
                ),
            )
        
        if name == "line-plot-colors":
            cmp = ListedColormap(
                (
                    self.get("blauw"),
                    self.get("oranje"),
                    self.get("donkergroen"),
                    self.get("rood"),
                    self.get("paars"),
                    self.get("donkerblauw"),
                    self.get("roze"),
                    self.get("turkoois"),
                    self.get("lichtgroen"),
                    self.get("cyaan")
                ), name=name)
        
        return cmp
