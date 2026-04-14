# Main application file for the Quiz Maker.
# Run this file to interact with the quiz app after running setup_db.py and import_questions.py.
import QuizDB as qdb

# QuizApp class manages all user interactions including authentication, quizzes, and admin functions
class QuizApp:

    def __init__(self):
        # Creates a QuizResults instance to access all database operations
        self.db = qdb.QuizResults()
        # Tracks the currently logged in user, None means no user is logged in
        self.current_user = None

    # User Authentication

    def register(self):
        # Allows a new user to create an account and automatically log them in
        print("\n=== Register ===")
        username = input("Enter a username: ")
        password = input("Enter a password: ")

        # Checks if username already exists before inserting
        existing = self.db.fetch(username=username)
        if existing:
            print("Username already exists. Please try a different one.")
            return

        # Adds new user as a student (is_admin=0 by default)
        self.db.add(username, password, is_admin=0)
        # Automatically logs in after registering by fetching the new user record
        self.current_user = self.db.fetch(username=username)
        print(f"Welcome, {username}! You are now logged in.")

    def login(self):
        # Verifies username and password and set current_user if successful
        print("\n=== Login ===")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        user = self.db.fetch(username=username)
        if user is None:
            print("Username not found. Please try again.")
            return
        # user tuple: (user_id, username, password, is_admin)
        if user[2] != password:
            print("Incorrect password. Please try again.")
            return

        # Stores the logged in user's data for use throughout the session
        self.current_user = user
        print(f"Welcome back, {username}!")

    def logout(self):
        # Clears the current user to return to the login/register menu
        print(f"Goodbye, {self.current_user[1]}!")
        self.current_user = None

    # The Quiz

    def take_quiz(self):
        # Fetches 10 random questions and present them one at a time to the user
        print("\n=== Quiz Time! ===")
        questions = self.db.fetch_random()

        if not questions:
            print("No questions found in the database.")
            return

        score = 0
        total = len(questions)

        for i, question in enumerate(questions):
            # question tuple: (question_id, question, choice_a, choice_b, choice_c, choice_d, correct_answer)
            # Displays question number and answer choices
            print(f"\nQuestion {i + 1}/{total}")
            print(f"{question[1]}")
            print(f"  A. {question[2]}")
            print(f"  B. {question[3]}")
            print(f"  C. {question[4]}")
            print(f"  D. {question[5]}")

            # Validates input to ensure only A, B, C, or D is accepted
            answer = input("Your answer (A/B/C/D): ").strip().upper()
            while answer not in ["A", "B", "C", "D"]:
                print("Invalid input. Please enter A, B, C, or D.")
                answer = input("Your answer (A/B/C/D): ").strip().upper()

            # Compares user's answer to the correct answer and update score
            if answer == question[6]:
                print("Correct!")
                score += 1
            else:
                print(f"Incorrect. The correct answer was {question[6]}.")

        # Displays final score and save the result to the database
        print(f"\n=== Quiz Complete! ===")
        print(f"Your score: {score}/{total}")
        self.db.add_result(self.current_user[0], score, total)

    # View Scores

    def view_scores(self):
        # Retrieves and display all past quiz results for the current user
        print("\n=== My Quiz Scores ===")
        results = self.db.fetch_result(user_id=self.current_user[0])

        if not results:
            print("No quiz results found.")
            return

        # result tuple: (result_id, user_id, score, total_questions, date_taken)
        for result in results:
            print(f"Date: {result[4]} | Score: {result[2]}/{result[3]}")

    # Admin Abilities

    def admin_add_question(self):
        # Allows admin to add a new question to the database
        # User can type 'cancel' at any prompt to abort the action
        print("\n=== Add a Question ===")
        print("(Type 'cancel' at any time to go back)\n")
        question = input("Enter question: ")
        if question.lower() == "cancel":
            print("Action cancelled.")
            return
        choice_a = input("Enter choice A: ")
        if choice_a.lower() == "cancel":
            print("Action cancelled.")
            return
        choice_b = input("Enter choice B: ")
        if choice_b.lower() == "cancel":
            print("Action cancelled.")
            return
        choice_c = input("Enter choice C: ")
        if choice_c.lower() == "cancel":
            print("Action cancelled.")
            return
        choice_d = input("Enter choice D: ")
        if choice_d.lower() == "cancel":
            print("Action cancelled.")
            return
        # Validates correct answer input to ensure only A, B, C, or D is accepted
        correct = input("Enter correct answer (A/B/C/D): ").strip().upper()
        while correct not in ["A", "B", "C", "D"]:
            if correct.lower() == "cancel":
                print("Action cancelled.")
                return
            print("Invalid input. Please enter A, B, C, or D.")
            correct = input("Enter correct answer (A/B/C/D): ").strip().upper()
        self.db.add_question(question, choice_a, choice_b, choice_c, choice_d, correct)

    def admin_edit_question(self):
        # Allows admin to update an existing question's text, choices, and correct answer
        # User can type 'cancel' at any prompt to abort the action
        print("\n=== Edit a Question ===")
        print("(Type 'cancel' at any time to go back)\n")
        self.admin_view_questions()
        try:
            question_id = input("Enter question ID to edit: ")
            if question_id.lower() == "cancel":
                print("Action cancelled.")
                return
            question_id = int(question_id)
            # Verifies the question exists before prompting for new values
            existing = self.db.fetch_question(question_id)
            if existing is None:
                print("Question ID not found.")
                return
            question = input("Enter new question: ")
            if question.lower() == "cancel":
                print("Action cancelled.")
                return
            choice_a = input("Enter new choice A: ")
            if choice_a.lower() == "cancel":
                print("Action cancelled.")
                return
            choice_b = input("Enter new choice B: ")
            if choice_b.lower() == "cancel":
                print("Action cancelled.")
                return
            choice_c = input("Enter new choice C: ")
            if choice_c.lower() == "cancel":
                print("Action cancelled.")
                return
            choice_d = input("Enter new choice D: ")
            if choice_d.lower() == "cancel":
                print("Action cancelled.")
                return
            # Validates correct answer input to ensure only A, B, C, or D is accepted
            correct = input("Enter correct answer (A/B/C/D): ").strip().upper()
            while correct not in ["A", "B", "C", "D"]:
                if correct.lower() == "cancel":
                    print("Action cancelled.")
                    return
                print("Invalid input. Please enter A, B, C, or D.")
                correct = input("Enter correct answer (A/B/C/D): ").strip().upper()
            self.db.update_question(question_id, question, choice_a, choice_b, choice_c, choice_d, correct)
        except ValueError:
            # Handles case where user enters a non-integer for question ID
            print("Invalid ID. Please enter a number.")

    def admin_delete_question(self):
        # Allows admin to delete a question from the database after confirmation
        print("\n=== Delete a Question ===")
        self.admin_view_questions()
        try:
            question_id = int(input("Enter question ID to delete: "))
            # Verifies the question exists before attempting to delete
            existing = self.db.fetch_question(question_id)
            if existing is None:
                print("Question ID not found.")
                return
            # Requires confirmation before permanently deleting
            confirm = input(f"Are you sure you want to delete question {question_id}? (y/n): ").lower()
            if confirm == "y":
                self.db.delete_question(question_id)
            else:
                print("Delete aborted.")
        except ValueError:
            # Handles case where user enters a non-integer for question ID
            print("Invalid ID. Please enter a number.")

    def admin_view_questions(self):
        # Displays all questions in the database showing ID and question text
        print("\n=== All Questions ===")
        questions = self.db.fetch_question()
        if not questions:
            print("No questions found.")
            return
        for q in questions:
            # q tuple: (question_id, question, choice_a, choice_b, choice_c, choice_d, correct_answer)
            print(f"[{q[0]}] {q[1]}")

    def admin_view_users(self):
        # Displays all users in the database showing ID, username, and role
        print("\n=== All Users ===")
        users = self.db.fetch()
        if not users:
            print("No users found.")
            return
        for user in users:
            # user tuple: (user_id, username, password, is_admin)
            # Converts is_admin value to a readable role label
            role = "Admin" if user[3] == 1 else "Student"
            print(f"[{user[0]}] {user[1]} - {role}")

    def admin_edit_user(self):
        # Allows admin to update a user's username, password, and admin status
        # User can type 'cancel' at any prompt to abort the action
        print("\n=== Edit a User ===")
        print("(Type 'cancel' at any time to go back)\n")
        self.admin_view_users()
        try:
            user_id = input("Enter user ID to edit: ")
            if user_id.lower() == "cancel":
                print("Action cancelled.")
                return
            user_id = int(user_id)
            # Verifies the user exists before prompting for new values
            existing = self.db.fetch(user_id=user_id)
            if existing is None:
                print("User ID not found.")
                return
            username = input("Enter new username: ")
            if username.lower() == "cancel":
                print("Action cancelled.")
                return
            password = input("Enter new password: ")
            if password.lower() == "cancel":
                print("Action cancelled.")
                return
            is_admin = input("Is this user an admin? (y/n): ").lower()
            if is_admin == "cancel":
                print("Action cancelled.")
                return
            # Converts y/n response to integer for database storage
            is_admin = 1 if is_admin == "y" else 0
            self.db.update(user_id, username, password, is_admin)
        except ValueError:
            # Handles case where user enters a non-integer for user ID
            print("Invalid ID. Please enter a number.")

    def admin_delete_user(self):
        # Allows admin to delete a user account after confirmation
        print("\n=== Delete a User ===")
        self.admin_view_users()
        try:
            user_id = input("Enter user ID to delete: ")
            if user_id.lower() == "cancel":
                print("Action cancelled.")
                return
            user_id = int(user_id)
            # Verifies the user exists before attempting to delete
            existing = self.db.fetch(user_id=user_id)
            if existing is None:
                print("User ID not found.")
                return
            # Prevents admin from deleting their own account to avoid lockout
            if user_id == self.current_user[0]:
                print("You cannot delete your own account.")
                return
            # Requires confirmation before permanently deleting
            confirm = input(f"Are you sure you want to delete user {existing[1]}? (y/n): ").lower()
            if confirm == "y":
                self.db.delete(user_id)
            else:
                print("Delete aborted.")
        except ValueError:
            # Handles case where user enters a non-integer for user ID
            print("Invalid ID. Please enter a number.")

    # Main Menu

    def run(self):
        # Main loop that keeps the app running until the user exits
        print("=== Welcome to the Quiz App ===")

        while True:
            # If no user is logged in, show login/register menu
            if self.current_user is None:
                print("\n1. Login")
                print("2. Register")
                print("3. Exit")
                choice = input("Select an option: ").strip()

                if choice == "1":
                    self.login()
                elif choice == "2":
                    self.register()
                elif choice == "3":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid selection. Please try again.")

            # If user is logged in, show the full main menu
            else:
                print(f"\n=== Main Menu === (Logged in as: {self.current_user[1]})")
                print("1. Take a Quiz")
                print("2. View My Scores")
                print("3. Logout")
                print("--- Admin ---")
                print("4. Add a Question")
                print("5. Edit a Question")
                print("6. Delete a Question")
                print("7. View All Questions")
                print("8. View All Users")
                print("9. Edit a User")
                print("10. Delete a User")
                choice = input("Select an option: ").strip()

                if choice == "1":
                    self.take_quiz()
                elif choice == "2":
                    self.view_scores()
                elif choice == "3":
                    self.logout()
                elif choice in ["4", "5", "6", "7", "8", "9", "10"]:
                    # Checks if the current user is an admin before allowing access
                    if self.current_user[3] == 1:
                        if choice == "4":
                            self.admin_add_question()
                        elif choice == "5":
                            self.admin_edit_question()
                        elif choice == "6":
                            self.admin_delete_question()
                        elif choice == "7":
                            self.admin_view_questions()
                        elif choice == "8":
                            self.admin_view_users()
                        elif choice == "9":
                            self.admin_edit_user()
                        elif choice == "10":
                            self.admin_delete_user()
                    else:
                        # Student users cannot access admin options
                        print("You cannot access this ability.")
                else:
                    print("Invalid selection. Please try again.")

# Creates an instance of QuizApp and start the application
app = QuizApp()
app.run()