# -*- coding: utf-8 -*-

# https://diegomagela.github.io/2023/09/09/become-a-mesh

import io
import os
import sys
import subprocess
import shutil


path_me = os.path.abspath(os.path.realpath(__file__))
pathd_me = os.path.abspath(os.path.dirname(path_me))
basename_me = os.path.splitext(os.path.basename(path_me))[0]
os.chdir(pathd_me)

path_png = os.path.abspath(sys.argv[1])
pathd_png = os.path.abspath(os.path.dirname(path_png))
basename_png = os.path.splitext(os.path.basename(path_png))[0]

shutil.copy(basename_png + '.png', basename_me + '.png')
path_png_tmp = os.path.join(pathd_png, basename_me + '.png')

path_png_f = f'"{path_png_tmp}"'

# Write GEO file as input for Gmsh
header = f'If(PostProcessing.NbViews == 0) \n \
\t Merge {path_png_f}; \n\
\t Plugin(ModifyComponents).Expression0 = "1 + v0^3 * 10"; \n\
\t Plugin(ModifyComponents).Run; \n\
EndIf\n'

# https://gmsh.info/doc/texinfo/gmsh.html#Other-general-commands
body = f"""
Background Mesh View[0];
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
    GmshOption "Mesh.CharacteristicLengthMin", Min w/200, Max w, Step 0.05,
    Name "Meshing parameters/Minimum element size"
  }},
  
  save = {{
    StrCat("View.ShowScale=0;Print '", CurrentDirectory, "{basename_me}.png';"),
    AutoCheck 0, Macro "GmshParseString",
    Name "Save PNG"
  }}
];

Mesh.ColorCarousel = 0;
Mesh.Color.Triangles = Black;
Mesh.Color.Quadrangles = Black;
Mesh.RecombineAll = (algo == 1);
Solver.AutoMesh = 2;
Mesh 2;
Save "{basename_me}.msh";
Save "{basename_me}.stl";
Save "{basename_me}@pic2stl.png";
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

# Run
prepare_geo()
png2stl()

# Post processing
os.remove(basename_me + '.png')

shutil.copy(basename_me + '.msh', basename_png + '.msh')
os.remove(basename_me + '.msh')

shutil.copy(basename_me + '.stl', basename_png + '.stl')
os.remove(basename_me + '.stl')

shutil.copy(basename_me + '@pic2stl.png', basename_png + '@pic2stl.png')
os.remove(basename_me + '@pic2stl.png')

