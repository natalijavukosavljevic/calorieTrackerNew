// Invoke Functions Call on Document Loaded

//dodali ovo u js za messages js dodali u main html


//da mozemo messages da zatvaramo ovaj hjs problem stavara
// Invoke Functions Call on Document Loaded
// document.addEventListener('DOMContentLoaded', function () {
//   hljs.highlightAll();
// });



document.addEventListener("DOMContentLoaded", function(event) {
  //deo za messages
  let alertWrapper = document.querySelector('.alert')
  let alertClose = document.querySelector('.alert__close')
  console.log(alertClose)
  console.log(alertWrapper)
  if (alertWrapper) {
    console.log('tu')
    alertClose.addEventListener('click', () =>
      alertWrapper.style.display = 'none'
    )
  }


  //deo za pie chart
  var ctx = document.getElementById('myChart')
  if (ctx){
    var carbsSum = document.getElementById("carbsSum").innerHTML
    var proteinsSum = document.getElementById("proteinsSum").innerHTML
    var fatsSum = document.getElementById("fatsSum").innerHTML
    var caloriesSum = document.getElementById("caloriesSum").innerHTML
    console.log(carbsSum)
    var myLineChart = new Chart(ctx.getContext('2d'), {
        type: 'pie',
        data: {
            labels: ["carbs", "proteins", "fats", "calories"],
            datasets: [{
                data: [carbsSum, proteinsSum, fatsSum, caloriesSum],
                backgroundColor: ["rgba(255, 0, 0, 0.5)", "rgba(100, 255, 0, 0.5)", "rgba(200, 50, 255, 0.5)", "rgba(0, 100, 255, 0.5)"]
            }]
        },
        
    });
 }

 var ctxDate=document.getElementById('dateChart')
 
 if(ctxDate){
  var caloriesArray = JSON.parse(document.getElementById("caloriesList").value);
  var selectedDates = JSON.parse(document.getElementById("selectedDates").value);
  var carbsArray = JSON.parse(document.getElementById("carbsList").value);
  var proteinsArray = JSON.parse(document.getElementById("proteinsList").value);
  var fatsArray = JSON.parse(document.getElementById("fatsList").value);
  console.log(ctxDate)
  console.log(selectedDates)
  console.log(caloriesArray)
      
    
    // var xyValues = [
    //   {x:20, y:7},
    //   {x:30, y:8},
    //   {x:40, y:8},
   
    // ];
    new Chart(ctxDate.getContext('2d'), {
      type: "line",
      data: {
        labels: selectedDates,
        datasets: [{
          label: "Calories",
          fill: true,
          backgroundColor: "transparent",
          borderColor:"#2d3cb3" ,
          data: caloriesArray
        }, {
          label: "Carbs",
          fill: true,
          backgroundColor: "transparent",
          borderColor: "#a62db3",
          borderDash: [4, 4],
          data: carbsArray
        }, {
          label: "Fats",
          fill: true,
          backgroundColor: "transparent",
          borderColor: "#b32d55",
          borderDash: [4, 4],
          data: fatsArray
        },
        {
          label: "Proteins",
          fill: true,
          backgroundColor: "transparent",
          borderColor: "#2db35a",
          borderDash: [4, 4],
          data: proteinsArray
        }
      ]
      },
      options: {
        scales: {
          xAxes: [{
            reverse: true,
            gridLines: {
              color: "rgba(0,0,0,0.05)"
            }
          }],
          yAxes: [{
            borderDash: [5, 5],
            gridLines: {
              color: "rgba(0,0,0,0)",
              fontColor: "#fff"
            }
          }]
        }
      }
    });

   
 }
 //deo za calorieLimit
  var slider = document.getElementById("rangeCalories");
  var output = document.getElementById("demo");
  output.innerHTML = slider.value; // Display the default slider value

  // Update the current slider value (each time you drag the slider handle)
  slider.oninput = function() {
    output.innerHTML = this.value;
  }

 
});





