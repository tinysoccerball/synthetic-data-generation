# synthetic-data-generation

## Runnning Instructions

Once you have blender installed on your system, you do not have to directly interact with it as we are running it in the background.

### Windows Instructions

Open the command line and paste the following command:
```
"C:\Users\path\to\blender\blender.lnk" "C:\Users\path\to\canvas.blend" --background --python "C:\Users\path\to\multifiles.py" 
```
Where the prepared blender file is a blender file that has been saved and had the default items deleted. To prepare this, simply open blender, delete the default cube, light source and camera (and anything else present) and save the .blend file. This will serve as our blank canvas.

The program will prompt you to enter the name of the configuration json file as follows: "Please enter the path to the JSON file:" Then enter the name of the json file that has the modifications desired. You can use the 'CreateMorphingConfigurations.html' file.  

### Mac Instructions

Go to the directory where you keep the code, canvas.blend file, multifiles.py file and your 3D models. Then run the following from the command line using the Terminal app on Mac: 
```
/Applications/Blender.app/Contents/MacOS/Blender canvas.blend --background --python Morphed3DGenerator.py
```

The program will prompt you to enter the name of the configuration json file as follows: "Please enter the path to the JSON file:" Then enter the name of the json file that has the modifications desired. You can use the 'CreateMorphingConfigurations.html' file.  

Note:
Due to the number of outputs and size of the individual outputs that could possibly be created, you may have to cancel the execution at some point with CTRL+C. If you do this will a file is being exported, it can lead to an incomplete file. Such a file can be disregarded and discarded.
