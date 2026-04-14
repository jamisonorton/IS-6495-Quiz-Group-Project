# Run this ONCE and first before to create the database and tables.
# Then run import_questions.py.
# You can now run the quiz_app.py file to take and use the quiz.
# Because QuizDB is being imported here, the script file itself does not need to be executed.
import QuizDB as qdb

users = qdb.Users()
users.reset_database()

questions = qdb.Questions()
questions.reset_database()

quiz = qdb.QuizResults()
quiz.reset_database()

print("Database setup complete.")

# Create admin user
users.add("admin", "admin123", is_admin=1)
print("Admin user created.")