import bpy #gives us access to blender python
import bmesh #gives us more tools to manipulate mesh
import mathutils #gives us access to the kdtree
import os # allows us to import and export files 
import json #allows us to parse and create JSON files
import sys#gives access to wider system functions
import csv #need to implement this cool stuff soon

#Pseudocode needs to be updated. Program has gotten cooler since last revision
#Accept filepath to .JSON file
#Open .JSON file as object
#Accept filepath to .obj file
#import object to blender environment
#select the object
#here we go
#switch to edit mode
#deselect all points
#back to object mode
#impllement a KD tree
#balance the tree
#loop through every object under "features in JSON file"
#create vertex groups with names of features
#read coordinates from JSON file
#reorient coordinates
#place 3D cursor at points specified by JSON data
#using KD tree searching, select vertex closest to 3D vertex
#add selected vertex to the group coresponding with name of feature in JSON data
#deselect point
#move to next feature
#loop through all newly created groups
#select vertex assigned to group
#snap 3 cursor to selected vertex
#print coordinates of selected vertex to show new coordinates of selected group
#deselect vertex group
#take name of landmark as argument
#take "delta values" how far along each axis the point is to be moved
#take proportional transform size as argument
#switch to edit mode
#transform mesh according to arguments taken
#take desired name of exported .obj file
#export file to working directory
#maybe loop back and keep going

def bringOBJ():#import .obj file into scene
    file_loc = input("Please inpute file path to .obj file. Please use backslash / in file path: ")
    #file_loc = 'C:/Users/jpbg2/OneDrive/Documents/NoseProject/Sample3D/Sample3D/female_head_1.obj'
    imported_object = bpy.ops.import_scene.obj(filepath=file_loc)
    #bpy.data.objects[str(obj_object.name)].select_set(True)
    #input_name = input("Please enter the name the object was imported under: ")
    obj_object = bpy.context.selected_objects[0] #sets variable to select object
    bpy.context.view_layer.objects.active = obj_object #selects object
    print('Imported name: ', obj_object.name)

def pointsOfInterest():#Funcion to select all vertex groups
    for i in range(len(face_data["features"])):
        bpy.context.object.vertex_groups.active_index = i
        bpy.ops.object.vertex_group_select()
       
def getJSON(tol):
    obj = bpy.context.active_object #sets a variable that allows for more readable code
    obj_object = bpy.context.selected_objects[0]
    head = obj_object.name
    cur = bpy.context.scene.cursor.location
    o   = bpy.context.object
    #deselect all points before doing anything
    bpy.ops.object.select_all(action = 'SELECT')
    bpy.ops.object.mode_set( mode = 'EDIT' ) #Set mode to Edit
    bpy.ops.mesh.select_all(action = 'DESELECT') #Deselect all points
    bpy.ops.object.mode_set( mode = 'OBJECT' ) #set mode to Object
    #tol = input("Please enter tolerance radius. 0.1 is recommended: ")
    bpy.ops.object.mode_set(mode = 'OBJECT') #mode to Object
    #implementing the kd tree
    mesh = obj_object.data
    size = len(mesh.vertices)
    kd = mathutils.kdtree.KDTree(size)
    for i, v in enumerate(mesh.vertices):
        kd.insert(v.co, i)
    #blanace the tree
    kd.balance()
    print("Read Values:") 
    for feature in face_data["features"]: #loop through every object in "features" in Json file
        new_vertex_group = bpy.context.active_object.vertex_groups.new(name=feature["abbrv"])
        #make vertex groups with proper names
        abbrv = feature["abbrv"]
        negx = feature["xVal"]
        negy = feature["yVal"]
        negz = feature["zVal"]
        x = float(negx)
        y = float(negy)
        z = float(negz)
        print(abbrv, -x, -z, y)
        bpy.context.scene.cursor.location = (-x, -z, y) 
        #order and magnitudes are due to blender's unconventional coordinate system 
        co_find = obj.matrix_world.inverted() @ bpy.context.scene.cursor.location
        #Search Using KD Tree
        co, index, dist = kd.find(co_find)
        kd.find_range(co_find, tol) #Implementing tolerance size
        obj.data.vertices[index].select = True #select chosen vertex
        vertex_group_data = [index]
        new_vertex_group.add(vertex_group_data, 1.0, 'ADD') #add vertex to created group
        obj.data.vertices[index].select = False #Deselect Vertex
        
def newPoints(): #Uses 3d cursor to find new coordinates of points
    bpy.ops.object.mode_set(mode = 'EDIT')
    for index in range(len(face_data["features"])): #loop through all groups
        bpy.context.active_object.vertex_groups.active_index = index
        bpy.ops.object.vertex_group_select()  #select group
        bpy.context.area.type = 'VIEW_3D' #must be in VIEW_3D or will throw a context error
        bpy.ops.view3d.snap_cursor_to_selected() #snaps #D cursor to location of selected vertex
        print(bpy.context.active_object.vertex_groups.active_index, round(bpy.context.scene.cursor.location[0], 2), round(bpy.context.scene.cursor.location[1], 2), round(bpy.context.scene.cursor.location[2], 2)) #prints location of 3D cursor values correct to 2 decimal points
        bpy.ops.object.vertex_group_deselect()
        bpy.context.area.type = 'TEXT_EDITOR'
        
def transformMesh():
    vgroup = input("Please input name of landmark: ")
    dx = input("Please input dx value: ")
    dy = input("Please input dy value: ")
    dz = input("Please input dz value: ")
    prop_size = input("Please input proportional transform size: ")
    #Takes 4 arguments. delta values as floats and prop size as float
#this is the transformation
    bpy.ops.object.mode_set(mode = 'EDIT') #mesh must be in Edit mode for us to edit the mesh
    bpy.ops.object.vertex_group_set_active(group=vgroup) 
    bpy.ops.object.vertex_group_select()
    bpy.ops.transform.translate(value=(float(dx), float(dy), float(dz)), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff='SMOOTH', proportional_size=float(prop_size), use_proportional_connected=False, use_proportional_projected=False)

def cursorReturn():
    #This bring the cursor back to the origin. Serves no necessary pracical purpose.
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.mode_set(mode = 'EDIT') #ensures the object is in edit mode after running script

def newJSON():
    bpy.ops.object.mode_set(mode = 'EDIT')
    for index in range(len(face_data["features"])): #loop through all groups
        bpy.context.active_object.vertex_groups.active_index = index
        bpy.ops.object.vertex_group_select()  #select group
        bpy.context.area.type = 'VIEW_3D' #must be in VIEW_3D or will throw a context error
        bpy.ops.view3d.snap_cursor_to_selected() #snaps #D cursor to location of selected vertex
        face_data["features"]["xVal"] = round(bpy.context.scene.cursor.location[0], 2)
        face_data["features"]["yVal"] = round(bpy.context.scene.cursor.location[1], 2)
        face_data["features"]["zVal"] = round(bpy.context.scene.cursor.location[2], 2)            
        bpy.ops.object.vertex_group_deselect()
        bpy.context.area.type = 'TEXT_EDITOR'
        modelname = face_data["threeDModel"]
        with open(modelname + '.json', 'w') as outfile:
            outfile.write(face_data)

def newerJSON():
    bpy.ops.object.mode_set(mode = 'EDIT')
    index = 0
    for feature in face_data["features"]: #loop through all groups
        bpy.context.active_object.vertex_groups.active_index = index
        bpy.ops.object.vertex_group_select()  #select group
        bpy.context.area.type = 'VIEW_3D' #must be in VIEW_3D or will throw a context error
        bpy.ops.view3d.snap_cursor_to_selected() #snaps #D cursor to location of selected vertex
        feature["xVal"] = -(round(bpy.context.scene.cursor.location[0], 2))
        feature["yVal"] = round(bpy.context.scene.cursor.location[2], 2)
        feature["zVal"] = -(round(bpy.context.scene.cursor.location[1], 2))
        bpy.ops.object.vertex_group_deselect()
        bpy.context.area.type = 'TEXT_EDITOR'
        modelname = face_data["threeDModel"]
        index = index + 1
    blend_file_path = bpy.data.filepath #create variable holding path to file
    directory = os.path.dirname(blend_file_path) #creates another variable holding path to folder file is (removes file from end of path)
    print("building  directory map")
    print(directory)
    print(blend_file_path)
    target_file = os.path.join(directory, input("Enter name you want JSON to be exported as: ")) #appends inputted name  to filepath to specify exported file name and location
    print(target_file)
    full_target_file = target_file + ".JSON" #adds file extension so the computer doesn't get mad
    print(full_target_file)
    with open(full_target_file, 'w') as outfile:
        json.dump(face_data, outfile, indent=4)
    print("Created new JSON file titled: " + full_target_file)

def export():#export the file as .obj
    bpy.ops.object.mode_set(mode = 'OBJECT') #mode to object
    blend_file_path = bpy.data.filepath #create variable holding path to file
    directory = os.path.dirname(blend_file_path) #creates another variable holding path to folder file is (removes file from end of path)
    target_file = os.path.join(directory, input("Enter name you want object to be exported as: ")) #appends inputted name  to filepath to specify exported file name and location
    full_target_file = target_file + ".obj" #adds file extension so the computer doesn't get mad
    bpy.ops.export_scene.obj(filepath=full_target_file) #actually export the file

def deleteOBJ():#prevent context errors that arise from object not being deleted
    if bpy.context.object.mode == 'EDIT': #make sure its in object mode
        bpy.ops.object.mode_set(mode='OBJECT') #change it if its not
    bpy.ops.object.delete() #delete it

def main():
    bringOBJ() 
    obj = bpy.context.active_object #sets a variable that allows for more readable code
    obj_object = bpy.context.selected_objects[0]
    head = obj_object.name
    cur = bpy.context.scene.cursor.location
    o   = bpy.context.object
    getJSON(0.1)
    #Print Statements are for ease of use in Console. Will be removed upon JSON implementation
    print("_______________________________") #makes it easier to read console
    print("Selected Points:")
    newPoints()
    #transformMesh("prn", -2.14156e-15, -16.0378, -9.64472, 30)
    print("_______________________________") #easy to read
    transformMesh()
    print("After Transform:")
    newPoints()
    print("+++++++++++++++++++++++++++++++") #shows end of run
    newerJSON()
    cursorReturn()
    export()
    deleteOBJ()
    
if __name__ == "__main__":
    #set variables for cleaner code
    
    inp = ""
    inp = input("Enter filepath to JSON file. Please use / backslash in file path: ")
    #assert os.path.exists(inp), "I did not find the file at, "+str(inp)
    with open(inp, encoding = 'utf-8') as f: #open JSON file as an object
        face_data = json.load(f) #set variable to that object
    main()