let data = {
     "featurePointAbbrv": "prn",
     "MagnitudeOfChange": 2,
     "NumberOfChangeX": 4,
     "NumberOfChangeY": 3,
     "NumberOfChangeZ": 2,
     "InfluenceRadius": 20
}

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
    FallOffType: "",
    modifications: [{
        feature_abbrv: "ac_l",
        deltaX: "10",
        deltaY: "10",
        deltaZ: "0",
        InfluenceRadius: "20"
                }]}]
  };
  var modelName = "hank";
  var modelGender = "Male";
  var modelAge = 20;

  var test2 = {
    threeDModel: modelName,
    gender: modelGender,
    age: modelAge,
    //features: createFeatureText(),
    //measurements: createMeasurementText()
  };
  var jsonReadyText = JSON.stringify(jsonText, null, 4);
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

console.log(changelist);