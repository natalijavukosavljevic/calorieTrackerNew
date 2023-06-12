

document.addEventListener("DOMContentLoaded", function(event) {
  //close messages
  let alertWrapper = document.querySelector('.alert')
  let alertClose = document.querySelector('.alert__close')
  if (alertWrapper) {
    alertClose.addEventListener('click', () =>
      alertWrapper.style.display = 'none'
    )
  }


  //pie chart generation
  let ctx = document.getElementById('myChart')
  if (ctx){
    let carbsSum = document.getElementById("carbsSum").innerHTML
    let proteinsSum = document.getElementById("proteinsSum").innerHTML
    let fatsSum = document.getElementById("fatsSum").innerHTML
    let caloriesSum = document.getElementById("caloriesSum").innerHTML
    console.log(carbsSum)
    new Chart(ctx.getContext('2d'), {
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
 // date chart generation
 let ctxDate=document.getElementById('dateChart')
 
 if(ctxDate){
  let caloriesArray = JSON.parse(document.getElementById("caloriesList").value);
  let selectedDates = JSON.parse(document.getElementById("selectedDates").value);
  let carbsArray = JSON.parse(document.getElementById("carbsList").value);
  let proteinsArray = JSON.parse(document.getElementById("proteinsList").value);
  let fatsArray = JSON.parse(document.getElementById("fatsList").value);
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
 //calorieLimit tracking
  let slider = document.getElementById("rangeCalories");
  if (slider){
    let output = document.getElementById("demo");
    output.innerHTML = slider.value; // Display the default slider value

    // Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
      output.innerHTML = this.value;
    }
    

  }
  

 
});





