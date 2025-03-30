import tkinter as tk
from tkinter import messagebox
import random

class MultiplicationQuiz:
    def __init__(self, master):
        self.master = master
        self.master.title("Multiplication Quiz")
        self.master.geometry("300x200")

        self.score = 0
        self.total_questions = 0

        self.question_label = tk.Label(master, text="", font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.answer_entry = tk.Entry(master, font=("Arial", 14))
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(master, text="Submit", command=self.check_answer)
        self.submit_button.pack(pady=10)

        self.score_label = tk.Label(master, text="Score: 0/0", font=("Arial", 12))
        self.score_label.pack(pady=10)

        self.new_question()

    def new_question(self):
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
        self.question_label.config(text=f"{self.num1} x {self.num2} = ?")
        self.answer_entry.delete(0, tk.END)

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
            correct_answer = self.num1 * self.num2
            self.total_questions += 1

            if user_answer == correct_answer:
                self.score += 1
                messagebox.showinfo("Correct!", "Your answer is correct!")
            else:
                messagebox.showerror("Incorrect", f"The correct answer is {correct_answer}")

            self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")
            self.new_question()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

if __name__ == "__main__":
    root = tk.Tk()
    quiz = MultiplicationQuiz(root)
    root.mainloop()