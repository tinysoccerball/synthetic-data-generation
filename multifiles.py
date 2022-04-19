import bpy #gives us access to blender python
import bmesh #gives us more tools to manipulate mesh
import mathutils #gives us access to the kdtree
import os # allows us to import and export files 
import json #allows us to parse and create JSON files

def bringOBJ():#import .obj file into scene
    file_loc = origOBJpath
    imported_object = bpy.ops.import_scene.obj(filepath=file_loc)
    obj_object = bpy.context.selected_objects[0] #sets variable to select object
    bpy.context.view_layer.objects.active = obj_object #selects object
    print('Imported name: ', obj_object.name)
       
def getJSON():
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
    for i, v in enumerate(mesh.vertices):
        kd.insert(v.co, i)
    #blanace the tree
    kd.balance()
    for feature in face_data["Features"]: #loop through every object in "Features" in Json file
        new_vertex_group = bpy.context.active_object.vertex_groups.new(name=feature["abbrv"])
        #make vertex groups with proper names
        abbrv = feature["abbrv"]
        negx = feature["xVal"]
        negy = feature["yVal"]
        negz = feature["zVal"]
        x = float(negx)
        y = float(negy)
        z = float(negz)
        bpy.context.scene.cursor.location = (-x, -z, y) 
        co_find = obj.matrix_world.inverted() @ bpy.context.scene.cursor.location
        #Search Using KD Tree
        co, index, dist = kd.find(co_find)
        kd.find_range(co_find, 0.1) #Implementing tolerance size
        obj.data.vertices[index].select = True #select chosen vertex
        vertex_group_data = [index]
        new_vertex_group.add(vertex_group_data, 1.0, 'ADD') #add vertex to created group
        obj.data.vertices[index].select = False #Deselect Vertex
        
def scale(vgroup, dx, dy, dz, prop_size):
    falloff = input_data["FallOffType"]
    if falloff == "":
        falloff = "SMOOTH"
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.object.vertex_group_set_active(group=vgroup) 
    bpy.ops.object.vertex_group_select()
    bpy.ops.transform.resize(value=(dx, dy, dz), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=True, proportional_edit_falloff=falloff, proportional_size=prop_size, use_proportional_connected=True, use_proportional_projected=False)
    bpy.ops.object.vertex_group_deselect()

def translate(vgroup, dx, dy, dz, prop_size):
    falloff = input_data["FallOffType"]
    if falloff == "":
        falloff = "SMOOTH"
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.object.vertex_group_set_active(group=vgroup) 
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(float(dx), float(dy), float(dz)), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff=falloff, proportional_size=float(prop_size), use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.vertex_group_deselect()

def transformMesh():
    for modification in input_data["Modifications"]:
        dx = modification["Delta-Magnitude-X"]
        dy = modification["Delta-Magnitude-Y"]
        dz = modification["Delta-Magnitude-Z"]
        prop_size = modification["InfluenceRadius"]
        bpy.ops.object.mode_set(mode = 'EDIT')
        vgroup = modification["Feature-abbrv"]
        bpy.ops.object.vertex_group_set_active(group=vgroup) 
        bpy.ops.object.vertex_group_select()
        if modification["TransformationType"] == "Scale":
            scale(vgroup, float(dx), float(dy), float(dz), float(prop_size))
        elif modification["TransformationType"] == "Translate":
            translate(vgroup, float(dx), float(dy), float(dz), float(prop_size))
        else:
            pass

def cursorReturn():
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.mode_set(mode = 'EDIT') #ensures the object is in edit mode after running script

def newJSON():
    bpy.ops.object.mode_set(mode = 'EDIT')
    for index in range(len(face_data["Features"])): #loop through all groups
        bpy.context.active_object.vertex_groups.active_index = index
        bpy.ops.object.vertex_group_select()  #select group
        bpy.ops.view3d.snap_cursor_to_selected() #snaps 3D cursor to location of selected vertex
        face_data["Features"]["xVal"] = round(bpy.context.scene.cursor.location[0], 2)
        face_data["Features"]["yVal"] = round(bpy.context.scene.cursor.location[1], 2)
        face_data["Features"]["zVal"] = round(bpy.context.scene.cursor.location[2], 2)            
        bpy.ops.object.vertex_group_deselect()
        modelname = face_data["ThreeDModel"]
        with open(modelname + '.json', 'w') as outfile:
            outfile.write(face_data)

def newerJSON():
    bm = bmesh.new()
    ob = bpy.context.active_object
    bm = bmesh.from_edit_mesh(ob.data)
    bpy.ops.object.mode_set(mode = 'EDIT')
    index = 0
    for feature in face_data["Features"]: #loop through all groups
        bpy.context.active_object.vertex_groups.active_index = index
        bpy.ops.object.vertex_group_select()  #select group
        for v in bm.verts:
            if v.select:
                tup = tuple(v.co)
        feature["xVal"] = -(round(tup[0], 2))
        feature["yVal"] = (round(tup[1], 2))
        feature["zVal"] = (round(tup[2], 2))
        bpy.ops.object.vertex_group_deselect()
        modelname = face_data["ThreeDModel"]
        index = index + 1
    target_file = os.path.join(directory, targetJSON)
    with open(target_file, 'w') as outfile:
        json.dump(face_data, outfile, indent=4)
    print("Created new JSON file titled: " + target_file)

def export():#export the file as .obj
    bpy.ops.object.mode_set(mode = 'OBJECT') #mode to object
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
    transformMesh()
    cursorReturn()
    newerJSON()
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
        modelname = input_data["ThreeDModel"]
        targetOBJ = input_data["TargetOBJFile"]
        targetOBJpath = os.path.join(script_dir, targetOBJ)
        targetJSON = input_data["TargetJSONFile"]
        targetJSONpath = os.path.join(script_dir, targetJSON)
        main()