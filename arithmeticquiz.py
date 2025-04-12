import random
import time
import customtkinter as ctk


class ArithmeticQuizApp(ctk.CTk):
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.root.geometry("400x400")

        # dark mode, dark blue theme for the app 
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # setting variables
        self.game_mode = None
        self.difficulty = None
        self.time_limit = None
        self.score = 0
        self.question_amount = None
        self.streak_length = 0
        self.questions_attempted = 0
        self.current_streak = 0

        # starting with welcome page
        self.show_welcome_page()

    def show_welcome_page(self):
        for widget in self.root.winfo_children():  # clean slate
            widget.destroy()
        
        welcome_label = ctk.CTkLabel(
            self.root,
            text='Welcome to the Arithmetic Quiz!',
            font=('Arial', 24, 'bold')
        )
        welcome_label.pack(pady=20)

        start_button = ctk.CTkButton(
            self.root,
            text='Start Quiz',
            command=self.show_mode_selection
        )
        start_button.pack(pady=20)

    def show_mode_selection(self): 
        pass

if __name__ == "__main__":
    root = ctk.CTk()
    app = ArithmeticQuizApp(root)
    root.mainloop()