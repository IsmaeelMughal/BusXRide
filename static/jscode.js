var sources= graph["sources"]
var destination=graph["destination"]
//For sources DropDown
var select = document.getElementById("source"), sources;
             for(var i = 0; i < sources.length; i++)
             {
                 var option = document.createElement("OPTION"),
                     txt = document.createTextNode(sources[i]);
                 option.appendChild(txt);
                 option.setAttribute("value",sources[i]);
                 select.insertBefore(option,select.lastChild);
             }
//For destinationDropDown
var selectDes = document.getElementById("destination"), destination;
             for(var j= 0; j < destination.length; j++)
             {
                 var option1 = document.createElement("OPTION"),
                     txt1 = document.createTextNode(destination[j]);
                 option1.appendChild(txt1);
                 option1.setAttribute("value",destination[j]);
                 selectDes.insertBefore(option1,selectDes.lastChild);
             }

