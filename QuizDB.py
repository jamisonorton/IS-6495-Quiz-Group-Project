# Database classes for the Quiz Maker application
# Defines Users, Questions, and QuizResults tables and their CRUD operations
import db_base as db

# Users class inherits from DBbase to handle all user-related database operations
class Users(db.DBbase):

    def __init__(self):
        # Connects to the quiz database file
        super().__init__("quiz.sqlite")

    def add(self, username, password, is_admin=0):
        # Inserts a new user into the Users table
        # is_admin defaults to 0 as student unless specified as 1 (admin)
        try:
            super().get_cursor.execute(
                "INSERT OR IGNORE INTO Users (username, password, is_admin) VALUES (?, ?, ?);",
                (username, password, is_admin))
            super().get_connection.commit()
            print(f"User '{username}' added successfully.")
        except Exception as e:
            print("An error has occurred.", e)

    def fetch(self, user_id=None, username=None):
        # Retrieves a user by user_id, by username, or all users if no argument is given
        try:
            if user_id is not None:
                # Fetches a single user by their ID
                return super().get_cursor.execute(
                    "SELECT * FROM Users WHERE user_id=?;", (user_id,)).fetchone()
            elif username is not None:
                # Fetches a single user by their username
                return super().get_cursor.execute(
                    "SELECT * FROM Users WHERE username=?;", (username,)).fetchone()
            else:
                # Fetches all users
                return super().get_cursor.execute(
                    "SELECT * FROM Users;").fetchall()
        except Exception as e:
            print("An error has occurred.", e)

    def update(self, user_id, username, password, is_admin=0):
        # Updates an existing user's username, password, and admin status
        try:
            super().get_cursor.execute(
                "UPDATE Users SET username=?, password=?, is_admin=? WHERE user_id=?;",
                (username, password, is_admin, user_id))
            super().get_connection.commit()
            print(f"User ID {user_id} updated successfully.")
        except Exception as e:
            print("An error has occurred.", e)

    def delete(self, user_id):
        # Deletes a user from the Users table by their ID
        try:
            super().get_cursor.execute(
                "DELETE FROM Users WHERE user_id=?;", (user_id,))
            super().get_connection.commit()
            print(f"User ID {user_id} deleted successfully.")
        except Exception as e:
            print("An error has occurred.", e)

    def reset_database(self):
        # Drops the Users table if it exists and recreate it fresh
        try:
            sql = """
                DROP TABLE IF EXISTS Users;

                CREATE TABLE Users (
                    user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    is_admin INTEGER NOT NULL DEFAULT 0  -- 0 = student, 1 = admin
                );
            """
            super().execute_script(sql)
            self._conn.commit()
            print("Users table created successfully.")
        except Exception as e:
            print("An error has occurred.", e)


# Questions class inherits from Users, sharing the same database connection
class Questions(Users):

    def add_question(self, question, choice_a, choice_b, choice_c, choice_d, correct_answer):
        # Inserts a new question into the Questions table
        try:
            super().get_cursor.execute("""
                INSERT INTO Questions (question, choice_a, choice_b, choice_c, choice_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?);""",
                (question, choice_a, choice_b, choice_c, choice_d, correct_answer))
            super().get_connection.commit()
            print(f"Question added successfully.")
        except Exception as e:
            print("An error has occurred.", e)

    def fetch_question(self, question_id=None):
        # Retrieves a single question by ID, or all questions if no ID is given
        try:
            if question_id is not None:
                # Fetches a single question by its ID
                return super().get_cursor.execute(
                    "SELECT * FROM Questions WHERE question_id=?;", (question_id,)).fetchone()
            else:
                # Fetches all questions
                return super().get_cursor.execute(
                    "SELECT * FROM Questions;").fetchall()
        except Exception as e:
            print("An error has occurred.", e)

    def fetch_random(self):
        # Retrieves 10 random questions from the database to build a quiz
        try:
            return super().get_cursor.execute(
                "SELECT * FROM Questions ORDER BY RANDOM() LIMIT 10;").fetchall()
        except Exception as e:
            print("An error has occurred.", e)

    def update_question(self, question_id, question, choice_a, choice_b, choice_c, choice_d, correct_answer):
        # Updates an existing question's text, choices, and correct answer
        try:
            super().get_cursor.execute("""
                UPDATE Questions SET question=?, choice_a=?, choice_b=?, choice_c=?,
                choice_d=?, correct_answer=? WHERE question_id=?;""",
                (question, choice_a, choice_b, choice_c, choice_d, correct_answer, question_id))
            super().get_connection.commit()
            print(f"Question ID {question_id} updated successfully.")
        except Exception as e:
            print("An error has occurred.", e)

    def delete_question(self, question_id):
        # Deletes a question from the Questions table by its ID
        try:
            super().get_cursor.execute(
                "DELETE FROM Questions WHERE question_id=?;", (question_id,))
            super().get_connection.commit()
            print(f"Question ID {question_id} deleted successfully.")
        except Exception as e:
            print("An error has occurred.", e)

    def reset_database(self):
        # Drops the Questions table if it exists and recreate it fresh
        try:
            sql = """
                DROP TABLE IF EXISTS Questions;

                CREATE TABLE Questions (
                    question_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    question TEXT NOT NULL,
                    choice_a TEXT NOT NULL,
                    choice_b TEXT NOT NULL,
                    choice_c TEXT NOT NULL,
                    choice_d TEXT NOT NULL,
                    correct_answer TEXT NOT NULL
                );
            """
            super().execute_script(sql)
            self._conn.commit()
            print("Questions table created successfully.")
        except Exception as e:
            print("An error has occurred.", e)


# QuizResults class inherits from Questions, sharing the same database connection
class QuizResults(Questions):

    def add_result(self, user_id, score, total_questions):
        # Inserts a new quiz result linked to a user, with an automatic timestamp
        try:
            super().get_cursor.execute("""
                INSERT INTO QuizResults (user_id, score, total_questions, date_taken)
                VALUES (?, ?, ?, datetime('now'));""",
                (user_id, score, total_questions))
            super().get_connection.commit()
            print("Quiz result saved successfully.")
        except Exception as e:
            print("An error has occurred.", e)

    def fetch_result(self, user_id=None):
        # Retrieves quiz results for a specific user, or all results if no user_id is given
        try:
            if user_id is not None:
                # Fetches all results for a specific user
                return super().get_cursor.execute(
                    "SELECT * FROM QuizResults WHERE user_id=?;", (user_id,)).fetchall()
            else:
                # Fetches all results across all users
                return super().get_cursor.execute(
                    "SELECT * FROM QuizResults;").fetchall()
        except Exception as e:
            print("An error has occurred.", e)

    def delete_result(self, result_id):
        # Deletes a specific quiz result by its ID
        try:
            super().get_cursor.execute(
                "DELETE FROM QuizResults WHERE result_id=?;", (result_id,))
            super().get_connection.commit()
            print(f"Result ID {result_id} deleted successfully.")
        except Exception as e:
            print("An error has occurred.", e)

    def reset_database(self):
        # Drops the QuizResults table if it exists and recreate it fresh
        try:
            sql = """
                DROP TABLE IF EXISTS QuizResults;

                CREATE TABLE QuizResults (
                    result_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    user_id INTEGER NOT NULL,       -- foreign key reference to Users
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    date_taken DATETIME             -- automatically set when quiz is submitted
                );
            """
            super().execute_script(sql)
            self._conn.commit()
            print("QuizResults table created successfully.")
        except Exception as e:
            print("An error has occurred.", e)