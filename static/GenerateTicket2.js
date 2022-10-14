
        var bk_id=sessionStorage.getItem("bookingId");
        var bus_id=sessionStorage.getItem("busId");
        var sn=sessionStorage.getItem("seatNumber");
        var price=sessionStorage.getItem("price");
        var bk_date=sessionStorage.getItem("BK_DATE");
        var d_dt=sessionStorage.getItem("D_DT");
        var a_dt=sessionStorage.getItem("A_DT");
        var email=sessionStorage.getItem("email");
        var source=sessionStorage.getItem("source");
        var destination=sessionStorage.getItem("destination");
        var p="Rs "+price

        document.getElementById("bk_id").innerHTML = bk_id;
        document.getElementById("bk_d").innerHTML = bk_date;
        document.getElementById("e-Value").innerHTML = email;

        document.getElementById("s-Value").innerHTML = source;
        document.getElementById("d-Value").innerHTML = destination;
        document.getElementById("bus_id").innerHTML = bus_id;
        document.getElementById("d_dt").innerHTML = d_dt;
        document.getElementById("A_dt").innerHTML = a_dt;
        document.getElementById("seat_num").innerHTML = sn;
//        document.getElementById("p_Value").innerHTML =p;
        document.getElementById("p2_Value").innerHTML =p;




          console.log(bk_id);
          console.log(email);
          console.log(source);
          console.log(destination);