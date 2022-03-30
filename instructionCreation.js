function everything() {
    let counter = 1;
    var dx = 0;
    var dy = 0;
    var dz = 0;
    var changelist = [];

    var inputDX = document.getElementById("dx").value;
    var inputDY = document.getElementById("dy").value;
    var inputDZ = document.getElementById("dz").value;
    var inputInfluence = document.getElementById("influence").value;
    var xInputMagnitude = document.getElementById("xmagnitude").value;
    var yInputMagnitude = document.getElementById("ymagnitude").value;
    var zInputMagnitude = document.getElementById("zmagnitude").value;
    var inputAbbrv = document.getElementById("abbrv").value;
    var modelName = document.getElementById("modelname").value;

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

    function uniq(a) {
        return a.sort().filter(function(item, pos, ary) {
            return !pos || item != ary[pos - 1];
        });
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

    function modlist() {
    mods = [];
    fileparts = [];
    counter = 1;
    changelist = removeDuplicates(changelist);
    for(i = 0; i < (changelist.length); i++){
        file = {
            "threeDModel": modelName,
            "OriginalOBJFile": modelName + ".obj",
            "OriginalJSONFile": modelName + ".json",
            "TargetOBJFile": modelName + "-Target-" + counter + ".obj",
            "TargetJSONFile": modelName + "-Target-" + counter +".json",
            "Folder": ".",
            "FallOffType": "",
            "modifications": makemods(inputAbbrv, changelist[i][0], changelist[i][1], changelist[i][2], inputInfluence)
        }
        fileparts.push(file);
        counter++;
        //mods.push(makemods(inputAbbrv, changelist[i][0], changelist[i][1], changelist[i][2], inputInfluence));
    }
    /*
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
    */
    return fileparts;
    }
    


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
    for (i = 0; i < changelist.length; i++) {
        files.push(makefile())
        counter++;
    }
    return files;
    }

    function finalmodfiles(){
    modfiles = {
        "ModificationFiles":modlist()
    }
    return modfiles;
    }


    //console.log(thejson);

    function revealMessage(){
        //document.getElementById("jsonOutput") = thejson;
        document.getElementById("hiddenMessage").style.display = 'block';
        document.getElementById("Output") = thejson;
    }

    function getUserInput() {
        let data = {
            "featurePointAbbrv": "prn",
            "MagnitudeOfChange": 2,
            "NumberOfChangeX": 4,
            "NumberOfChangeY": 3,
            "NumberOfChangeZ": 2,
            "InfluenceRadius": 20
        }
        
        changes = inputDX;
        if (changes <= inputDY){
        changes = inputDY
        }
        if (changes <= inputDZ){
        changes = inputDZ
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
    
        
        for (xmag = 0; xmag < changes; xmag++){
            for (ymag = 0; ymag < changes; ymag++){
                for (zmag = 0; zmag < changes; zmag++){
                    changelist.push([dx, dy, dz]);
                    if (dz < (inputDZ * zInputMagnitude)){
                        dz += parseInt(zInputMagnitude);
                    }
                    changelist.push([dx, dy, dz]);
                }
                if (dy < inputDY * yInputMagnitude){
                    dy += parseInt(yInputMagnitude);
                }
                dz = 0;
            }
        if (dx < (inputDX * xInputMagnitude)){
            dx += parseInt(xInputMagnitude);
        }
        dy = 0;
        dz = 0;
        }

        var thejson = JSON.stringify(finalmodfiles(), null, 4);
        return thejson;
    }
    console.log(getUserInput());
    return getUserInput(); 
}

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

function closer() {
    iterations = [];
    filesheet = everything();
}

// Start file download.
function beginDownload(){
    var inputDX = document.getElementById("dx").value;
    var inputDY = document.getElementById("dy").value;
    var inputDZ = document.getElementById("dz").value;
    var inputInfluence = document.getElementById("influence").value;
    var xInputMagnitude = document.getElementById("xmagnitude").value;
    var yInputMagnitude = document.getElementById("ymagnitude").value;
    var zInputMagnitude = document.getElementById("zmagnitude").value;
    var inputAbbrv = document.getElementById("abbrv").value;
    var modelName = document.getElementById("modelname").value;
    var filename = modelName+"_"+inputAbbrv+"_"+inputDX+"_"+inputDY+"_"+inputDZ+"_"+inputInfluence+"_"+xInputMagnitude+"_"+yInputMagnitude+"_"+zInputMagnitude+".json";
    download(filename, everything());
}