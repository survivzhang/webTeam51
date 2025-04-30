# webTeam51

Group_51 in CITS5505 2025 Semester 1.

| UWA ID       | Name             | GitHub Username     |
|--------------|------------------|---------------------|
| 24064091     | Zichen Zhang     | survivzhang         |
| 23773086     | Jinshu Zhang     | JocelynZhang01      |
| 24042674     | Zhaoyang Lin     | adamslin            |
| 24455032     | Anvesh Reddy M   | anvesh1903          |


A webapp for Caltracker

# First of all

### Pre-Commit Checklist

Before you start writing or committing code, please follow these steps to ensure your work is in sync with the latest updates from the team:

1. **Work on Your Own Branch**:

   - Make sure you are working on your own feature branch, not directly on the `main` branch. Use the following command to check your current branch:
     ```bash
     git branch
     ```

2. **Pull Latest Changes from Main**:

   - Switch to the `main` branch and pull the latest changes:
     ```bash
     git checkout main
     git pull origin main
     ```

3. **Update Your Working Branch**:

   - Switch back to your working branch and merge the changes from the `main` branch into it:
     ```bash
     git checkout your-feature-branch
     git merge main
     ```

4. **Resolve Merge Conflicts (if any)**:

   - If there are any merge conflicts, resolve them promptly and ensure that your code runs correctly.

5. **Continue Your Development Work**:
   - Once everything is in order, continue developing on your branch.

By following these steps, you can ensure that your working branch includes the latest changes from the team, reducing the likelihood of merge conflicts and improving collaboration efficiency.

Thank you for your cooperation!

# Calorie Tracker Web App

A simple calorie tracking web app built with HTML, CSS, and JavaScript. Designed for easy logging of daily calorie intake, exercise, and progress tracking, this app helps users reach their fitness goals with motivation from friends.

## 🌟 Features

### 1. Home Page (Welcome & Authentication)

- Brief introduction to the app and its purpose.
- **Sign Up**: Register with email, height, weight, and target weight.
- **Sign In**: Log in to access personalized tracking.
- Once loged in, Dashboard must be shown.

### 2. Calorie Log Page

- Add food intake (+ calories).
- Log exercises (- calories).
- Automatically calculates daily net calories.
- Stores and displays history using localStorage.

### 3. Friends Page

- View your friends' calorie progress and stats.
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

Certainly! Here's the documentation in English:

---

### Tailwind CSS Successfully Added

I have successfully integrated Tailwind CSS into the project. Please follow the steps below to configure and use it:

1. **Modify CSS Settings**

   Open and edit the `static/css/styles.css` file to add or modify styles as needed.

2. **Run Tailwind CLI**

   In the root directory of your project, run the following command to process and generate the final CSS file:

   ```bash
   npx tailwindcss -i ./static/css/styles.css -o ./static/css/output.css --watch
   ```

   This command will watch for changes in the `styles.css` file and automatically update the `output.css` file.

3. **Include the Generated CSS in HTML**

   In your HTML file, add the following code to include the generated CSS file:

   ```html
   <link
     href="{{ url_for('static', filename='css/output.css') }}"
     rel="stylesheet"
   />
   ```

   This ensures that your HTML file uses the styles generated by Tailwind CSS.

---

By following these steps, you have successfully integrated Tailwind CSS into your project and can start using its powerful features to design and develop your web pages.
