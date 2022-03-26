let data = {
    "featurePointAbbrv": "prn",
    "MagnitudeOfChange": 2,
    "NumberOfChangeX": 4,
    "NumberOfChangeY": 3,
    "NumberOfChangeZ": 2,
    "InfluenceRadius": 20
}

let counter = 1;

var origdirectory = '';
var basename = "JuanGlinton";

var jsonText = {ModificationFiles:[{
   threeDModel: "jack",
   threeDModel: basename,
   OriginalOBJFile: basename + ".obj",
   OriginalJSONFile: basename + ".json",
   TargetOBJFile: basename + "-Target-1.obj",
   TargetJSONFile: basename + "-Target-1.json",
   Folder: ".",
   FallOffType: ""
   //modifications: modlist()
   }]
 };
 //var modelName = "hank";
 var modelGender = "Male";
 var modelAge = 20;
/*
 var test2 = {
   threeDModel: modelName,
   gender: modelGender,
   age: modelAge,
   //features: createFeatureText(),
   //measurements: createMeasurementText()
 };
 var jsonReadyText = JSON.stringify(jsonText, null, 4);*/
////////////////////////////////////////////////
   var dx = 0;
   var dy = 0;
   var dz = 0;
   var changelist = [];

   changes = data["NumberOfChangeX"];
if (changes <= data["NumberOfChangeY"]){
   changes = data["NumberOfChangeY"]
}
if (changes <= data["NumberOfChangeZ"]){
   changes = data["NumberOfChangeZ"]
}

for (xmag = 0; xmag < changes; xmag++){
   for (ymag = 0; ymag < changes; ymag++){
       for (zmag = 0; zmag < changes; zmag++){
           changelist.push([dx, dy, dz]);
           if (dz < (data["NumberOfChangeZ"] * data["MagnitudeOfChange"])){
               dz += data["MagnitudeOfChange"];
           }
           changelist.push([dx, dy, dz]);
       }
       if (dy < data["NumberOfChangeY"] * data["MagnitudeOfChange"]){
           dy += data["MagnitudeOfChange"];
       }
       dz = 0;
   }
   if (dx < (data["NumberOfChangeX"] * data["MagnitudeOfChange"])){
       dx += data["MagnitudeOfChange"];
   }
   dy = 0;
   dz = 0;
}

function arraysEqual(a, b) {
    if (a === b) return true;
    if (a == null || b == null) return false;
    if (a.length !== b.length) return false;
  
    // If you don't care about the order of the elements inside
    // the array, you should sort both arrays here.
    // Please note that calling sort on an array will modify that array.
    // you might want to clone your array first.
  
    for (var i = 0; i < a.length; ++i) {
      if (a[i] !== b[i]) return false;
    }
    return true;
  }

function removeDuplicates(arr) {
    for (i= 0; i<arr.length; i++){
        if (arraysEqual(arr[i], arr[i+1])){
            arr.splice(i, 1); 
            i--; 
        }
    }
    return arr;
}
function makemods(point, dx, dy, dz, infl) { 
   mod = {
       "feature_abbrv": point,
       "deltaX": dx,
       "deltaY": dy,
       "deltaZ": dz,
       "InfluenceRadius": infl
               }
   //console.log(mod);
   return mod;
}

function modlist() {
   mods = [];
   changelist = removeDuplicates(changelist);
   for(i = 0; i < (changelist.length); i++){
       mods.push(makemods(data["featurePointAbbrv"], changelist[i][0], changelist[i][1], changelist[i][2], data["InfluenceRadius"]));
   }
   //console.log(mods);
   return mods;
}

var modelName = "Kim";

function makefile(){
   file = {
       "threeDModel": modelName,
       "OriginalOBJFile": modelName + ".obj",
       "OriginalJSONFile": modelName + ".json",
       "TargetOBJFile": modelName + "-Target-" + counter + ".obj",
       "TargetJSONFile": modelName + "-Target-" + counter +".json",
       "Folder": ".",
       "FallOffType": "",
       "modifications": modlist()
   }
   return file
}

function myfiles(){
   files = []
   for (i = 0; i < 3; i++) {
       files.push(makefile())
       counter++;
   }
   return files;
}

function finalmodfiles(){
   modfiles = {
       "ModificationFiles":myfiles()
   }
   return modfiles;
}

var thejson = JSON.stringify(finalmodfiles(), null, 4);

console.log(thejson);