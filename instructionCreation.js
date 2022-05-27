inputs = [];
let modificationsCount = 0;
let counter = 1;
let allChangeList = [];

function modificationJSON(point, dx, dy, dz, infl, transformation) {
    modification = {
        "feature-abbrv": point,
        "deltaX": dx,
        "deltaY": dy,
        "deltaZ": dz,
        "InfluenceRadius": infl,
        "TransformationType": transformation
            }
    return modification;
}

function targetModificationsJSON(modelName, counter, falloff, modifications) {
    targetModifications = {
        "threeDModel": modelName,
        "OriginalOBJFile": modelName + ".obj",
        "OriginalJSONFile": modelName + ".json",
        "TargetOBJFile": modelName + "-Target-" + counter + ".obj",
        "TargetJSONFile": modelName + "-Target-" + counter +".json",
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
                               modificationJSON(allChangeList[i][j][0],
                                 allChangeList[i][j][1],
                                 allChangeList[i][j][2],
                                 allChangeList[i][j][3],
                                 allChangeList[i][j][4],
                                allChangeList[i][j][5] )
                               );
        }
        counter++;
        allTargetChanges.push(targetModificationsJSON(modelname, counter, falloff, targetChanges));

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

    for (i = 0; i < inputs.length; i++) {
        // get inner array
        var vals = inputs[i];
        var currentInfl = vals[6];
        var iterationNo = parseInt(vals[7]); //changenumber
        var currentAbbrv = vals[8];
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
            changeDx = parseFloat(vals[0]) + (parseFloat(vals[3]) * j);
            changeDy = parseFloat(vals[1]) + (parseFloat(vals[4]) * j);
            changeDz = parseFloat(vals[2]) + (parseFloat(vals[5]) * j);
            changes.push([currentAbbrv,
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

function addModification() {
    //startx, starty, startz, dx, dy, dz, influence, changenumber, abbrv, modelname, falloff, translation
    currentInput = [document.getElementById("startx").value,
                    document.getElementById("starty").value,
                    document.getElementById("startz").value,
                    document.getElementById("dx").value,
                    document.getElementById("dy").value,
                    document.getElementById("dz").value,
                    document.getElementById("influence").value,
                    document.getElementById("changenumber").value,
                    document.getElementById("abbrv").value,
                    document.getElementById("modelname").value,
                    document.getElementById("falloff").value,
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
    // loop array

    var row = document.createElement('tr');
    var cell = document.createElement('td');
    cell.textContent = "Start X";
    cell.style.border = '1px solid black';
    row.appendChild(cell);
    var cell = document.createElement('td');
    cell.textContent = "Start Y";
    cell.style.border = '1px solid black';
    row.appendChild(cell);
    var cell = document.createElement('td');
    cell.textContent = "Start Z";
    cell.style.border = '1px solid black';
    row.appendChild(cell);
    var cell = document.createElement('td');
    cell.textContent = "Magnitude X";
    cell.style.border = '1px solid black';
    row.appendChild(cell);
    var cell = document.createElement('td');
    cell.textContent = "Magnitude Y";
    cell.style.border = '1px solid black';
    row.appendChild(cell);
    var cell = document.createElement('td');
    cell.textContent = "Magnitude Z";
    cell.style.border = '1px solid black';
    row.appendChild(cell);
    var cell = document.createElement('td');
    cell.textContent = "Influence";
    cell.style.border = '1px solid black';
    row.appendChild(cell);
    var cell = document.createElement('td');
    cell.textContent = "Number of Iterations";
    cell.style.border = '1px solid black';
    row.appendChild(cell);
    var cell = document.createElement('td');
    cell.textContent = "Abbrv";
    cell.style.border = '1px solid black';
    row.appendChild(cell);
    var cell = document.createElement('td');
    cell.textContent = "Model Name";
    cell.style.border = '1px solid black';
    row.appendChild(cell);
    var cell = document.createElement('td');
    cell.textContent = "Fall Off";
    cell.style.border = '1px solid black';
    row.appendChild(cell);
    var cell = document.createElement('td');
    cell.textContent = "Transformation";
    cell.style.border = '1px solid black';
    row.appendChild(cell);
    tbody.appendChild(row);
    
    for (i = 0; i < inputs.length; i++) {
        // get inner array
        var vals = inputs[i];
        // create tr element
        var row = document.createElement('tr');
        // loop inner array
        for (var j = 0; j < vals.length; j++) {
            // create td element
            var cell = document.createElement('td');
            // set text
            cell.textContent = vals[j];
            cell.style.border = '1px solid black';
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
            inputAbbrvs = inputAbbrvs + "_" + vals[8];
        else
            inputAbbrvs = vals[8];
    }
    var modelName = document.getElementById("modelname").value;
    var filename = modelName + "_" + inputAbbrvs + ".json";
    console.log(inputAbbrvs);
    console.log(filename);
    download(filename, prepareJSON());
}
