import db_base as db

class Users(db.DBbase):

    def __init__(self):
        super().__init__("quiz.sqlite")

    def add(self, username, password, is_admin=0):
        try:
            super().get_cursor.execute(
                "INSERT OR IGNORE INTO Users (username, password, is_admin) VALUES (?, ?, ?);",
                (username, password, is_admin))
            super().get_connection.commit()
            print(f"User '{username}' added successfully.")
        except Exception as e:
            print("An error has occurred.", e)

    def fetch(self, user_id=None, username=None):
        try:
            if user_id is not None:
                return super().get_cursor.execute(
                    "SELECT * FROM Users WHERE user_id=?;", (user_id,)).fetchone()
            elif username is not None:
                return super().get_cursor.execute(
                    "SELECT * FROM Users WHERE username=?;", (username,)).fetchone()
            else:
                return super().get_cursor.execute(
                    "SELECT * FROM Users;").fetchall()
        except Exception as e:
            print("An error has occurred.", e)

    def update(self, user_id, username, password, is_admin=0):
        try:
            super().get_cursor.execute(
                "UPDATE Users SET username=?, password=?, is_admin=? WHERE user_id=?;",
                (username, password, is_admin, user_id))
            super().get_connection.commit()
            print(f"User ID {user_id} updated successfully.")
        except Exception as e:
            print("An error has occurred.", e)

    def delete(self, user_id):
        try:
            super().get_cursor.execute(
                "DELETE FROM Users WHERE user_id=?;", (user_id,))
            super().get_connection.commit()
            print(f"User ID {user_id} deleted successfully.")
        except Exception as e:
            print("An error has occurred.", e)

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Users;

                CREATE TABLE Users (
                    user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    is_admin INTEGER NOT NULL DEFAULT 0
                );
            """
            super().execute_script(sql)
            self._conn.commit()
            print("Users table created successfully.")
        except Exception as e:
            print("An error has occurred.", e)


class Questions(Users):

    def add_question(self, question, choice_a, choice_b, choice_c, choice_d, correct_answer):
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
        try:
            if question_id is not None:
                return super().get_cursor.execute(
                    "SELECT * FROM Questions WHERE question_id=?;", (question_id,)).fetchone()
            else:
                return super().get_cursor.execute(
                    "SELECT * FROM Questions;").fetchall()
        except Exception as e:
            print("An error has occurred.", e)

    def fetch_random(self):
        try:
            return super().get_cursor.execute(
                "SELECT * FROM Questions ORDER BY RANDOM() LIMIT 10;").fetchall()
        except Exception as e:
            print("An error has occurred.", e)

    def update_question(self, question_id, question, choice_a, choice_b, choice_c, choice_d, correct_answer):
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
        try:
            super().get_cursor.execute(
                "DELETE FROM Questions WHERE question_id=?;", (question_id,))
            super().get_connection.commit()
            print(f"Question ID {question_id} deleted successfully.")
        except Exception as e:
            print("An error has occurred.", e)

    def reset_database(self):
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


class QuizResults(Questions):

    def add_result(self, user_id, score, total_questions):
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
        try:
            if user_id is not None:
                return super().get_cursor.execute(
                    "SELECT * FROM QuizResults WHERE user_id=?;", (user_id,)).fetchall()
            else:
                return super().get_cursor.execute(
                    "SELECT * FROM QuizResults;").fetchall()
        except Exception as e:
            print("An error has occurred.", e)

    def delete_result(self, result_id):
        try:
            super().get_cursor.execute(
                "DELETE FROM QuizResults WHERE result_id=?;", (result_id,))
            super().get_connection.commit()
            print(f"Result ID {result_id} deleted successfully.")
        except Exception as e:
            print("An error has occurred.", e)

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS QuizResults;

                CREATE TABLE QuizResults (
                    result_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    user_id INTEGER NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    date_taken DATETIME
                );
            """
            super().execute_script(sql)
            self._conn.commit()
            print("QuizResults table created successfully.")
        except Exception as e:
            print("An error has occurred.", e)