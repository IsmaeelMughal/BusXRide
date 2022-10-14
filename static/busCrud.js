var table = document.getElementById("table");
var errorMsg = document.getElementById("msg");
var row = null;
var idCount = latestBusID;
function Submit() {
    if (validateRequiredFields() == true) {
        errorMsg.innerHTML = ``;
        var formData = getFormData();
        console.log(formData);
        console.log("formDatas")
        if (row == null) {
            var arr = insert(formData);
            insertObject = {
                'BUS_ID': arr[0],
                'MODEL': arr[1],
                'COLOR': arr[2],
                'TICKET_PRICE': arr[3],
            }
            console.log(insertObject);
            insertObject = JSON.stringify(insertObject);
            $.ajax({
                url: '/admin_dashboard/bus_crud/add_bus',
                type: 'POST',
                contentType: 'application/json',
                data: insertObject
            });
        }
        else {

            var arr = update();
            updateObject = {
                'BUS_ID': arr[0],
                'MODEL': arr[1],
                'COLOR': arr[2],
                'TICKET_PRICE': arr[3],
            }
            console.log(updateObject);
            updateObject = JSON.stringify(updateObject);
            $.ajax({
                url: '/admin_dashboard/bus_crud/update_bus',
                type: 'POST',
                contentType: 'application/json',
                data: updateObject
            });
        }
        reset();
    }
    else
    {
        if (document.getElementById('ticketprice').value == '0')
        {
            errorMsg.innerHTML = `Ticket Price cannot be Zero!!!`;
        }
        else if (parseInt(document.getElementById('ticketprice').value) > 100000)
        {
            errorMsg.innerHTML = `Max Ticket Price can be 100000`;
        }
        else
        {
            errorMsg.innerHTML = `Please Fill All the Fields!!!`;
        }

    }
}
function validateRequiredFields() {
    if (document.getElementById('buscolor').value == '' || document.getElementById('busmodel').value == '' || document.getElementById('ticketprice').value == '' || document.getElementById('ticketprice').value == '0' || parseInt(document.getElementById('ticketprice').value) > 100000) {
        return false;
    }
    else {
        return true;
    }
}
function reset() {
    document.getElementById('buscolor').value = '';
    document.getElementById('busmodel').value = '';
    document.getElementById('ticketprice').value = '';
}
function edit(td) {
    row = td.parentElement.parentElement;
    document.getElementById('buscolor').value = row.cells[2].innerHTML.trim();
    document.getElementById('busmodel').value = row.cells[1].innerHTML.trim();
    document.getElementById('ticketprice').value = Number(row.cells[3].innerHTML);
}
function getFormData() {
    var color = document.getElementById('buscolor').value;
    var model = document.getElementById('busmodel').value;
    var tp = document.getElementById('ticketprice').value;
    var arr = [model, color, tp];
    return arr;
}
function insert(formData) {
    row = table.insertRow();
    idCount = idCount + 1;
    row.insertCell(0).innerHTML = idCount;
    row.insertCell(1).innerHTML = formData[0];
    row.insertCell(2).innerHTML = formData[1];
    row.insertCell(3).innerHTML = formData[2];
    row.insertCell(4).innerHTML = `<button onclick="edit(this)">Edit</button>
                                    <button onclick="remove(this)" id="delete-button">Delete</button>`;
    row = null;
    arr = [idCount, formData[0], formData[1], formData[2]];
    return arr;
}
function update() {

    row.cells[1].innerHTML = document.getElementById('busmodel').value;
    row.cells[2].innerHTML = document.getElementById('buscolor').value;
    row.cells[3].innerHTML = document.getElementById('ticketprice').value;
    arr = [row.cells[0].innerHTML.trim(), row.cells[1].innerHTML, row.cells[2].innerHTML, row.cells[3].innerHTML]
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
                'MODEL': arr[1],
                'COLOR': arr[2],
                'TICKET_PRICE': arr[3],
            }

            removeObject = JSON.stringify(removeObject);
            $.ajax({
                url: '/admin_dashboard/bus_crud/remove_bus',
                type: 'POST',
                contentType: 'application/json',
                data: removeObject
            });
        }
    })
}