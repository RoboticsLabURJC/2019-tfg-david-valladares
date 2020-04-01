var referee_ws;
    
function Referee_Ws(url) {
    ///Init de WebSocket connection with the Referee Server

    // Connect to Web Socket
    referee_ws = new WebSocket(url);

    // Set event handlers.
    referee_ws.onopen = function() {
        console.log("Referee WebSocket connection opened");
        setInterval(function(){ referee_ws.send("Keep_Alive"); console.log("Keep Alive to server")}, 1000);

    };

    referee_ws.onclose = function() {
         console.log("Conexión de WebSocket closed");
    };

    referee_ws.onerror = function(e) {
        console.log("Referee WebSocket Error:" + e)
    };

}


function Distance_Chart(){

    dataRedLine = []

    for(var i=1;i<=1200;i++){
        dataRedLine.push(4);
    }

    labels = new Array(1200)

    for (let index = 0; index < labels.length; index++) {
        labels[index] = ""
        
    }
    var ctx = document.getElementById("chart_canvas").getContext('2d')
    distance_chart = new Chart(ctx, {
        type: 'line',
        scaleOverride: true,
        data: {
            labels: labels,
            datasets: [{
                backgroundColor: '#ff6384',
                label: 'Distancia al Ratón',
                backgroundColor:'#16b4ff',
                borderColor: '#16b4ff',
                data: [],
                fill: false,
            },
            {
                label: 'Red Line',
                backgroundColor:'#e41111',
                borderColor: '#e41111',
                data: dataRedLine,
                fill: false
            }]
        },
        options: {
            legend: {
                display: false
            },
            maintainAspectRatio : false,
            chartArea: {
                backgroundColor: 'rgba(255, 255, 255, 1)'
            },
            elements: {
                point: { 
                    radius: 0 
                } 
            },
            scales: {
                xAxes: [{
                    gridLines: {
                        display: true
                    },
                    ticks: {
                        callback: function(tick, index, ticksArray) {
                            // return the string representation of the tick value. Return undefined to hide the grid line
                            if((index % 100) == 0){
                                return (index/10) + "s"
                            }else if(index == (ticksArray.length - 1)){ // Necesario para pintar el último tick
                                return (ticksArray.length/10) + "s"
                            }else{
                                return undefined
                            }
                        },
                        fontSize: 12,
                        tickMarkLength:20,
                        offsetGridLines: true,
                        autoSkip: false
                    }   
                }],
                yAxes: [{
                    gridLines: {
                        color: "rgba(0, 0, 0, 0.3)",
                    },
                    ticks: {
                        beginAtZero: true,
                        reverse: true,
                        start: 0,
                        max: 10
                    }   
                }]
            }
        }
    });

    Chart.pluginService.register({
        beforeDraw: function (chart, easing) {
            if (chart.config.options.chartArea && chart.config.options.chartArea.backgroundColor) {
                var helpers = Chart.helpers;
                var ctx = chart.chart.ctx;
                var chartArea = chart.chartArea;
    
                ctx.save();
                ctx.fillStyle = chart.config.options.chartArea.backgroundColor;
                ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);
                ctx.restore();
            }
        }
    });
    

    return distance_chart

}