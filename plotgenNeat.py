import matplotlib as mpl
import glob
import os
import matplotlib.pyplot as plt
import h5py as h5

import mpl_toolkits as tk
import numpy as np
import netCDF4 as nc
import h5py as h5
from matplotlib.colors import ListedColormap
import pandas as pd
from mpl_toolkits.basemap import Basemap
import metpy.calc
import matplotlib.animation as animation

dpi = 96

""" This is Sean's plotting function """
def plot_mask_double(namedir, img_array, img_array2, storm_mask, plt_title, 
    my_cmap=None,my_cmap2=None, my_cmap3=None, u_wind=None, v_wind=None, 
    v_max=None, v_min=None,v_max2=None, v_min2=None, line=None, land=True):
    """
    img_array: This is the contour that is being plotted (i.e. TMQ)
    storm_mask: This creates a mask on top of the img_array contour showing the storm labels.  If you do not wish
            to see a predefined mask, you can input np.zeros(img_array.shape) for this field
    plt_title: The title of the plot
    my_cmap: input a custom colormap for the img_array contour.  The default colormap is good though
    u_wind: wind values in the u direction
    v_wind: wind values in the v direction
    """
    # Sets to whiteish colormap
    if my_cmap is None:
        # Choose colormap
        cmap = mpl.cm.viridis
        # Get the colormap colors
        my_cmap = cmap(np.arange(cmap.N))
        alpha = np.linspace(0, 1, cmap.N)
        my_cmap[:,0] = (1-alpha) + alpha * my_cmap[:,0]
        my_cmap[:,1] = (1-alpha) + alpha * my_cmap[:,1]
        my_cmap[:,2] = (1-alpha) + alpha * my_cmap[:,2]

        # Create new colormap
        my_cmap = ListedColormap(my_cmap)

    # l = p['label'] / 100
    p = storm_mask #p['prediction']
    p = np.roll(p,[0,1152//2])
    p1 = (p == 100)
    p2 = (p == 2)

    d = img_array #h['climate']['data'][0,...]
    d = np.roll(d,[0,1152//2])
    
    d2 = img_array2
    d2 = np.roll(d2,[0,1152//2])

    lats = np.linspace(-90,90,768)
    longs = np.linspace(-180,180,1152)

    def do_fig(figsize):
        fig = plt.figure(figsize=figsize, dpi=dpi)
        ax=fig.add_axes([0,0,1,1])
        ax.axis('off')

        my_map = Basemap(projection='cyl', llcrnrlat=min(lats), lon_0=np.median(longs),
                  llcrnrlon=min(longs), urcrnrlat=max(lats), urcrnrlon=max(longs), resolution = 'c',fix_aspect=False)
        xx, yy = np.meshgrid(longs, lats)
        x_map,y_map = my_map(xx,yy)
        my_map.drawcoastlines(color=[0.5,0.5,0.5])

        my_map.contour(x_map,y_map,d,line,cmap=my_cmap, vmax=v_max, vmin=v_min)
        my_map.contourf(x_map,y_map,d2,64,cmap=my_cmap2, vmax=v_max2, vmin=v_min2)
        if u_wind is not None and v_wind is not None:
            wind_speed = np.sqrt(u_wind**2 + v_wind**2)
            my_map.quiver(x_map[::20,::20],y_map[::20,::20], u_wind[::20,::20], v_wind[::20,::20], wind_speed[::20,::20], alpha=0.5, cmap=my_cmap3)

        if (not land):
            my_map.fillcontinents(alpha=0.5)
        mask_ex = plt.gcf()
        mask_ex.savefig(namedir + "/" + plt_title, dpi=dpi, quality=100,pad_inches = 0)
        plt.clf()

    do_fig((1152/dpi,768/dpi))


""" This is Sean's plotting function """
def plot_mask_flat(namedir ,img_array, storm_mask, plt_title, my_cmap=None, 
    my_cmap2 = None, u_wind=None, v_wind=None, 
    v_max=None, v_min=None, land=True):
    """
    img_array: This is the contour that is being plotted (i.e. TMQ)
    storm_mask: This creates a mask on top of the img_array contour showing the storm labels.  If you do not wish
            to see a predefined mask, you can input np.zeros(img_array.shape) for this field
    plt_title: The title of the plot
    my_cmap: input a custom colormap for the img_array contour.  The default colormap is good though
    u_wind: wind values in the u direction
    v_wind: wind values in the v direction
    """
    # Set alpha
    if my_cmap is None:
        # Choose colormap
        cmap = mpl.cm.viridis
        # Get the colormap colors
        my_cmap = cmap(np.arange(cmap.N))
        alpha = np.linspace(0, 1, cmap.N)
        my_cmap[:,0] = (1-alpha) + alpha * my_cmap[:,0]
        my_cmap[:,1] = (1-alpha) + alpha * my_cmap[:,1]
        my_cmap[:,2] = (1-alpha) + alpha * my_cmap[:,2]

        # Create new colormap
        my_cmap = ListedColormap(my_cmap)

    # l = p['label'] / 100
    p = storm_mask #p['prediction']
    p = np.roll(p,[0,1152//2])
    p1 = (p == 100)
    p2 = (p == 2)

    d = img_array #h['climate']['data'][0,...]
    d = np.roll(d,[0,1152//2])

    lats = np.linspace(-90,90,768)
    longs = np.linspace(-180,180,1152)

    def do_fig(figsize):
        fig = plt.figure(figsize=figsize,dpi=dpi)
        ax=fig.add_axes([0,0,1,1])
        ax.axis('off')

        my_map = Basemap(projection='cyl', llcrnrlat=min(lats), lon_0=np.median(longs),
                  llcrnrlon=min(longs), urcrnrlat=max(lats), urcrnrlon=max(longs), resolution = 'c',fix_aspect=False)
        xx, yy = np.meshgrid(longs, lats)
        x_map,y_map = my_map(xx,yy)
        my_map.drawcoastlines(color=[0.5,0.5,0.5])

        my_map.contourf(x_map,y_map,d,64,cmap=my_cmap, vmax=v_max, vmin=v_min)

        if u_wind is not None and v_wind is not None:
            wind_speed = np.sqrt(u_wind**2 + v_wind**2)
            my_map.quiver(x_map[::20,::20],y_map[::20,::20], u_wind[::20,::20], v_wind[::20,::20], wind_speed[::20,::20], alpha=0.5, cmap=my_cmap2)
        
        if (not land):
            my_map.fillcontinents(alpha=0.5)
        mask_ex = plt.gcf()
        mask_ex.savefig( namedir + "/" + plt_title,dpi=dpi,quality=100,pad_inches = 0)
        plt.clf()

    do_fig((1152/dpi,768/dpi))


def plot_mask_triple(namedir, img_array, img_array2, img_array3, storm_mask, plt_title, 
                     my_cmap=None,my_cmap2=None, my_cmap3=None, my_cmap4=None,
                     u_wind=None, v_wind=None, v_max=None, v_min=None,thresh=False,
                     v_max2=None, v_min2=None, v_max3=None, v_min3=None, line=None, line2=None,
                    land = True):
    """
    img_array: This is the contour that is being plotted (i.e. TMQ)
    storm_mask: This creates a mask on top of the img_array contour showing the storm labels.  If you do not wish
            to see a predefined mask, you can input np.zeros(img_array.shape) for this field
    plt_title: The title of the plot
    my_cmap: input a custom colormap for the img_array contour.  The default colormap is good though
    u_wind: wind values in the u direction
    v_wind: wind values in the v direction
    """
    # Set alpha
    if my_cmap2 is None:
        # Choose colormap
        cmap2 = mpl.cm.viridis
        # Get the colormap colors
        my_cmap2 = cmap2(np.arange(cmap2.N))
        alpha2 = np.linspace(0, 1, cmap2.N)
        my_cmap2[:,0] = (1-alpha2) + alpha2 * my_cmap2[:,0]
        my_cmap2[:,1] = (1-alpha2) + alpha2 * my_cmap2[:,1]
        my_cmap2[:,2] = (1-alpha2) + alpha2 * my_cmap2[:,2]

        # Create new colormap
        my_cmap2 = ListedColormap(my_cmap2)

    if my_cmap is None:
        # Choose colormap
        cmap = mpl.cm.viridis
        # Get the colormap colors
        my_cmap = cmap(np.arange(cmap.N))
        alpha = np.linspace(0, 1, cmap.N)
        my_cmap[:,0] = (1-alpha) + alpha * my_cmap[:,0]
        my_cmap[:,1] = (1-alpha) + alpha * my_cmap[:,1]
        my_cmap[:,2] = (1-alpha) + alpha * my_cmap[:,2]

        # Create new colormap
        my_cmap = ListedColormap(my_cmap)

    # l = p['label'] / 100
    p = storm_mask #p['prediction']
    p = np.roll(p,[0,1152//2])
    p1 = (p == 100)
    p2 = (p == 2)

    d = img_array #h['climate']['data'][0,...]
    d = np.roll(d,[0,1152//2])
    
    d2 = img_array2
    d2 = np.roll(d2,[0,1152//2])
    
    d3 = img_array3
    d3 = np.roll(d3,[0,1152//2])

    lats = np.linspace(-90,90,768)
    longs = np.linspace(-180,180,1152)

    def do_fig(figsize):
        fig = plt.figure(figsize=figsize,dpi=dpi)
        ax=fig.add_axes([0,0,1,1])
        ax.axis('off')

        my_map = Basemap(projection='cyl', llcrnrlat=min(lats), lon_0=np.median(longs),
                  llcrnrlon=min(longs), urcrnrlat=max(lats), urcrnrlon=max(longs), resolution = 'c',fix_aspect=False)
        xx, yy = np.meshgrid(longs, lats)
        x_map,y_map = my_map(xx,yy)
        my_map.drawcoastlines(color=[0.5,0.5,0.5])

        my_map.contour(x_map,y_map,d,line,cmap=my_cmap, vmax=v_max, vmin=v_min)
        my_map.contour(x_map,y_map,d3,line2,cmap=my_cmap4, vmax=v_max3, vmin=v_min3)
        my_map.contourf(x_map,y_map,d2,64,cmap=my_cmap2, vmax=v_max2, vmin=v_min2)
        if u_wind is not None and v_wind is not None:
            wind_speed = np.sqrt(u_wind**2 + v_wind**2)
            my_map.quiver(x_map[::20,::20],y_map[::20,::20], u_wind[::20,::20], v_wind[::20,::20], wind_speed[::20,::20], alpha=0.5, cmap=my_cmap3)

        if (not land):
            my_map.fillcontinents(alpha=0.5)
        mask_ex = plt.gcf()
        mask_ex.savefig( namedir + "/" + plt_title,dpi=dpi,quality=100,pad_inches = 0)
        plt.clf()

    do_fig((1152/dpi,768/dpi))

def start_composit_img(source_files_iter):
    count = 0
    for sfile in source_files_iter:
        if count > 1: return
        name = sfile[-23:-2] + 'jpg'
        if sfile in source_files: continue
        count += 1
        print(count)
        filepath = sfile[:]
        print(filepath)
        data_in = h5.File(filepath)
        TMQ = data_in['climate']['data'][:,:,0]
        # PS = data_in['climate']['data'][:,:,6]
        PSL = data_in['climate']['data'][:,:,7]
        U850 = data_in['climate']['data'][:,:,1]
        V850 = data_in['climate']['data'][:,:,2]
        UBOT = data_in['climate']['data'][:,:,3]
        VBOT = data_in['climate']['data'][:,:,4]
        QREFHT = data_in['climate']['data'][:,:,5]
        #print(TMQ.shape)

        """ Plot TMQ from the data file"""

        plot_mask_flat("/global/project/projectdirs/ClimateNet/Images_test/tmq", TMQ, np.zeros(TMQ.shape), name, 
                       'viridis', land=False)


        # Plot TMQ, U850, and V850 from the data file
        plot_mask_flat("/global/project/projectdirs/ClimateNet/Images_test/tmq_wind_850", TMQ, np.zeros(TMQ.shape), 
                       name, 'viridis',my_cmap2='Blues', u_wind=U850, v_wind=V850, land=False)


        # Plot TMQ, UBOT, and VBOT from the data file
        plot_mask_flat("/global/project/projectdirs/ClimateNet/Images_test/tmq_wind_bot", TMQ, np.zeros(TMQ.shape), 
                       name, 'viridis',my_cmap2='Blues', u_wind=UBOT, v_wind=VBOT, land=False)


        #  Calculate and plot the IVT approximation
        IVT_u = U850 * QREFHT
        IVT_v = V850 * QREFHT
        IVT = np.sqrt(IVT_u**2 + IVT_v**2)
        plot_mask_flat("/global/project/projectdirs/ClimateNet/Images_test/ivt", IVT, np.zeros(TMQ.shape), name, 'viridis',v_max=0.42,v_min=0)


        """ Plot Vorticity calculated by U850, and V850 from the data file"""
        # vorticity = abs(np.gradient(V850, axis=1) - np.gradient(U850, axis=0))
        new_vor = metpy.calc.vorticity(U850, V850,
            np.full((768, 1151), 1), np.full((767, 1152), 1))
        new_vor_arr = np.array(abs(new_vor))
        plot_mask_flat("/global/project/projectdirs/ClimateNet/Images_test/vorticity", new_vor_arr, np.zeros(new_vor_arr.shape), 
                      name, 'viridis',v_max=7,v_min=1.3, land=False)


        """ Plot PSL, Vorticity from the data file"""
        plot_mask_double("/global/project/projectdirs/ClimateNet/Images_test/vor_psl", new_vor_arr, PSL, np.zeros(new_vor_arr.shape), name, 
                       my_cmap='Reds',my_cmap2='viridis',v_max2=101500,v_min2=99000,line=8,v_max=7,v_min=1.3, land=False)


        """ Plot PSL, Vorticity, IVT from the data file"""
        plot_mask_triple("/global/project/projectdirs/ClimateNet/Images_test/vor_psl_ivt", new_vor_arr, IVT, PSL, np.zeros(PSL.shape), name, 
                  my_cmap='Reds',my_cmap2='viridis',my_cmap4='cool',line=10,line2=10,
                    v_max=7,v_min=1.3,
                    v_max2=0.42,v_min2=0.00,
                    v_max3=101500,v_min3=99000)


        # plot_mask_double("./global/project/projectdirs/ClimateNet/Images_test/vor_ps_wind", PS, vorticity, np.zeros(vorticity.shape), name, 
        #                my_cmap='Wistia',v_max=129000,v_min=55000,my_cmap2='viridis',my_cmap3 = 'PiYG',line=3,v_max2=7,v_min2=1.3, u_wind=U850, v_wind=V850)

def process_tmq_field(img_array, my_cmap=None, v_max=None, v_min=None, land=True):
    """
    Takes in a list of numpy arrays, returning a gif with each frame corresponding to an array with basemap transformations
    img_array: a list of nparrays, each corresponding to a frame in the resulting animation
    my_cmap: input a custom colormap for the img_array contour.  The default colormap is good though
    """
    # Set alpha
    if my_cmap is None:
        # Choose colormap
        cmap = mpl.cm.viridis
        # Get the colormap colors
        my_cmap = cmap(np.arange(cmap.N))
        alpha = np.linspace(0, 1, cmap.N)
        my_cmap[:,0] = (1-alpha) + alpha * my_cmap[:,0]
        my_cmap[:,1] = (1-alpha) + alpha * my_cmap[:,1]
        my_cmap[:,2] = (1-alpha) + alpha * my_cmap[:,2]

        # Create new colormap
        my_cmap = ListedColormap(my_cmap)


    # defining some hardcoded variables
    lats = np.linspace(-90, 90, 768)
    longs = np.linspace(-180, 180, 1152)
    figsize = (1152 / dpi, 768 / dpi)

    # create the figure and apply basemap transformations
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax=fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    my_map = Basemap(projection='cyl', llcrnrlat=min(lats), lon_0=np.median(longs),
              llcrnrlon=min(longs), urcrnrlat=max(lats), urcrnrlon=max(longs), resolution='c', fix_aspect=False)
    xx, yy = np.meshgrid(longs, lats)
    x_map,y_map = my_map(xx,yy)
    my_map.drawcoastlines(color=[0.5, 0.5, 0.5])

    if land:
        my_map.fillcontinents(alpha=0.5)

    # animate here
    def do_fig_animate(i):
        data_array = np.roll(img_array[i], [0, 1152 // 2])
        my_map.contourf(x_map, y_map, data_array, 64, cmap=my_cmap, vmax=v_max, vmin=v_min)
        print("doing fig animate: " + str(i) + " out of " + str(len(img_array)))
        return my_map

    return animation.FuncAnimation(plt.gcf(), do_fig_animate, frames=len(img_array), interval=100, blit=False)
