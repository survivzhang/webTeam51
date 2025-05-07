// --- EXERCISE CALORIE ESTIMATION LOGIC ---
const exerciseTypeSelect = document.getElementById("exercise-type");
const durationInput = document.getElementById("duration");
const caloriesBurnedInput = document.getElementById("calories-burned");
const calorieEstimation = document.getElementById("calorie-estimation");
const estimatedCalories = document.getElementById("estimated-calories");

const metValues = {
  1: 10, // running
  2: 7, // swimming
  3: 8, // cycling
  4: 5, // weightlifting
  5: 3, // yoga
  6: 3.5, // walking
  7: 8, // hiit
  8: 3, // pilates
};

function updateCalorieEstimation() {
  const type = exerciseTypeSelect.value;
  const duration = parseFloat(durationInput.value);
  if (type && duration && !caloriesBurnedInput.value) {
    const met = metValues[type] || 5;
    const weightKg = 70;
    const hours = duration / 60;
    const estimated = Math.round(met * weightKg * hours);
    estimatedCalories.textContent = estimated;
    calorieEstimation.classList.remove("hidden");
  } else {
    calorieEstimation.classList.add("hidden");
  }
}

exerciseTypeSelect?.addEventListener("change", updateCalorieEstimation);
durationInput?.addEventListener("input", updateCalorieEstimation);
caloriesBurnedInput?.addEventListener("input", () => {
  if (caloriesBurnedInput.value) {
    calorieEstimation.classList.add("hidden");
  } else {
    updateCalorieEstimation();
  }
});

// --- ON SUBMIT, SAVE ESTIMATED CALORIES IF INPUT IS EMPTY ---
document
  .getElementById("exercise-form")
  ?.addEventListener("submit", function (e) {
    const type = exerciseTypeSelect.value;
    const duration = durationInput.value;

    if (!type || !duration) {
      e.preventDefault();
      alert("Please select an exercise type and enter duration.");
      return;
    }

    if (!caloriesBurnedInput.value && estimatedCalories.textContent) {
      caloriesBurnedInput.value = estimatedCalories.textContent;
    }
  });

// --- RECENT ACTIVITIES FETCH LOGIC ---
async function fetchRecentEntries() {
  try {
    const res = await fetch("/api/get_all_data");
    const data = await res.json();
    const container = document.getElementById("recent-entries");
    container.innerHTML = "";

    if (data.status === "success" && data.data.length > 0) {
      data.data.forEach((entry) => {
        const div = document.createElement("div");
        div.className = "border rounded-lg p-4";

        if (entry.type === "meal") {
          div.innerHTML = `
            <div class="flex justify-between items-center">
              <span class="text-gray-600">${entry.date}</span>
              <div class="flex gap-4">
                <span class="text-blue-600">${entry.meal_type}</span>
                <span class="text-green-600">${entry.calories} cal</span>
              </div>
            </div>
          `;
        } else {
          div.innerHTML = `
            <div class="flex justify-between items-center">
              <span class="text-gray-600">${entry.date}</span>
              <div class="flex gap-4">
                <span class="text-blue-600">${entry.exercise_type}</span>
                <span class="text-green-600">${entry.duration} min</span>
                ${
                  entry.calories_burned
                    ? `<span class="text-red-600">${entry.calories_burned} cal</span>`
                    : ""
                }
              </div>
            </div>
          `;
        }

        container.appendChild(div);
      });
    } else {
      container.innerHTML = `<p class="text-center text-gray-500">No entries found</p>`;
    }
  } catch (err) {
    console.error("Error loading recent entries:", err);
    document.getElementById(
      "recent-entries"
    ).innerHTML = `<p class="text-center text-red-500">Error loading entries. Please try again.</p>`;
  }
}

fetchRecentEntries();

// --- MEAL FORM LOGIC ---
const mealForm = document.getElementById("meal-form");

// Function to fetch food information
async function fetchFoodInfo(description) {
  try {
    const response = await fetch(
      `/api/food_info?description=${encodeURIComponent(description)}`
    );
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching food info:", error);
    return { success: false, error: "Failed to fetch food information" };
  }
}

// Function to calculate nutrition based on gram amount
function calculateNutrition(foodData, grams) {
  if (!foodData || !foodData.success) return null;

  const multiplier = grams / 100; // Nutrition data is per 100g
  return {
    calories: Math.round(foodData.energy_per_100g * multiplier * 10) / 10,
    proteins: Math.round(foodData.protein_per_100g * multiplier * 10) / 10,
    fats: Math.round(foodData.fat_per_100g * multiplier * 10) / 10,
    carbohydrates: Math.round(foodData.carb_per_100g * multiplier * 10) / 10,
    fiber: Math.round(foodData.fiber_per_100g * multiplier * 10) / 10,
    sugars: Math.round(foodData.sugar_per_100g * multiplier * 10) / 10,
  };
}

// Function to update total nutrition
function updateTotalNutrition() {
  const foodEntries = document.querySelectorAll(".food-entry");
  let totalCalories = 0;
  let totalProteins = 0;
  let totalFats = 0;
  let totalCarbohydrates = 0;
  let totalFiber = 0;
  let totalSugars = 0;

  foodEntries.forEach((entry) => {
    const caloriesEl = entry.querySelector(
      'input[name="calculated_calories[]"]'
    );
    const proteinsEl = entry.querySelector(
      'input[name="calculated_proteins[]"]'
    );
    const fatsEl = entry.querySelector('input[name="calculated_fats[]"]');
    const carbsEl = entry.querySelector(
      'input[name="calculated_carbohydrates[]"]'
    );
    const fiberEl = entry.querySelector('input[name="calculated_fiber[]"]');
    const sugarsEl = entry.querySelector('input[name="calculated_sugars[]"]');

    totalCalories += parseFloat(caloriesEl.value) || 0;
    totalProteins += parseFloat(proteinsEl.value) || 0;
    totalFats += parseFloat(fatsEl.value) || 0;
    totalCarbohydrates += parseFloat(carbsEl.value) || 0;
    totalFiber += parseFloat(fiberEl.value) || 0;
    totalSugars += parseFloat(sugarsEl.value) || 0;
  });

  // Update totals display
  document.getElementById("total-calories").textContent =
    totalCalories.toFixed(1);
  document.getElementById("total-proteins").textContent =
    totalProteins.toFixed(1);
  document.getElementById("total-fats").textContent = totalFats.toFixed(1);
  document.getElementById("total-carbohydrates").textContent =
    totalCarbohydrates.toFixed(1);
  document.getElementById("total-fiber").textContent = totalFiber.toFixed(1);
  document.getElementById("total-sugars").textContent = totalSugars.toFixed(1);

  // Update hidden form fields
  document.getElementById("total_calories").value = totalCalories;
  document.getElementById("total_proteins").value = totalProteins;
  document.getElementById("total_fats").value = totalFats;
  document.getElementById("total_carbohydrates").value = totalCarbohydrates;
  document.getElementById("total_fiber").value = totalFiber;
  document.getElementById("total_sugars").value = totalSugars;
}

// Function to add a new food entry
function addFoodEntry() {
  const container = document.getElementById("food-entries");
  const newEntry = container.querySelector(".food-entry").cloneNode(true);

  // Clear values
  const inputs = newEntry.querySelectorAll("input");
  inputs.forEach((input) => {
    input.value = "";
    if (input.name === "grams_intake[]") {
      input.addEventListener("input", handleGramsChange);
    }
    if (input.id === "food_name") {
      input.addEventListener("change", handleFoodChange);
    }
  });

  container.appendChild(newEntry);
}

// Function to handle food selection change
async function handleFoodChange(event) {
  const foodName = event.target.value;
  const entryDiv = event.target.closest(".food-entry");
  const gramsInput = entryDiv.querySelector('input[name="grams_intake[]"]');

  if (foodName && gramsInput.value) {
    const foodData = await fetchFoodInfo(foodName);
    updateEntryNutrition(entryDiv, foodData, parseFloat(gramsInput.value));
  }
}

// Function to handle grams change
async function handleGramsChange(event) {
  const grams = parseFloat(event.target.value);
  const entryDiv = event.target.closest(".food-entry");
  const foodNameInput = entryDiv.querySelector("#food_name");

  if (foodNameInput.value && grams) {
    const foodData = await fetchFoodInfo(foodNameInput.value);
    updateEntryNutrition(entryDiv, foodData, grams);
  }
}

// Function to update a single entry's nutrition values
function updateEntryNutrition(entryDiv, foodData, grams) {
  if (!foodData || !foodData.success) return;

  const nutrition = calculateNutrition(foodData, grams);
  if (!nutrition) return;

  // Update hidden fields
  entryDiv.querySelector('input[name="calculated_calories[]"]').value =
    nutrition.calories;
  entryDiv.querySelector('input[name="calculated_proteins[]"]').value =
    nutrition.proteins;
  entryDiv.querySelector('input[name="calculated_fats[]"]').value =
    nutrition.fats;
  entryDiv.querySelector('input[name="calculated_carbohydrates[]"]').value =
    nutrition.carbohydrates;
  entryDiv.querySelector('input[name="calculated_fiber[]"]').value =
    nutrition.fiber;
  entryDiv.querySelector('input[name="calculated_sugars[]"]').value =
    nutrition.sugars;

  // Update total nutrition
  updateTotalNutrition();
}

// Add initial event listeners
document.querySelectorAll('input[name="grams_intake[]"]').forEach((input) => {
  input.addEventListener("input", handleGramsChange);
});

document.querySelectorAll("#food_name").forEach((input) => {
  input.addEventListener("change", handleFoodChange);
});

// Fetch food suggestions for datalist
async function fetchFoodSuggestions() {
  try {
    const response = await fetch("/api/food_suggestions");
    const data = await response.json();

    if (data.success) {
      const datalist = document.getElementById("food_suggestions");
      data.suggestions.forEach((suggestion) => {
        const option = document.createElement("option");
        option.value = suggestion;
        datalist.appendChild(option);
      });
    }
  } catch (error) {
    console.error("Error fetching food suggestions:", error);
  }
}

fetchFoodSuggestions();

if (mealForm) {
  mealForm.addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent default form submission

    const mealType = document.getElementById("meal-type")?.value;
    const calories = document.getElementById("total_calories")?.value;
    const proteins = document.getElementById("total_proteins")?.value;
    const fats = document.getElementById("total_fats")?.value;
    const carbohydrates = document.getElementById("total_carbohydrates")?.value;
    const fiber = document.getElementById("total_fiber")?.value;
    const sugars = document.getElementById("total_sugars")?.value;

    if (!mealType || !calories) {
      alert("Please select a meal type and enter calories.");
      return;
    }

    const formData = new FormData();
    formData.append("meal_type_id", mealType);
    formData.append("total_calories", calories);
    formData.append("total_proteins", proteins || 0);
    formData.append("total_fats", fats || 0);
    formData.append("total_carbohydrates", carbohydrates || 0);
    formData.append("total_fiber", fiber || 0);
    formData.append("total_sugars", sugars || 0);

    fetch(mealForm.action, {
      method: "POST",
      body: formData,
      credentials: "same-origin",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          window.location.reload();
        } else {
          alert(data.message || "Error saving meal.");
        }
      })
      .catch((err) => {
        console.error("Error submitting meal:", err);
        alert("Error submitting meal.");
      });
  });
}
