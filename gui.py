import customtkinter as ctk
from tkinter import font as tkfont
from PIL import Image, ImageTk
from main import start_game
from chessboard import ChessBoard
import threading

class ChessApp(ctk.CTk):
    def __init__(self, update_label_callback, update_eval_bar_callback, update_best_moves_callback):
        super().__init__()
        self.title("Scacchi")
        self.geometry("600x1000")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.update_label_callback = update_label_callback
        self.update_eval_bar_callback = update_eval_bar_callback
        self.update_best_moves_callback = update_best_moves_callback
        self.start_page = StartPage(self)
        self.difficulty_page = DifficultyPage(self)
        self.game_frame = ctk.CTkFrame(self)
        self.chessboard = ChessBoard(self.game_frame)
        self.label = ctk.CTkLabel(self.game_frame, text="", bg_color="grey", text_color="black", font=ctk.CTkFont(size=18))

        # Labels per le migliori mosse
        self.first_move_label = ctk.CTkLabel(self.game_frame, text="", text_color="white", font=ctk.CTkFont(size=18))
        self.second_move_label = ctk.CTkLabel(self.game_frame, text="", text_color="white", font=ctk.CTkFont(size=18))
        self.third_move_label = ctk.CTkLabel(self.game_frame, text="", text_color="white", font=ctk.CTkFont(size=18))

        # Pulsanti
        self.toggle_eval_button = ctk.CTkButton(self.game_frame, text="Toggle Eval Bar", command=self.toggle_eval_bar)
        self.toggle_best_moves_button = ctk.CTkButton(self.game_frame, text="Toggle Best Moves", command=self.toggle_best_moves)

        self.eval_bar = ctk.CTkCanvas(self.game_frame, width=512, height=20, bg="white")
        self.show_eval_bar = False
        self.show_best_moves = False

        self.start_page.pack(fill="both", expand=True)
        self.update_gui()
        self.resizable(False, False)

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
        self.label.pack(fill="x")
        self.toggle_eval_button.pack(side="bottom")
        self.toggle_best_moves_button.pack(side="bottom")
        self.chessboard.pack(side="top", fill="both", expand=True)
        self.update_label("waiting for first move")
        threading.Thread(target=start_game, args=(self.update_label_callback, self.update_eval_bar, difficulty, self.chessboard, self.update_best_moves_callback)).start()

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

    def toggle_best_moves(self):
        self.show_best_moves = not self.show_best_moves
        if self.show_best_moves:
            self.first_move_label.pack()
            self.second_move_label.pack()
            self.third_move_label.pack()
        else:
            self.first_move_label.pack_forget()
            self.second_move_label.pack_forget()
            self.third_move_label.pack_forget()

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

    def update_best_moves(self, moves):
        if not self.show_best_moves:
            return
        self.first_move_label.configure(text=moves[0] if len(moves) > 0 else "")
        self.second_move_label.configure(text=moves[1] if len(moves) > 1 else "")
        self.third_move_label.configure(text=moves[2] if len(moves) > 2 else "")

    def update_gui(self):
        self.after(100, self.update_gui)


class StartPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg_color="white")

        # Carica l'immagine
        img = Image.open("images/chesslogo.png")
        img = img.resize((180, 180), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(img)

        # Crea un CTkLabel con l'immagine come sfondo
        image_label = ctk.CTkLabel(self, image=self.image, text="")

        # Posiziona l'immagine in alto al centro
        image_label.pack(side="top", pady=20)

        pvc = ctk.CTkButton(self, text="Player vs computer", text_color="white", font=ctk.CTkFont(size=14),
                            command=master.show_difficulty_page, width=300)
        pvc.pack(pady=20)  # Aggiungi fill="x" per espandere il pulsante orizzontalmente

        pvp = ctk.CTkButton(self, text="Player vs Player", text_color="white", font=ctk.CTkFont(size=14),
                            command=master.show_difficulty_page, width=300)
        pvp.pack(pady=20)  # Aggiungi fill="x" per espandere il pulsante orizzontalmente


class DifficultyPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg_color="grey")

        self.title = ctk.CTkLabel(self, text="Select difficulty", font=ctk.CTkFont(size=20), text_color="white")
        self.title.pack(pady=20)

        self.goback = ctk.CTkButton(self, text="Go back", text_color="white", font=ctk.CTkFont(size=14), command=master.show_start_page)
        self.goback.pack(pady=20)
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

def update_best_moves(moves):
    app.update_best_moves(moves)

if __name__ == "__main__":
    app = ChessApp(update_label, update_eval_bar, update_best_moves)
    app.mainloop()
