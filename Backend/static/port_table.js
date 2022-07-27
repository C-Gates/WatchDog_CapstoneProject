var portstocks = document.getElementById('portfoliostocks').value.replace(/'/g, '"');
var portrows = JSON.parse(portstocks);

var columns = [
                {title:"Code", field:"code"},
                {title:"Name", field:"name"},
                {title:"Price", field:"price"},
                {title:"Vol", field:"vol"},
                {title:"Purchase price", field:"purchase"},
                {title:"Market", field:"market"},
                {title:"Change", field:"change", formatter:function(cell, formatterParams){
                        var value = cell.getValue();
                        if(value[0] == "-" | value < 0){   // If column is change detail, will turn green/red for increase/decrease
                            return "<span style='color:#E07962;'>" + value + "</span>";
                        }else{
                            return "<span style='color:#68CD6F;'>" + value + "</span>";
                        }
                    }
                    },
                {title:"%", field:"changep", formatter:function(cell, formatterParams){
                        var value = cell.getValue();
                        if(value[0] == "-" | value < 0){   // If column is change detail, will turn green/red for increase/decrease
                            return "<span style='color:#E07962;'>" + value + "</span>";
                        }else{
                            return "<span style='color:#68CD6F;'>" + value + "</span>";
                        }
                    }
                    },
                {title:"P/L", field:"pnl"},
                {title:"Market Cap", field:"market_cap"},
                {title:"Market Volume", field:"volume"},
            ]
            
makeTable(columns, portrows);

function makeTable(cols, rows) {
    console.log(rows);
    console.log(cols);
    var table = new Tabulator("#stock-table", {
        data:rows, //assign data to table
        layout:"fitColumns", //fit columns to width of table (optional)
        columns: cols,
    });
}