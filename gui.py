import customtkinter as ctk
from tkinter import font as tkfont
from main import start_game
from chessboard import ChessBoard
import threading

class ChessApp(ctk.CTk):
    def __init__(self, update_label_callback, update_eval_bar_callback):
        super().__init__()
        self.title("Scacchi")
        self.geometry("600x1000")

        self.update_label_callback = update_label_callback
        self.update_eval_bar_callback = update_eval_bar_callback
        self.start_page = StartPage(self)
        self.difficulty_page = DifficultyPage(self)
        self.game_frame = ctk.CTkFrame(self)
        self.chessboard = ChessBoard(self.game_frame)
        self.label = ctk.CTkLabel(self.game_frame, text="", bg_color="grey", text_color="black", font=ctk.CTkFont(size=18))

        self.toggle_eval_button = ctk.CTkButton(self.game_frame, text="Toggle Eval Bar", command=self.toggle_eval_bar)
        self.eval_bar = ctk.CTkCanvas(self.game_frame, width=512, height=20, bg="white")
        self.show_eval_bar = False

        self.start_page.pack(fill="both", expand=True)
        self.update_gui()

    def show_start_page(self):
        self.difficulty_page.pack_forget()
        self.game_frame.pack_forget()
        self.start_page.pack(fill="both", expand=True)

    def show_difficulty_page(self):
        self.start_page.pack_forget()
        self.game_frame.pack_forget()
        self.difficulty_page.pack(fill="both", expand=True)
        self.difficulty_page.focus_set()

    def show_game_page(self, difficulty):
        self.difficulty_page.pack_forget()
        self.start_page.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        self.label.pack(side="bottom", fill="x")
        self.toggle_eval_button.pack(side="bottom")
        self.chessboard.pack(side="top", fill="both", expand=True)
        self.update_label("waiting for first move")
        threading.Thread(target=start_game, args=(self.update_label_callback, self.update_eval_bar, difficulty, self.chessboard)).start()

    def update_label(self, text):
        self.label.configure(text=text)

    def toggle_eval_bar(self):
        self.show_eval_bar = not self.show_eval_bar
        if self.show_eval_bar:
            self.eval_bar.place(relx=0.5, y=562, width=512, height=20, anchor='n')
            self.eval_bar.create_rectangle(0, 0, 256, 20, fill="black", outline="black")
            self.eval_bar.create_rectangle(256, 0, 512, 20, fill="white", outline="black")
        else:
            self.eval_bar.place_forget()

    def update_eval_bar(self, eval_score):
        if not self.show_eval_bar:
            return
        self.eval_bar.delete("eval")
        middle_x = 256
        if eval_score > 0:
            eval_width = min(512, middle_x * eval_score / 10)
            self.eval_bar.create_rectangle(middle_x - eval_width, 0, middle_x, 20, fill="white",
                                                   outline="grey", tags="eval")
        else:
            eval_width = min(512, middle_x * abs(eval_score) / 10)
            self.eval_bar.create_rectangle(middle_x, 0, middle_x + eval_width, 20, fill="black",
                                                   outline="grey", tags="eval")

    def update_gui(self):
        self.after(100, self.update_gui)

class StartPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg_color="white")
        button = ctk.CTkButton(self, text="Start Game", fg_color="red", text_color="black", font=ctk.CTkFont(size=18),
                               command=master.show_difficulty_page)
        button.pack(pady=200)

class DifficultyPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg_color="grey")

        self.buttons = [
            self.create_button("Easy", 1),
            self.create_button("Medium", 10),
            self.create_button("Hard", 20)
        ]
        self.current_button_index = 0

        self.buttons[self.current_button_index].focus_set()
        for button in self.buttons:
            button.bind("<Up>", self.move_focus_up)
            button.bind("<Down>", self.move_focus_down)
            button.bind("<Return>", self.select_button)
        self.focus_set()

        self.highlight_button(self.current_button_index)

    def create_button(self, text, difficulty):
        button = ctk.CTkButton(self, text=text, command=lambda: self.master.show_game_page(difficulty), font=ctk.CTkFont(size=18))
        button.pack(pady=20)
        return button

    def highlight_button(self, index):
        for i, btn in enumerate(self.buttons):
            if i == index:
                btn.configure(fg_color="yellow")
            else:
                btn.configure(fg_color="grey")

    def move_focus_up(self, event):
        self.current_button_index = (self.current_button_index - 1) % len(self.buttons)
        self.highlight_button(self.current_button_index)

    def move_focus_down(self, event):
        self.current_button_index = (self.current_button_index + 1) % len(self.buttons)
        self.highlight_button(self.current_button_index)

    def select_button(self, event):
        self.buttons[self.current_button_index].invoke()
        return "break"

def update_label(text):
    app.update_label(text)

def update_eval_bar(eval_score):
    app.update_eval_bar(eval_score)

if __name__ == "__main__":
    app = ChessApp(update_label, update_eval_bar)
    app.mainloop()
