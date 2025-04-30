document.addEventListener("DOMContentLoaded", function () {
  // Initialize date inputs with default range (last 30 days)
  const today = new Date();
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(today.getDate() - 30);

  document.getElementById("date-from").value = thirtyDaysAgo
    .toISOString()
    .split("T")[0];
  document.getElementById("date-to").value = today.toISOString().split("T")[0];

  // Initialize charts
  initializeCharts();

  // Update charts when date range changes
  document
    .getElementById("update-charts")
    .addEventListener("click", updateCharts);

  // Handle visualization selection
  document
    .getElementById("visualization-selector")
    .addEventListener("change", function (e) {
      updateVisualization(e.target.value);
    });
});

function initializeCharts() {
  // Health Score Chart
  const healthScoreCtx = document
    .getElementById("healthScoreChart")
    .getContext("2d");
  new Chart(healthScoreCtx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Health Score",
          data: [],
          borderColor: "rgb(75, 192, 192)",
          tension: 0.1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: {
            display: true,
            text: "Score (0-100)",
          },
        },
      },
    },
  });
}

function updateVisualization(type) {
  const container = document.getElementById("visualization-container");
  container.innerHTML = `<canvas id="${type}-chart"></canvas>`;

  // Initialize the selected chart
  const ctx = document.getElementById(`${type}-chart`).getContext("2d");
  let chart;

  switch (type) {
    case "calorie-trends":
      chart = new Chart(ctx, {
        type: "line",
        data: {
          labels: [],
          datasets: [
            {
              label: "Daily Calories",
              data: [],
              borderColor: "rgb(75, 192, 192)",
              tension: 0.1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Calories",
              },
            },
          },
        },
      });
      break;

    case "exercise-analysis":
      chart = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: [
            "Running",
            "Walking",
            "Cycling",
            "Swimming",
            "Yoga",
            "Weights",
          ],
          datasets: [
            {
              data: [],
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
                "rgb(75, 192, 192)",
                "rgb(153, 102, 255)",
                "rgb(255, 159, 64)",
              ],
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
      break;

    case "weight-sleep":
      chart = new Chart(ctx, {
        type: "scatter",
        data: {
          datasets: [
            {
              label: "Weight vs Sleep",
              data: [],
              backgroundColor: "rgb(75, 192, 192)",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: {
                display: true,
                text: "Sleep Hours",
              },
            },
            y: {
              title: {
                display: true,
                text: "Weight (kg)",
              },
            },
          },
        },
      });
      break;

    // case "nutrition-analysis":
    //   chart = new Chart(ctx, {
    //     type: "bar",
    //     data: {
    //       labels: ["Great", "Good", "Okay", "Tired", "Stressed"],
    //       datasets: [
    //         {
    //           label: "Mood Distribution",
    //           data: [],
    //           backgroundColor: [
    //             "rgb(75, 192, 192)",
    //             "rgb(54, 162, 235)",
    //             "rgb(255, 205, 86)",
    //             "rgb(255, 159, 64)",
    //             "rgb(255, 99, 132)",
    //           ],
    //         },
    //       ],
    //     },
    //     options: {
    //       responsive: true,
    //       maintainAspectRatio: false,
    //     },
    //   });
    //   break;

    case "meal-distribution":
      chart = new Chart(ctx, {
        type: "pie",
        data: {
          labels: ["Breakfast", "Lunch", "Dinner", "Snack"],
          datasets: [
            {
              data: [],
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
                "rgb(75, 192, 192)",
              ],
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
      break;
  }

  return chart;
}

// function updateCharts() {
//   const dateFrom = document.getElementById("date-from").value;
//   const dateTo = document.getElementById("date-to").value;
//   const selectedVisualization = document.getElementById(
//     "visualization-selector"
//   ).value;

//   // Fetch data from API
//   fetch(`/api/visualization/data?from=${dateFrom}&to=${dateTo}`)
//     .then((response) => response.json())
//     .then((data) => {
//       // Update Health Score
//       updateHealthScore(data.healthScore);

//       // Update Insights
//       updateInsights(data.insights);

//       // Update selected visualization
//       const chart = updateVisualization(selectedVisualization);

//       // Update chart data based on selection
//       switch (selectedVisualization) {
//         case "calorie-trends":
//           updateCalorieTrends(data.calorieTrends, chart);
//           break;
//         case "exercise-analysis":
//           updateExerciseDistribution(data.exerciseDistribution, chart);
//           break;
//         case "weight-sleep":
//           updateWeightSleepCorrelation(data.weightSleepData, chart);
//           break;
//         case "nutrition-analysis":
//           updateMoodAnalysis(data.moodData, chart);
//           break;
//         case "meal-distribution":
//           updateMealDistribution(data.mealData, chart);
//           break;
//       }
//     })
//     .catch((error) => {
//       console.error("Error fetching visualization data:", error);
//       alert("Error loading visualization data. Please try again.");
//     });
// }

// function updateHealthScore(data) {
//   const chart = Chart.getChart("healthScoreChart");
//   chart.data.labels = data.dates;
//   chart.data.datasets[0].data = data.scores;
//   chart.update();
// }

// function updateInsights(insights) {
//   const container = document.getElementById("insights-container");
//   container.innerHTML = insights
//     .map(
//       (insight) => `
//       <div class="p-4 bg-blue-50 rounded-lg">
//           <h3 class="font-semibold text-blue-800">${insight.title}</h3>
//           <p class="text-gray-700 mt-1">${insight.description}</p>
//       </div>
//   `
//     )
//     .join("");
// }

// function updateCalorieTrends(data, chart) {
//   chart.data.labels = data.dates;
//   chart.data.datasets[0].data = data.calories;
//   chart.update();
// }

// function updateExerciseDistribution(data, chart) {
//   chart.data.datasets[0].data = data;
//   chart.update();
// }

// function updateWeightSleepCorrelation(data, chart) {
//   chart.data.datasets[0].data = data.points;
//   chart.update();
// }

// function updateMoodAnalysis(data, chart) {
//   chart.data.datasets[0].data = data.distribution;
//   chart.update();
// }

// function updateMealDistribution(data, chart) {
//   chart.data.datasets[0].data = data.distribution;
//   chart.update();
// }
