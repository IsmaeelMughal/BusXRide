var table = document.getElementById("table");
var errorMsg = document.getElementById("msg");
var row = null;
var idCount = latestBusID;
var oldBus_id=null;
var oldD_dt=null;
function Submit() {

    if (validateRequiredFields() == true) {
        errorMsg.innerHTML = ``;
        var formData = getFormData();
        console.log(formData);
        if (row == null) {
            var arr = insert(formData);
            insertObject = {
                'BUS_ID': arr[0],
                'DEPARTURE_DATE_TIME': arr[1],
                'ARRIVAL_DATE_TIME': arr[2],
                'ROUTE_ID': arr[3],
            }
            console.log(insertObject);
            insertObject = JSON.stringify(insertObject);
            $.ajax({
                url: '/admin_dashboard/schedule_crud/add_schedule',
                type: 'POST',
                contentType: 'application/json',
                data: insertObject
            });
        }
        else {

            var arr = update();
              console.log(oldBus_id)//the old bus_id to be used in update statement
               console.log(oldD_dt)//the old Departure Date Time  to be used in update statement
            updateObject = {
                'old_busId':oldBus_id,
                'oldD-dt':oldD_dt,
                'oldRoute_id':oldRoute_id,
                'BUS_ID': arr[0],
                'DEPARTURE_DATE_TIME': arr[1],
                'ARRIVAL_DATE_TIME': arr[2],
                'ROUTE_ID': arr[3],
            }
            console.log(updateObject);
            updateObject = JSON.stringify(updateObject);
            $.ajax({
                url: '/admin_dashboard/schedule_crud/update_schedule',
                type: 'POST',
                contentType: 'application/json',
                data: updateObject
            });
        }
        reset();
    }
    else
    {
        errorMsg.innerHTML = `Fill all the fields before Submission!!!`;
    }
}
function validateRequiredFields() {
    if (document.getElementById('bus').value == '' || document.getElementById('d_dt').value == '' || document.getElementById('a_dt').value == ''|| document.getElementById('route').value == '') {
        return false;
    }
    else {
        return true;
    }
}
function reset() {
    document.getElementById('bus').value = '';
    document.getElementById('d_dt').value = '';
    document.getElementById('a_dt').value = '';
    document.getElementById('route').value = '';

}
function edit(td) {
    row = td.parentElement.parentElement;
    document.getElementById('bus').value = row.cells[0].innerHTML.trim();
    document.getElementById('d_dt').value = row.cells[1].innerHTML.trim();
    document.getElementById('a_dt').value = row.cells[2].innerHTML.trim();
    document.getElementById('route').value = row.cells[3].innerHTML.trim();
     oldBus_id=row.cells[0].innerHTML.trim();
     oldD_dt=row.cells[1].innerHTML.trim();
     oldRoute_id = row.cells[3].innerHTML.trim();

//    document.getElementById('ticketprice').value = Number(row.cells[3].innerHTML);
}
function getFormData() {
    var bus = document.getElementById('bus').value;
    var d_dt = document.getElementById('d_dt').value;
    var a_dt = document.getElementById('a_dt').value;
    var route = document.getElementById('route').value;
    var arr = [bus, d_dt, a_dt,route];
    return arr;
}
function insert(formData) {
    row = table.insertRow();
    idCount = idCount + 1;
    row.insertCell(0).innerHTML = formData[0];
    console.log(formData[0])
    row.insertCell(1).innerHTML = formData[1];
    row.insertCell(2).innerHTML = formData[2];
    row.insertCell(3).innerHTML = formData[3];
    row.insertCell(4).innerHTML = `<button onclick="edit(this)">Edit</button>
                                    <button onclick="remove(this)" id="delete-button">Delete</button>`;
    row = null;
    arr = [ formData[0], formData[1], formData[2],formData[3]];
    return arr;
}
function update() {

    row.cells[0].innerHTML = document.getElementById('bus').value;
    row.cells[1].innerHTML = document.getElementById('d_dt').value;
    row.cells[2].innerHTML = document.getElementById('a_dt').value;
     row.cells[3].innerHTML = document.getElementById('route').value;
    arr = [row.cells[0].innerHTML, row.cells[1].innerHTML, row.cells[2].innerHTML, row.cells[3].innerHTML]
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
            var arr = [row.cells[0].innerHTML.trim(), row.cells[1].innerHTML.trim(), row.cells[2].innerHTML.trim(), row.cells[3].innerHTML.trim()];
            row = null;
            removeObject = {
               'BUS_ID': arr[0],
                'DEPARTURE_DATE_TIME': arr[1],
                'ARRIVAL_DATE_TIME': arr[2],
                'ROUTE_ID': arr[3],
            }

            removeObject = JSON.stringify(removeObject);
            $.ajax({
                url: '/admin_dashboard/schedule_crud/delete_schedule',
                type: 'POST',
                contentType: 'application/json',
                data: removeObject
            });
        }
    })
}