inputs = [];
let modificationsCount = 0;
let counter = 1;
let allChangeList = [];

function modificationJSON(abbrv, dx, dy, dz, infl, transformation) {
    modification = {
        "Feature-abbrv": abbrv,
        "Delta-Magnitude-X": dx,
        "Delta-Magnitude-Y": dy,
        "Delta-Magnitude-Z": dz,
        "InfluenceRadius": infl,
        "TransformationType": transformation
            }
    return modification;
}

function targetModificationsJSON(counter, modelName, falloff, modifications) {
    targetModifications = {
        "ThreeDModel": modelName,
        "OriginalOBJFile": modelName + ".obj",
        "OriginalLandmarkFile": modelName + ".json",
        "TargetOBJFile": modelName + "-Target-" + counter + ".obj",
        "TargetLandmarkFile": modelName + "-Target-" + counter +".json",
        "Folder": ".",
        "FallOffType": falloff,
        "Modifications": modifications
            }
    return targetModifications;
}


function allModificationsJSON() {
    var modelname = document.getElementById("modelname").value;
    var falloff = document.getElementById("falloff").value;
    
    var allTargetChanges = [];
    counter = 0;

    loopContinue = true;
    loopIndexCurrent = [];
    loopIndexLength = [];
    for(i = 0; i < allChangeList.length; i++){
        loopIndexCurrent.push(0);
        loopIndexLength.push(allChangeList[i].length);
        //console.log('current:' + loopIndexCurrent[i] + " - length:" + loopIndexLength[i]);
    }
    
    //console.log('loop starts');
    while (loopContinue)
    {
        //console.log('loop next items');
        j = 0;
        var targetChanges = [];
        for (i = 0; i < loopIndexCurrent.length; i++)
        {
            console.log(i + ": " + loopIndexCurrent[i]);
            j = loopIndexCurrent[i];
            targetChanges.push(
                               //(abbrv, dx, dy, dz, infl, transformation)
                               modificationJSON(
                                                allChangeList[i][j][0],
                                                allChangeList[i][j][3],
                                                allChangeList[i][j][4],
                                                allChangeList[i][j][5],
                                                allChangeList[i][j][6],
                                                allChangeList[i][j][7]                                                )
                               );
            if (allChangeList[i][j][1] == 'Y')
            {
                targetChanges.push(
                                   //(dualabbrv, -dx, -dy, -dz, infl, transformation)
                                   modificationJSON(
                                                    allChangeList[i][j][2],
                                                    (allChangeList[i][j][3] * -1),
                                                    (allChangeList[i][j][4] * -1),
                                                    (allChangeList[i][j][5] * -1),
                                                    allChangeList[i][j][6],
                                                    allChangeList[i][j][7]                                                )
                                   );
            }

        }
        counter++;
        allTargetChanges.push(targetModificationsJSON(counter, modelname, falloff, targetChanges));

        // This for loop prepares the index of the next item
        // Increments the index of the last abbrv
        // If the last abbrv index exceeds the number of items (length),
        // it increments the previous item's index
        // If first item's (i == 0) current index reaches its length,
        // then it means we are done with the outher loop
        for (i = loopIndexCurrent.length-1; i >= 0; i--)
        {
            loopIndexCurrent[i] ++;
            if (loopIndexCurrent[i] < loopIndexLength[i])
            {
                break;
            }
            else if (i == 0)
            {
                loopContinue = false;
            }
            else
            {
                loopIndexCurrent[i] = 0;
            }
        }
    }
    //console.log('loop ended');
    return allTargetChanges;
}

function finalModificationsJSON(){
    modfiles = {
        "ModificationFiles":allModificationsJSON()
    }
    return modfiles;
}

function prepareChanges() {

    document.getElementById("abbrv").value,
    document.getElementById("dual").value,
    document.getElementById("dualabbrv").value,
    document.getElementById("changenumber").value,
    document.getElementById("startx").value,
    document.getElementById("starty").value,
    document.getElementById("startz").value,
    document.getElementById("dx").value,
    document.getElementById("dy").value,
    document.getElementById("dz").value,
    document.getElementById("influence").value,
    //document.getElementById("modelname").value,
    //document.getElementById("falloff").value,
    document.getElementById("transformation").value
    
    for (i = 0; i < inputs.length; i++) {
        // get inner array
        var vals = inputs[i];
        var currentAbbrv = vals[0];
        var currentDual = vals[1];
        var currentDualAbbrv = vals[2];
        var iterationNo = parseInt(vals[3]); //changenumber
        var currentInfl = vals[10];
        var currentTranslation = vals[11];
        var startX = 0.0;
        var startY = 0.0;
        var startZ = 0.0;
        var changeDx = 0.0;
        var changeDy = 0.0;
        var changeDz = 0.0;
        var changes = [];
        //dx, dy, dz, influence, changenumber, abbrv, modelname, falloff
        for (var j = 0; j < iterationNo; j++) {
            changeDx = parseFloat(vals[4]) + (parseFloat(vals[7]) * j);
            changeDy = parseFloat(vals[5]) + (parseFloat(vals[8]) * j);
            changeDz = parseFloat(vals[6]) + (parseFloat(vals[9]) * j);
            changes.push([currentAbbrv,
                          currentDual,
                          currentDualAbbrv,
                          changeDx,
                          changeDy,
                          changeDz,
                          currentInfl,
                          currentTranslation]);
        }
        console.log(changes);
        allChangeList.push(changes);
    }
}

function prepareJSON() {
        prepareChanges();
        var thejson = JSON.stringify(finalModificationsJSON(), null, 4);// last parameter is for space
        return thejson;
}

function createAddCell(row, cellValue, bold) {
    var cell = document.createElement('td');
    cell.textContent = cellValue;
    cell.style.border = '1px solid black';
    if (bold == 'Y') cell.style = 'font-weight:bold';
    row.appendChild(cell);
}

function addModification() {
    //startx, starty, startz, dx, dy, dz, influence, changenumber, abbrv, modelname, falloff, translation
    currentInput = [
        document.getElementById("abbrv").value,
        document.getElementById("dual").value,
        document.getElementById("dualabbrv").value,
        document.getElementById("changenumber").value,
        document.getElementById("startx").value,
        document.getElementById("starty").value,
        document.getElementById("startz").value,
        document.getElementById("dx").value,
        document.getElementById("dy").value,
        document.getElementById("dz").value,
        document.getElementById("influence").value,
        //document.getElementById("modelname").value,
        //document.getElementById("falloff").value,
        document.getElementById("transformation").value
                    ];
    //console.log(thisInput);
    inputs.push(currentInput);
    //alert("Modification Added!");
    //console.log(inputs);
    modificationsCount++;
    var container = document.getElementById('container');
    container.innerHTML = '';
    // create table element
    var table = document.createElement('table');
    var tbody = document.createElement('tbody');
    var row = document.createElement('tr');

    createAddCell(row, "Abbrv", 'Y');
    createAddCell(row, "Dual", 'Y');
    createAddCell(row, "Dual Abbrv", 'Y');
    createAddCell(row, "Number of Iterations", 'Y');
    createAddCell(row, "Start X", 'Y');
    createAddCell(row, "Start Y", 'Y');
    createAddCell(row, "Start Z", 'Y');
    createAddCell(row, "Magnitude X", 'Y');
    createAddCell(row, "Magnitude Y", 'Y');
    createAddCell(row, "Magnitude Z", 'Y');
    createAddCell(row, "Influence", 'Y');
    //createAddCell(row, "Model Name", 'Y');
    //createAddCell(row, "Fall Off", 'Y');
    createAddCell(row, "Transformation", 'Y');
    tbody.appendChild(row);
    
    for (i = 0; i < inputs.length; i++) {
        // get inner array
        var vals = inputs[i];
        // create tr element
        var row = document.createElement('tr');
        // loop inner array
        for (var j = 0; j < vals.length; j++) {
            createAddCell(row, vals[j], 'N');
        }
        //append tr to tbody
        tbody.appendChild(row);
    }
    // append tbody to table
    table.appendChild(tbody);
    // append table to container
    container.appendChild(table);
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

// Start file download.
function downloadJSON(){
    var inputAbbrvs = "";
    for (i = 0; i < inputs.length; i++) {
        console.log(inputAbbrvs);
        // get inner array
        var vals = inputs[i];
        if (i>0)
            inputAbbrvs = inputAbbrvs + "_" + vals[0];//adds abbrv names to the list
        else
            inputAbbrvs = vals[0];
    }
    var modelName = document.getElementById("modelname").value;
    var filename = modelName + "_" + inputAbbrvs + ".json";
    console.log(inputAbbrvs);
    console.log(filename);
    download(filename, prepareJSON());
}
