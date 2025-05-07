function bindAutocomplete(entry) {
  const foodInput = entry.querySelector('input[name="food_name"]');
  const gramsInput = entry.querySelector('input[name="grams_intake[]"]');

  // Get all the hidden nutrition inputs
  const energyInput = entry.querySelector('input[name="calculated_energy[]"]');
  const proteinInput = entry.querySelector(
    'input[name="calculated_protein[]"]'
  );
  const fatInput = entry.querySelector('input[name="calculated_fat[]"]');
  const carbInput = entry.querySelector('input[name="calculated_carb[]"]');
  const fiberInput = entry.querySelector('input[name="calculated_fiber[]"]');
  const sugarInput = entry.querySelector('input[name="calculated_sugar[]"]');

  // Remove any existing event listeners
  const newFoodInput = foodInput.cloneNode(true);
  foodInput.parentNode.replaceChild(newFoodInput, foodInput);

  const newGramsInput = gramsInput.cloneNode(true);
  gramsInput.parentNode.replaceChild(newGramsInput, gramsInput);

  // Add event listeners to the new inputs
  newFoodInput.addEventListener("input", async () => {
    const food = newFoodInput.value;
    const grams = parseFloat(newGramsInput.value) || 0;
    console.log(`Calculating nutrition for ${food} (${grams}g)`);

    if (!food || grams <= 0) {
      console.log("Invalid food or grams value");
      // Reset all nutrition values to 0
      if (energyInput) energyInput.value = "0";
      if (proteinInput) proteinInput.value = "0";
      if (fatInput) fatInput.value = "0";
      if (carbInput) carbInput.value = "0";
      if (fiberInput) fiberInput.value = "0";
      if (sugarInput) sugarInput.value = "0";
      updateTotalNutrition();
      return;
    }

    try {
      const res = await fetch(
        `/api/food_info?description=${encodeURIComponent(food)}`
      );
      const info = await res.json();
      console.log("Food info:", info);

      if (info.success) {
        // Values are per 100g in the database
        const multiplier = grams / 100; // Convert per 100g to actual grams

        const calculatedValues = {
          energy: parseFloat(info.energy_per_100g || 0) * multiplier,
          protein: parseFloat(info.protein_per_100g || 0) * multiplier,
          fat: parseFloat(info.fat_per_100g || 0) * multiplier,
          carb: parseFloat(info.carb_per_100g || 0) * multiplier,
          fiber: parseFloat(info.fiber_per_100g || 0) * multiplier,
          sugar: parseFloat(info.sugar_per_100g || 0) * multiplier,
        };

        console.log(
          `Calculated nutrition for ${grams}g of ${food}:`,
          calculatedValues
        );

        // Update hidden inputs with calculated values
        if (energyInput) energyInput.value = calculatedValues.energy.toFixed(1);
        if (proteinInput)
          proteinInput.value = calculatedValues.protein.toFixed(1);
        if (fatInput) fatInput.value = calculatedValues.fat.toFixed(1);
        if (carbInput) carbInput.value = calculatedValues.carb.toFixed(1);
        if (fiberInput) fiberInput.value = calculatedValues.fiber.toFixed(1);
        if (sugarInput) sugarInput.value = calculatedValues.sugar.toFixed(1);

        updateTotalNutrition();
      } else {
        console.error("Error in food info response:", info.error);
      }
    } catch (error) {
      console.error("Error fetching food info:", error);
    }
  });

  newGramsInput.addEventListener("input", () => {
    // Trigger food input event to recalculate nutrition
    newFoodInput.dispatchEvent(new Event("input"));
  });

  // Add food suggestions
  fetch("/api/food_suggestions")
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        const datalist = document.getElementById("food_suggestions");
        datalist.innerHTML = ""; // Clear existing options
        data.suggestions.forEach((food) => {
          const option = document.createElement("option");
          option.value = food;
          datalist.appendChild(option);
        });
      }
    })
    .catch((error) => console.error("Error fetching food suggestions:", error));
}

function updateTotalNutrition() {
  const entries = document.querySelectorAll(".food-entry");
  let totals = {
    calories: 0,
    protein: 0,
    fat: 0,
    carb: 0,
    fiber: 0,
    sugar: 0,
  };

  entries.forEach((entry) => {
    // Parse values as float and handle null/undefined
    totals.calories += parseFloat(
      entry.querySelector('input[name="calculated_energy[]"]')?.value || 0
    );
    totals.protein += parseFloat(
      entry.querySelector('input[name="calculated_protein[]"]')?.value || 0
    );
    totals.fat += parseFloat(
      entry.querySelector('input[name="calculated_fat[]"]')?.value || 0
    );
    totals.carb += parseFloat(
      entry.querySelector('input[name="calculated_carb[]"]')?.value || 0
    );
    totals.fiber += parseFloat(
      entry.querySelector('input[name="calculated_fiber[]"]')?.value || 0
    );
    totals.sugar += parseFloat(
      entry.querySelector('input[name="calculated_sugar[]"]')?.value || 0
    );
  });

  // Update total nutrition display
  document.getElementById("total-calories").textContent =
    totals.calories.toFixed(1);
  document.getElementById("total-protein").textContent =
    totals.protein.toFixed(1);
  document.getElementById("total-fat").textContent = totals.fat.toFixed(1);
  document.getElementById("total-carbs").textContent = totals.carb.toFixed(1);
  document.getElementById("total-fiber").textContent = totals.fiber.toFixed(1);
  document.getElementById("total-sugar").textContent = totals.sugar.toFixed(1);

  console.log("Updated total nutrition values:", totals);

  return totals;
}

// document.addEventListener("input", async function (e) {
//   if (!e.target.matches('input[name="food_name"]')) return;

//   const query = e.target.value;
//   if (query.length < 2) return;

//   const res = await fetch(`/autocomplete?query=${encodeURIComponent(query)}`);
//   const suggestions = await res.json();

//   let datalist = e.target.nextElementSibling;
//   if (!datalist || datalist.tagName !== "DATALIST") {
//     datalist = document.createElement("datalist");
//     datalist.id = `suggestions-${Math.random().toString(36).substring(2, 8)}`;
//     e.target.setAttribute("list", datalist.id);
//     e.target.parentNode.appendChild(datalist);
//   }

//   datalist.innerHTML = "";
//   suggestions.forEach((food) => {
//     const option = document.createElement("option");
//     option.value = food;
//     datalist.appendChild(option);
//   });
// });

document.addEventListener("DOMContentLoaded", function () {
  // Animate input fields on focus/blur
  const formInputs = document.querySelectorAll("input, select, textarea");
  formInputs.forEach((input) => {
    input.addEventListener("focus", () => {
      input.parentElement.classList.add("scale-105");
      input.classList.add("bg-blue-50");
      setTimeout(() => {
        input.parentElement.classList.remove("scale-105");
      }, 300);
    });

    input.addEventListener("blur", () => {
      input.classList.remove("bg-blue-50");
    });
  });

  // Calorie estimation for exercise form
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
    const exerciseType = exerciseTypeSelect.value;
    const duration = durationInput.value;

    if (exerciseType && duration && !caloriesBurnedInput.value) {
      const weightKg = 70; // default assumption
      const met = metValues[exerciseType] || 5;
      const durationHours = duration / 60;
      const calories = Math.round(met * weightKg * durationHours);
      caloriesBurnedInput.value = calories;
      estimatedCalories.textContent = calories;
      calorieEstimation.classList.remove("hidden");
    } else {
      calorieEstimation.classList.add("hidden");
    }
  }

  if (exerciseTypeSelect && durationInput) {
    exerciseTypeSelect.addEventListener("change", updateCalorieEstimation);
    durationInput.addEventListener("input", updateCalorieEstimation);
  }

  if (caloriesBurnedInput) {
    caloriesBurnedInput.addEventListener("input", () => {
      if (caloriesBurnedInput.value) {
        calorieEstimation.classList.add("hidden");
      } else {
        updateCalorieEstimation();
      }
    });
  }

  // Add another food entry in meal form
  const addButton = document.getElementById("add-food");
  const container = document.getElementById("food-entries");

  // Bind autocomplete to the first entry
  const firstEntry = container.querySelector(".food-entry");
  if (firstEntry) bindAutocomplete(firstEntry);

  if (addButton && container) {
    addButton.addEventListener("click", function () {
      const entry = container.querySelector(".food-entry");
      if (!entry) return;

      const newEntry = entry.cloneNode(true);
      // Clear all input values
      newEntry.querySelectorAll("input").forEach((input) => (input.value = ""));

      // Remove any existing datalists
      const oldDatalist = newEntry.querySelector("datalist");
      if (oldDatalist) oldDatalist.remove();

      container.appendChild(newEntry);
      bindAutocomplete(newEntry);
    });
  }

  // Form validation with visual feedback

  exerciseForm.addEventListener("submit", function (e) {
    const exerciseType = document.getElementById("exercise-type").value;
    const duration = document.getElementById("duration").value;

    if (!exerciseType || !duration) {
      e.preventDefault();
      showValidationError("Please select an exercise type and enter duration");
    }
  });

  // Get the meal form
  const mealForm = document.getElementById("meal-form");

  if (mealForm) {
    mealForm.addEventListener("submit", function (e) {
      e.preventDefault(); // Prevent default form submission

      // Calculate latest totals
      const totals = updateTotalNutrition();
      console.log("Final totals before submission:", totals);

      // Get meal type
      const mealTypeId = document.getElementById("meal-type").value;

      // Validate meal type
      if (!mealTypeId) {
        showValidationError("Please select a meal type");
        return;
      }

      // Create FormData object
      const formData = new FormData();
      formData.append("meal_type_id", mealTypeId);
      formData.append("calories", totals.calories.toString());
      formData.append("proteins", totals.protein.toString());
      formData.append("fats", totals.fat.toString());
      formData.append("carbohydrates", totals.carb.toString());
      formData.append("fiber", totals.fiber.toString());
      formData.append("sugars", totals.sugar.toString());

      // Log the form data for debugging
      console.log("Submitting nutrition data to server:");
      for (let pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
      }

      // Submit the form using fetch
      fetch(mealForm.action, {
        method: "POST",
        body: formData,
        credentials: "same-origin",
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Server response:", data);
          if (data.status === "success") {
            window.location.reload();
          } else {
            showValidationError(data.message);
          }
        })
        .catch((error) => {
          console.error("Error submitting form:", error);
          showValidationError("Error saving meal data");
        });
    });
  }

  function showValidationError(message) {
    // Create and show a toast notification
    const toast = document.createElement("div");
    toast.classList.add(
      "fixed",
      "bottom-4",
      "right-4",
      "bg-red-500",
      "text-white",
      "py-2",
      "px-4",
      "rounded-lg",
      "shadow-lg",
      "z-50",
      "transform",
      "transition-transform",
      "duration-300"
    );
    toast.style.transform = "translateY(100px)";
    toast.textContent = message;

    document.body.appendChild(toast);

    // Animate in
    setTimeout(() => {
      toast.style.transform = "translateY(0)";
    }, 10);

    // Animate out and remove
    setTimeout(() => {
      toast.style.transform = "translateY(100px)";
      setTimeout(() => {
        document.body.removeChild(toast);
      }, 300);
    }, 3000);
  }

  // Helper function to validate form fields and highlight errors
  function validateForm(form, requiredFields) {
    let valid = true;

    form.querySelectorAll(".invalid-feedback").forEach((el) => el.remove());

    requiredFields.forEach((field) => {
      const element = form.elements[field];
      if (!element.value.trim()) {
        valid = false;

        // Add invalid class
        element.classList.add("border-red-500");
        element.classList.remove("border-gray-300");

        // Add invalid feedback message
        const feedback = document.createElement("p");
        feedback.classList.add(
          "text-red-500",
          "text-xs",
          "mt-1",
          "invalid-feedback"
        );
        feedback.textContent = "This field is required";
        element.parentNode.appendChild(feedback);

        // Shake animation
        element.classList.add("shake");
        setTimeout(() => {
          element.classList.remove("shake");
        }, 500);
      } else {
        element.classList.remove("border-red-500");
        element.classList.add("border-gray-300");
      }
    });

    return valid;
  }

  // Fetch recent entries using the API
  async function fetchRecentEntries() {
    try {
      const response = await fetch("/api/get_all_data");
      const data = await response.json();

      const entriesContainer = document.getElementById("recent-entries");
      entriesContainer.innerHTML = ""; // Clear loading message

      if (data.status === "success" && data.data.length > 0) {
        data.data.forEach((entry) => {
          const entryElement = document.createElement("div");
          entryElement.className = "border rounded-lg p-4";

          if (entry.type === "meal") {
            entryElement.innerHTML = `
                                <div class="flex justify-between items-center">
                                    <span class="text-gray-600">${entry.date}</span>
                                    <div class="flex gap-4">
                                        <span class="text-blue-600">${entry.meal_type}</span>
                                        <span class="text-green-600">${entry.calories} cal</span>
                                    </div>
                                </div>
                            `;
          } else {
            entryElement.innerHTML = `
                                <div class="flex justify-between items-center">
                                    <span class="text-gray-600">${
                                      entry.date
                                    }</span>
                                    <div class="flex gap-4">
                                        <span class="text-blue-600">${
                                          entry.exercise_type
                                        }</span>
                                        <span class="text-green-600">${
                                          entry.duration
                                        } min</span>
                                        ${
                                          entry.calories_burned
                                            ? `<span class="text-red-600">${entry.calories_burned} cal</span>`
                                            : ""
                                        }
                                    </div>
                                </div>
                            `;
          }

          entriesContainer.appendChild(entryElement);
        });
      } else {
        entriesContainer.innerHTML =
          '<p class="text-center text-gray-500">No entries found</p>';
      }
    } catch (error) {
      console.error("Error fetching recent entries:", error);
      document.getElementById("recent-entries").innerHTML =
        '<p class="text-center text-red-500">Error loading entries. Please try again.</p>';
    }
  }

  // Fetch data on page load
  fetchRecentEntries();
});

// Add Food Button functionality
function addFoodEntry() {
  const container = document.getElementById("food-entries");
  const entry = container.querySelector(".food-entry");
  if (!entry) return;

  const newEntry = entry.cloneNode(true);
  // Clear all input values
  newEntry.querySelectorAll("input").forEach((input) => (input.value = ""));

  container.appendChild(newEntry);
  bindAutocomplete(newEntry);

  // Update totals
  updateTotalNutrition();
}
