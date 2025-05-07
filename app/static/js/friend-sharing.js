// Sidebar navigation functionality
document.querySelectorAll(".sidebar-nav-item").forEach((item) => {
  item.addEventListener("click", function (e) {
    e.preventDefault();

    // Remove active class from all nav items
    document.querySelectorAll(".sidebar-nav-item").forEach((navItem) => {
      navItem.classList.remove("active", "bg-blue-50", "text-cal-blue");
      navItem.classList.add("text-gray-700");
    });

    // Add active class to clicked item
    this.classList.add("active", "bg-blue-50", "text-cal-blue");
    this.classList.remove("text-gray-700");

    // Hide all content sections
    document.querySelectorAll(".content-section").forEach((section) => {
      section.classList.add("hidden");
      section.classList.remove("block");
    });

    // Show the target section
    const targetId = this.getAttribute("href").substring(1);
    document.getElementById(targetId).classList.remove("hidden");
    document.getElementById(targetId).classList.add("block");
  });
});

// Create notification modal container if it doesn't exist
if (!document.getElementById('notification-modal')) {
  const modalContainer = document.createElement('div');
  modalContainer.id = 'notification-modal';
  modalContainer.className = 'fixed inset-0 flex items-center justify-center z-50 hidden';
  modalContainer.innerHTML = `
    <div class="fixed inset-0 bg-black bg-opacity-30" id="modal-overlay"></div>
    <div class="bg-white rounded-lg shadow-lg p-6 max-w-md w-full mx-4 relative z-10 transform transition-all">
      <div class="flex items-start mb-4">
        <div id="modal-icon" class="flex-shrink-0 w-10 h-10 flex items-center justify-center rounded-full mr-4"></div>
        <div class="flex-1">
          <h3 id="modal-title" class="text-lg font-semibold text-gray-900"></h3>
          <p id="modal-message" class="mt-2 text-gray-600"></p>
        </div>
      </div>
      <div class="mt-6 flex justify-end">
        <button id="modal-close-btn" class="px-4 py-2 bg-cal-blue text-white rounded-md hover:bg-cal-blue-dark transition-colors">
          OK
        </button>
      </div>
    </div>
  `;
  document.body.appendChild(modalContainer);
  
  // Close modal when clicking the overlay or close button
  document.getElementById('modal-overlay').addEventListener('click', hideNotification);
  document.getElementById('modal-close-btn').addEventListener('click', hideNotification);
}

// Show notification function
function showNotification(type, title, message) {
  const modal = document.getElementById('notification-modal');
  const modalTitle = document.getElementById('modal-title');
  const modalMessage = document.getElementById('modal-message');
  const modalIcon = document.getElementById('modal-icon');
  
  modalTitle.textContent = title;
  modalMessage.textContent = message;
  
  // Set icon and color based on notification type
  if (type === 'success') {
    modalIcon.innerHTML = '<i data-lucide="check-circle" class="w-8 h-8 text-green-500"></i>';
    modalIcon.className = 'flex-shrink-0 w-10 h-10 flex items-center justify-center rounded-full mr-4 bg-green-100';
  } else if (type === 'error') {
    modalIcon.innerHTML = '<i data-lucide="alert-circle" class="w-8 h-8 text-red-500"></i>';
    modalIcon.className = 'flex-shrink-0 w-10 h-10 flex items-center justify-center rounded-full mr-4 bg-red-100';
  } else if (type === 'info') {
    modalIcon.innerHTML = '<i data-lucide="info" class="w-8 h-8 text-cal-blue"></i>';
    modalIcon.className = 'flex-shrink-0 w-10 h-10 flex items-center justify-center rounded-full mr-4 bg-blue-100';
  } else if (type === 'warning') {
    modalIcon.innerHTML = '<i data-lucide="alert-triangle" class="w-8 h-8 text-yellow-500"></i>';
    modalIcon.className = 'flex-shrink-0 w-10 h-10 flex items-center justify-center rounded-full mr-4 bg-yellow-100';
  }
  
  // Show modal
  modal.classList.remove('hidden');
  
  // Initialize Lucide icons in the modal
  lucide.createIcons({
    attrs: {
      class: ["w-8", "h-8"]
    },
    icons: {
      'check-circle': lucide.icons['check-circle'],
      'alert-circle': lucide.icons['alert-circle'],
      'info': lucide.icons['info'],
      'alert-triangle': lucide.icons['alert-triangle']
    }
  });
}

// Hide notification function
function hideNotification() {
  const modal = document.getElementById('notification-modal');
  modal.classList.add('hidden');
}

// Friend search functionality
const searchInput = document.getElementById("friend-search");
const searchResults = document.getElementById("search-results");
let searchTimeout;
let selectedUserId = null;

searchInput.addEventListener("input", () => {
  clearTimeout(searchTimeout);
  const query = searchInput.value.trim();
  selectedUserId = null;

  if (query === "") {
    searchResults.classList.add("hidden");
    return;
  }

  console.log(`Searching for friends: keyword=${query}`);

  searchTimeout = setTimeout(() => {
    fetch(`/api/users/search?q=${encodeURIComponent(query)}`, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    })
      .then((response) => {
        console.log("Response status:", response.status);
        console.log("Response headers:", [...response.headers.entries()]);

        // Try to parse JSON response regardless of success or failure
        return response
          .json()
          .then((data) => ({
            status: response.status,
            data: data,
          }))
          .catch((err) => {
            // If JSON parsing fails, return error information
            console.error("JSON parsing error:", err);
            return {
              status: response.status,
              data: {
                users: [],
                error: "Server returned a non-JSON format response",
              },
            };
          });
      })
      .then((result) => {
        console.log("Response data:", result);
        searchResults.innerHTML = "";

        if (result.status >= 200 && result.status < 300) {
          if (!result.data.users || result.data.users.length === 0) {
            searchResults.innerHTML =
              '<div class="p-3 text-gray-500 text-sm">No users found</div>';
          } else {
            result.data.users.forEach((user) => {
              const userItem = document.createElement("div");
              userItem.className = "p-3 hover:bg-gray-100 cursor-pointer";
              userItem.textContent = user.username;
              userItem.dataset.userId = user.id;

              userItem.addEventListener("click", () => {
                searchInput.value = user.username;
                selectedUserId = user.id;
                searchResults.classList.add("hidden");
              });

              searchResults.appendChild(userItem);
            });
          }
        } else {
          searchResults.innerHTML = `<div class="p-3 text-red-500 text-sm">${
            result.data.error || "Search failed"
          }</div>`;
        }

        searchResults.classList.remove("hidden");
      })
      .catch((error) => {
        console.error("Network error while searching for users:", error);
        searchResults.innerHTML =
          '<div class="p-3 text-red-500 text-sm">Error occurred during search</div>';
        searchResults.classList.remove("hidden");
      });
  }, 300);
});

// Send button for friend request
document
  .getElementById("send-friend-request-btn")
  .addEventListener("click", function () {
    if (selectedUserId) {
      sendFriendRequest(selectedUserId);
      searchInput.value = "";
      selectedUserId = null;
    } else {
      showNotification('warning', 'User Selection Required', 'Please select a user from the search results');
    }
  });

// Data friend search filter functionality
const dataFriendSearch = document.getElementById("data-friend-search");
const dataFriendItems = document.querySelectorAll(".data-friend-item");

dataFriendSearch.addEventListener("input", () => {
  const query = dataFriendSearch.value.trim().toLowerCase();

  dataFriendItems.forEach((item) => {
    const username = item.querySelector("span").textContent.toLowerCase();
    if (username.includes(query) || query === "") {
      item.style.display = "flex";
    } else {
      item.style.display = "none";
    }
  });
});

// Share friend search functionality
const shareFriendSearch = document.getElementById("share-friend-search");
let selectedShareUserId = null;

shareFriendSearch.addEventListener("input", () => {
  // Clear any previous selection
  selectedShareUserId = null;
  const selectedFriendDiv = document.getElementById("selected-friend");
  selectedFriendDiv.classList.add("hidden");

  // Disable sharing button
  const saveButton = document.getElementById("save-sharing-settings");
  saveButton.setAttribute("disabled", "");
  saveButton.classList.add("opacity-50", "cursor-not-allowed");
});

// Select friend button
document
  .getElementById("select-friend-btn")
  .addEventListener("click", function () {
    const query = shareFriendSearch.value.trim();

    if (query === "") {
      showNotification('warning', 'Missing Information', 'Please enter a search term');
      return;
    }

    console.log(`Selecting sharing friend: keyword=${query}`);

    fetch(`/api/users/search?q=${encodeURIComponent(query)}`, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    })
      .then((response) => {
        console.log("Response status:", response.status);
        console.log("Response headers:", [...response.headers.entries()]);

        // Try to parse JSON response regardless of success or failure
        return response
          .json()
          .then((data) => ({
            status: response.status,
            data: data,
          }))
          .catch((err) => {
            // If JSON parsing fails, return error information
            console.error("JSON parsing error:", err);
            return {
              status: response.status,
              data: {
                users: [],
                error: "Server returned a non-JSON format response",
              },
            };
          });
      })
      .then((result) => {
        console.log("Response data:", result);

        if (result.status >= 200 && result.status < 300) {
          if (result.data.users && result.data.users.length > 0) {
            // Select the first matching user
            const user = result.data.users[0];
            selectedShareUserId = user.id;

            // Show selected friend
            const selectedFriendDiv =
              document.getElementById("selected-friend");
            selectedFriendDiv.querySelector("span").textContent = user.username;
            selectedFriendDiv.classList.remove("hidden");

            // Enable sharing button
            const saveButton = document.getElementById("save-sharing-settings");
            saveButton.removeAttribute("disabled");
            saveButton.classList.remove("opacity-50", "cursor-not-allowed");
          } else {
            showNotification('info', 'No Results', 'No matching users found');
          }
        } else {
          showNotification('error', 'Search Failed', result.data.error || `Failed to search users (Code: ${result.status})`);
        }
      })
      .catch((error) => {
        console.error("Network error while searching for users:", error);
        showNotification('error', 'Network Error', 'Network error occurred while searching for users, please try again later');
      });
  });

// Remove selected friend
document
  .getElementById("remove-selected-friend")
  .addEventListener("click", function () {
    const selectedFriendDiv = document.getElementById("selected-friend");
    selectedFriendDiv.classList.add("hidden");
    shareFriendSearch.value = "";
    selectedShareUserId = null;

    // Disable sharing button
    const saveButton = document.getElementById("save-sharing-settings");
    saveButton.setAttribute("disabled", "");
    saveButton.classList.add("opacity-50", "cursor-not-allowed");
  });

// Hide search results when clicking outside
document.addEventListener("click", (e) => {
  if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
    searchResults.classList.add("hidden");
  }
});

// Send friend request function
function sendFriendRequest(friendId) {
  if (!friendId) {
    showNotification('warning', 'Selection Required', 'Please select a user first');
    return;
  }

  // Ensure friendId is a number
  friendId = parseInt(friendId, 10);
  if (isNaN(friendId)) {
    showNotification('error', 'Invalid Selection', 'Invalid user ID');
    return;
  }

  console.log(
    `Preparing to send friend request: ID=${friendId}, Type=${typeof friendId}`
  );
  const requestData = { friend_id: friendId };
  console.log("Request data:", requestData);
  const jsonData = JSON.stringify(requestData);
  console.log("JSON string:", jsonData);

  fetch("/api/friend/request", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: jsonData,
  })
    .then((response) => {
      console.log("Response status:", response.status);
      console.log("Response headers:", [...response.headers.entries()]);

      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        return response.json().then((data) => ({
          status: response.status,
          data: data,
        }));
      } else {
        console.error("Non-JSON response received");
        return response.text().then((text) => {
          console.error("Response text:", text);
          throw new Error("Server returned non-JSON response");
        });
      }
    })
    .then((result) => {
      if (result.status >= 200 && result.status < 300) {
        console.log("Success response:", result.data);
        
        // Show success notification and wait for user to click OK before reloading
        const modal = document.getElementById('notification-modal');
        const closeBtn = document.getElementById('modal-close-btn');
        
        // Create a new function for one-time event handler
        const handleClose = function() {
          window.location.reload();
          closeBtn.removeEventListener('click', handleClose);
          document.getElementById('modal-overlay').removeEventListener('click', handleClose);
        };
        
        // Replace existing event listeners with new ones
        closeBtn.removeEventListener('click', hideNotification);
        document.getElementById('modal-overlay').removeEventListener('click', hideNotification);
        
        // Add event listeners with page reload
        closeBtn.addEventListener('click', handleClose);
        document.getElementById('modal-overlay').addEventListener('click', handleClose);
        
        // Show the notification
        showNotification('success', 'Friend Request Sent Successfully', result.data.message || 'Friend request has been sent successfully');
      } else {
        console.error("Error response:", result.data);
        showNotification('error', 'Request Failed', result.data.message || 'Failed to send friend request');
      }
    })
    .catch((error) => {
      console.error("Request error:", error);
      showNotification('error', 'Network Error', 'Error occurred while sending friend request: ' + error.message);
    });
}

// Handle friend request responses
document.querySelectorAll(".accept-request").forEach((button) => {
  button.addEventListener("click", function () {
    const requestElement = this.closest("[data-request-id]");
    if (!requestElement) {
      showNotification('error', 'Request Error', 'Could not identify this request');
      return;
    }

    const requestId = requestElement.dataset.requestId;
    respondToRequest(requestId, "accept");
  });
});

document.querySelectorAll(".decline-request").forEach((button) => {
  button.addEventListener("click", function () {
    const requestElement = this.closest("[data-request-id]");
    if (!requestElement) {
      showNotification('error', 'Request Error', 'Could not identify this request');
      return;
    }

    const requestId = requestElement.dataset.requestId;
    respondToRequest(requestId, "decline");
  });
});

function respondToRequest(requestId, action) {
  if (!requestId || !action) {
    showNotification('error', 'Missing Information', 'Missing necessary information for processing');
    return;
  }

  // Ensure requestId is a number
  requestId = parseInt(requestId, 10);
  if (isNaN(requestId)) {
    showNotification('error', 'Invalid Request', 'Invalid request ID');
    return;
  }

  console.log(
    `Preparing to process friend request: ID=${requestId}, Type=${typeof requestId}, Action=${action}`
  );
  const requestData = { request_id: requestId, action: action };
  console.log("Request data:", requestData);
  const jsonData = JSON.stringify(requestData);
  console.log("JSON string:", jsonData);

  fetch("/api/friend/respond", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: jsonData,
  })
    .then((response) => {
      console.log("Response status:", response.status);
      console.log("Response headers:", [...response.headers.entries()]);

      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        return response.json().then((data) => ({
          status: response.status,
          data: data,
        }));
      } else {
        console.error("Non-JSON response received");
        return response.text().then((text) => {
          console.error("Response text:", text);
          throw new Error("Server returned non-JSON response");
        });
      }
    })
    .then((result) => {
      if (result.status >= 200 && result.status < 300) {
        console.log("Success response:", result.data);
        
        const actionText = action === 'accept' ? 'accepted' : 'declined';
        showNotification('success', 'Request Processed', result.data.message || `Friend request has been ${actionText}`);

        // Remove the responded request element
        const requestElement = document.querySelector(
          `[data-request-id="${requestId}"]`
        );
        if (requestElement) {
          requestElement.remove();
        }

        // If no more requests, show "No pending requests" message
        if (document.querySelectorAll("#friend-requests > div").length === 0) {
          document.getElementById("friend-requests").innerHTML =
            '<p class="text-gray-500 text-sm italic">No pending friend requests</p>';
        }

        // If the request was accepted, refresh the page to show the new friend
        if (action === "accept") {
          window.location.reload();
        }
      } else {
        console.error("Error response:", result.data);
        showNotification('error', 'Process Failed', result.data.message || 'Failed to process friend request');
      }
    })
    .catch((error) => {
      console.error("Request error:", error);
      showNotification('error', 'Network Error', 'Error occurred while processing friend request: ' + error.message);
    });
}

// Friend selection and data visualization
let currentChart = null;

document.querySelectorAll(".friend-item, .data-friend-item").forEach((item) => {
  item.addEventListener("click", function () {
    const friendId = this.dataset.friendId;
    loadFriendData(friendId);

    // Highlight selected friend in all lists
    document
      .querySelectorAll(".friend-item, .data-friend-item")
      .forEach((el) => {
        el.classList.remove("bg-cal-blue-light", "text-white");
        el.classList.add("bg-gray-50");
      });

    document
      .querySelectorAll(
        `.friend-item[data-friend-id="${friendId}"], .data-friend-item[data-friend-id="${friendId}"]`
      )
      .forEach((el) => {
        el.classList.remove("bg-gray-50");
        el.classList.add("bg-cal-blue-light", "text-white");
      });

    // If clicking from friend management, switch to friend data tab
    if (this.classList.contains("friend-item")) {
      document.querySelector('.sidebar-nav-item[href="#friend-data"]').click();
    }
  });
});

function loadFriendData(friendId) {
  if (!friendId) {
    console.error("No friend ID provided for data loading");
    document.getElementById("friend-data-container").innerHTML = `
            <div class="text-center p-4">
                <i data-lucide="alert-circle" class="w-8 h-8 mx-auto text-red-500"></i>
                <p class="mt-2 text-red-500">Invalid friend selection</p>
            </div>`;
    lucide.createIcons();
    return;
  }

  document.getElementById("friend-data-container").innerHTML = `
        <div class="flex items-center justify-center h-full">
            <div class="text-center">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-cal-blue"></div>
                <p class="mt-2 text-sm text-gray-600">Loading friend data...</p>
            </div>
        </div>`;

  fetch(`/api/friend/data/${friendId}`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  })
    .then((response) => {
      return response
        .json()
        .then((data) => ({
          status: response.status,
          data: data,
        }))
        .catch((err) => {
          console.error("JSON parsing error:", err);
          return {
            status: response.status,
            data: {
              status: "error",
              message: "Server returned invalid data format",
            },
          };
        });
    })
    .then((result) => {
      console.log("Response complete data:", result);

      if (
        result.status >= 200 &&
        result.status < 300 &&
        result.data.status === "success"
      ) {
        // Store data in localStorage
        try {
          localStorage.setItem(`friendData_${friendId}`, JSON.stringify(result.data));
        } catch (e) {
          console.error("Error saving to localStorage:", e);
        }
        renderFriendData(result.data);
      } else {
        document.getElementById("friend-data-container").innerHTML = `
                    <div class="text-center p-4">
                        <i data-lucide="alert-circle" class="w-8 h-8 mx-auto text-red-500"></i>
                        <p class="mt-2 text-red-500">${
                          result.data.message ||
                          `Failed to load data (Code: ${result.status})`
                        }</p>
                    </div>`;
        lucide.createIcons();
      }
    })
    .catch((error) => {
      console.error("Network error loading friend data:", error);
      document.getElementById("friend-data-container").innerHTML = `
                <div class="text-center p-4">
                    <i data-lucide="alert-circle" class="w-8 h-8 mx-auto text-red-500"></i>
                    <p class="mt-2 text-red-500">Network error occurred while loading data</p>
                    <p class="text-sm text-gray-500">${error.message || ""}</p>
                </div>`;
      lucide.createIcons();
    });
}

function renderFriendData(data) {
  document.getElementById("friend-data-container").innerHTML = "";
  document
    .getElementById("friend-data-container")
    .classList.remove("flex", "items-center", "justify-center");

  // Create header
  const headerElement = document.createElement("div");
  headerElement.className = "mb-4";
  headerElement.innerHTML = `<h3 class="text-lg font-medium">${data.username}'s Shared Data</h3>`;
  document.getElementById("friend-data-container").appendChild(headerElement);

  // Group data by type
  const meals = data.data.filter((item) => item.type === "meal");
  const exercises = data.data.filter((item) => item.type === "exercise");

  // Create section for meals
  const mealsSection = document.createElement("div");
  mealsSection.className = "mb-6";
  mealsSection.innerHTML = `
            <h4 class="text-md font-medium mb-2 flex items-center">
                <i data-lucide="utensils" class="w-4 h-4 mr-2 text-blue-600"></i>
                Meals
            </h4>
        `;

  if (meals.length > 0) {
    const mealsTable = document.createElement("div");
    mealsTable.className = "overflow-x-auto";
    mealsTable.innerHTML = `
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Meal</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Calories</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200" id="meals-table-body">
                    </tbody>
                </table>
            `;
    mealsSection.appendChild(mealsTable);

    const mealsTableBody = mealsTable.querySelector("#meals-table-body");
    meals.forEach((meal) => {
      const row = document.createElement("tr");
      row.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${meal.date}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-blue-600">${meal.meal_type}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">${meal.calories} cal</td>
                `;
      mealsTableBody.appendChild(row);
    });
    
    // Add Calorie Intake Distribution pie chart
    const mealChartContainer = document.createElement("div");
    mealChartContainer.className = "mt-6 border p-4 rounded-md";
    mealChartContainer.innerHTML = `
        <h5 class="text-lg font-medium mb-4 text-center">Calorie Intake Distribution</h5>
        <div id="meal-pie-chart" style="height: 400px; width: 100%; position: relative;"></div>
    `;
    mealsSection.appendChild(mealChartContainer);
    
    // Render meal pie chart after DOM is updated
    setTimeout(() => {
      renderMealPieChart(meals);
    }, 100);
  } else {
    mealsSection.innerHTML += `<p class="text-sm text-gray-500 italic">No meal data shared</p>`;
  }

  document.getElementById("friend-data-container").appendChild(mealsSection);

  // Create section for exercises
  const exercisesSection = document.createElement("div");
  exercisesSection.className = "mb-6";
  exercisesSection.innerHTML = `
            <h4 class="text-md font-medium mb-2 flex items-center">
                <i data-lucide="activity" class="w-4 h-4 mr-2 text-green-600"></i>
                Exercises
            </h4>
        `;

  if (exercises.length > 0) {
    const exercisesTable = document.createElement("div");
    exercisesTable.className = "overflow-x-auto";
    exercisesTable.innerHTML = `
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Exercise</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Duration</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Calories Burned</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200" id="exercises-table-body">
                    </tbody>
                </table>
            `;
    exercisesSection.appendChild(exercisesTable);

    const exercisesTableBody = exercisesTable.querySelector("#exercises-table-body");
    exercises.forEach((exercise) => {
      const row = document.createElement("tr");
      row.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${exercise.date}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600">${exercise.exercise_type}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${exercise.duration} min</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">${exercise.calories_burned || "-"} cal</td>
                `;
      exercisesTableBody.appendChild(row);
    });
    
    // Add Calorie Burn Distribution pie chart
    const exerciseChartContainer = document.createElement("div");
    exerciseChartContainer.className = "mt-6 border p-4 rounded-md";
    exerciseChartContainer.innerHTML = `
        <h5 class="text-lg font-medium mb-4 text-center">Calorie Burn Distribution</h5>
        <div id="exercise-pie-chart" style="height: 400px; width: 100%; position: relative;"></div>
    `;
    exercisesSection.appendChild(exerciseChartContainer);
    
    // Render exercise pie chart after DOM is updated
    setTimeout(() => {
      renderExercisePieChart(exercises);
    }, 100);
  } else {
    exercisesSection.innerHTML += `<p class="text-sm text-gray-500 italic">No exercise data shared</p>`;
  }

  document.getElementById("friend-data-container").appendChild(exercisesSection);

  // Prepare chart data for the main chart (line chart)
  const chartData = prepareChartData(data.data);
  renderChart(chartData);

  // Initialize Lucide icons in the added DOM elements
  lucide.createIcons();
}

function prepareChartData(entries) {
  // Group entries by date and type
  const entriesByDate = {};
  const types = new Set();

  if (!entries || entries.length === 0) {
    return {
      labels: [],
      datasets: [],
    };
  }

  // Initialize date structure
  entries.forEach((entry) => {
    if (!entriesByDate[entry.date]) {
      entriesByDate[entry.date] = {};
    }

    // Determine type for chart
    let chartType;
    if (entry.type === "meal") {
      chartType = "meal";
    } else if (entry.type === "exercise") {
      chartType = "exercise";
    } else if (entry.type === "metrics") {
      if (entry.weight) chartType = "weight";
      else if (entry.sleep_hours) chartType = "sleep";
      else {
        // Skip mood as it's not numeric
        return; // Return inside forEach callback is ok
      }
    }

    types.add(chartType);

    // Add value to the date
    entriesByDate[entry.date][chartType] =
      (entriesByDate[entry.date][chartType] || 0) + entry.value;
  });

  // Sort dates
  const sortedDates = Object.keys(entriesByDate).sort();

  // Prepare datasets
  const datasets = [];
  const typeColors = {
    meal: "#3b82f6", // blue
    exercise: "#22c55e", // green
    weight: "#8b5cf6", // purple
    sleep: "#6366f1", // indigo
  };

  types.forEach((type) => {
    datasets.push({
      label: type.charAt(0).toUpperCase() + type.slice(1),
      data: sortedDates.map((date) => entriesByDate[date][type] || 0),
      backgroundColor: typeColors[type] || "#94a3b8",
      borderColor: typeColors[type] || "#94a3b8",
      borderWidth: 1,
    });
  });

  return {
    labels: sortedDates,
    datasets: datasets,
  };
}

function renderChart(chartData) {
  const ctx = document.getElementById("chart-container");

  // Destroy existing chart if it exists
  if (currentChart) {
    currentChart.destroy();
  }

  if (!chartData.labels || chartData.labels.length === 0) {
    ctx.innerHTML =
      '<p class="text-center text-gray-500 pt-4">No data available to display</p>';
    return;
  }

  currentChart = new Chart(ctx, {
    type: "bar",
    data: chartData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Value",
          },
        },
        x: {
          title: {
            display: true,
            text: "Date",
          },
        },
      },
    },
  });
}

document
  .getElementById("save-sharing-settings")
  .addEventListener("click", function () {
    if (!selectedShareUserId) {
      showNotification('warning', 'Friend Selection Required', 'Please search and select a friend to share data with');
      return;
    }

    // Ensure selectedShareUserId is a number
    selectedShareUserId = parseInt(selectedShareUserId, 10);
    if (isNaN(selectedShareUserId)) {
      showNotification('error', 'Invalid Selection', 'Invalid friend ID');
      return;
    }

    // Show loading state
    const originalButtonText = this.textContent;
    this.textContent = "Saving...";
    this.disabled = true;

    // Collect meal types
    const mealTypes = Array.from(
      document.querySelectorAll(".meal-type-checkbox:checked")
    ).map((checkbox) => parseInt(checkbox.value));

    // Collect daily metrics
    const dailyMetrics = Array.from(
      document.querySelectorAll(".metrics-checkbox:checked")
    ).map((checkbox) => checkbox.value);

    // Collect exercise types
    const exerciseTypes = Array.from(
      document.querySelectorAll(".exercise-type-checkbox:checked")
    ).map((checkbox) => checkbox.value);

    const conditions = {
      meal_types: mealTypes,
      daily_metrics: dailyMetrics,
      exercise_types: exerciseTypes,
    };

    console.log(
      `Preparing to save sharing settings: Recipient ID=${selectedShareUserId}, Type=${typeof selectedShareUserId}, Conditions=`,
      conditions
    );
    const requestData = {
      recipient_id: selectedShareUserId,
      conditions: conditions,
    };
    console.log("Request data:", requestData);
    const jsonData = JSON.stringify(requestData);
    console.log("JSON string:", jsonData);

    // Save sharing settings
    fetch("/api/share/settings", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: jsonData,
    })
      .then((response) => {
        console.log("Response status:", response.status);
        console.log("Response headers:", [...response.headers.entries()]);

        // Try to parse JSON response regardless of success or failure
        return response
          .json()
          .then((data) => ({
            status: response.status,
            data: data,
          }))
          .catch((err) => {
            // If JSON parsing fails, return error information
            console.error("JSON parsing error:", err);
            return {
              status: response.status,
              data: { message: "Server returned a non-JSON format response" },
            };
          });
      })
      .then((result) => {
        console.log("Response complete data:", result);

        if (
          result.status >= 200 &&
          result.status < 300 &&
          result.data.status === "success"
        ) {
          showNotification('success', 'Sharing Successfully', result.data.message || "Sharing saved successfully");
        } else {
          showNotification('error', 'Save Failed', result.data.message || `Failed to save sharing settings (Code: ${result.status})`);
        }
      })
      .catch((error) => {
        console.error("Error saving sharing settings:", error);
        showNotification('error', 'Network Error', 'Error occurred while saving sharing settings, please try again later');
      })
      .finally(() => {
        // Reset button state
        this.textContent = originalButtonText;
        this.disabled = false;
      });
  });

// Initialize Lucide icons after DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  lucide.createIcons();

  document
    .getElementById("share-all-data")
    .addEventListener("change", function () {
      const isChecked = this.checked;
      const selectors = [
        ".meal-type-checkbox",
        ".metrics-checkbox",
        ".exercise-type-checkbox",
      ];
      selectors.forEach((selector) => {
        document.querySelectorAll(selector).forEach((checkbox) => {
          checkbox.checked = isChecked;
        });
      });
    });

  // Automatically deselect the 'Select All' checkbox
  document
    .querySelectorAll(
      ".meal-type-checkbox, .metrics-checkbox, .exercise-type-checkbox"
    )
    .forEach((checkbox) => {
      checkbox.addEventListener("change", function () {
        const allCheckboxes = document.querySelectorAll(
          ".meal-type-checkbox, .metrics-checkbox, .exercise-type-checkbox"
        );
        const allChecked = Array.from(allCheckboxes).every((cb) => cb.checked);
        document.getElementById("share-all-data").checked = allChecked;
      });
    });
});

// Render meal pie chart function
function renderMealPieChart(meals) {
  if (!meals || meals.length === 0) return;
  
  console.log("Rendering meal pie chart with data:", meals);
  
  // Check if the pie chart container exists
  const container = document.getElementById('meal-pie-chart');
  if (!container) {
    console.error("Meal pie chart container not found!");
    return;
  }
  
  // Make sure the container is empty
  container.innerHTML = '';
  
  // Create Canvas element
  const canvas = document.createElement('canvas');
  canvas.id = 'meal-pie-canvas';
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  container.appendChild(canvas);
  
  // Group meals by type and sum calories
  const mealsByType = {};
  let totalCalories = 0;
  
  meals.forEach(meal => {
    // Make sure calories is a number
    const calories = parseInt(meal.calories) || 0;
    
    if (!mealsByType[meal.meal_type]) {
      mealsByType[meal.meal_type] = 0;
    }
    
    mealsByType[meal.meal_type] += calories;
    totalCalories += calories;
  });
  
  console.log("Meal calories by type:", mealsByType);
  console.log("Total calories intake:", totalCalories);
  
  if (totalCalories === 0) {
    container.innerHTML = '<p class="text-center text-gray-500">No calorie data available</p>';
    return;
  }
  
  const labels = Object.keys(mealsByType);
  const data = Object.values(mealsByType);
  
  // calculate percentages for labels
  const percentages = data.map(value => ((value / totalCalories) * 100).toFixed(1));
  const labelsWithPercentages = labels.map((label, i) => 
    `${label} (${percentages[i]}%)`
  );
  
  // Color map for meal types
  const colorMap = {
    'Breakfast': '#FF9EB2', // Light pink
    'Lunch': '#74C0FF',     // Light blue
    'Dinner': '#FFE390',    // Light yellow
    'Snacks': '#8FE1D4'     // Light teal
  };
  
  const colors = labels.map(label => colorMap[label] || getRandomColor());
  
  try {
    new Chart(canvas, {
      type: 'pie',
      data: {
        labels: labelsWithPercentages,
        datasets: [{
          data: data,
          backgroundColor: colors,
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Calorie Intake Distribution',
            align: 'center',
            font: {
              size: 16,
              weight: 'bold'
            }
          },
          legend: {
            position: 'right'
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const value = context.raw;
                const percentage = ((value / totalCalories) * 100).toFixed(1);
                return `${context.label.split(' (')[0]}: ${value} cal (${percentage}%)`;
              }
            }
          }
        }
      }
    });
    console.log("Meal pie chart rendered successfully");
  } catch (e) {
    console.error("Failed to render meal pie chart:", e);
    container.innerHTML = '<p class="text-center text-red-500">Failed to create chart</p>';
  }
}

// Render exercise pie chart function
function renderExercisePieChart(exercises) {
  if (!exercises || exercises.length === 0) return;
  
  console.log("Rendering exercise pie chart with data:", exercises);
  
  // Check if the pie chart container exists
  const container = document.getElementById('exercise-pie-chart');
  if (!container) {
    console.error("Exercise pie chart container not found!");
    return;
  }
  
  // Make sure the container is empty
  container.innerHTML = '';
  
  // Create Canvas element
  const canvas = document.createElement('canvas');
  canvas.id = 'exercise-pie-canvas';
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  container.appendChild(canvas);
  
  // Group exercises by type and sum calories burned
  const exercisesByType = {};
  let totalCalories = 0;
  
  exercises.forEach(exercise => {
    // Make sure calories_burned is a number
    const caloriesBurned = parseInt(exercise.calories_burned) || 0;
    
    if (!exercisesByType[exercise.exercise_type]) {
      exercisesByType[exercise.exercise_type] = 0;
    }
    
    exercisesByType[exercise.exercise_type] += caloriesBurned;
    totalCalories += caloriesBurned;
  });
  
  console.log("Exercise calories by type:", exercisesByType);
  console.log("Total calories burned:", totalCalories);
  
  if (totalCalories === 0) {
    container.innerHTML = '<p class="text-center text-gray-500">No calorie data available</p>';
    return;
  }
  
  const labels = Object.keys(exercisesByType);
  const data = Object.values(exercisesByType);
  
  // calculate percentages for labels
  const percentages = data.map(value => ((value / totalCalories) * 100).toFixed(1));
  const labelsWithPercentages = labels.map((label, i) => 
    `${label} (${percentages[i]}%)`
  );
  
  // Color map for exercise types
  const colorMap = {
    'Running': '#FF9EB2',     // Light pink
    'Cycling': '#74C0FF',     // Light blue
    'Swimming': '#FFE390',    // Light yellow 
    'Yoga': '#8FE1D4',        // Light teal
    'Weight Training': '#D8B7FB', // Light purple
    'HIIT': '#A78BFA'         // Purple
  };
  
  const colors = labels.map(label => colorMap[label] || getRandomColor());
  
  try {
    new Chart(canvas, {
      type: 'pie',
      data: {
        labels: labelsWithPercentages,
        datasets: [{
          data: data,
          backgroundColor: colors,
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: false
          },
          legend: {
            position: 'right'
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const value = context.raw;
                const percentage = ((value / totalCalories) * 100).toFixed(1);
                return `${context.label.split(' (')[0]}: ${value} cal (${percentage}%)`;
              }
            }
          }
        }
      }
    });
    console.log("Exercise pie chart rendered successfully");
  } catch (e) {
    console.error("Failed to render exercise pie chart:", e);
    container.innerHTML = '<p class="text-center text-red-500">Failed to create chart</p>';
  }
}

// Helper function to generate random colors
function getRandomColor() {
  const letters = '789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * letters.length)];
  }
  return color;
}
