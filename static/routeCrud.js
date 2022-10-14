var table = document.getElementById("table");
var errorMsg = document.getElementById("msg");
var row = null;
var idCount = latestRouteID;

function Submit() {

    if (validateRequiredFields() == true) {
        
        
        errorMsg.innerHTML = ``;
        var formData = getFormData();
        if (row == null) {
            if(validateIfRouteExist() == false)
            {
                var arr = insert(formData);
                insertObject = {
                    'ROUTE_ID': arr[0],
                    'SOURCE': arr[1],
                    'DESTINATION': arr[2],
                }
                insertObject = JSON.stringify(insertObject);
                $.ajax({
                    url: '/admin_dashboard/route_crud/add_route',
                    type: 'POST',
                    contentType: 'application/json',
                    data: insertObject
                });
            }
            else
            {
                errorMsg.innerHTML = `Route Already Exist in database!`;
            }
           
        }
        else {

            var arr = update();
            updateObject = {
                'ROUTE_ID': arr[0],
                'SOURCE': arr[1],
                'DESTINATION': arr[2],
            }
            console.log(updateObject);
            updateObject = JSON.stringify(updateObject);
            $.ajax({
                url: '/admin_dashboard/route_crud/update_route',
                type: 'POST',
                contentType: 'application/json',
                data: updateObject
            });
        }
        reset();
    }
    else {
        errorMsg.innerHTML = `Fill all the fields before Submission!!!`;
    }
}
function validateIfRouteExist() {
    for (var i = 0, r; r = table.rows[i]; i++) {
        if (document.getElementById('source').value.trim().toLowerCase() == r.cells[1].innerHTML.trim().toLowerCase() && document.getElementById('destination').value.trim().toLowerCase() == r.cells[2].innerHTML.trim().toLowerCase()) {
            return true;
        }
    }
    return false;
}
function validateRequiredFields() {
    if (document.getElementById('source').value == '' || document.getElementById('destination').value == '') {
        return false;
    }
    else {
        return true;
    }
}
function reset() {
    document.getElementById('source').value = '';
    document.getElementById('destination').value = '';
}
function edit(td) {
    row = td.parentElement.parentElement;
    document.getElementById('source').value = row.cells[1].innerHTML.trim();
    document.getElementById('destination').value = row.cells[2].innerHTML.trim();
}
function getFormData() {
    var src = document.getElementById('source').value;
    var dest = document.getElementById('destination').value;
    var arr = [src, dest];
    return arr;
}
function insert(formData) {
    row = table.insertRow();
    idCount = idCount + 1;
    row.insertCell(0).innerHTML = idCount;
    row.insertCell(1).innerHTML = formData[0];
    row.insertCell(2).innerHTML = formData[1];
    row.insertCell(3).innerHTML = `<button onclick="edit(this)" id="edit-button">Edit</button>
                                    <button onclick="remove(this)" id="delete-button">Delete</button>`;
    row = null;
    arr = [idCount, formData[0], formData[1]];
    return arr;
}
function update() {

    row.cells[1].innerHTML = document.getElementById('source').value;
    row.cells[2].innerHTML = document.getElementById('destination').value;
    arr = [row.cells[0].innerHTML.trim(), row.cells[1].innerHTML, row.cells[2].innerHTML]
    row = null;
    return arr;
}
function remove(td) {
    Confirm.open({
        title: 'DELETE RECORD',
        message: 'Are you sure you want to Delete Record?',
        onok: () => {
            row = td.parentElement.parentElement;
            document.getElementById("table").deleteRow(row.rowIndex);
            var arr = [row.cells[0].innerHTML.trim(), row.cells[1].innerHTML.trim(), row.cells[2].innerHTML.trim()];
            row = null;
            removeObject = {
                'ROUTE_ID': arr[0],
                'SOURCE': arr[1],
                'DESTINATION': arr[2],
            }

            removeObject = JSON.stringify(removeObject);
            $.ajax({
                url: '/admin_dashboard/route_crud/remove_route',
                type: 'POST',
                contentType: 'application/json',
                data: removeObject
            });
        }
    })
}