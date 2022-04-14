import bpy #gives us access to blender python
import bmesh #gives us more tools to manipulate mesh
import mathutils #gives us access to the kdtree
import os # allows us to import and export files 
import json #allows us to parse and create JSON files
import sys#gives access to wider system functions
import csv #need to implement this cool stuff soon

def bringOBJ():#import .obj file into scene
    #file_loc = input("Please inpute file path to .obj file. Please use / in file path: ")
    file_loc = origOBJpath
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
       
def getJSON():
    obj = bpy.context.active_object #sets a variable that allows for more readable code
    obj_object = bpy.context.selected_objects[0]
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
        kd.find_range(co_find, 0.1) #Implementing tolerance size
        obj.data.vertices[index].select = True #select chosen vertex
        vertex_group_data = [index]
        new_vertex_group.add(vertex_group_data, 1.0, 'ADD') #add vertex to created group
        obj.data.vertices[index].select = False #Deselect Vertex
        
def newPoints(): #Uses 3d cursor to find new coordinates of points
    bpy.ops.object.mode_set(mode = 'EDIT')
    for index in range(len(face_data["features"])): #loop through all groups
        bpy.context.active_object.vertex_groups.active_index = index
        bpy.ops.object.vertex_group_select()  #select group
        #bpy.context.area.type = 'VIEW_3D' #must be in VIEW_3D or will throw a context error
        bpy.ops.view3d.snap_cursor_to_selected() #snaps #D cursor to location of selected vertex
        print(bpy.context.active_object.vertex_groups.active_index, round(bpy.context.scene.cursor.location[0], 2), round(bpy.context.scene.cursor.location[1], 2), round(bpy.context.scene.cursor.location[2], 2)) #prints location of 3D cursor values correct to 2 decimal points
        bpy.ops.object.vertex_group_deselect()
        bpy.context.area.type = 'TEXT_EDITOR'

def newerPoints():
    bpy.ops.object.mode_set(mode = 'EDIT')
    bm = bmesh.new()
    ob = bpy.context.active_object
    bm = bmesh.from_edit_mesh(ob.data)
    for index in range(len(face_data["features"])): #loop through all groups
        bpy.context.active_object.vertex_groups.active_index = index
        bpy.ops.object.vertex_group_select()  #select group
        #bpy.context.area.type = 'VIEW_3D' #must be in VIEW_3D or will throw a context error
        #bpy.ops.view3d.snap_cursor_to_selected() #snaps #D cursor to location of selected vertex
        for v in bm.verts:
            if v.select:
                print(tuple(v.co))
        #print(bpy.context.active_object.vertex_groups.active_index, round(bpy.context.scene.cursor.location[0], 2), round(bpy.context.scene.cursor.location[1], 2), round(bpy.context.scene.cursor.location[2], 2)) #prints location of 3D cursor values correct to 2 decimal points
        bpy.ops.object.vertex_group_deselect()
        #bpy.context.area.type = 'TEXT_EDITOR'


def transformMesh():
    falloff = input_data["FallOffType"]
    if falloff == "":
        falloff = "SMOOTH"
    for modification in input_data["modifications"]:
        #vgroup = input("Please input name of landmark: ")
        vgroup = modification["feature-abbrv"]
        #dx = input("Please input dx value: ")
        dx = modification["deltaX"]
        #dy = input("Please input dy value: ")
        dy = modification["deltaY"]
        #dz = input("Please input dz value: ")
        dz = modification["deltaZ"]
        #prop_size = input("Please input proportional transform size: ")
        prop_size = modification["InfluenceRadius"]
        #falloff = input("Please input falloff type. Your options are 'SMOOTH', 'SPHERE', and 'INVERSE SQUARE': ")
        #Takes 5 arguments. delta values as floats and prop size as float and fallof as string
        #this is the transformation
        bpy.ops.object.mode_set(mode = 'EDIT') #mesh must be in Edit mode for us to edit the mesh
        bpy.ops.object.vertex_group_set_active(group=vgroup) 
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(float(dx), float(dy), float(dz)), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff=falloff, proportional_size=float(prop_size), use_proportional_connected=False, use_proportional_projected=False)

def cursorReturn():
    #This bring the cursor back to the origin. Serves no necessary pracical purpose.
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.mode_set(mode = 'EDIT') #ensures the object is in edit mode after running script

def newJSON():
    bpy.ops.object.mode_set(mode = 'EDIT')
    for index in range(len(face_data["features"])): #loop through all groups
        bpy.context.active_object.vertex_groups.active_index = index
        bpy.ops.object.vertex_group_select()  #select group
        #bpy.context.area.type = 'VIEW_3D' #must be in VIEW_3D or will throw a context error
        bpy.ops.view3d.snap_cursor_to_selected() #snaps 3D cursor to location of selected vertex
        face_data["features"]["xVal"] = round(bpy.context.scene.cursor.location[0], 2)
        face_data["features"]["yVal"] = round(bpy.context.scene.cursor.location[1], 2)
        face_data["features"]["zVal"] = round(bpy.context.scene.cursor.location[2], 2)            
        bpy.ops.object.vertex_group_deselect()
        #bpy.context.area.type = 'TEXT_EDITOR'
        modelname = face_data["threeDModel"]
        with open(modelname + '.json', 'w') as outfile:
            outfile.write(face_data)

def newerJSON():
    bm = bmesh.new()
    ob = bpy.context.active_object
    bm = bmesh.from_edit_mesh(ob.data)
    bpy.ops.object.mode_set(mode = 'EDIT')
    index = 0
    for feature in face_data["features"]: #loop through all groups
        bpy.context.active_object.vertex_groups.active_index = index
        bpy.ops.object.vertex_group_select()  #select group
        #bpy.context.area.type = 'VIEW_3D' #must be in VIEW_3D or will throw a context error
        #bpy.ops.view3d.snap_cursor_to_selected() #snaps #D cursor to location of selected vertex
        for v in bm.verts:
            if v.select:
                tup = tuple(v.co)
        #feature["xVal"] = -(round(bpy.context.scene.cursor.location[0], 2))
        feature["xVal"] = -(round(tup[0], 2))
        #feature["yVal"] = round(bpy.context.scene.cursor.location[2], 2)
        feature["yVal"] = (round(tup[1], 2))
        #feature["zVal"] = -(round(bpy.context.scene.cursor.location[1], 2))
        feature["zVal"] = (round(tup[2], 2))
        bpy.ops.object.vertex_group_deselect()
        #bpy.context.area.type = 'TEXT_EDITOR'
        modelname = face_data["threeDModel"]
        index = index + 1
    #blend_file_path = bpy.data.filepath #create variable holding path to file
    #directory = os.path.dirname(blend_file_path) #creates another variable holding path to folder file is (removes file from end of path)
    print("building  directory map")
    print(directory)
    #print(blend_file_path)
    #target_file = os.path.join(directory, input("Enter name you want JSON to be exported as: ")) #appends inputted name  to filepath to specify exported file name and location
    target_file = os.path.join(directory, targetJSON)
    print(target_file)
    #full_target_file = target_file + ".JSON" #adds file extension so the computer doesn't get mad
    print(target_file)
    with open(target_file, 'w') as outfile:
        json.dump(face_data, outfile, indent=4)
    print("Created new JSON file titled: " + target_file)

def export():#export the file as .obj
    bpy.ops.object.mode_set(mode = 'OBJECT') #mode to object
    #blend_file_path = bpy.data.filepath #create variable holding path to file
    #directory = os.path.dirname(blend_file_path) #creates another variable holding path to folder file is (removes file from end of path)
    #target_file = os.path.join(directory, input("Enter name you want object to be exported as: ")) #appends inputted name  to filepath to specify exported file name and location
    target_file = os.path.join(directory, targetOBJ)
    print(target_file)
    full_target_file = target_file + ".obj" #adds file extension so the computer doesn't get mad
    bpy.ops.export_scene.obj(filepath=target_file) #actually export the file

def deleteOBJ():#prevent context errors that arise from object not being deleted
    if bpy.context.object.mode == 'EDIT': #make sure its in object mode
        bpy.ops.object.mode_set(mode='OBJECT') #change it if its not
    bpy.ops.object.delete() #delete it

def main():
    bringOBJ() 
    getJSON()
    newerPoints()
    transformMesh()
    newerPoints()
    newerJSON()
    cursorReturn()
    export()
    deleteOBJ()
    
if __name__ == "__main__":
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    myinp = input("Please enter the path to the JSON file. Please use forward slash / your input: ")
    with open(myinp, encoding = 'utf-8') as f: #open JSON file as an object
            main_data = json.load(f) #set variable to that object
    print("Files will be stored in this directory")
    directory = os.path.dirname(myinp)
    print(directory)
    #Pull out original json file, buid path to it and open it as face_data
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