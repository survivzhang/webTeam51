# CalTrack - Calorie Tracker Web App

Group_51 in CITS5505 2025 Semester 1.

| UWA ID    | Name           | GitHub Username   |
|-----------|----------------|-------------------|
| 24064091  | Zichen Zhang   | survivzhang       |
| 23773086  | Jinshu Zhang   | JocelynZhang01    |
| 24042674  | Zhaoyang Lin   | adamslin          |
| 24455032  | Anvesh Reddy M | anvesh1903        |

## Getting Started

Follow the steps below to set up and run the project on your local machine.

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)

### Setup Instructions

#### 1. Check Python & pip Versions

Run the following commands to verify your Python and pip installations:

```bash
# Check Python version
python3 --version  # Linux/macOS
python --version   # Windows

# Check pip version
pip --version
```

#### 2. Create a Virtual Environment

Set up a new virtual environment to manage dependencies:

```bash
# Linux/macOS
python3 -m venv venv

# Windows
python -m venv venv
```

#### 3. Activate the Virtual Environment

Activate the virtual environment:

```bash
# Linux/macOS
source venv/bin/activate


# Windows (Git Bash or WSL)
source venv/Scripts/activate

# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

#### 4. Install Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

#### 5. Run the Flask App

Start the Flask development server:

```bash
# Linux/macOS
python3 app.py

# Windows
python app.py
```

#### 6. Access the App

Open your browser and navigate to the following URL:

```
http://127.0.0.1:5000
```

## :warning: Testing Accounts :warning:

**The project has already included a small database (app.db) with pre-configured test users:**

| Username     | Password  |
|--------------|-----------|
| john_doe     | 123456    |
| jane_smith   | 123456    |

**These accounts come with sample data for testing the application's features without starting from scratch. You can either create brand new accounts (following the Sign Up & Sign In instructions below) or use these testing accounts.**

## Application Features

CalTrack is a comprehensive calorie tracking application designed to help users monitor and manage their health and fitness journey. The application provides robust features for tracking daily calorie intake, recording exercise activities, and analysing nutritional data. Users can set personal weight goals, monitor their progress, and share their achievements with friends for mutual motivation and support. 

### Sign Up & Sign In
Create your account with a simple registration process or log in to access your personalised tracking dashboard. The app securely manages user authentication to protect your health data.

![Registration Page](/app/static/img/register1.png)

When registering, you need to click the "Get Code" button to receive a verification code. You can use a real email address and find the code in your inbox or spam folder, or use a mock email address and view the verification code in the terminal as shown below:

![Sign In Page](/app/static/img/register2.png)

### Home Dashboard
The home dashboard provides an overview of your calorie tracking journey, displaying recent activities and a chart of your calorie intake and output. When you click the "Start tracking" button, you'll be redirected to the upload interface where you can log your exercise and meal data.

![Home Dashboard](/app/static/img/homepage.png)

### Data Upload
The data upload page consists of three main components: Exercise Tracking, Meal Tracking, and Recent Activities.

#### Exercise Tracking
In the Exercise Tracking section, you can:
- Select the type of exercise from the dropdown menu
- Enter the duration of your exercise in minutes
- The system automatically calculates the calories burned based on the exercise type and duration
- Click the "Add Exercise" button to save your exercise data to the database

#### Meal Tracking
In the Meal Tracking section, you can:
- Choose a meal type (Breakfast, Lunch, Dinner, Snacks)
- Search for food items by typing keywords in the search field
- The app includes a large database of foods with detailed nutritional information imported from JSON data
- When you select a food item and specify the gram amount, the system automatically calculates and displays the nutritional content
- View the total nutrition information including calories, protein, carbs, fats, fibre, and sugar
- Add multiple food items for a single meal
- Click "Add Meal" to save your meal data to the database

#### Recent Activities
The Recent Activities section displays your exercise and meal entries, allowing you to review your recently logged data.

![Upload Page](/app/static/img/upload.png)

### Data Visualisation
View detailed charts and graphs of your calorie intake, exercise habits, and nutritional balance over time. The visualisation page includes:

- **Calorie Intake Distribution**: A pie chart showing the breakdown of your calorie intake by meal type
- **Calorie Burn Distribution**: A pie chart displaying the distribution of calories burned across different exercise types
- **Calorie Trends**: A line graph tracking your calorie intake and output over time
- **Nutrition Analysis**: A chart analysing your nutritional intake patterns

![Visualization](/app/static/img/visualisation.png)

When you click the "Request New AI Recommendation" button, the system analyses your data and generates personalised AI recommendations, including:
- **Nutrition Recommendations**: Suggestions for improving your diet and nutritional balance
- **Exercise Analysis**: Insights about your exercise habits and recommendations for optimisation

![AI Recommendation](/app/static/img/AI_recommendation.png)

### Data Sharing
Connect with friends to share your progress and motivate each other. Manage your friend connections, view your friends' data, and control what information you want to share with them.

#### Friend Management
The Friend Management feature consists of three main components:

- **Send A Friend Request**: You can search for users by name and the system provides suggestions through fuzzy search matching. Simply enter a name in the search field and send a friend request.
- **Friend Requests**: View incoming friend requests from other users. When you accept a request, both users establish a friendship, appear in each other's My Friends list, and gain permission for two-way data sharing. When you decline a request, no friendship is established.
- **My Friends**: Displays all your established friendships. Clicking on a friend will redirect you to the Friend's Data page where you can view their shared data.

![Friend Management](/app/static/img/friend_management.png)

#### Friend's Data
In the Friend's Data page, you can:
- Find specific friends using the search function
- Select friends directly from your friend list
- View shared calorie data and statistics in both text and graphical format on the main display area

![Friend Data](/app/static/img/friend_data.png)

#### Share My Data
In the Share My Data page:
- First, search for a friend (they must be in your friend list)
- Select the friend you want to share data with
- Use the Data Filter Options to selectively share specific data types
- Optionally use the "Select all" checkbox to share all information at once
- Click "Confirm Sharing" to complete the process
- The system provides notifications for all successful or failed operations

![Share Data](/app/static/img/share_data.png)

### User Profile
After successful registration, users are directed to the profile setup page where they are required to enter their weight information. This value is recorded as the "Initial Weight." Key features of the profile page include:

- **Weight Tracking**: Users can set a Target Weight and update their Current Weight
- **Progress Visualisation**: The Target Progress indicator in the upper right shows progress toward weight goals
- **Avatar Management**: Users can update their profile avatar by uploading a new image
- **Personalised BMR**: The system calculates and displays the Basal Metabolic Rate (BMR) based on the user's personal data
- **Daily Calorie Tracking**: Users can view their Net Daily Calorie data, which helps in monitoring their calorie balance

The profile page serves as a personal dashboard where users can manage their information and track their progress toward fitness goals.

![Profile Page](/app/static/img/profile.png)

## Running Tests

The CalTrack application includes a comprehensive test suite to ensure the reliability and functionality of all features. The tests are organised into unit tests and Selenium-based tests.

### Test Categories

#### Unit Tests
Fast, database-focused tests that don't require a browser:
- **Basic Application Tests**: Tests for database connection, page rendering, login functionality, and session management
- **Calorie Tracking Tests**: Tests for adding meals, exercises, and retrieving activity data
- **Friendship Tests**: Tests for sending, accepting, and declining friend requests
- **Data Sharing Tests**: Tests for creating, updating, and viewing shared data between friends

#### Selenium Tests
Browser-based tests that validate the full functionality through the browser:
- **Login Tests**: Tests for login page rendering, successful login, and authentication failures
- **Registration Tests**: Tests for the user registration process
- **Exercise Tracking Tests**: Tests for adding and tracking exercise activities
- **Profile Tests**: Tests for viewing and updating user profile information
- **Sharing Tests**: Tests for the friend management and data sharing interface

### Running the Tests

You can run different test suites with these commands:

```bash
# Run all tests
python -m tests.run_tests

# Run only unit tests
python -m tests.run_tests unit

# Run all Selenium tests
python -m tests.run_tests selenium

# Run individual test categories
python -m tests.run_tests login_page
python -m tests.run_tests login_success
python -m tests.run_tests login_failure
python -m tests.run_tests registration
python -m tests.run_tests track_exercise
python -m tests.run_tests view_profile
python -m tests.run_tests sharing
```

## Project Structure

```
CalTrack/
├── app/                        # Application package
│   ├── __init__.py             # App initialisation and factory
│   ├── auth.py                 # Authentication functions
│   ├── blueprints.py           # Flask blueprint definitions
│   ├── forms.py                # Form definitions
│   ├── models.py               # Database models
│   ├── route_api.py            # API routes
│   ├── route_nav.py            # Navigation routes
│   ├── routes.py               # Main routes
│   ├── utils.py                # Utility functions
│   ├── static/                 # Static assets
│   │   ├── css/                # CSS stylesheets
│   │   ├── data/               # JSON data files for food nutrition
│   │   ├── img/                # Image assets
│   │   ├── images/             # Additional images
│   │   ├── js/                 # JavaScript files
│   │   └── profile_photos/     # User profile photos
│   └── templates/              # HTML templates
│       ├── base.html           # Base template with layout
│       ├── home.html           # Home dashboard template
│       ├── index.html          # Landing/login page
│       ├── profile.html        # User profile page
│       ├── sharing.html        # Friend sharing page
│       ├── upload.html         # Data upload page
│       ├── visualisation.html  # Data visualisation page
│       └── emails/             # Email templates
├── migrations/                 # Database migration files
├── tests/                      # Test files
│   ├── run_tests.py            # Test runner script
│   ├── seleniumTest.py         # Selenium browser tests
│   └── unitTest.py             # Unit tests
├── app.py                      # Application entry point
├── config.py                   # Configuration settings
├── init_db.py                  # Database initialisation script
├── requirements.txt            # Python dependencies
├── run.py                      # Flask run script
└── wsgi.py                     # WSGI entry point for production
```

## External Libraries and CDNs

The application uses the following external libraries and CDNs:

### CDN Resources
- **Tailwind CSS**: Used for styling the application
  ```html
  <script src="https://cdn.tailwindcss.com"></script>
  ```
- **Lucide Icons**: Provides the icon set used throughout the application
  ```html
  <script src="https://unpkg.com/lucide@latest"></script>
  ```
- **Chart.js**: Used for data visualisation and charts
  ```html
  <script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.0/dist/chart.min.js"></script>
  ```

### Python Libraries
Key dependencies include:
- Flask: Web framework
- SQLAlchemy: ORM for database operations
- Werkzeug: Authentication and security
- Flask-WTF: Form handling
- Selenium: Browser automation for testing
- Alembic: Database migrations

See `requirements.txt` for the complete list of dependencies.

## References

Grinberg, M. (2023, December 3). *The Flask mega-tutorial, part I: Hello, world!* Miguel Grinberg. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

Pallets. (2023). *Flask documentation (2.3.x)*. Flask. https://flask.palletsprojects.com/en/2.3.x/

Digital Ocean. (2022). *How to structure large Flask applications*. DigitalOcean. https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications

OpenAI. (2023). *ChatGPT (GPT-4 model)*. https://openai.com/gpt-4
