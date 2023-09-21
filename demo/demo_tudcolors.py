# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 16:47:06 2023

@author: Christoph M. Schmidt
"""

from pypaperutils.design import TUDcolors
import matplotlib.pyplot as plt

tudcols = TUDcolors()


fig = plt.figure()
plt.plot([0,10], [1, 2], color=tudcols.get(0), label="cyaan")
plt.plot([0,10], [2, 3], color=tudcols.get(1), label="donkerblauw")
plt.plot([0,10], [3, 4], color=tudcols.get(2), label="turkoois")
plt.plot([0,10], [4, 5], color=tudcols.get(3), label="blau")
plt.plot([0,10], [5, 6], color=tudcols.get(4), label="paars")
plt.plot([0,10], [6, 7], color=tudcols.get(5), label="roze")
plt.plot([0,10], [7, 8], color=tudcols.get(6), label="framboos")
plt.plot([0,10], [8, 9], color=tudcols.get(7), label="rood")
plt.plot([0,10], [9, 10], color=tudcols.get(8), label="oranje")
plt.plot([0,10], [10, 11], color=tudcols.get(9), label="geel")
plt.plot([0,10], [11, 12], color=tudcols.get(10), label="lichtgroen")
plt.plot([0,10], [12, 13], color=tudcols.get(11), label="donkergroen")

plt.title("Colors of the TU Delft corporate design.\n (https://www.tudelft.nl/huisstijl/bouwstenen/kleur)")
plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
plt.subplots_adjust(right=0.7)

plt.savefig("example_plot.png")


