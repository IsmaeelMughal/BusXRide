const container = document.querySelector('.seats-panel');

var refundList = [];

function makePayment() {
    refundObject = {
        'refundList': refundList,
        'updatedUserAccountBalance': userAccountBalance,
    }
    console.log(refundList, userAccountBalance);
    refundObject = JSON.stringify(refundObject);
    $.ajax({
        url: '/user_dashboard/refund_schedule/select_refund/seats',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(refundObject)
    });
    window.location.href = "http://127.0.0.1:5000/user_dashboard";
}
function setSeatsToOccupied() {
    for (let i = 0; i < occupiedSeatsArray.length; i++) {
        document.getElementById(occupiedSeatsArray[i]).classList.toggle('occupied');
    }
}
setSeatsToOccupied();
function setSeatsToSelected() {
    for (let i = 0; i < selectedSeatsArray.length; i++) {
        document.getElementById(selectedSeatsArray[i]).classList.toggle('selected');

    }
}
setSeatsToSelected();

container.addEventListener('click', e => {
    if (e.target.classList.contains('seat') && e.target.classList.contains('selected')) {
        Confirm.open({
            title: 'Ticket Refund',
            message: 'Are you sure you want to Refund Ticket?',
            onok: () => {
                e.target.classList.toggle('selected');
                refundList.push(e.target.id);

                userAccountBalance = userAccountBalance + ticketPrice;
                console.log(refundList, userAccountBalance);
            }
        })
        
    }
})
