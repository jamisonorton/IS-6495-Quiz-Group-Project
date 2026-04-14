import QuizDB as qdb

class QuizApp:

    def __init__(self):
        self.db = qdb.QuizResults()
        self.current_user = None

    # User Authentication

    def register(self):
        print("\n=== Register ===")
        username = input("Enter a username: ")
        password = input("Enter a password: ")

        # Check if username already exists
        existing = self.db.fetch(username=username)
        if existing:
            print("Username already exists. Please try a different one.")
            return

        self.db.add(username, password, is_admin=0)
        # Automatically log in after registering
        self.current_user = self.db.fetch(username=username)
        print(f"Welcome, {username}! You are now logged in.")

    def login(self):
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

        self.current_user = user
        print(f"Welcome back, {username}!")

    def logout(self):
        print(f"Goodbye, {self.current_user[1]}!")
        self.current_user = None

    # The Quiz

    def take_quiz(self):
        print("\n=== Quiz Time! ===")
        questions = self.db.fetch_random()

        if not questions:
            print("No questions found in the database.")
            return

        score = 0
        total = len(questions)

        for i, question in enumerate(questions):
            # question tuple: (question_id, question, choice_a, choice_b, choice_c, choice_d, correct_answer)
            print(f"\nQuestion {i + 1}/{total}")
            print(f"{question[1]}")
            print(f"  A. {question[2]}")
            print(f"  B. {question[3]}")
            print(f"  C. {question[4]}")
            print(f"  D. {question[5]}")

            answer = input("Your answer (A/B/C/D): ").strip().upper()
            while answer not in ["A", "B", "C", "D"]:
                print("Invalid input. Please enter A, B, C, or D.")
                answer = input("Your answer (A/B/C/D): ").strip().upper()

            if answer == question[6]:
                print("Correct!")
                score += 1
            else:
                print(f"Incorrect. The correct answer was {question[6]}.")

        # Save result and display score
        print(f"\n=== Quiz Complete! ===")
        print(f"Your score: {score}/{total}")
        self.db.add_result(self.current_user[0], score, total)

    # View Scores

    def view_scores(self):
        print("\n=== My Quiz Scores ===")
        results = self.db.fetch_result(user_id=self.current_user[0])

        if not results:
            print("No quiz results found.")
            return

        for result in results:
            print(f"Date: {result[4]} | Score: {result[2]}/{result[3]}")

    # Admin Abilities

    def admin_add_question(self):
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
        correct = input("Enter correct answer (A/B/C/D): ").strip().upper()
        while correct not in ["A", "B", "C", "D"]:
            if correct.lower() == "cancel":
                print("Action cancelled.")
                return
            print("Invalid input. Please enter A, B, C, or D.")
            correct = input("Enter correct answer (A/B/C/D): ").strip().upper()
        self.db.add_question(question, choice_a, choice_b, choice_c, choice_d, correct)

    def admin_edit_question(self):
        print("\n=== Edit a Question ===")
        print("(Type 'cancel' at any time to go back)\n")
        self.admin_view_questions()
        try:
            question_id = input("Enter question ID to edit: ")
            if question_id.lower() == "cancel":
                print("Action cancelled.")
                return
            question_id = int(question_id)
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
            correct = input("Enter correct answer (A/B/C/D): ").strip().upper()
            while correct not in ["A", "B", "C", "D"]:
                if correct.lower() == "cancel":
                    print("Action cancelled.")
                    return
                print("Invalid input. Please enter A, B, C, or D.")
                correct = input("Enter correct answer (A/B/C/D): ").strip().upper()
            self.db.update_question(question_id, question, choice_a, choice_b, choice_c, choice_d, correct)
        except ValueError:
            print("Invalid ID. Please enter a number.")

    def admin_delete_question(self):
        print("\n=== Delete a Question ===")
        self.admin_view_questions()
        try:
            question_id = int(input("Enter question ID to delete: "))
            existing = self.db.fetch_question(question_id)
            if existing is None:
                print("Question ID not found.")
                return
            confirm = input(f"Are you sure you want to delete question {question_id}? (y/n): ").lower()
            if confirm == "y":
                self.db.delete_question(question_id)
            else:
                print("Delete aborted.")
        except ValueError:
            print("Invalid ID. Please enter a number.")

    def admin_view_questions(self):
        print("\n=== All Questions ===")
        questions = self.db.fetch_question()
        if not questions:
            print("No questions found.")
            return
        for q in questions:
            print(f"[{q[0]}] {q[1]}")

    # Main Menu

    def run(self):
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

            # If user is logged in, show main menu
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
                choice = input("Select an option: ").strip()

                if choice == "1":
                    self.take_quiz()
                elif choice == "2":
                    self.view_scores()
                elif choice == "3":
                    self.logout()
                elif choice in ["4", "5", "6", "7"]:
                    if self.current_user[3] == 1:  # check is_admin
                        if choice == "4":
                            self.admin_add_question()
                        elif choice == "5":
                            self.admin_edit_question()
                        elif choice == "6":
                            self.admin_delete_question()
                        elif choice == "7":
                            self.admin_view_questions()
                    else:
                        print("You cannot access this ability.")
                else:
                    print("Invalid selection. Please try again.")

# Run the app
app = QuizApp()
app.run()