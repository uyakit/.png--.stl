# -*- coding: utf-8 -*-

# https://diegomagela.github.io/2023/09/09/become-a-mesh

import io
import os
import sys
import subprocess
import shutil
from PIL import Image

path_me = os.path.abspath(os.path.realpath(__file__)).replace(os.sep,'/')
pathd_me = os.path.abspath(os.path.dirname(path_me)).replace(os.sep,'/')
basename_me = os.path.splitext(os.path.basename(path_me))[0]
os.chdir(pathd_me)

path_png = os.path.abspath(sys.argv[1]).replace(os.sep,'/')
pathd_png = os.path.abspath(os.path.dirname(path_png)).replace(os.sep,'/')
basename_png = os.path.splitext(os.path.basename(path_png))[0]

shutil.copy(basename_png + '.png', basename_me + '.png')
path_png_tmp = os.path.join(pathd_png, basename_me + '.png')

path_png_tmp = path_png_tmp.replace(os.sep,'/')
path_png_f = f'"{path_png_tmp}"'

# Write GEO file as input for Gmsh
header = f'If(PostProcessing.NbViews == 0) \n \
\t Merge {path_png_f}; \n\
\t Plugin(ModifyComponents).Expression0 = "1 + v0^3 * 10"; \n\
\t Plugin(ModifyComponents).Run; \n\
EndIf\n'

# https://gmsh.info/doc/texinfo/gmsh.html#Other-general-commands
body = f"""
//-------------------------------------------------------------------------
General.Antialiasing = 1; // Use multisample antialiasing (will slow down rendering)
General.BackgroundGradient = 0; // Draw background gradient (0: none, 1: vertical, 2: horizontal, 3: radial)
General.BoundingBoxSize = 1210; // Overall bounding box size (read-only)
General.ConfirmOverwrite = 0; // Ask confirmation before overwriting files?
General.Light0X = -0.7; // X position of light source 0
General.Light0Y = -0; // Y position of light source 0
General.Light0Z = 0.55; // Z position of light source 0
General.SmallAxes = 0; // Display the small axes
General.Color.Foreground = {{255,255,255}}; // Foreground color
General.Color.Text = {{101,106,92}};
Geometry.Curves = 0; // Display geometry curves?
Geometry.Points = 0; // Display geometry points?
Mesh.ColorCarousel = 0; // Mesh coloring (0: by element type, 1: by elementary entity, 2: by physical group, 3: by mesh partition)
Mesh.MinQuality = 0.5; // Minimum mesh quality (inverse conditioning number, ICN) after the generation of the current mesh (read-only)
Mesh.VolumeEdges = 0; // Display edges of volume mesh?
Mesh.Color.Triangles = {{158,157,91}}; // Mesh triangle color (if Mesh.ColorCarousel=0)
Mesh.Color.Quadrangles = {{158,157,91}}; // Mesh quadrangle color (if Mesh.ColorCarousel=0)

General.GraphicsFontSizeTitle = 0;
General.GraphicsWidth = 1350;
General.GraphicsHeight = 912;

General.FieldHeight = 350;
General.FieldWidth = 450;

General.SaveOptions = 1;
General.ScaleX = 1.25;
General.ScaleY = 1.25;
General.ScaleZ = 1.25;
General.TranslationX = 0;
General.TranslationY = 17;

Solver.AutoMesh = 2;

Background Mesh View[0];
View[0].ColormapNumber = 5;
View[0].DrawStrings = 0;
View[0].Name = "";
View[0].Light = 0;
View[0].ShowTime = 0;
//-------------------------------------------------------------------------
w = View[0].MaxX;
h = View[0].MaxY;

Point(1)={{0,0,0,w}};
Point(2)={{w,0,0,w}};
Point(3)={{w,h,0,w}};
Point(4)={{0,h,0,w}};
Line(1) = {{1,2}};
Line(2) = {{2,3}};
Line(3) = {{3,4}};
Line(4) = {{4,1}};
Line Loop(5) = {{3,4,1,2}};
Plane Surface(6) = {{5}};

// Mesh options: https://gmsh.info/doc/texinfo/gmsh.html#Mesh-options
DefineConstant[
  algo = {{
    Mesh.Algorithm, AutoCheck 0, GmshOption "Mesh.Algorithm",
    Choices{{
      1="MeshAdapt",
      2="Automatic",
      5="Delaunay",
      6="Frontal-Delaunay",
      7="BAMG",
      8="Frontal-Delaunay for Quads",
      9="Packing of Parallelograms",
      11="Quasi-structured Quad"
    }},
    Name "Meshing parameters/Algorithm"
  }},
  
  sizeFact = {{
    Mesh.CharacteristicLengthFactor, AutoCheck 0,
    GmshOption "Mesh.CharacteristicLengthFactor", Min 0.05, Max 10, Step 0.05,
    Name "Meshing parameters/Element size factor"
  }},
  
  sizeMin = {{
    Mesh.CharacteristicLengthMin, AutoCheck 0,
    GmshOption "Mesh.CharacteristicLengthMin", Min 4, Max (w * h)^(1/2), Step 1,
    Name "Meshing parameters/Minimum element size"
  }},
];

Mesh.RecombineAll = (algo == 8);
//Mesh.Algorithm = 6; // Frontal-Delaunay
Mesh 2;

Draw;
Save "{basename_me}_Cntr.png";

View[0].Visible = 0;
Draw;
Save "{basename_me}_Mesh.png";

Save "{basename_me}.msh";
Save "{basename_me}.stl";
Exit;
"""

def prepare_geo():
  f = open(basename_me + '.geo', 'w')
  f.write(header + body)
  f.close()

# https://www.rccm.co.jp/icem/pukiwiki/index.php?%E3%83%A1%E3%83%83%E3%82%B7%E3%83%A5%E3%81%AE%E5%87%BA%E5%8A%9B%E5%BD%A2%E5%BC%8F%28Gmsh%29
# https://qiita.com/natsuriver/items/98434b86a1d65f1f76a3
def png2stl():
  # subprocess.run(['C:\Program Files\gmsh\gmsh.exe', basename_me + '.geo'])
  subprocess.run(['gmsh.exe', basename_me + '.geo'])

def main():
    prepare_geo()
    png2stl()
    
    # Post processing
    
    shutil.copy(basename_me + '.msh', basename_png + '.msh')
    os.remove(basename_me + '.msh')
    
    shutil.copy(basename_me + '.stl', basename_png + '.stl')
    os.remove(basename_me + '.stl')
    # -----------------------------------------------
    # https://imagingsolution.net/program/python/pillow/pillow_image_crop/
    # im = Image.open(basename_me + '_Cntr.png')
    # im.crop((0, 0, (im.width -1), im.height)).save(basename_me + '_Cntr.png')  # (left, upper, right, lower)
    
    # shutil.copy(basename_me + '_Cntr.png', basename_png + '_Cntr.png')
    # -----------------------------------------------
    # im = Image.open(basename_me + '_Mesh.png')
    # im.crop((0, 0, (im.width -1), im.height)).save(basename_me + '_Mesh.png')  # (left, upper, right, lower)
    
    # shutil.copy(basename_me + '_Mesh.png', basename_png + '_Mesh.png')
    # -----------------------------------------------

if __name__ == '__main__':
    main()
