Pygame Framework
-
This is a game framework for pygame. Currently, it's feature list is very limited (a few useful functions and a basic tilemap system), but it is under active development.

Feature List
-
- Tilemap system
  - Divides the world into chunks
  - Stores tiles as strings (the names of the tiles)
- Camera
  - Projects world coordinates to pixel coordinates
  - Scaling & Translation
  - Project & Unproject coordinates, distances, and pygame Rects
  - Graph coordinates - 0,0 center, +y goes up and +self goes right
- Basic image loading system 
  - Load image from path
  - Load directory of images
  - Load images from directory & all subdirectories
