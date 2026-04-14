# Run this ONCE after db_setup.py to populate the Questions table from the CSV file.
# This script reads questions.csv and inserts each row into the database.
import QuizDB as qdb
import csv

# Question class maps each row from the CSV file to an object with names attributes
class Question:
    def __init__(self, row):
        self.question_id = row[0]
        self.question = row[1]
        self.choice_a = row[2]
        self.choice_b = row[3]
        self.choice_c = row[4]
        self.choice_d = row[5]
        self.correct_answer = row[6]

# QuizImport inherits from Questions to gain access to the database connection
class QuizImport(qdb.Questions):

    def __init__(self):
        # Initializes the parent class to connect to quiz.sqlite
        super().__init__()

    def read_questions(self, file_name):
        # Opens the CSV file and parses each row into a Question object
        self.questions_list = []

        try:
            with open(file_name, 'r') as record:
                csv_contents = csv.reader(record)
                next(csv_contents)  # skip header row
                for row in csv_contents:
                    # Creates a Question object for each row and add to the list
                    question = Question(row)
                    self.questions_list.append(question)
            print(f"Successfully read {len(self.questions_list)} questions from {file_name}")

        except FileNotFoundError:
            # Handles case where the CSV file cannot be found
            print(f"Error: Could not find file '{file_name}'")
        except Exception as e:
            print("An error has occurred.", e)

    def save_to_database(self):
        # Confirms with user before inserting all questions into the database
        print(f"Number of questions to save: {len(self.questions_list)}")
        save = input("Continue? (y/n) ").lower()

        if save == "y":
            for item in self.questions_list:
                try:
                    # Inserts each question into the Questions table
                    super().get_cursor.execute("""
                        INSERT INTO Questions 
                        (question, choice_a, choice_b, choice_c, choice_d, correct_answer)
                        VALUES (?, ?, ?, ?, ?, ?);""",
                        (item.question, item.choice_a, item.choice_b,
                         item.choice_c, item.choice_d, item.correct_answer))
                    super().get_connection.commit()
                    # Prints first 30 characters of question to confirm it saved
                    print(f"Saved question: {item.question_id} - {item.question[:30]}...")
                except Exception as e:
                    print("An error has occurred.", e)
            print("Import complete!")
        else:
            print("Save to database aborted.")


# Run the import
# Creates an instance of QuizImport, reads the CSV, and saves to the database
importer = QuizImport()
importer.read_questions("questions.csv")
importer.save_to_database()