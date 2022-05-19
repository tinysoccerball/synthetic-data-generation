# synthetic-data-generation

## Runnning Instructions

once you have blender installed on your system, you do not have to directly interact with it as we are running it in the background.


Open the command line and paste the following command:
```
"C:\Users\path\to\blender\blender.lnk" "C:\Users\path\to\canvas.blend" --background --python "C:\Users\path\to\multifiles.py" 
```
Where the prepared blender file is a blender file that has been saved and had the default items deleted. To prepare this, simply open blender, delete the default cube, light source and camera (and anything else present) and save the .blend file. This will serve as our blank canvas.

Run the command and paste the path to your created json file. Remember to use / and remove any quotations.

Note:
Due to the number of outputs and size of the individual outputsthat could possibly be created, you may have to cancel the execution at some point with CTRL+C. If you do this will a file is being exported, it can lead to an incomplete file. Such a file can be disregarded and discarded.
