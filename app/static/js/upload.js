function bindAutocomplete(entry) {
  const foodInput = entry.querySelector('input[name="food_name"]');
  const gramsInput = entry.querySelector('input[name="grams_intake[]"]');

  const caloriesInput = entry.querySelector(
    'input[name="calculated_calories[]"]'
  );
  const proteinInput = entry.querySelector(
    'input[name="calculated_protein[]"]'
  );
  const fatInput = entry.querySelector('input[name="calculated_fat[]"]');
  const carbInput = entry.querySelector('input[name="calculated_carb[]"]');
  const fiberInput = entry.querySelector('input[name="calculated_fiber[]"]');
  const sugarInput = entry.querySelector('input[name="calculated_sugar[]"]');

  const newFoodInput = foodInput.cloneNode(true);
  foodInput.parentNode.replaceChild(newFoodInput, foodInput);

  const newGramsInput = gramsInput.cloneNode(true);
  gramsInput.parentNode.replaceChild(newGramsInput, gramsInput);

  newFoodInput.addEventListener("input", () =>
    updateNutrition(newFoodInput, newGramsInput, {
      caloriesInput,
      proteinInput,
      fatInput,
      carbInput,
      fiberInput,
      sugarInput,
    })
  );

  newGramsInput.addEventListener("input", () =>
    newFoodInput.dispatchEvent(new Event("input"))
  );

  fetch("/api/food_suggestions")
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        const datalist = document.getElementById("food_suggestions");
        datalist.innerHTML = "";
        data.suggestions.forEach((food) => {
          const option = document.createElement("option");
          option.value = food;
          datalist.appendChild(option);
        });
      }
    });
}

async function updateNutrition(foodInput, gramsInput, inputs) {
  const food = foodInput.value;
  const grams = parseFloat(gramsInput.value) || 0;
  if (!food || grams <= 0) {
    Object.values(inputs).forEach((input) => (input.value = "0"));
    updateTotalNutrition();
    return;
  }

  try {
    const res = await fetch(
      `/api/food_info?description=${encodeURIComponent(food)}`
    );
    const info = await res.json();
    if (!info.success) return;

    const multiplier = grams / 100;
    const values = {
      calories: parseFloat(info.energy_per_100g || 0) * multiplier,
      protein: parseFloat(info.protein_per_100g || 0) * multiplier,
      fat: parseFloat(info.fat_per_100g || 0) * multiplier,
      carb: parseFloat(info.carb_per_100g || 0) * multiplier,
      fiber: parseFloat(info.fiber_per_100g || 0) * multiplier,
      sugar: parseFloat(info.sugar_per_100g || 0) * multiplier,
    };

    inputs.caloriesInput.value = values.calories.toFixed(1);
    inputs.proteinInput.value = values.protein.toFixed(1);
    inputs.fatInput.value = values.fat.toFixed(1);
    inputs.carbInput.value = values.carb.toFixed(1);
    inputs.fiberInput.value = values.fiber.toFixed(1);
    inputs.sugarInput.value = values.sugar.toFixed(1);

    updateTotalNutrition();
  } catch (err) {
    console.error("Fetch error:", err);
  }
}

function updateTotalNutrition() {
  const entries = document.querySelectorAll(".food-entry");
  const totals = {
    calories: 0,
    protein: 0,
    fat: 0,
    carb: 0,
    fiber: 0,
    sugar: 0,
  };

  entries.forEach((entry) => {
    totals.calories += parseFloat(
      entry.querySelector('input[name="calculated_calories[]"]').value || 0
    );
    totals.protein += parseFloat(
      entry.querySelector('input[name="calculated_protein[]"]').value || 0
    );
    totals.fat += parseFloat(
      entry.querySelector('input[name="calculated_fat[]"]').value || 0
    );
    totals.carb += parseFloat(
      entry.querySelector('input[name="calculated_carb[]"]').value || 0
    );
    totals.fiber += parseFloat(
      entry.querySelector('input[name="calculated_fiber[]"]').value || 0
    );
    totals.sugar += parseFloat(
      entry.querySelector('input[name="calculated_sugar[]"]').value || 0
    );
  });

  document.getElementById("total-calories").textContent =
    totals.calories.toFixed(1);
  document.getElementById("total-protein").textContent =
    totals.protein.toFixed(1);
  document.getElementById("total-fat").textContent = totals.fat.toFixed(1);
  document.getElementById("total-carbs").textContent = totals.carb.toFixed(1);
  document.getElementById("total-fiber").textContent = totals.fiber.toFixed(1);
  document.getElementById("total-sugar").textContent = totals.sugar.toFixed(1);

  document.getElementById("total_calories").value = totals.calories.toFixed(1);
  document.getElementById("total_protein").value = totals.protein.toFixed(1);
  document.getElementById("total_fat").value = totals.fat.toFixed(1);
  document.getElementById("total_carb").value = totals.carb.toFixed(1);
  document.getElementById("total_fiber").value = totals.fiber.toFixed(1);
  document.getElementById("total_sugar").value = totals.sugar.toFixed(1);

  return totals;
}

function addFoodEntry() {
  const container = document.getElementById("food-entries");
  const entry = container.querySelector(".food-entry");
  const newEntry = entry.cloneNode(true);
  newEntry.querySelectorAll("input").forEach((input) => (input.value = ""));
  container.appendChild(newEntry);
  bindAutocomplete(newEntry);
  updateTotalNutrition();
}

document.addEventListener("DOMContentLoaded", function () {
  const exerciseForm = document.getElementById("exercise-form");
  const exerciseTypeSelect = document.getElementById("exercise-type");
  const durationInput = document.getElementById("duration");
  const caloriesBurnedInput = document.getElementById("calories-burned");
  const calorieEstimation = document.getElementById("calorie-estimation");
  const estimatedCalories = document.getElementById("estimated-calories");

  // MET values mapping (activity_type_id: MET)
  const metValues = {
    1: 10, // Running
    2: 7, // Swimming
    3: 8, // Cycling
    4: 5, // Weightlifting
    5: 3, // Yoga
    6: 3.5, // Walking
    7: 8, // HIIT
    8: 3, // Pilates
  };

  function updateCalorieEstimation() {
    const exerciseType = parseInt(exerciseTypeSelect.value);
    const duration = parseFloat(durationInput.value);

    if (exerciseType && duration && !caloriesBurnedInput.value) {
      const weightKg = 70; // default user weight
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

  if (exerciseForm) {
    exerciseForm.addEventListener("submit", function (e) {
      const exerciseType = exerciseTypeSelect.value;
      const duration = durationInput.value;

      if (!exerciseType || !duration) {
        e.preventDefault();
        showValidationError("Please select exercise type and enter duration.");
      }
    });
  }

  function showValidationError(message) {
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
    setTimeout(() => (toast.style.transform = "translateY(0)"), 10);
    setTimeout(() => {
      toast.style.transform = "translateY(100px)";
      setTimeout(() => document.body.removeChild(toast), 300);
    }, 3000);
  }
});
