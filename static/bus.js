const container = document.querySelector('.seats-panel');
const seats = document.querySelectorAll('.row .seat:not(.occupied)');
const seatCount = document.getElementById('seat-count');
const totalPrice = document.getElementById('price-total');
const error = document.getElementById("error");
console.log(error.innerText);


function makePayment()
{
    arr=[];
    const selectedSeats = document.querySelectorAll('.row .seat.selected');
    for(let i=0;i<selectedSeats.length;i++)
    {
        arr.push(selectedSeats[i].id);
    }
    arr = JSON.stringify(arr);
    console.log(arr)
    $.ajax({
        url: '/user_dashboard/buy_ticket/schedules/tickets/buy_tickets',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(arr)
    });
    window.location.href = "http://127.0.0.1:5000/user_dashboard";
}
function setSeatsToOccupied() {
    for (let i = 0; i < seatArray.length; i++) {
        document.getElementById(seatArray[i]).classList.toggle('occupied');
    }
}
var allSelectSeats = setSeatsToOccupied();
function updateSelectedCount() {
    const selectedSeats = document.querySelectorAll('.row .seat.selected');
    
    count = selectedSeats.length;
    seatCount.innerText = count;
    totalPrice.innerText = ticketPrice * count;
}
function getSelecteSeatsCount() {
    const selectedSeats = document.querySelectorAll('.row .seat.selected');
    count = selectedSeats.length;
    return count;
}

container.addEventListener('click', e => {
    count = getSelecteSeatsCount();
    if (((count + 1) * ticketPrice) < userAccountBalance) {
        if (e.target.classList.contains('seat') && !e.target.classList.contains('occupied')) {
            e.target.classList.toggle('selected');
        }
        updateSelectedCount();
    }
    else if(e.target.classList.contains('seat') && !e.target.classList.contains('occupied'))
    {
        if(e.target.classList.contains('seat') && e.target.classList.contains('selected'))
        {
            e.target.classList.toggle('selected');
        }
        count = getSelecteSeatsCount();
        if(((count + 1) * ticketPrice) > userAccountBalance)
        {
            
            error.innerText = "You have insufficient Balance!";
        }
        else
        {
            error.innerText = "";
        }
        updateSelectedCount();

    }

})
