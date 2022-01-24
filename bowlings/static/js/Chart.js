var ctx = document.getElementById("myChart").getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
    labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    datasets: [{
    label: '# of Votes',
    data: [12, 19, 3, 5, 2, 3],
    backgroundColor: [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)'
    ],
    borderColor: [
    'rgba(255,99,132,1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)'
    ],
    borderWidth: 1
    }]
    },
    options: {
    scales: {
    yAxes: [{
    ticks: {
    beginAtZero: true
    }
    }]
    }
    }
  });



//doughnut
var ctxP = document.getElementById("doughnutChart").getContext('2d');
var doughnut = new Chart(ctxP, {
    type: 'doughnut',
    data: {
    labels: ["TV", "Internet"],
    datasets: [{
    data: [300, 80],
    backgroundColor: ["#F7464A", "#4D5360"],
    hoverBackgroundColor: ["#FF5A5E", "#616774"]
    }]
    },
    options: {
    responsive: true
    }
});

