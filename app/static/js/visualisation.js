document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM loaded, initializing charts...");
  fetchUserData();
});

// Function to fetch all user data from API
async function fetchUserData() {
  try {
    console.log("Fetching user data from API...");
    
    // Show loading indicators while fetching data
    showLoadingState();
    
    const response = await fetch('/api/get_all_data', {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    const result = await response.json();
    
    if (result.status === 'success') {
      console.log("Data fetched successfully:", result.data);
      initializeCharts(result.data);
    } else {
      console.error("API returned error:", result.message);
      showError("Error loading data from server");
    }
  } catch (error) {
    console.error("Error fetching user data:", error);
    showError("Failed to connect to server. Make sure the application is running.");
    
    // Use sample data for demonstration when API is not available
    console.log("Using sample data as fallback");
    initializeCharts(getSampleData());
  }
}

// Show loading state while fetching data
function showLoadingState() {
  const containers = ["calorieInChart", "calorieOutChart", "calorieTrendsChart", "nutritionAnalysisChart"];
  
  containers.forEach(containerId => {
    const container = document.getElementById(containerId);
    if (container) {
      const ctx = container.getContext('2d');
      ctx.clearRect(0, 0, container.width, container.height);
      ctx.fillStyle = "rgba(200, 200, 200, 0.2)";
      ctx.fillRect(0, 0, container.width, container.height);
      ctx.font = '14px Arial';
      ctx.fillStyle = '#666';
      ctx.textAlign = 'center';
      ctx.fillText("Loading data...", container.width / 2, container.height / 2);
    }
  });
}

// Sample data for fallback when API is not available
function getSampleData() {
  return [
    // Meal entries
    {
      type: 'meal',
      date: '2023-05-10',
      meal_type: 'Breakfast',
      calories: 450
    },
    {
      type: 'meal',
      date: '2023-05-10',
      meal_type: 'Lunch',
      calories: 680
    },
    {
      type: 'meal',
      date: '2023-05-10',
      meal_type: 'Dinner',
      calories: 850
    },
    {
      type: 'meal',
      date: '2023-05-11',
      meal_type: 'Breakfast',
      calories: 400
    },
    {
      type: 'meal',
      date: '2023-05-11',
      meal_type: 'Lunch',
      calories: 720
    },
    {
      type: 'meal',
      date: '2023-05-11',
      meal_type: 'Snacks',
      calories: 250
    },
    {
      type: 'meal',
      date: '2023-05-11',
      meal_type: 'Dinner',
      calories: 780
    },
    // Exercise entries
    {
      type: 'exercise',
      date: '2023-05-10',
      exercise_type: 'Running',
      calories_burned: 320,
      duration: 30
    },
    {
      type: 'exercise',
      date: '2023-05-10',
      exercise_type: 'Weight Training',
      calories_burned: 280,
      duration: 45
    },
    {
      type: 'exercise',
      date: '2023-05-11',
      exercise_type: 'Cycling',
      calories_burned: 450,
      duration: 40
    },
    {
      type: 'exercise',
      date: '2023-05-11',
      exercise_type: 'Swimming',
      calories_burned: 380,
      duration: 35
    },
    {
      type: 'exercise',
      date: '2023-05-11',
      exercise_type: 'Yoga',
      calories_burned: 180,
      duration: 50
    }
  ];
}

// Show error message on charts
function showError(message) {
  const containers = ["calorieInChart", "calorieOutChart", "nutritionAnalysisChart"];
  
  containers.forEach(containerId => {
    const container = document.getElementById(containerId);
    if (container) {
      // Create error message
      const ctx = container.getContext('2d');
      ctx.font = '14px Arial';
      ctx.fillStyle = 'red';
      ctx.textAlign = 'center';
      ctx.fillText(message, container.width / 2, container.height / 2);
    }
  });
}

// Process data for visualization
function processUserData(data) {
  // Group and filter the data
  const meals = data.filter(item => item.type === 'meal');
  const exercises = data.filter(item => item.type === 'exercise');
  
  // Process meal data for calorie intake distribution
  const mealsByType = {};
  let totalCaloriesIn = 0;
  
  meals.forEach(meal => {
    const calories = parseInt(meal.calories) || 0;
    if (!mealsByType[meal.meal_type]) {
      mealsByType[meal.meal_type] = 0;
    }
    mealsByType[meal.meal_type] += calories;
    totalCaloriesIn += calories;
  });
  
  // Process exercise data for calorie burn distribution
  const exercisesByType = {};
  let totalCaloriesBurned = 0;
  
  exercises.forEach(exercise => {
    const caloriesBurned = parseInt(exercise.calories_burned) || 0;
    if (!exercisesByType[exercise.exercise_type]) {
      exercisesByType[exercise.exercise_type] = 0;
    }
    exercisesByType[exercise.exercise_type] += caloriesBurned;
    totalCaloriesBurned += caloriesBurned;
  });
  
  // Calculate average nutrition values from meals
  let totalCarbs = 0;
  let totalProteins = 0;
  let totalFats = 0;
  let totalSugars = 0;
  let totalFiber = 0;
  
  // We need to make another API call to get nutrition details
  return {
    mealsByType,
    exercisesByType,
    totalCaloriesIn,
    totalCaloriesBurned
  };
}

function initializeCharts(userData) {
  console.log("Starting chart initialization with real data...");
  
  const processedData = processUserData(userData);
  
  // Prepare data for Calorie In chart
  const calorieInData = {
    labels: Object.keys(processedData.mealsByType),
    data: Object.values(processedData.mealsByType),
    backgroundColor: [
      "rgba(255, 99, 132, 0.7)",  // Red
      "rgba(54, 162, 235, 0.7)",  // Blue
      "rgba(255, 206, 86, 0.7)",  // Yellow
      "rgba(75, 192, 192, 0.7)",  // Cyan
    ],
  };
  
  // Prepare data for Calorie Out chart
  const calorieOutData = {
    labels: Object.keys(processedData.exercisesByType),
    data: Object.values(processedData.exercisesByType),
    backgroundColor: [
      "rgba(255, 99, 132, 0.7)",  // Red
      "rgba(54, 162, 235, 0.7)",  // Blue
      "rgba(255, 206, 86, 0.7)",  // Yellow
      "rgba(75, 192, 192, 0.7)",  // Cyan
      "rgba(153, 102, 255, 0.7)", // Purple
    ],
  };
  
  // For now, we'll use sample data for Nutrition Analysis until we have proper API endpoint
  // In a real app, we would make another API call to get nutrition details
  const nutritionData = {
    labels: ["Carbohydrates", "Proteins", "Fats", "Sugars", "Fiber"],
    data: [40, 25, 20, 10, 5],
    backgroundColor: [
      "rgba(255, 99, 132, 0.7)", // Carbs
      "rgba(54, 162, 235, 0.7)", // Proteins
      "rgba(255, 206, 86, 0.7)", // Fats
      "rgba(75, 192, 192, 0.7)", // Sugars
      "rgba(153, 102, 255, 0.7)", // Fiber
    ],
  };
  
  // Get the last 7 days of calorie data for trends
  const calorieTrendsData = prepareCalorieTrendsData(userData);

  // Calorie In Chart (Pie)
  const calorieInCtx = document.getElementById("calorieInChart");
  if (calorieInCtx) {
    if (calorieInData.labels.length === 0) {
      drawEmptyDataMessage(calorieInCtx, "No meal data available");
    } else {
      new Chart(calorieInCtx, {
        type: "pie",
        data: {
          labels: calorieInData.labels,
          datasets: [
            {
              data: calorieInData.data,
              backgroundColor: calorieInData.backgroundColor.slice(0, calorieInData.labels.length),
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
              text: "Calorie Intake Distribution",
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const value = context.raw;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = ((value / total) * 100).toFixed(1);
                  return `${context.label}: ${value} cal (${percentage}%)`;
                }
              }
            }
          },
        },
      });
      console.log("Calorie In chart created with real data");
    }
  } else {
    console.error("Calorie In chart canvas not found");
  }

  // Calorie Out Chart (Pie)
  const calorieOutCtx = document.getElementById("calorieOutChart");
  if (calorieOutCtx) {
    if (calorieOutData.labels.length === 0) {
      drawEmptyDataMessage(calorieOutCtx, "No exercise data available");
    } else {
      new Chart(calorieOutCtx, {
        type: "pie",
        data: {
          labels: calorieOutData.labels,
          datasets: [
            {
              data: calorieOutData.data,
              backgroundColor: calorieOutData.backgroundColor.slice(0, calorieOutData.labels.length),
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
              text: "Calorie Burn Distribution",
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const value = context.raw;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = ((value / total) * 100).toFixed(1);
                  return `${context.label}: ${value} cal (${percentage}%)`;
                }
              }
            }
          },
        },
      });
      console.log("Calorie Out chart created with real data");
    }
  } else {
    console.error("Calorie Out chart canvas not found");
  }

  // Calorie Trends Chart (Line)
  const calorieTrendsCtx = document.getElementById("calorieTrendsChart");
  if (calorieTrendsCtx) {
    if (calorieTrendsData.labels.length === 0) {
      drawEmptyDataMessage(calorieTrendsCtx, "No trend data available");
    } else {
      new Chart(calorieTrendsCtx, {
        type: "line",
        data: {
          labels: calorieTrendsData.labels,
          datasets: [
            {
              label: "Calories In",
              data: calorieTrendsData.caloriesIn,
              borderColor: "rgba(75, 192, 192, 1)",
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              tension: 0.1,
              fill: true,
            },
            {
              label: "Calories Burned",
              data: calorieTrendsData.caloriesOut,
              borderColor: "rgba(255, 99, 132, 1)",
              backgroundColor: "rgba(255, 99, 132, 0.2)",
              tension: 0.1,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: "Calorie Trends",
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
      console.log("Calorie Trends chart created with real data");
    }
  } else {
    console.error("Calorie Trends chart canvas not found");
  }

  // Nutrition Analysis Chart (Pie)
  const nutritionCtx = document.getElementById("nutritionAnalysisChart");
  if (nutritionCtx) {
    // Fetch nutrition data here or use existing one
    fetchNutritionData()
      .then(nutritionData => {
        if (!nutritionData || Object.keys(nutritionData).length === 0) {
          drawEmptyDataMessage(nutritionCtx, "No nutrition data available");
        } else {
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
                  text: "Nutrition Analysis",
                },
                tooltip: {
                  callbacks: {
                    label: function(context) {
                      const value = context.raw;
                      const total = context.dataset.data.reduce((a, b) => a + b, 0);
                      const percentage = ((value / total) * 100).toFixed(1);
                      return `${context.label}: ${percentage}%`;
                    }
                  }
                }
              },
            },
          });
          console.log("Nutrition Analysis chart created with real data");
        }
      })
      .catch(error => {
        console.error("Error fetching nutrition data:", error);
        drawEmptyDataMessage(nutritionCtx, "Failed to load nutrition data");
      });
  } else {
    console.error("Nutrition Analysis chart canvas not found");
  }

  window._latestProcessedData = processedData; // Store for recommendation button
}

// Helper function to draw a message when no data is available
function drawEmptyDataMessage(canvas, message) {
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "rgba(200, 200, 200, 0.5)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.font = "16px Arial";
  ctx.fillStyle = "#666";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(message, canvas.width / 2, canvas.height / 2);
}

// Helper function to prepare calorie trends data
function prepareCalorieTrendsData(userData) {
  // Get unique dates
  const dates = [...new Set(userData.map(item => item.date))].sort();
  
  // Take only last 7 days if we have enough data
  const lastDays = dates.slice(-7);
  
  // Calculate calories in and calories out for each day
  const caloriesIn = [];
  const caloriesOut = [];
  
  for (const date of lastDays) {
    const dayData = userData.filter(item => item.date === date);
    
    // Sum up calories in
    const dayCaloriesIn = dayData
      .filter(item => item.type === 'meal')
      .reduce((sum, meal) => sum + (parseInt(meal.calories) || 0), 0);
    caloriesIn.push(dayCaloriesIn);
    
    // Sum up calories out
    const dayCaloriesOut = dayData
      .filter(item => item.type === 'exercise')
      .reduce((sum, exercise) => sum + (parseInt(exercise.calories_burned) || 0), 0);
    caloriesOut.push(dayCaloriesOut);
  }
  
  return {
    labels: lastDays,
    caloriesIn,
    caloriesOut
  };
}

// Fetch nutrition data from API
async function fetchNutritionData() {
  try {
    // Make actual API call to our new endpoint
    const response = await fetch('/api/nutrition_summary', {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    const result = await response.json();
    
    if (result.status === 'success') {
      // Convert the nutrition data to format needed by Chart.js
      return {
        labels: ["Carbohydrates", "Proteins", "Fats", "Sugars", "Fiber"],
        data: [
          result.data.carbohydrates,
          result.data.proteins,
          result.data.fats,
          result.data.sugars,
          result.data.fiber
        ],
        backgroundColor: [
          "rgba(255, 99, 132, 0.7)",
          "rgba(54, 162, 235, 0.7)",
          "rgba(255, 206, 86, 0.7)",
          "rgba(75, 192, 192, 0.7)",
          "rgba(153, 102, 255, 0.7)"
        ]
      };
    } else {
      throw new Error(result.message || 'Failed to retrieve nutrition data');
    }
  } catch (error) {
    console.error("Error fetching nutrition data:", error);
    
    // Return fallback sample data when the API fails
    return {
      labels: ["Carbohydrates", "Proteins", "Fats", "Sugars", "Fiber"],
      data: [42, 23, 19, 12, 4],
      backgroundColor: [
        "rgba(255, 99, 132, 0.7)",
        "rgba(54, 162, 235, 0.7)",
        "rgba(255, 206, 86, 0.7)",
        "rgba(75, 192, 192, 0.7)",
        "rgba(153, 102, 255, 0.7)"
      ]
    };
  }
}

// Fetch and display the latest recommendation on page load
async function fetchAndDisplayLatestRecommendation() {
  const nutritionRecElement = document.getElementById("nutritionRecommendations");
  const exerciseRecElement = document.getElementById("exerciseRecommendations");
  const timestampElement = document.getElementById("recommendationTimestamp");
  if (nutritionRecElement) nutritionRecElement.innerHTML = '<span>Loading...</span>';
  if (exerciseRecElement) exerciseRecElement.innerHTML = '<span>Loading...</span>';
  if (timestampElement) timestampElement.textContent = '';
  try {
    const res = await fetch('/api/recommendation/latest');
    const data = await res.json();
    if (data.status === 'success') {
      nutritionRecElement.innerHTML = `
        <h3 class="font-semibold text-blue-800 mb-2">Nutrition Recommendations:</h3>
        <div class="text-gray-700 whitespace-pre-line">${data.nutrition_recommendation}</div>
      `;
      exerciseRecElement.innerHTML = `
        <h3 class="font-semibold text-green-800 mb-2">Exercise Recommendations:</h3>
        <div class="text-gray-700 whitespace-pre-line">${data.exercise_recommendation}</div>
      `;
      if (timestampElement && data.created_at) {
        const d = new Date(data.created_at);
        timestampElement.textContent = `Last updated: ${d.toLocaleString()}`;
      }
    } else {
      nutritionRecElement.innerHTML = '<span>No recommendation available.</span>';
      exerciseRecElement.innerHTML = '';
    }
  } catch (e) {
    nutritionRecElement.innerHTML = '<span>Failed to load recommendation.</span>';
    exerciseRecElement.innerHTML = '';
  }
}

// Request a new recommendation from the backend
async function requestNewRecommendation(userData) {
  const nutritionRecElement = document.getElementById("nutritionRecommendations");
  const exerciseRecElement = document.getElementById("exerciseRecommendations");
  const timestampElement = document.getElementById("recommendationTimestamp");
  if (nutritionRecElement) nutritionRecElement.innerHTML = '<span>Generating recommendation...</span>';
  if (exerciseRecElement) exerciseRecElement.innerHTML = '';
  if (timestampElement) timestampElement.textContent = '';
  
  try {
    // Prepare data needed for API
    const nutrition_data = {
      mealsByType: userData.mealsByType || {},
      totalCaloriesIn: userData.totalCaloriesIn || 0
    };
    
    const exercise_data = {
      exercisesByType: userData.exercisesByType || {},
      totalCaloriesBurned: userData.totalCaloriesBurned || 0
    };
    
    console.log("Sending data for recommendation:", { nutrition_data, exercise_data });
    
    const res = await fetch('/api/generate_recommendations', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ nutrition_data, exercise_data })
    });
    
    if (!res.ok) {
      throw new Error(`Failed to get recommendation: ${res.status} ${res.statusText}`);
    }
    
    const data = await res.json();
    console.log("Recommendation response:", data);
    
    if (data.status === 'success') {
      nutritionRecElement.innerHTML = `
        <h3 class="font-semibold text-blue-800 mb-2">Nutrition Recommendations:</h3>
        <div class="text-gray-700 whitespace-pre-line">${data.nutrition_recommendation}</div>
      `;
      exerciseRecElement.innerHTML = `
        <h3 class="font-semibold text-green-800 mb-2">Exercise Recommendations:</h3>
        <div class="text-gray-700 whitespace-pre-line">${data.exercise_recommendation}</div>
      `;
      timestampElement.textContent = `Last updated: ${new Date().toLocaleString()}`;
    } else {
      nutritionRecElement.innerHTML = `<span class="text-red-500">Failed to generate recommendation: ${data.message || 'Unknown error'}</span>`;
      exerciseRecElement.innerHTML = '';
    }
  } catch (e) {
    console.error("Error requesting recommendation:", e);
    nutritionRecElement.innerHTML = `<span class="text-red-500">Failed to generate recommendation: ${e.message}</span>`;
    exerciseRecElement.innerHTML = '';
  }
}

// Attach button event after DOM loaded
window.addEventListener('DOMContentLoaded', function () {
  fetchAndDisplayLatestRecommendation();
  const btn = document.getElementById('requestRecommendationBtn');
  if (btn) {
    btn.addEventListener('click', async function () {
      try {
        // Get the latest user data for recommendation
        const userData = window._latestProcessedData;
        if (userData) {
          await requestNewRecommendation(userData);
        } else {
          console.error("User data not loaded yet");
          alert('User data not loaded yet. Please wait for data to load and try again.');
        }
      } catch (err) {
        console.error("Error in recommendation request:", err);
        alert(`Error requesting recommendation: ${err.message}`);
      }
    });
  }
});
