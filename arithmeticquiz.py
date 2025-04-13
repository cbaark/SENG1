import random
import time
import customtkinter as ctk

# TODO: input validation/error handling for invalid inputs
# help/insturctions page on welcome page
# keyboard bindings (esc for quit etc..)
# improve current error messages
# confirmation dialog for quitting
# progress bar for fixed mode
# custom icons for modes
# color code correct/incorrect answers
# practice mode/infinite mode where users can practice without any conditions
# support for numpad
# optimise question generation how though???
# sound effects for correct/incorrect answers???
# tooltips for what easy, medium, hard mode means and text underneath telling users to hover over the buttons to see what it means???
# perfect score celebration screen???
# light mode option?? high contrast option??
# settings page for customisation of stuff said above

# VENI VIDI VICI

class ArithmeticQuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()  # initialise the parent CTk class
        self.title("Arithmetic Quiz")
        self.geometry("400x400")

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
        for widget in self.winfo_children():  # clean slate
            widget.destroy()
        
        welcome_label = ctk.CTkLabel(
            self,
            text='Welcome to the Arithmetic Quiz!',
            font=('Arial', 24, 'bold')
        ).pack(pady=20)

        start_button = ctk.CTkButton(
            self,
            text='Start Quiz',
            command=self.show_difficulty_selection
        ).pack(pady=20)

    def show_mode_selection(self): 
        for widget in self.winfo_children():
            widget.destroy()

        # title label
        mode_label = ctk.CTkLabel(
            self,
            text='Select Game Mode',
            font=('Arial', 24, 'bold')
        ).pack(pady=20)

        # mode buttons
        timed_button = ctk.CTkButton(
            self,
            text='Timed Mode',
            command=lambda: self.set_game_mode("timed")
        ).pack(pady=10)

        fixed_button = ctk.CTkButton(
            self,
            text='Fixed Amount Mode',
            command=lambda: self.set_game_mode("fixed")
        ).pack(pady=10)

        streak_button = ctk.CTkButton(
            self,
            text='Streak Mode',
            command=lambda: self.set_game_mode("streak")
        ).pack(pady=10)

    def set_game_mode(self, mode):
        self.game_mode = mode
        if self.difficulty: 
            if mode == "timed":
                self.show_time_selection()
            elif mode == "fixed":
                self.show_question_amount()
            else:
                self.show_streak_selection()
        else:
            self.show_difficulty_selection()

    def show_difficulty_selection(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Title label
        difficulty_label = ctk.CTkLabel(
            self,
            text="Select Difficulty Level",
            font=("Arial", 24, "bold")
        )
        difficulty_label.pack(pady=20)

        # Difficulty buttons
        easy_button = ctk.CTkButton(
            self,
            text="Easy",
            command=lambda: self.set_difficulty({
                "name": "Easy",
                "operators": ["+", "-"],
                "range": [1, 10]
            })
        )
        easy_button.pack(pady=10)

        medium_button = ctk.CTkButton(
            self,
            text="Medium",
            command=lambda: self.set_difficulty({
                "name": "Medium",
                "operators": ["+", "-", "*"],
                "range": [1, 15]
            })
        )
        medium_button.pack(pady=10)

        hard_button = ctk.CTkButton(
            self,
            text="Hard",
            command=lambda: self.set_difficulty({
                "name": "Hard",
                "operators": ["+", "-", "*", "/"],
                "range": [1, 20]
            })
        )
        hard_button.pack(pady=10)

        custom_button = ctk.CTkButton(
            self,
            text="Custom",
            command=self.show_custom_difficulty
        )
        custom_button.pack(pady=10)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        if self.game_mode == "timed":
            self.show_time_selection()
        elif self.game_mode == "fixed":
            self.show_question_amount()
        elif self.game_mode == "streak":
            self.show_streak_selection()
        else:
            self.show_mode_selection()

    def show_custom_difficulty(self):
        for widget in self.winfo_children():
            widget.destroy()

        # title label
        custom_label = ctk.CTkLabel(
            self,
            text="Customize Difficulty",
            font=("Arial", 24, "bold")
        )
        custom_label.pack(pady=20)

        # select operator
        operator_frame = ctk.CTkFrame(self)
        operator_frame.pack(pady=10)
        
        self.operator_vars = {
            '+': ctk.BooleanVar(value=True),
            '-': ctk.BooleanVar(value=True),
            '*': ctk.BooleanVar(value=False),
            '/': ctk.BooleanVar(value=False)
        }

        for operator in self.operator_vars:
            checkbox = ctk.CTkCheckBox(
                operator_frame,
                text=operator,
                variable=self.operator_vars[operator]
            )
            checkbox.pack(side='left', padx=5)

        # number range
        range_frame = ctk.CTkFrame(self)
        range_frame.pack(pady=10)

        ctk.CTkLabel(range_frame, text="Number Range:").pack()
        
        self.min_entry = ctk.CTkEntry(range_frame, placeholder_text="Min (1)")
        self.min_entry.pack(side='left', padx=5)
        
        self.max_entry = ctk.CTkEntry(range_frame, placeholder_text="Max (20)")
        self.max_entry.pack(side='left', padx=5)

        # submission button
        submit_button = ctk.CTkButton(
            self,
            text="Continue",
            command=self.process_custom_difficulty
        )
        submit_button.pack(pady=20)

    def show_time_selection(self):
        for widget in self.winfo_children():
            widget.destroy()

        time_label = ctk.CTkLabel(
            self,
            text="Select Time Limit (seconds)",
            font=("Arial", 24, "bold")
        )
        time_label.pack(pady=20)

        self.time_entry = ctk.CTkEntry(self, placeholder_text="60")
        self.time_entry.pack(pady=10)

        submit_button = ctk.CTkButton(
            self,
            text="Start Quiz",
            command=self.process_time_selection
        )
        submit_button.pack(pady=20)

    def show_question_amount(self):
        for widget in self.winfo_children():
            widget.destroy()

        amount_label = ctk.CTkLabel(
            self,
            text="Number of Questions",
            font=("Arial", 24, "bold")
        )
        amount_label.pack(pady=20)

        self.amount_entry = ctk.CTkEntry(self, placeholder_text="10")
        self.amount_entry.pack(pady=10)

        submit_button = ctk.CTkButton(
            self,
            text="Start Quiz",
            command=self.process_question_amount
        )
        submit_button.pack(pady=20)

    def show_streak_selection(self):
        for widget in self.winfo_children():
            widget.destroy()

        streak_label = ctk.CTkLabel(
            self,
            text="Streak Goal",
            font=("Arial", 24, "bold")
        )
        streak_label.pack(pady=20)

        self.streak_entry = ctk.CTkEntry(self, placeholder_text="5")
        self.streak_entry.pack(pady=10)

        submit_button = ctk.CTkButton(
            self,
            text="Start Quiz",
            command=self.process_streak_selection
        )
        submit_button.pack(pady=20)

    def process_custom_difficulty(self):
        selected_operators = [op for op, var in self.operator_vars.items() if var.get()]
        if not selected_operators:
            return  
            
        try:
            min_val = int(self.min_entry.get() or 1)
            max_val = int(self.max_entry.get() or 20)
            if min_val >= max_val:
                return  
        except ValueError:
            return  

        self.set_difficulty({
            "name": "Custom",
            "operators": selected_operators,
            "range": [min_val, max_val]
        })

    def process_time_selection(self):
        try:
            self.time_limit = int(self.time_entry.get() or 60)
            if self.time_limit <= 0:
                return  
            self.start_quiz()
        except ValueError:
            return  

    def process_question_amount(self):
        try:
            self.question_amount = int(self.amount_entry.get() or 10)
            if self.question_amount <= 0:
                return  
            self.start_quiz()
        except ValueError:
            return  

    def process_streak_selection(self):
        try:
            self.streak_length = int(self.streak_entry.get() or 5)
            if self.streak_length <= 0:
                return  
            self.start_quiz()
        except ValueError:
            return  
    def start_quiz(self):
        self.score = 0
        self.questions_attempted = 0
        self.current_streak = 0
        self.start_time = time.time()
        self.show_quiz_interface()

    def show_quiz_interface(self):
        for widget in self.winfo_children():
            widget.destroy()

        # top frame
        status_frame = ctk.CTkFrame(self)
        status_frame.pack(fill='x', padx=20, pady=10)

        self.status_label = ctk.CTkLabel(
            status_frame,
            text=self.get_status_text(),
            font=("Arial", 14)
        )
        self.status_label.pack(side='left', padx=10)

        self.score_label = ctk.CTkLabel(
            status_frame,
            text=f"Score: {self.score}/{self.questions_attempted}",
            font=("Arial", 14)
        )
        self.score_label.pack(side='right', padx=10)

        # middle frame
        question_frame = ctk.CTkFrame(self)
        question_frame.pack(pady=20)

        self.question = self.generate_question()
        question_text = f"{self.question['num1']} {self.question['operator']} {self.question['num2']} = ?"
        
        self.question_label = ctk.CTkLabel(
            question_frame,
            text=question_text,
            font=("Arial", 32, "bold")
        )
        self.question_label.pack(pady=20)

        # bottom frame
        answer_frame = ctk.CTkFrame(self)
        answer_frame.pack(pady=20)

        self.answer_entry = ctk.CTkEntry(
            answer_frame,
            placeholder_text="Enter your answer",
            width=200
        )
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())

        submit_button = ctk.CTkButton(
            answer_frame,
            text="Submit",
            command=self.check_answer
        )
        submit_button.pack(pady=10)

        self.answer_entry.focus()

        # timer update for timed mode
        if self.game_mode == "timed":
            self.update_timer()

    def generate_question(self):
        operators = self.difficulty["operators"]
        num_range = self.difficulty["range"]
        
        operator = random.choice(operators)
        
        if self.difficulty["name"] == "Easy":
            if operator == "-":
                # avoid negative answers for easy mode
                num2 = random.randint(num_range[0], num_range[1])
                num1 = random.randint(num2, num_range[1])
            else:
                num1 = random.randint(num_range[0], num_range[1])
                num2 = random.randint(num_range[0], num_range[1])

        if operator == "/":
            # whole numbers only for division
            num2 = random.randint(1, num_range[1])
            multiplier = random.randint(1, num_range[1] // num2)
            num1 = num2 * multiplier
        else:
            num1 = random.randint(num_range[0], num_range[1])
            num2 = random.randint(num_range[0], num_range[1])

        return {
            "num1": num1,
            "num2": num2,
            "operator": operator,
            "answer": self.calculate_answer(num1, operator, num2)
        }

    def calculate_answer(self, num1, operator, num2):
        if operator == "+":
            return num1 + num2
        elif operator == "-":
            return num1 - num2
        elif operator == "*":
            return num1 * num2
        elif operator == "/":
            return num1 // num2

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
            correct = user_answer == self.question["answer"]
            
            self.questions_attempted += 1
            if correct:
                self.score += 1
                self.current_streak += 1
            else:
                self.current_streak = 0

            self.show_result(correct)
            
        except ValueError:
            # error handling for non int
            self.answer_entry.delete(0, 'end')
            return

    def show_result(self, correct):
        # clear answer_entry
        self.answer_entry.delete(0, 'end')
        
        # update score
        self.score_label.configure(text=f"Score: {self.score}/{self.questions_attempted}")
        
        # quiz end check
        if self.should_end_quiz():
            self.show_end_screen()
        else:
            # make and show next question
            self.question = self.generate_question()
            self.question_label.configure(
                text=f"{self.question['num1']} {self.question['operator']} {self.question['num2']} = ?"
            )
            self.status_label.configure(text=self.get_status_text())

    def should_end_quiz(self):
        if self.game_mode == "timed":
            return time.time() - self.start_time >= self.time_limit
        elif self.game_mode == "fixed":
            return self.questions_attempted >= self.question_amount
        else:  # streak mode
            return self.current_streak >= self.streak_length

    def get_status_text(self):
        if self.game_mode == "timed":
            time_left = max(0, self.time_limit - int(time.time() - self.start_time))
            return f"Time left: {time_left}s"
        elif self.game_mode == "fixed":
            return f"Question {self.questions_attempted + 1}/{self.question_amount}"
        else:
            return f"Current streak: {self.current_streak}/{self.streak_length}"

    def update_timer(self):
        if self.game_mode == "timed" and not self.should_end_quiz():
            self.status_label.configure(text=self.get_status_text())
            self.after(1000, self.update_timer)

    def show_end_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        # end screen
        title_label = ctk.CTkLabel(
            self,
            text="Quiz Complete!",
            font=("Arial", 32, "bold")
        )
        title_label.pack(pady=20)

        # final score
        score_label = ctk.CTkLabel(
            self,
            text=f"Final Score: {self.score}/{self.questions_attempted}",
            font=("Arial", 24)
        )
        score_label.pack(pady=10)

        # extra stats based on game mode
        if self.game_mode == "timed":
            time_taken = int(time.time() - self.start_time)
            stats_label = ctk.CTkLabel(
                self,
                text=f"Time taken: {time_taken} seconds\nQuestions per minute: {(self.questions_attempted * 60) // time_taken}",
                font=("Arial", 18)
            )
            stats_label.pack(pady=10)
        elif self.game_mode == "streak":
            stats_label = ctk.CTkLabel(
                self,
                text=f"Highest streak: {self.current_streak}",
                font=("Arial", 18)
            )
            stats_label.pack(pady=10)

        # accuracy percentage
        if self.questions_attempted > 0:
            accuracy = (self.score / self.questions_attempted) * 100
            accuracy_label = ctk.CTkLabel(
                self,
                text=f"Accuracy: {accuracy:.1f}%",
                font=("Arial", 18)
            )
            accuracy_label.pack(pady=10)

        # button frame
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=20)

        # play again button
        play_again_button = ctk.CTkButton(
            buttons_frame,
            text="Play Again",
            command=self.show_difficulty_selection
        )
        play_again_button.pack(side='left', padx=10)

        # main menu button
        main_menu_button = ctk.CTkButton(
            buttons_frame,
            text="Main Menu",
            command=self.show_welcome_page
        )
        main_menu_button.pack(side='left', padx=10)

# start the app
if __name__ == "__main__":
    app = ArithmeticQuizApp()
    app.mainloop()