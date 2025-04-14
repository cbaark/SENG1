import random
import time
import customtkinter as ctk

# TODO:
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
        self.geometry("500x500")

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
        self.nav_history = []

        # tracker
        self.error_window = None
        self.timer_id = None  # Add timer ID tracker

        # keyboard bindings
        self.bind('<Escape>', lambda e: self.show_quit_dialog())
        self.bind('<Return>', lambda e: self.handle_return_key())
        self.bind('<KP_Enter>', lambda e: self.handle_return_key()) 

        # starting with welcome page
        self.show_welcome_page()

    # HISTORY NAVIGATION

    def push_to_history(self, current_page):
        """Add current page to navigation history"""
        self.nav_history.append(current_page)

    def go_back(self):
        """Navigate to previous page"""
        if len(self.nav_history) > 1:
            self.nav_history.pop()  # remove page
            previous_page = self.nav_history[-1]  # call prev page
            self.nav_history.pop()  # remove prev page to be called again
        
        # call page
        if previous_page == "welcome":
            self.show_welcome_page()
        elif previous_page == "mode":
            self.show_mode_selection()
        elif previous_page == "difficulty":
            self.show_difficulty_selection()
        elif previous_page == "custom":
            self.show_custom_difficulty()
        elif previous_page == "time":
            self.show_time_selection()
        elif previous_page == "questions":
            self.show_question_amount()
        elif previous_page == "streak":
            self.show_streak_selection()

    def show_welcome_page(self):
        # cancel timer when returning to menu
        self.cancel_timer()
        self.push_to_history("welcome")
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

        # add help button
        help_button = ctk.CTkButton(
            self,
            text="Help & Instructions",
            command=self.show_help_page
        )
        help_button.pack(pady=10)

    def show_help_page(self):
        """Show help and instructions page"""
        self.geometry('600x700')
        for widget in self.winfo_children():
            widget.destroy()
            
        # title
        help_label = ctk.CTkLabel(
            self,
            text="Help & Instructions",
            font=("Arial", 24, "bold")
        )
        help_label.pack(pady=20)
        
        # instructions text
        instructions = """
        Game Modes:
        • Timed Mode: Answer as many questions as you can within the time limit
        • Fixed Mode: Answer a set number of questions
        • Streak Mode: Try to get a streak of correct answers
        
        Difficulty Levels:
        • Easy: Addition and subtraction (1-10)
        • Medium: Add multiplication (1-15)
        • Hard: Add division (1-20)
        • Custom: Create your own settings
        
        Keyboard Shortcuts:
        • Enter/Return: Submit answer
        • Escape: Quit quiz
        • Numpad: Supported for number entry
        
        Tips:
        • Use keyboard for faster input
        • Watch your time in timed mode
        • Practice with easy mode first
        """
        
        text_box = ctk.CTkTextbox(self, width=500, height=400)
        text_box.pack(pady=10)
        text_box.insert("1.0", instructions)
        text_box.configure(state="disabled")
        
        back_button = ctk.CTkButton(
            self,
            text="Back to Menu",
            command=self.show_welcome_page
        )
        back_button.pack(pady=20)

    def show_mode_selection(self): 
        self.push_to_history("mode")
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

        # Add back button
        back_button = ctk.CTkButton(
            self,
            text="Back",
            command=self.go_back
        )
        back_button.pack(pady=10)

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
        self.push_to_history("difficulty")
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

        # Add back button
        back_button = ctk.CTkButton(
            self,
            text="Back",
            command=self.go_back
        )
        back_button.pack(pady=10)

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
        self.push_to_history("custom")
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

        # Add back button below submit button
        back_button = ctk.CTkButton(
            self,
            text="Back",
            command=self.go_back
        )
        back_button.pack(pady=10)

    def show_time_selection(self):
        self.push_to_history("time")
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

        # Add back button
        back_button = ctk.CTkButton(
            self,
            text="Back",
            command=self.go_back
        )
        back_button.pack(pady=10)

    def show_question_amount(self):
        self.push_to_history("questions")
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

        # Add back button
        back_button = ctk.CTkButton(
            self,
            text="Back",
            command=self.go_back
        )
        back_button.pack(pady=10)

    def show_streak_selection(self):
        self.push_to_history("streak")
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

        # back 2 menu
        back_button = ctk.CTkButton(
            self,
            text="Back",
            command=self.go_back
        )
        back_button.pack(pady=10)

    def process_custom_difficulty(self):
        selected_operators = [op for op, var in self.operator_vars.items() if var.get()]
        if not selected_operators:
            self.show_error_message("Please select at least one operator")
            return
            
        try:
            min_val = int(self.min_entry.get() or 1)
            max_val = int(self.max_entry.get() or 20)
            if min_val >= max_val:
                self.show_error_message("Maximum value must be greater than minimum value")
                return
            if min_val < 0:
                self.show_error_message("Numbers must be positive")
                return
        except ValueError:
            self.show_error_message("Please enter valid numbers for the range")
            return

        self.set_difficulty({
            "name": "Custom",
            "operators": selected_operators,
            "range": [min_val, max_val]
        })

    def process_time_selection(self):
        try:
            time_limit = int(self.time_entry.get() or 60)
            if time_limit <= 0:
                self.show_error_message("Please enter a positive number of seconds")
                return
            if time_limit > 3600:  # 1 hour max
                self.show_error_message("Time limit cannot exceed 1 hour (3600 seconds)")
                return
            self.time_limit = time_limit
            self.start_quiz()
        except ValueError:
            self.show_error_message("Please enter a valid number")

    def process_question_amount(self):
        try:
            amount = int(self.amount_entry.get() or 10)
            if amount <= 0:
                self.show_error_message("Please enter a positive number of questions")
                return
            if amount > 100:  # Reasonable maximum
                self.show_error_message("Maximum 100 questions allowed")
                return
            self.question_amount = amount
            self.start_quiz()
        except ValueError:
            self.show_error_message("Please enter a valid number")

    def process_streak_selection(self):
        try:
            streak = int(self.streak_entry.get() or 5)
            if streak <= 0:
                self.show_error_message("Please enter a positive streak goal")
                return
            if streak > 50:  # Reasonable maximum
                self.show_error_message("Maximum streak goal is 50")
                return
            self.streak_length = streak
            self.start_quiz()
        except ValueError:
            self.show_error_message("Please enter a valid number")

    def start_quiz(self):
        self.score = 0
        self.questions_attempted = 0
        self.current_streak = 0
        self.start_time = time.time()
        self.show_quiz_interface()

    def show_quiz_interface(self):
        # Cancel any existing timer first
        self.cancel_timer()
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

        submit_button = ctk.CTkButton(
            answer_frame,
            text="Submit",
            command=self.check_answer
        )
        submit_button.pack(pady=10)

        # result label 
        self.result_label = ctk.CTkLabel(
            answer_frame,
            text="",
            font=("Arial", 16),
            text_color="white" # default color
        )
        self.result_label.pack(pady=10)

        self.answer_entry.focus()

        # timer update for timed mode
        if self.game_mode == "timed":
            self.update_timer()

    def generate_question(self):
        operators = self.difficulty["operators"]
        num_range = self.difficulty["range"]
        
        operator = random.choice(operators)
        
        if self.difficulty["name"] == "Easy":
            # no negative answers in easy mode
            if operator == "-":
                num2 = random.randint(num_range[0], num_range[1])
                num1 = random.randint(num2, num_range[1])  # num1 will always be >= num2
            elif operator == "/":
                num2 = random.randint(1, num_range[1])
                multiplier = random.randint(1, num_range[1] // num2)
                num1 = num2 * multiplier  # ensures whole number division
            else:
                num1 = random.randint(num_range[0], num_range[1])
                num2 = random.randint(num_range[0], num_range[1])
        else:
            # other difficulties
            if operator == "/":
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
                self.result_label.configure(text="Correct!", text_color="green")
            else:
                self.current_streak = 0
                self.result_label.configure(
                    text=f"Incorrect! The correct answer was {self.question['answer']}", 
                    text_color="red"
                )

            self.show_result(correct)
            
        except ValueError:
            self.show_error_message("Please enter a valid number")
            self.answer_entry.delete(0, 'end')

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
            # clear result label when showing next question
            self.after(1000, lambda: self.result_label.configure(text=""))

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
        """Update the timer display and schedule next update"""
        if self.game_mode == "timed" and not self.should_end_quiz():
            self.status_label.configure(text=self.get_status_text())
            # Store the timer ID
            self.timer_id = self.after(1000, self.update_timer)

    def cancel_timer(self):
        """Cancel any existing timer callback"""
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    def show_end_screen(self):
        # Cancel timer when quiz ends
        self.cancel_timer()
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

    def show_quit_dialog(self):
        """Show confirmation dialog when quitting"""
        quit_window = ctk.CTkToplevel(self)
        quit_window.title("Quit?")
        quit_window.geometry("300x150")
        quit_window.transient(self)  # display on top
        quit_window.lift()
        
        label = ctk.CTkLabel(
            quit_window,
            text="Are you sure you want to quit?",
            font=("Arial", 16)
        )
        label.pack(pady=20)
        
        button_frame = ctk.CTkFrame(quit_window)
        button_frame.pack(pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Yes",
            command=self.quit
        ).pack(side='left', padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="No",
            command=quit_window.destroy
        ).pack(side='left', padx=10)

    def handle_return_key(self):
        """Handle Return key press based on current screen"""
        if hasattr(self, 'answer_entry') and self.answer_entry.winfo_viewable():
            self.check_answer()

    def show_error_message(self, message):
        """Show error message in a popup"""
        # update message if window exists alreaady
        if hasattr(self, 'error_window') and self.error_window is not None:
            try:
                # update error window status
                self.error_window.lift()
                for widget in self.error_window.winfo_children():
                    if isinstance(widget, ctk.CTkLabel):
                        widget.configure(text=message)
                return
            except ctk.TclError:  # window close
                self.error_window = None
        
        # create new error window
        self.error_window = ctk.CTkToplevel(self)
        self.error_window.title("Error")
        self.error_window.geometry("400x150")
        self.error_window.transient(self)
        self.error_window.lift()
        
        label = ctk.CTkLabel(
            self.error_window,
            text=message,
            font=("Arial", 16)
        )
        label.pack(pady=20)
        
        def close_error():
            self.error_window.destroy()
            self.error_window = None
        
        ctk.CTkButton(
            self.error_window,
            text="OK",
            command=close_error
        ).pack(pady=10)

# start the app
if __name__ == "__main__":
    app = ArithmeticQuizApp()
    app.mainloop()