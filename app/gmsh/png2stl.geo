If(PostProcessing.NbViews == 0) 
 	 Merge "C:\Users\uyasp\Desktop\Node.js\Express.js\png2stl.js\app\gmsh\png2stl.png"; 
	 Plugin(ModifyComponents).Expression0 = "1 + v0^3 * 10"; 
	 Plugin(ModifyComponents).Run; 
EndIf

//-------------------------------------------------------------------------
General.Antialiasing = 1; // Use multisample antialiasing (will slow down rendering)
General.BackgroundGradient = 0; // Draw background gradient (0: none, 1: vertical, 2: horizontal, 3: radial)
General.BoundingBoxSize = 1210; // Overall bounding box size (read-only)
General.ConfirmOverwrite = 0; // Ask confirmation before overwriting files?
General.Light0X = -0.7; // X position of light source 0
General.Light0Y = -0; // Y position of light source 0
General.Light0Z = 0.55; // Z position of light source 0
General.SmallAxes = 0; // Display the small axes
General.Color.Foreground = {255,255,255}; // Foreground color
General.Color.Text = {101,106,92};
Geometry.Curves = 0; // Display geometry curves?
Geometry.Points = 0; // Display geometry points?
Mesh.ColorCarousel = 0; // Mesh coloring (0: by element type, 1: by elementary entity, 2: by physical group, 3: by mesh partition)
Mesh.MinQuality = 0.5; // Minimum mesh quality (inverse conditioning number, ICN) after the generation of the current mesh (read-only)
Mesh.VolumeEdges = 0; // Display edges of volume mesh?
Mesh.Color.Triangles = {158,157,91}; // Mesh triangle color (if Mesh.ColorCarousel=0)
Mesh.Color.Quadrangles = {158,157,91}; // Mesh quadrangle color (if Mesh.ColorCarousel=0)

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

Point(1)={0,0,0,w};
Point(2)={w,0,0,w};
Point(3)={w,h,0,w};
Point(4)={0,h,0,w};
Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};
Line Loop(5) = {3,4,1,2};
Plane Surface(6) = {5};

// Mesh options: https://gmsh.info/doc/texinfo/gmsh.html#Mesh-options
DefineConstant[
  algo = {
    Mesh.Algorithm, AutoCheck 0, GmshOption "Mesh.Algorithm",
    Choices{
      1="MeshAdapt",
      2="Automatic",
      5="Delaunay",
      6="Frontal-Delaunay",
      7="BAMG",
      8="Frontal-Delaunay for Quads",
      9="Packing of Parallelograms",
      11="Quasi-structured Quad"
    },
    Name "Meshing parameters/Algorithm"
  },
  
  sizeFact = {
    Mesh.CharacteristicLengthFactor, AutoCheck 0,
    GmshOption "Mesh.CharacteristicLengthFactor", Min 0.05, Max 10, Step 0.05,
    Name "Meshing parameters/Element size factor"
  },
  
  sizeMin = {
    Mesh.CharacteristicLengthMin, AutoCheck 0,
    GmshOption "Mesh.CharacteristicLengthMin", Min 4, Max (w * h)^(1/2), Step 1,
    Name "Meshing parameters/Minimum element size"
  },
];

Mesh.RecombineAll = (algo == 8);
//Mesh.Algorithm = 6; // Frontal-Delaunay
Mesh 2;

Save "png2stl_Cntr.png";

View[0].Visible = 0;
Save "png2stl_Mesh.png";

Save "png2stl.msh";
Save "png2stl.stl";
Exit;
