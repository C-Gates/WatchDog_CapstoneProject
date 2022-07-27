
var xarray = document.getElementById("myVar").value;  //.value.split(',');
var yarray = document.getElementById("myVar2").value; //.value.split(',');
var xValues = xarray.split(',');
var yValues = yarray.split(',');


var yNon0 = yValues.filter(gtzero);
var barColors = "rgba(100,200,200,1.0)";

// Create chart given variables
const myChart = new Chart("myChart", {
    type: "bar",
    data: {
        labels: xValues,
        datasets: [{
        backgroundColor: barColors,
        data: yValues
        }]
    },
    options: {
        legend: {display: false},
        scales: {
            yAxes: [{ ticks: { min : (Math.min.apply(Math, yNon0))*0.9}}] }, 
        title: {
        display: true,
        text: "Watchlist Performance"
        }
    }
    });


// Update graph for 1 week/month/year
function updateChart(chart, histX, histY) {

    var yValues = histY.split(',');
    var yNon0 = yValues.filter(gtzero);

    chart.data.datasets[0].data = yValues;
    chart.data.labels = histX.split(','),
    chart.options.scales.yAxes[0].ticks.min = (Math.min.apply(Math, yNon0))*0.9;
    chart.update();
}


function gtzero(num) {
    return num > 0;
}

// Functions to change the period of data displayed on the graph

function oneweek() {
    fetch(`${window.origin}/watchlist/history/1w`)  
    .then(function (response) {
        if (response.status !== 200) {
            console.log(`Error ${response.status}`);
            return;
        }
        response.json(). then(function (data) {
            //console.log(data);
            updateChart(myChart, data['histdates'].toString(), data['histvals'].toString());
        })
    })
}

function onemonth() {
    fetch(`${window.origin}/watchlist/history/1m`) 
    .then(function (response) {
        if (response.status !== 200) {
            console.log(`Error ${response.status}`);
            return;
        }
        response.json(). then(function (data) {
            //console.log(data);
            updateChart(myChart, data['histdates'].toString(), data['histvals'].toString());
        })
    })
}

function oneyear() {
    fetch(`${window.origin}/watchlist/history/1y`)  
    .then(function (response) {
        if (response.status !== 200) {
            console.log(`Error ${response.status}`);
            return;
        }
        response.json(). then(function (data) {
            //console.log(data);
            updateChart(myChart, data['histdates'].toString(), data['histvals'].toString());
        })
    })
}