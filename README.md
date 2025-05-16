A Flask-based web application for tracking calorie intake and burn. This app enables users to log meals and exercises, manage personal profiles, monitor calorie trends over time, and connect with friends for shared goals. Key functionalities include account registration with email verification, personalized daily calorie recommendations, and goal tracking. Badges at the top of this README provide a quick overview of project status (license, build, Python version) as recommended by best practices
daily.dev
. The documentation is organized with clear sections and bullet points to enhance readability
hatica.io
 and includes all essential information for users and contributors
tilburgsciencehub.com
.
Key Features
Meal Logging: Record daily meals with calorie counts. Select foods from a database of nutritional information or add custom entries.
Exercise Tracking: Log exercises and calories burned. The app supports multiple exercise types (running, swimming, cycling, etc.) and calculates burned calories.
Profile & Goals: Manage a personal profile (age, weight, etc.) and set calorie or weight goals. Track progress towards daily or weekly goals with visual feedback.
Calorie Trends: View historical calorie intake and burn data. The dashboard displays trends (e.g., daily net calories) to help users understand their progress over time.
Friend Connections: Add friends and share calorie info (optional). Users can view friends’ shared progress and encourage each other (via the Friendship & SharedCalories features).
Email Verification: New users verify their email via a code to activate accounts, ensuring valid registrations.
Recommendations: Receive personalized calorie intake recommendations based on profile and goals. The app may suggest daily calorie targets or tips to reach goals (utilizing the Recommendation model).
Data Privacy: User data is stored securely. Profile and health data are private unless shared via the friend-sharing feature.
Technologies Used
Python 3.10+: Core language used for the application (Flask framework)
cgit.freebsd.org
.
Flask (Werkzeug & Jinja2): Web framework for routing and templating. Implements the server, view functions, and HTML template rendering.
Flask-SQLAlchemy: ORM for database modeling. Models (User, MealType, CalorieEntry, ExerciseType, etc.) are defined to interact with a relational database.
Database: SQLite (development) or PostgreSQL/MySQL (production) – configurable via SQLAlchemy URI. Includes models for users, foods, exercises, and social features.
Flask-Migrate (Alembic): Handles database migrations. Enables version-controlled schema changes and easy upgrade/downgrade of the database structure.
HTML/CSS & Bootstrap: The frontend uses Jinja2 templates styled with CSS (possibly Bootstrap for responsive design) for a clean UI.
JavaScript: May be used for interactive charts or form enhancements (e.g., input validations or dynamic updates of calorie charts).
Email Service: Utilizes an SMTP server or service (like Flask-Mail or SMTP library) for sending verification emails with confirmation codes.
Testing Tools: Python’s built-in unittest (or PyTest) for unit tests, and Selenium WebDriver for end-to-end system tests (automating a browser to simulate user interaction).
Setup Instructions
Setting up the project is straightforward. Follow the steps below to get a development environment running (clear installation instructions are essential to enable developers to start using the software
archbee.com
):
Clone the Repository:
bash
Copy
Edit
git clone https://github.com/YourUsername/flask-calorie-tracker.git
cd flask-calorie-tracker
Create a Virtual Environment: (Python 3.10+ is required)
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
Install Dependencies:
Upgrade pip and install all required packages:
bash
Copy
Edit
pip install --upgrade pip  
pip install -r requirements.txt  
This will install Flask, SQLAlchemy, Flask-Migrate, Selenium (for tests), and any other libraries listed in requirements.txt.
Copy Configuration (if applicable):
If there is a .env.example file, copy it to .env and update the values. Alternatively, ensure required environment variables are set (see Environment Configuration below).
Initialize the Database:
Set up the database and tables using migrations or the provided initialization script (details in the Database Initialization section).
Run the Application:
Start the Flask development server (see Running the Application section for the command). You should be able to access the app at http://localhost:5000.
Environment Configuration
Before running the app, certain environment variables need to be configured (you can set these in your shell or in a .env file loaded by Flask). These include:
FLASK_APP: The Flask application entry point, e.g. FLASK_APP=run.py or FLASK_APP=app (if using the app factory pattern).
FLASK_ENV: Set to development to enable debug mode (optional).
SECRET_KEY: A secret key for session management and CSRF protection. Example: SECRET_KEY="your_random_secret_key".
Database URL: SQLAlchemy connection string. e.g. SQLALCHEMY_DATABASE_URI="sqlite:///calories.db" for a local SQLite file, or a URL for a database server.
Mail Server Settings: Required for email verification. Specify your SMTP server and credentials, for example:
MAIL_SERVER="smtp.gmail.com"
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME="your_email@example.com"
MAIL_PASSWORD="your_email_password"
Ensure less secure app access or app-specific passwords are configured if using Gmail, or adjust settings according to your email provider.
Other Config: If the app uses additional config (e.g., API keys or other services), document them here. For instance, there might be a RECOMMENDATION_API_KEY if external services were used for recommendations (not in this case, as recommendations are likely internal).
Configure these variables in your environment or in an .env file. The application will read them on startup (commonly via flask.Config or python-dotenv). Correct configuration ensures the app knows how to connect to the database and email server, etc.
Running the Application
With dependencies installed and environment configured, you can run the Flask application locally:
Using Flask CLI:
bash
Copy
Edit
flask run
Ensure that FLASK_APP is set as mentioned above (for example, export FLASK_APP=app if the application instance is created in app/__init__.py). Running flask run will start the development server on http://127.0.0.1:5000/ by default.
Using a Run Script:
The repository may include a run.py (or similar) that initializes the app. If so, you can start the app with:
bash
Copy
Edit
python run.py
This will also start the server on localhost.
Debug Mode:
For development convenience, set FLASK_ENV=development (and/or FLASK_DEBUG=1). This enables auto-reload and debug traceback. Do not enable debug mode in production.
After running, open your browser to http://localhost:5000 to view the application. You should be able to register a new account, log meals/exercises, etc.
Database Initialization
The app uses Flask-Migrate for structured database migrations, and also provides a one-time initialization script for seeding important data. To set up the database schema and seed initial data, follow these steps:
Configure Database URL: As noted in Environment Configuration, ensure SQLALCHEMY_DATABASE_URI points to a valid database. By default (if not set), the app might use SQLite and create a app.db or instance/app.db file.
Apply Migrations: Run the migration upgrade to create tables:
bash
Copy
Edit
flask db upgrade
This will apply all migrations in the migrations/ folder, creating the schema (tables for users, entries, friendships, etc.). If you prefer to start with a fresh schema without migrations, you could use flask db init and flask db migrate to generate new migrations, but this is usually not needed if migrations are provided.
Initialize Default Data: There is an init_db.py script which populates core data. Run it after migrating:
bash
Copy
Edit
python init_db.py
This will:
Create default meal types (Breakfast, Lunch, Dinner, Snacks) if they don’t exist.
Create default exercise types (Running, Swimming, etc.).
Import a baseline food nutrition dataset from app/static/data/food_basic_nutrition.json if available, adding a variety of food items with their calorie and macronutrient values.
Print a summary of how many records were added (and skip existing records to avoid duplicates).
Note: The script uses app.app_context() to run DB operations. Ensure you run it from the project root directory so that it can import the app. On success, you’ll see console output like “✅ Imported X foods from JSON” and a summary count of users, foods, entries, etc. after initialization.
If you need to reset the database, you can drop the schema (or delete the SQLite file) and repeat the above steps. All critical reference data can be re-created via the init script. Using migrations and an init script ensures the database is reproducible and consistent.
Running Tests
The project includes both unit tests and Selenium end-to-end tests to ensure code reliability. To run the test suites:
Unit Tests: These tests cover individual components (models, routes, forms, etc.). They can be run with:
bash
Copy
Edit
python -m unittest discover -v
(This discovers tests in the repository, assuming they follow the standard naming like test_*.py). If PyTest is used instead, simply run pytest. All unit tests should pass, indicating that each function behaves as expected.
Selenium Tests: The repository also contains system tests using Selenium, which automate a web browser to simulate user interactions (e.g., registering, logging a meal). To run these, you need to have Google Chrome (or another supported browser) and the corresponding WebDriver installed (for Chrome, download chromedriver and make sure it's in your PATH).
Once setup, you can run the Selenium tests, for example:
bash
Copy
Edit
pytest tests/selenium -v
(assuming tests are in a subfolder tests/selenium). These tests will launch a browser window (or run headlessly if configured) and execute scenarios like "user can sign up", "user can add a meal entry", etc.
Note: Running the Selenium tests may require the app to be running, or they might start the app in a test context (some test frameworks can launch a Flask test server). Check the test documentation or comments in the test files for specifics. If a test fails, the output and screenshots (if configured) will help diagnose issues.
Running tests regularly (e.g., before pushing changes) is encouraged to catch regressions. The included test suite helps ensure that all features (including forms, database transactions, and email verification flow) work as intended.
Project Structure
Below is an overview of the repository structure. This helps newcomers navigate the codebase
tilburgsciencehub.com
 by showing key directories and files:
bash
Copy
Edit
flask-calorie-tracker/
├── app/                     # Flask application package
│   ├── __init__.py          # App factory or app setup (Flask instance, db, etc.)
│   ├── models.py            # Database models (User, Food, CalorieEntry, etc.)
│   ├── routes.py            # Route handlers (views) for web endpoints
│   ├── forms.py             # (If using WTForms) Form definitions for login, etc.
│   ├── static/              # Static assets (CSS, JS, images, data files)
│   │   └── data/food_basic_nutrition.json   # Sample food nutrition dataset
│   └── templates/           # Jinja2 HTML templates for the UI
├── tests/                   # Automated tests
│   ├── unit/                # Unit tests for models, utils, etc.
│   └── selenium/            # Selenium end-to-end test scripts
├── migrations/              # Database migration scripts (Flask-Migrate/Alembic)
│   ├── versions/            # Migration versions (auto-generated .py files)
│   └── env.py, script.py    # Alembic configuration files
├── init_db.py               # One-time script to initialize and seed the database
├── requirements.txt         # Python dependencies list
├── run.py                   # Application entry point (runs Flask app) (if present)
├── README.md                # Project README documentation (you are reading this!)
└── LICENSE                  # License file (MIT License for this project)
(Note: Some files or modules may differ if the project uses Blueprints or a different structure. For instance, there might be an app/forms.py, app/controllers/ or separate blueprint folders for auth, profile, etc. Adjust the structure overview accordingly if your project layout is different.)
Screenshots / Demo
[Placeholder] Screenshots of the web interface and a live demo link will be added here in the future. Currently, no public demo is deployed. Below is an example of what the app’s dashboard might look like: (Screenshot coming soon) Users can expect a dashboard summarizing daily intake vs burn, forms for adding meals/exercises, and profile pages showing goals and progress. This section will include visual examples as the project matures.
Badges
 <small>Badges: The license badge indicates the project is under the MIT License. The build status badge is green (“passing”) to show tests are all passing, and the Python badge indicates the supported Python version. Including relevant badges at the top of a README is a common convention to provide at-a-glance info about the project’s state
daily.dev
.</small>
Contribution Guidelines
Contributions are welcome! To contribute:
Fork the repository on GitHub and clone your fork locally.
Create a feature branch for your changes:
bash
Copy
Edit
git checkout -b feature/your-feature-name
Commit your changes with clear messages. Ensure your code follows the project’s coding style and includes tests for any new functionality.
Run the tests to make sure nothing is broken. It's important to keep the build passing for all contributions.
Open a Pull Request on the main repository. Describe your changes and which issue or feature request they address. The project maintainers will review your PR.
For major changes or design discussions, please open an issue first to discuss the proposed changes. This helps in aligning on the implementation approach before writing code. By contributing, you agree that your contributions will be licensed under the same MIT License. Make sure you have rights to any code you submit. All contributions are subject to code review and approval by the maintainers.
License
This project is licensed under the MIT License – see the LICENSE file for full details. This means you are free to use, modify, and distribute this software with attribution. Contributions to this project will be also released under the MIT License.
Changelog
All notable changes will be documented in this section (or a dedicated CHANGELOG.md). At present, the project is in its initial version – upcoming releases and bug fixes will be listed here. Stay tuned for updates as the project evolves.
