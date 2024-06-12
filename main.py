import chess
import chess.engine
import threading
from chessboard import ChessBoard

engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")

board = chess.Board()


def best_move(board):
    result = engine.play(board, chess.engine.Limit(time=2.0))
    return result.move


def best_moves(board, num_moves=3):
    result = engine.analyse(board, chess.engine.Limit(time=2.0), multipv=num_moves)
    return [(info['pv'][0], info['score'].relative) for info in result]


def evaluate_position(board):
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    return info["score"].relative.score(mate_score=10000) / 100.0


def start_game(update_label_callback, update_eval_bar_callback, difficulty, chessboard, update_best_moves_callback):
    engine.configure({"Skill Level": difficulty})

    def game_loop():
        game_over = False
        while not game_over:
            print()
            print()
            print(board)
            print()
            print()
            moves = best_moves(board)
            best_moves_san = [board.san(move) for move, score in moves]  # Converti le migliori mosse in SAN
            update_best_moves_callback(best_moves_san)  # Passa le migliori mosse alla funzione di callback
            for i, (move, score) in enumerate(moves):
                print(f"Top {i + 1} move: {board.san(move)} with score {score}")
            print()
            user_move = input("Enter your move: ")
            game_over = make_move(user_move, update_label_callback, update_eval_bar_callback, chessboard,
                                  update_best_moves_callback)

        engine.quit()

    game_thread = threading.Thread(target=game_loop)
    game_thread.start()


def make_move(move, update_label_callback, update_eval_bar_callback, chessboard, update_best_moves_callback=None):
    try:
        board.push_san(move)
        print(f"Player move: {move}")
        update_label_callback(f"Player move: {move}")
        chessboard.update_board(board.fen())
        eval_score = evaluate_position(board)
        print(f"Player evaluation: {eval_score}")
        update_eval_bar_callback(eval_score)
        if board.is_game_over():
            print("Game over")
            update_label_callback("Game over")
            return True
        response = best_move(board)
        board.push(response)
        print(f"Engine move: {response}")
        update_label_callback(f"Engine move: {response}")
        chessboard.update_board(board.fen())
        eval_score = evaluate_position(board)
        print(f"Engine evaluation: {eval_score}")
        update_eval_bar_callback(eval_score)

        # Aggiorna le migliori mosse per il prossimo turno
        if update_best_moves_callback:
            moves = best_moves(board)
            best_moves_san = [board.san(move) for move, score in moves]
            update_best_moves_callback(best_moves_san)

    except ValueError:
        print("Invalid move. Try again.")
        update_label_callback("Invalid move. Try again.")
    return False


if __name__ == "__main__":
    from gui import start_gui

    start_gui(lambda x: print(x), lambda x: print(f"Eval: {x}"), lambda x: print(f"Best moves: {x}"), 1, ChessBoard())
