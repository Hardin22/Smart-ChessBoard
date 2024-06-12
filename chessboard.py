import tkinter as tk
from PIL import Image, ImageTk
import chess
import os

class ChessBoard(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master if master else tk.Tk()
        self.canvas = tk.Canvas(self.master, width=512, height=512)
        self.canvas.pack()
        self.canvas.pack_configure(pady=(40, 0))  # Adds a top margin of 40 pixels
        self.images = {}
        self.load_images()
        self.draw_board()
        self.update_board(chess.Board().fen())

    def load_images(self):
        pieces = {
            'r': 'r.png',
            'n': 'n.png',
            'b': 'b.png',
            'q': 'q.png',
            'k': 'k.png',
            'p': 'p.png',
            'R': 'wR.png',
            'N': 'wN.png',
            'B': 'wB.png',
            'Q': 'wQ.png',
            'K': 'wK.png',
            'P': 'wP.png'
        }
        for piece, filename in pieces.items():
            img_path = os.path.join(os.path.dirname(__file__), 'images', filename)
            img = Image.open(img_path).convert("RGBA").resize((64, 64), Image.Resampling.LANCZOS)
            self.images[piece] = ImageTk.PhotoImage(img)

    def draw_board(self):
        colors = ["#ebebd3", "#7a945a"]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(col * 64, row * 64, (col + 1) * 64, (row + 1) * 64, fill=color, outline=color)

    def update_board(self, fen):
        self.canvas.delete("piece")
        board = chess.Board(fen)
        for row in range(8):
            for col in range(8):
                piece = board.piece_at(chess.square(col, row))
                if piece:
                    self.canvas.create_image(col * 64, (7 - row) * 64, image=self.images[piece.symbol()], anchor=tk.NW, tags="piece")
        self.master.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    board = ChessBoard(root)
    root.mainloop()
