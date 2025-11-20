# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 11:22:30 2023

pypaperutils.measure

simple measurements and tools to draw these measurements into figures

@author: Christoph M. Konrad
"""

import numpy as np

def distance_to_line(p0, p1, p2):
    '''Calculate the distance betweeen p0 and the line drawn by p1 and p2

    Equations from: 
    "Distance from point to a line". wikipedia.org,
    https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
    accessed 21.09.2023
    
    Parameters
    ----------
    p0 : array
        Point p0.
    p1 : array
        Point p1.
    p2 : array
        Point p2.

    Returns
    -------
    float
        Distance to line
    array
        Point on the line with the smallest distance
    '''

    a = p1[1]-p2[1]
    b = p2[0]-p1[0]
    c = p1[0]*p2[1]-p1[1]*p2[0]
    
    d = np.abs(a*p0[0]+b*p0[1]+c)/np.sqrt(a**2+b**2)

    pc = ((b*( b*p0[0]-a*p0[1])-a*c)/(a**2+b**2),
          (a*(-b*p0[0]+a*p0[1])-b*c)/(a**2+b**2))
    
    #special cases: horizontal and vertical lines. 
    if a == 0:
        d = np.abs(p1[1]-p0[1])
        pc = (p0[0], p1[1])
    if b == 0:
        d = np.abs(p1[0]-p0[0])
        pc = (p1[0], p0[1])
    
    return d, pc

def draw_distance_to_line(ax, p0, p1, p2, offset=0, width=0.1, drawPoints=False,
                          linewidth=1, color='black'):
    '''Calculate the distance betweeen p0 and the line drawn by p1 and p2 and
    draw that masurement into axes. 
 
    Parameters
    ----------
    ax : array
         Point p0.
    p0 : array
         Point p0.
    p1 : array
         Point p1.
    p2 : array
         Point p2.
    offset : float, default = 0
             Offset of the measurement bar from the closest point on the line.
    width : float, default = 0.1 
            Width of the measurement bar delimiters.
    drawPoints : bool, default = False
                 Draw the points. 

    Returns
    -------
    float
        Distance to line
    array
        Point on the line with the smallest distance
    
    '''

    phi = np.arctan2(p2[1]-p1[1], p2[0]-p1[0])
    d, pc = distance_to_line(p0,p1,p2)
    
    a = np.sign(offset)
    if a ==0:
        a = 1
    
    ax.plot((pc[0]+offset*np.cos(phi), p0[0]+offset*np.cos(phi)), 
            (pc[1]+offset*np.sin(phi), p0[1]+offset*np.sin(phi)),
            color=color, linewidth=1)
    
    ax.plot((pc[0]+(-a*width+offset)*np.cos(phi), pc[0]+(a*width+offset)*np.cos(phi)), 
            (pc[1]+(-a*width+offset)*np.sin(phi), pc[1]+(a*width+offset)*np.sin(phi)),
            color=color, linewidth=1)

    ax.plot((p0[0]+(-a*width+offset)*np.cos(phi), p0[0]+(a*width+offset)*np.cos(phi)), 
            (p0[1]+(-a*width+offset)*np.sin(phi), p0[1]+(a*width+offset)*np.sin(phi)),
            color=color, linewidth=1)
    
    ax.plot((p0[0], p0[0]+(offset)*np.cos(phi)), 
            (p0[1], p0[1]+(offset)*np.sin(phi)),
            color=color, linewidth=.5, linestyle='--')
    
    
    if drawPoints:
        ax.scatter((p0[0],p1[0],p2[0],pc[0]),(p0[1],p1[1],p2[1],pc[1]))
    
    return d, pc 