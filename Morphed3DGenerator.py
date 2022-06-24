import bpy #gives us access to blender python
import bmesh #gives us more tools to manipulate mesh
import mathutils #gives us access to the kdtree
import os # allows us to import and export files 
import json #allows us to parse and create JSON files

def bringOBJ():#import .obj file into scene
    file_loc = origOBJpath
    imported_object = bpy.ops.import_scene.obj(filepath=file_loc) 
    #The blender API, when importing an object into the scene, must store that object in a variable.
    #The imported_object variable will not be accessed but is initialized to permit the import.
    obj_object = bpy.context.selected_objects[0] #sets variable to select object
    bpy.context.view_layer.objects.active = obj_object #makes the selected object active.
    #There are 3 states an object can be in in Blender: inactive, active, and selected.
    #The active and selected states typically coincide with one another but are not necessarily the same
    print('Imported name: ', obj_object.name)

def join(): #In case the obj file contained multiple objects, join them all into one object
    #Deselect all
    bpy.ops.object.select_all(action='DESELECT')
    #Mesh objects
    MSH_OBJS = [m for m in bpy.context.scene.objects if m.type == 'MESH']
    for OBJS in MSH_OBJS:
        #Select all mesh objects
        OBJS.select_set(state=True)
        #Makes one active
        bpy.context.view_layer.objects.active = OBJS
    #Joins objects
    bpy.ops.object.join()
       
def getJSON(): #read file data from JSON file and create vertex groups corresponding to landmarks
    obj = bpy.context.active_object #sets a variable that allows for more readable code
    obj_object = bpy.context.selected_objects[0]
    bpy.ops.object.select_all(action = 'SELECT')
    bpy.ops.object.mode_set( mode = 'EDIT' ) #Set mode to Edit
    bpy.ops.mesh.select_all(action = 'DESELECT') #Deselect all points
    bpy.ops.object.mode_set( mode = 'OBJECT' ) #set mode to Object
    bpy.ops.object.mode_set(mode = 'OBJECT') #mode to Object
    #implementing the kd tree
    mesh = obj_object.data
    size = len(mesh.vertices)
    kd = mathutils.kdtree.KDTree(size)
    #In order to create the landmark groups we will be using a KD tree.
    #Landmark coordinates are read from the object's data JSON file.
    #The 3D cursor is placed at that those coordinates.
    #We then use the KD tree to search the scene for the closest vertex to the 3D cursor.
    #That vertex is designated as that landmark by adding it to a vertex group that can be referenced later.
    #Since the vertex may not be exactly where the landmark specified, there may be a slight shift in the location.
    #This is necessary as we are manipulating the model through the vertices.
    for i, v in enumerate(mesh.vertices):
        kd.insert(v.co, i)
    #blanace the tree
    kd.balance()
    for feature in face_data["features"]: #loop through every object in "Features" in Json file
        new_vertex_group = bpy.context.active_object.vertex_groups.new(name=feature["abbrv"])
        #make vertex groups that represent the landmarks
        abbrv = feature["abbrv"]
        negx = feature["xVal"]
        negy = feature["yVal"]
        negz = feature["zVal"]
        x = float(negx)
        y = float(negy)
        z = float(negz)
        bpy.context.scene.cursor.location = (-x, -z, y) 
        #Here is where we place the 3D cursor according to the coordinates given.
        #Note the unconventional coordinates.
        #This is because Blender uses a different coordinate system than most other applications.
        #This means that we must mathematically rotate our coordinate system when interfacing between the two.
        co_find = obj.matrix_world.inverted() @ bpy.context.scene.cursor.location
        #Search Using KD Tree
        co, index, dist = kd.find(co_find)
        kd.find_range(co_find, 0.1) #Implementing tolerance size
        obj.data.vertices[index].select = True #select chosen vertex
        vertex_group_data = [index] #select the vertex group we are going to add to.
        new_vertex_group.add(vertex_group_data, 1.0, 'ADD') #add vertex to created group
        obj.data.vertices[index].select = False #Deselect Vertex
        
def scale(vgroup, dx, dy, dz, prop_size): #uses a multiplier that scales the distace of a point from the origin.
    falloff = input_data["FallOffType"] #read the falloff type specified in the instructions
    if falloff == "": #if no falloff is given default to smooth
        falloff = "SMOOTH"
    bpy.ops.object.mode_set(mode = 'EDIT') #set to edit mode
    bpy.ops.object.vertex_group_set_active(group=vgroup) #set vertex group to active
    bpy.ops.object.vertex_group_select()
    #this function performs a scale. It calculayted the distance of a point from the origin and applies a multiplier to that distance.
    #This can be restricted along certain axis or axes.
    bpy.ops.transform.resize(value=(dx, dy, dz), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=True, proportional_edit_falloff=falloff, proportional_size=prop_size, use_proportional_connected=True, use_proportional_projected=False)
    bpy.ops.object.vertex_group_deselect()

def translate(vgroup, dx, dy, dz, prop_size): #moves the vertex in 3D space by adding values to its positional coordinates
    falloff = input_data["FallOffType"]#read the falloff type specified in the instructions
    if falloff == "": #if no falloff is given default to smooth
        falloff = "SMOOTH"
    #bpy.ops.object.mode_set(mode = 'EDIT') #set to edit mode
    bpy.ops.object.vertex_group_set_active(group=vgroup) #set vertex group to active
    #bpy.ops.object.vertex_group_select() 
    #this function performs a translation on a point. The point is moved in 3D space based on adding the given delta values to its coordinates.
    bpy.ops.transform.translate(value=(float(dx), float(dy), float(dz)), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff=falloff, proportional_size=float(prop_size), use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.object.vertex_group_deselect()

def transformMesh(): #reads transformation instructions from the JSON instruction file and manipulates the mesh
    for modification in input_data["Modifications"]:
        dx = modification["Delta-Magnitude-X"]
        dy = modification["Delta-Magnitude-Y"]
        dz = modification["Delta-Magnitude-Z"]
        prop_size = modification["InfluenceRadius"]
        bpy.ops.object.mode_set(mode = 'EDIT')
        vgroup = modification["Feature-abbrv"]
        bpy.ops.object.vertex_group_set_active(group=vgroup) 
        bpy.ops.object.vertex_group_select()
        #calls the appropirate function based on which modification was specified.
        if modification["TransformationType"] == "Scale":
            scale(vgroup, float(dx), float(dy), float(dz), float(prop_size))
        elif modification["TransformationType"] == "Translation":
            translate(vgroup, float(dx), float(dy), float(dz), float(prop_size))
        else:
            print("TRANSFORMATION FAILED")

def cursorReturn(): #returns the cursor to origin
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.mode_set(mode = 'EDIT') #ensures the object is in edit mode after running script

def newerJSON(): #create new JSON file data for output file model
    bm = bmesh.new()
    ob = bpy.context.active_object
    bm = bmesh.from_edit_mesh(ob.data) #using the bmesh module to get vertex location data
    bpy.ops.object.mode_set(mode = 'EDIT')
    index = 0
    for feature in face_data["features"]: #loop through all groups
        bpy.context.active_object.vertex_groups.active_index = index
        bpy.ops.object.vertex_group_select()  #select group
        for v in bm.verts:
            if v.select:
                tup = tuple(v.co)
        #for every vertex group, select the vertex and store its coordinates to the tup array
        feature["xVal"] = -(round(tup[0], 2))
        feature["yVal"] = (round(tup[1], 2))
        feature["zVal"] = (round(tup[2], 2))
        #overwrite the coordinates in the new JSON file with the coordinates of the landmarks as they are after transformation.
        # ensuring to mathematically rotate the orientation as we are once again interfacing outside of blender. 
        bpy.ops.object.vertex_group_deselect()
        modelname = face_data["threeDModel"]
        index = index + 1
    face_data["measurements"].clear()
    target_file = os.path.join(directory, targetJSON)
    with open(target_file, 'w') as outfile:
        json.dump(face_data, outfile, indent=4)
        #create new json file with updated data
    print("Created new JSON file titled: " + target_file)

def mtlPath(input): #This function ensures that the file path contained in the mtl file is a relative path
    MYFILE = input[:-3] + "mtl" #we took input as the obj file so we are just changing the extention here
    print("MTL file to be adjusted: " + MYFILE)
    with open(MYFILE, "r", encoding="utf-8") as f:
        mtl = f.readlines()
        last_line = mtl[-1]
    path = last_line.split()[-1] #this just takes the last "word" of the line which should be the file path
    filename = path.split("/")[-1] #extract the filename by splitting on / and taking the last element
    path = filename
    splitlines = last_line.split()
    while len(splitlines) > 2:
        splitlines.pop(1)
    splitlines[1] = filename
    splitlines.insert(1, ' ')
    attempt = [''.join(splitlines)]
    string = attempt[0]
    #for line in mtl:
    #    pass
    #line = string
    print(mtl)
    mtl[-1] = string
    # read the file into a list of lines
    with open(MYFILE, 'r') as f:
        lines = f.readlines()
    # now edit the last line of the list of lines
    lines[-1] = string
    # now write the modified list back out to the file0
    #open(MYFILE, 'w').writelines(lines)
    with open(MYFILE, 'w') as f:
        f.writelines(lines)

def export():#export the transformed model as a .obj file
    bpy.ops.object.mode_set(mode = 'OBJECT') #mode to object
    target_file = os.path.join(directory, targetOBJ)
    print(target_file)
    bpy.ops.export_scene.obj(filepath=target_file) #actually export the file
    mtlPath(target_file)

def deleteOBJ():#prevent context errors that arise from object not being deleted
    if bpy.context.object.mode == 'EDIT': #make sure its in object mode
        bpy.ops.object.mode_set(mode='OBJECT') #change it if its not
    bpy.ops.object.delete() #delete model

def main():
    bringOBJ()
    join() 
    getJSON()
    transformMesh()
    cursorReturn()
    newerJSON()
    export()
    deleteOBJ()
    
if __name__ == "__main__":
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    myinp = input("Please enter the path to the JSON file: ")
    myinp = myinp.replace('\\', '/') #this allows for slashes to be corrected in a pasted file path
    myinp = myinp.replace('"', '') #removes quotations from pasted file path
    with open(myinp, encoding = 'utf-8') as f: #open JSON file as an object
            main_data = json.load(f) #set variable to that object
    #The file data is stored in a JSON file which is an object notation.
    #Using python's json library, we are reading that file and making a copy of that object in memory
    #We are then storing that object as a python dictionary and assigning it to a variable.
    print("Files will be stored in this directory")
    directory = os.path.dirname(myinp)
    print(directory)
    #For every file specified in the ModificationFiles array, assign the variables to be the data specified in those files and run main again.
    for file in main_data["ModificationFiles"]:
        input_data = file
        origJSON = input_data["OriginalJSONFile"]
        origJSONpath = os.path.join(directory, origJSON)
        with open(origJSONpath, encoding = 'utf-8') as f: #open JSON file as an object
            face_data = json.load(f) #set variable to that object
        origOBJ = input_data["OriginalOBJFile"]
        origOBJpath = os.path.join(directory, origOBJ)
        modelname = input_data["threeDModel"]
        targetOBJ = input_data["TargetOBJFile"]
        targetOBJpath = os.path.join(script_dir, targetOBJ)
        targetJSON = input_data["TargetJSONFile"]
        targetJSONpath = os.path.join(script_dir, targetJSON)
        main()