set "openscad=C:\Program Files\OpenSCAD (Nightly)\openscad.exe"

"%openscad%" ^
    --view=edges ^
    --colorscheme="Nocturnal Gem" ^
    --camera=0,0,0,60,0,40,100 ^
    --viewall ^
    --imgsize 3840,2160 ^
    -o "wireframe.png" ^
    wireframe.scad
