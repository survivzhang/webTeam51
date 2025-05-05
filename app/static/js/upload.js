document.addEventListener("input", async function (e) {
  if (!e.target.matches('input[name="food_name"]')) return;

  const query = e.target.value;
  if (query.length < 2) return;

  const res = await fetch(`/autocomplete?query=${encodeURIComponent(query)}`);
  const suggestions = await res.json();

  let datalist = e.target.nextElementSibling;
  if (!datalist || datalist.tagName !== "DATALIST") {
    datalist = document.createElement("datalist");
    datalist.id = `suggestions-${Math.random().toString(36).substring(2, 8)}`;
    e.target.setAttribute("list", datalist.id);
    e.target.parentNode.appendChild(datalist);
  }

  datalist.innerHTML = "";
  suggestions.forEach((food) => {
    const option = document.createElement("option");
    option.value = food;
    datalist.appendChild(option);
  });
});

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

  if (addButton && container) {
    addButton.addEventListener("click", function () {
      const entry = container.querySelector(".food-entry");
      if (!entry) return;

      const newEntry = entry.cloneNode(true);
      newEntry.querySelectorAll("input").forEach((input) => (input.value = ""));
      container.appendChild(newEntry);
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

  mealForm.addEventListener("submit", function (e) {
    const mealType = document.getElementById("meal-type").value;
    const calories = document.getElementById("calories").value;

    if (!mealType || !calories) {
      e.preventDefault();
      showValidationError("Please select a meal type and enter calories");
    }
  });

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
