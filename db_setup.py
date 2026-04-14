# Run this ONCE and first before to create the database and tables.
# Then run import_questions.py.
# You can now run the quiz_app.py file to take and use the quiz.
# Because QuizDB is being imported here, the script file itself does not need to be executed.
import QuizDB as qdb

# Creates a Users instance and resets/creates the Users table
users = qdb.Users()
users.reset_database()

# Create a Questions instance and reset/create the Questions table
questions = qdb.Questions()
questions.reset_database()

# Create a QuizResults instance and reset/create the QuizResults table
quiz = qdb.QuizResults()
quiz.reset_database()

print("Database setup complete.")

# Creates admin user, is_admin=1
# Account is used to manage questions and users in the app
users.add("admin", "admin123", is_admin=1)
print("Admin user created.")