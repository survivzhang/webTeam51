# webTeam51

Group_51 in CITS5505

A webapp for Caltracker

# Calorie Tracker Web App

A simple calorie tracking web app built with HTML, CSS, and JavaScript. Designed for easy logging of daily calorie intake, exercise, and progress tracking, this app helps users reach their fitness goals with motivation from friends.

## 🌟 Features

### 1. Home Page (Welcome & Authentication)

- Brief introduction to the app and its purpose.
- **Sign Up**: Register with email, height, weight, and target weight.
- **Sign In**: Log in to access personalized tracking.

### 2. Calorie Log Page

- Add food intake (+ calories).
- Log exercises (- calories).
- Automatically calculates daily net calories.
- Stores and displays history using localStorage.

### 3. Friends Page

- View your friends' calorie progress and stats.
- Compare net calorie balances and target weight progress.
- Add friends using their email.

### 4. Profile Page

- Displays user information (email, height, weight, target weight).
- Calculates and shows **recommended daily calorie intake** (BMR).
- Displays **net daily calories** based on logs.
- Shows **progress bar** toward target weight.
- Edit personal info if needed.

## 💡 Technologies Used

- HTML
- CSS
- JavaScript
- Flask

## 🚀 How to Use

1. Open the `index.html` file in your browser.
2. Register or log in using your email.
3. Log daily food and exercise.
4. View personal progress and friend comparison.

## 📁 Project Structure

=======

## Getting Started

Follow the steps below to set up and run the project on your local machine.

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- pip (Python package manager)

### Setup Instructions

#### 1. Check Python & pip Versions

Run the following commands to verify your Python and pip installations:

```
python3 --version
```

or:

```
python --version
```

<br>

```
pip --version
```

#### 2. Create a Virtual Environment

Set up a new virtual environment to manage dependencies:

```bash
python3 -m venv venv
```

or:

```
python -m venv venv
```

#### 3. Activate the Virtual Environment

Activate the virtual environment using the command for your operating system:
<br>
• Linux/Mac:

```bash
source venv/bin/activate
```

• Windows:

```bash
.\venv\Scripts\activate
```

#### 4. Install Dependencies

Install the required dependencies listed in **requirements.txt**:

```bash
pip install -r requirements.txt
```

#### 5. Run the Flask App

Start the Flask development server:

```
flask run
```

6. Access the App

Open your browser and navigate to the following URL to view the application:

```
http://127.0.0.1:5000
```

## Project Structure

├── app/
<br>
├── templates/  
├── static/   
├── venv/ <br>
├── requirements.txt  
├── README.md

app: _Application source code_<br>
templates: _HTML templates_<br>
static: _Static files (CSS, JS, images)_<br>
venv: _Virtual environment (not included in GitHub)_<br>
requirements: _Python dependencies_<br>
README.md: _Project documentation_

change css setting in input.css
then run
npx tailwindcss -i ./input.css -o ./static/css/output.css --watch
