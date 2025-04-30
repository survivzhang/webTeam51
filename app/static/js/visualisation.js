document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM loaded, initializing charts...");
  initializeCharts();
});

function initializeCharts() {
  console.log("Starting chart initialization...");

  // Sample data for Calorie In
  const calorieInData = {
    labels: ["Breakfast", "Lunch", "Dinner", "Snacks"],
    data: [500, 800, 1000, 300],
    backgroundColor: [
      "rgba(255, 99, 132, 0.7)", // Breakfast - Red
      "rgba(54, 162, 235, 0.7)", // Lunch - Blue
      "rgba(255, 206, 86, 0.7)", // Dinner - Yellow
      "rgba(75, 192, 192, 0.7)", // Snacks - Cyan
    ],
  };

  // Sample data for Calorie Out
  const calorieOutData = {
    labels: ["Running", "Cycling", "Swimming", "Yoga", "Weight Training"],
    data: [600, 450, 350, 200, 400],
    backgroundColor: [
      "rgba(255, 99, 132, 0.7)", // Running
      "rgba(54, 162, 235, 0.7)", // Cycling
      "rgba(255, 206, 86, 0.7)", // Swimming
      "rgba(75, 192, 192, 0.7)", // Yoga
      "rgba(153, 102, 255, 0.7)", // Weight Training
    ],
  };

  // Sample data for Calorie Trends (Last 7 days)
  const calorieTrendsData = {
    labels: [
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
      "Sunday",
    ],
    data: [2500, 2300, 2700, 2600, 2400, 2800, 2200],
  };

  // Sample data for Nutrition Analysis
  const nutritionData = {
    labels: ["Carbohydrates", "Proteins", "Fats", "Vitamins", "Sugars"],
    data: [40, 25, 20, 10, 5],
    backgroundColor: [
      "rgba(255, 99, 132, 0.7)", // Carbs
      "rgba(54, 162, 235, 0.7)", // Proteins
      "rgba(255, 206, 86, 0.7)", // Fats
      "rgba(75, 192, 192, 0.7)", // Vitamins
      "rgba(153, 102, 255, 0.7)", // Sugars
    ],
  };

  // Calorie In Chart (Pie)
  const calorieInCtx = document.getElementById("calorieInChart");
  if (calorieInCtx) {
    new Chart(calorieInCtx, {
      type: "pie",
      data: {
        labels: calorieInData.labels,
        datasets: [
          {
            data: calorieInData.data,
            backgroundColor: calorieInData.backgroundColor,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "right",
          },
          title: {
            display: true,
            text: "Daily Calorie Intake Distribution",
          },
        },
      },
    });
    console.log("Calorie In chart created");
  } else {
    console.error("Calorie In chart canvas not found");
  }

  // Calorie Out Chart (Pie)
  const calorieOutCtx = document.getElementById("calorieOutChart");
  if (calorieOutCtx) {
    new Chart(calorieOutCtx, {
      type: "pie",
      data: {
        labels: calorieOutData.labels,
        datasets: [
          {
            data: calorieOutData.data,
            backgroundColor: calorieOutData.backgroundColor,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "right",
          },
          title: {
            display: true,
            text: "Daily Calorie Burn Distribution",
          },
        },
      },
    });
    console.log("Calorie Out chart created");
  } else {
    console.error("Calorie Out chart canvas not found");
  }

  // Calorie Trends Chart (Line)
  const calorieTrendsCtx = document.getElementById("calorieTrendsChart");
  if (calorieTrendsCtx) {
    new Chart(calorieTrendsCtx, {
      type: "line",
      data: {
        labels: calorieTrendsData.labels,
        datasets: [
          {
            label: "Total Daily Calories",
            data: calorieTrendsData.data,
            borderColor: "rgba(75, 192, 192, 1)",
            tension: 0.1,
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: "Weekly Calorie Trends",
          },
        },
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
    console.log("Calorie Trends chart created");
  } else {
    console.error("Calorie Trends chart canvas not found");
  }

  // Nutrition Analysis Chart (Pie)
  const nutritionCtx = document.getElementById("nutritionAnalysisChart");
  if (nutritionCtx) {
    new Chart(nutritionCtx, {
      type: "pie",
      data: {
        labels: nutritionData.labels,
        datasets: [
          {
            data: nutritionData.data,
            backgroundColor: nutritionData.backgroundColor,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "right",
          },
          title: {
            display: true,
            text: "Nutrition Intake Analysis",
          },
        },
      },
    });
    console.log("Nutrition Analysis chart created");
  } else {
    console.error("Nutrition Analysis chart canvas not found");
  }

  // Generate recommendations
  generateRecommendations();
}

function generateRecommendations() {
  // Nutrition Recommendations
  const nutritionRecommendations = [
    "Your carbohydrate intake is slightly high. Consider reducing refined carbs and increasing protein intake.",
    "Good protein balance! Maintain this level for muscle health.",
    "Fat intake is within healthy range. Focus on healthy fats like avocados and nuts.",
    "Consider increasing vitamin-rich foods like fruits and vegetables.",
    "Sugar intake is well controlled. Keep it up!",
  ];

  // Exercise Recommendations
  const exerciseRecommendations = [
    "Great cardio performance! Consider adding more strength training for better muscle balance.",
    "Good variety in exercises. Try to maintain consistency in your workout schedule.",
    "Consider adding flexibility exercises like yoga to improve mobility.",
    "Increase weight training duration to help boost your base metabolic rate.",
    "Aim for 3-4 cardio sessions and 2-3 strength training sessions per week.",
  ];

  // Update recommendation sections
  const nutritionRecElement = document.getElementById(
    "nutritionRecommendations"
  );
  if (nutritionRecElement) {
    nutritionRecElement.innerHTML = `
      <h3 class="font-semibold text-blue-800 mb-2">Nutrition Recommendations:</h3>
      <ul class="list-disc list-inside text-gray-700">
        ${nutritionRecommendations.map((rec) => `<li>${rec}</li>`).join("")}
      </ul>
    `;
  }

  const exerciseRecElement = document.getElementById("exerciseRecommendations");
  if (exerciseRecElement) {
    exerciseRecElement.innerHTML = `
      <h3 class="font-semibold text-green-800 mb-2">Exercise Recommendations:</h3>
      <ul class="list-disc list-inside text-gray-700">
        ${exerciseRecommendations.map((rec) => `<li>${rec}</li>`).join("")}
      </ul>
    `;
  }
}
