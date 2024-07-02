# -*- coding: utf-8 -*-


import io
import os
import sys
import numpy as np
import shutil
from PIL import Image
from matplotlib import pyplot as plt
# from tkinter import Tk
# from tkinter import messagebox
# from tkinter import TclError
from stl import mesh
from mpl_toolkits import mplot3d

path_me = os.path.abspath(os.path.realpath(__file__)).replace(os.sep,'/')
pathd_me = os.path.abspath(os.path.dirname(path_me)).replace(os.sep,'/')
basename_me = os.path.splitext(os.path.basename(path_me))[0]
os.chdir(pathd_me)

#Count Arguments
# if len(sys.argv) != 2:
    # root = Tk()
    # root.withdraw()
    # try:
        # root.after(5000, root.destroy)  # in milliseconds 
        # messagebox.Message(title='Error', message='Specify just one .stl file as argument !', icon='error', master=root).show()
    # except TclError:
        # pass
    # sys.exit()

path_stl = os.path.abspath(sys.argv[1]).replace(os.sep,'/')
pathd_stl = os.path.abspath(os.path.dirname(path_stl)).replace(os.sep,'/')
basename_stl = os.path.splitext(os.path.basename(path_stl))[0]

#Filter by Extention
# if os.path.splitext(path_stl)[1] != '.stl':
    # root = Tk()
    # root.withdraw()
    # try:
        # root.after(5000, root.destroy)  # in milliseconds 
        # messagebox.Message(title='Error', message='Just a .stl file available !', icon='error', master=root).show()
    # except TclError:
        # pass
    # sys.exit()

print('# LOADED: '+ path_stl)

def main():
    #---------------------------------------------------------
    # https://pypi.org/project/numpy-stl/
    mesh_stl = mesh.Mesh.from_file(path_stl)
    
    #Transform
    mesh_stl.x = mesh_stl.x - mesh_stl.min_[0]
    mesh_stl.y = mesh_stl.y - mesh_stl.min_[1]
    mesh_stl.z = mesh_stl.z - mesh_stl.min_[2]
    
    mesh_stl.update_areas()
    mesh_stl.update_max()
    mesh_stl.update_min()
    mesh_stl.update_units()
    
    range_x = mesh_stl.max_[0] - mesh_stl.min_[0]
    range_y = mesh_stl.max_[1] - mesh_stl.min_[1]
    range_z = mesh_stl.max_[2] - mesh_stl.min_[2]
    #---------------------------------------------------------
    fig = plt.figure(figsize=(4.5, 3.5), dpi=300, facecolor=(1.0, 1.0, 1.0, 0.0))  #figsize: inches
    ax = fig.add_subplot(111, projection='3d')
    
    ax.set_xlim(mesh_stl.min_[0] - range_x * 0.005, mesh_stl.max_[0] + range_x * 0.005)
    ax.set_ylim(mesh_stl.min_[1] - range_x * 0.005, mesh_stl.max_[1] + range_x * 0.005)
    ax.set_zlim(mesh_stl.min_[2] - range_x * 0.005, mesh_stl.max_[2] + range_x * 0.005)
    
    ax.set_aspect('equal')
    #---------------------------------------------------------
    # Visuals
    clct = ax.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh_stl.vectors))
    clct.set_linewidth(0.15)
    clct.set_facecolor((1.0, 1.0, 1.0, 1.0))
    clct.set_edgecolor('#9e9d5b')
    
    # Hide panes
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    
    # Hide axises
    ax.xaxis.line.set_color((0.0, 0.0, 0.0, 0.0))
    ax.yaxis.line.set_color((0.0, 0.0, 0.0, 0.0))
    ax.zaxis.line.set_color((0.0, 0.0, 0.0, 0.0))
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    #---------------------------------------------------------
    ax.view_init(elev=90, azim=-90)
    # ax.view_init(elev=30, azim=-120)
    plt.tight_layout()
    
    path_png = pathd_stl + '/' + basename_stl + '.stl.png'
    plt.savefig(path_png, transparent=True, format='png')
    print('# OUTPUT: '+ path_png)
    
    # plt.show()
    #---------------------------------------------------------
    #Crop  https://imagingsolution.net/program/python/pillow/pillow_image_crop/
    im = Image.open(path_png)
    crop_dw = 75
    crop_dh = 75
    im.crop((crop_dw, crop_dh, (im.width -crop_dw), (im.height - crop_dh))).save(path_png)  # (left, upper, right, lower)
    #---------------------------------------------------------

if __name__ == '__main__':
    main()
