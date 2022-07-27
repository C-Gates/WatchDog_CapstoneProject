var tabledata = document.getElementById("stockinfo").value.replace(/'/g, '"');
var stockdetails = document.getElementById("stockdetails").value.replace(/'/g, '"').split(',');

var tabledata2 = JSON.parse(tabledata);

makeTable(stockdetails, tabledata2);


function updatetable(view) {
    console.log(view);
    fetch(`${window.origin}/watchlist/get_view/${view}`)
    .then(function (response) {
        if (response.status !== 200) {
            console.log(`Error ${response.status}`);
            return;
        }
    
        response.json(). then(function (data) {
            console.log(data);
            var newCols = data['columns'].replace(/'/g, '').split(',');
            var newRows = data['rows'];
            console.log(newCols);
            console.log(newRows);
            makeTable(newCols, newRows);
            //updateChart(myChart, data['histdates'].toString(), data['histvals'].toString());
        })
    })
}

// Generate stock information tables
function makeTable(stockdetails, rows) {
    var cols = [];

    for(var i = 0; i < stockdetails.length; i++) {
        if(stockdetails[i] == 'change' || stockdetails[i] == 'change%') {  // If column is change detail, will turn green/red for increase/decrease
            cols.push({title:stockdetails[i], field:stockdetails[i], formatter:function(cell, formatterParams){
                var value = cell.getValue();
                if(value[0] == "-" | value < 0){
                    return "<span style='color:#E07962;'>" + value + "</span>";
                }else{
                    return "<span style='color:#68CD6F;'>" + value + "</span>";
                }
            }
            })

        }
        else if (stockdetails[i] == 'change_perc') {  // If column is change detail, will turn green/red for increase/decrease
            cols.push({title:'%', field:'change_perc', formatter:function(cell, formatterParams){
                var value = cell.getValue();
                if(value[0] == "-"){
                    return "<span style='color:#E07962;'>" + value + "</span>";
                }else{
                    return "<span style='color:#68CD6F;'>" + value + "</span>";
                }
            }
            })

        }
        else{cols.push({title:stockdetails[i], field:stockdetails[i]}) }
    }

    //console.log(rows);
    //console.log(cols);
    // Generate Table
    var table = new Tabulator("#stock-table", {
        data:rows, //assign data to table
        layout:"fitColumns", //fit columns to width of table (optional)
        columns: cols,
    });
}

// Function for earier specified button delete view
function deleteView(view)  {
    fetch(`${window.origin}/watchlist/delete_view`, {
    method: "POST",
    credentials : "include",
    body: JSON.stringify({'name' : view}),
    cache: "no-cache",
    headers : new Headers({
        "content-type" : "application/json"
    })
    })
    .then(function (response) {
        if (response.status !== 200) {
            console.log(`Error ${response.status}`);
            return;
        }
        else {
            location.reload();
        }
    })

}