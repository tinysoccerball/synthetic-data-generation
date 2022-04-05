inputs = [];
let modcount = 0;

const cartesian =
        (...a) => a.reduce((a, b) => a.flatMap(d => b.map(e => [d, e].flat())));

function cartesianCalc(arr){
    let output = [];
    for(i = 0; i < (arr.length - 1); i++) {
        console.log("hello Juan");
        console.log(cartesian(arr[i], arr[i+1]));
        console.log("Hello World");
        output.push(cartesian(arr[i], arr[i+1]));
    }
    return output;
}

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

    function combineArrays( array_of_arrays ){

        // First, handle some degenerate cases...
    
        if( ! array_of_arrays ){
            // Or maybe we should toss an exception...?
            return [];
        }
    
        if( ! Array.isArray( array_of_arrays ) ){
            // Or maybe we should toss an exception...?
            return [];
        }
    
        if( array_of_arrays.length == 0 ){
            return [];
        }
    
        for( let i = 0 ; i < array_of_arrays.length; i++ ){
            if( ! Array.isArray(array_of_arrays[i]) || array_of_arrays[i].length == 0 ){
                // If any of the arrays in array_of_arrays are not arrays or zero-length, return an empty array...
                return [];
            }
        }
    
        // Done with degenerate cases...
    
        // Start "odometer" with a 0 for each array in array_of_arrays.
        let odometer = new Array( array_of_arrays.length );
        odometer.fill( 0 ); 
    
        let output = [];
    
        let newCombination = formCombination( odometer, array_of_arrays );
    
        output.push( newCombination );
    
        while ( odometer_increment( odometer, array_of_arrays ) ){
            newCombination = formCombination( odometer, array_of_arrays );
            output.push( newCombination );
        }
        //output = JSON.stringify(output, null, 4)
        return output;
    }/* combineArrays() */


    // Translate "odometer" to combinations from array_of_arrays
    function formCombination( odometer, array_of_arrays ){
    // In Imperative Programmingese (i.e., English):
     let s_output = "";
     for( let i=0; i < odometer.length; i++ ){
        s_output += "" + array_of_arrays[i][odometer[i]]; 
     }
     return s_output;

    // In Functional Programmingese (Henny Youngman one-liner):
    //return odometer.reduce(
    //  function(accumulator, odometer_value, odometer_index){
    //    return "" + accumulator + array_of_arrays[odometer_index][odometer_value];
    //  },
    //  ""
    //);
    }   /* formCombination() */

    function odometer_increment( odometer, array_of_arrays ){

        // Basically, work you way from the rightmost digit of the "odometer"...
        // if you're able to increment without cycling that digit back to zero,
        // you're all done, otherwise, cycle that digit to zero and go one digit to the
        // left, and begin again until you're able to increment a digit
        // without cycling it...simple, huh...?

        for( let i_odometer_digit = odometer.length-1; i_odometer_digit >=0; i_odometer_digit-- ){ 

            let maxee = array_of_arrays[i_odometer_digit].length - 1;         

            if( odometer[i_odometer_digit] + 1 <= maxee ){
                // increment, and you're done...
                odometer[i_odometer_digit]++;
                return true;
            }
            else{
                if( i_odometer_digit - 1 < 0 ){
                    // No more digits left to increment, end of the line...
                    return false;
                }
                else{
                    // Can't increment this digit, cycle it to zero and continue
                    // the loop to go over to the next digit...
                    odometer[i_odometer_digit]=0;
                    continue;
                }
            }
        }/* for( let odometer_digit = odometer.length-1; odometer_digit >=0; odometer_digit-- ) */

    }/* odometer_increment() */

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
                //console.log("discarded " + i + ' ' + arr);
            }
        }
        return arr;
    }

    function objectProduct(obj) {
        var keys = Object.keys(obj),
            values = keys.map(function(x) { return obj[x] });
    
        return product(values).map(function(p) {
            var e = {};
            keys.forEach(function(k, n) { e[k] = p[n] });
            return e;
        });
    }

    const cartesianProduct = (arr1, arr2) => {
        const res = [];
        for(let i = 0; i < arr1.length; i++){
           for(let j = 0; j < arr2.length; j++){
              res.push(
                 [arr1[i]].concat(arr2[j])
              );
           };
        };
        return res;
     };
     

    function manymods(i) {
        holding = [];
        smalllist = [];
        secondary = [];
        thismod = [];
        for(i = 0; i < (changelistlist.length); i++){
            for (j = 0; j < changelistlist[i].length; j++){
                holding.push(inputs[i][7], changelistlist[i][j][0], changelistlist[i][j][1], changelistlist[i][j][2], inputInfluence);
                thismod.push(makemods(inputs[i][7], changelistlist[i][j][0], changelistlist[i][j][1], changelistlist[i][j][2], inputInfluence));
                smalllist.push(holding);
                holding = [];
            }
            secondary.push(thismod);
            thismod = [];
        }
        //let biglist = cartesianCalc(secondary);// cartesianProduct(secondary[0], secondary[1]);
        //console.log(biglist);
        return biglist[i];
    }

    function modlist() {
        holding = [];
        smalllist = [];
        secondary = [];
        thismod = [];
        for(i = 0; i < (changelistlist.length); i++){
            for (j = 0; j < changelistlist[i].length; j++){
                holding.push(inputs[i][7], changelistlist[i][j][0], changelistlist[i][j][1], changelistlist[i][j][2], inputInfluence);
                thismod.push(makemods(inputs[i][7], changelistlist[i][j][0], changelistlist[i][j][1], changelistlist[i][j][2], inputInfluence));
                smalllist.push(holding);
                holding = [];
            }
            secondary.push(thismod);
            thismod = [];
        }
        let biglist = cartesianProduct(secondary[0], secondary[1]);
        fileparts = [];
        thismod = [];
        counter = 0;
        changelist = removeDuplicates(changelist);
        for (i = 0; i < changelistlist.length - 1; i++){
            //changelistlist[i] = removeDuplicates(changelistlist[i]);
            changelistlist[i+1] = removeDuplicates(changelistlist[i+1]);
        }
        for(i = 0; i < (biglist.length); i++){
            file = {
                "threeDModel": modelName,
                "OriginalOBJFile": modelName + ".obj",
                "OriginalJSONFile": modelName + ".json",
                "TargetOBJFile": modelName + "-Target-" + counter + ".obj",
                "TargetJSONFile": modelName + "-Target-" + counter +".json",
                "Folder": ".",
                "FallOffType": "",
                "modifications": biglist[i]//manymods(i)
            }
                counter++;
                fileparts.push(file);
        }
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
        changelistlist = [];
        for (i = 0; i < inputs.length; i++){
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
            changelistlist.push(changelist);
            //console.log(changelistlist);
            changelist = [];
            dx = 0;
        }
        

        var thejson = JSON.stringify(finalmodfiles(), null, 4);
        return thejson;
    }
    console.log(getUserInput());
    //console.log(modlist());
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

function addMod() {
    thisInput = [document.getElementById("dx").value, document.getElementById("dy").value, document.getElementById("dz").value, document.getElementById("influence").value, document.getElementById("xmagnitude").value, document.getElementById("ymagnitude").value, document.getElementById("zmagnitude").value, document.getElementById("abbrv").value, document.getElementById("modelname").value];
    //console.log(thisInput);
    inputs.push(thisInput);
    //alert("Modification Added!");
    //console.log(inputs);
    modcount++;
    var container = document.getElementById('container');
    container.innerHTML = '';
    // create table element
    var table = document.createElement('table');
    var tbody = document.createElement('tbody');
    // loop array
    for (i = 0; i < inputs.length; i++) {
        // get inner array
        var vals = inputs[i];
        // create tr element
        var row = document.createElement('tr');
        // loop inner array
        for (var b = 0; b < vals.length; b++) {
            // create td element
            var cell = document.createElement('td');
            // set text
            cell.textContent = vals[b];
            // append td to tr
            row.appendChild(cell);
        }
        //append tr to tbody
        tbody.appendChild(row);
    }
    // append tbody to table
    table.appendChild(tbody);
    // append table to container
    container.appendChild(table);
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