# De La Paz, Jhoanna Alexandra C. De La Paz - J3A
# Tic Tac Toe game - Midterm Activity 2

import time  # used for timing

# STEP 1: Create a 3×3 board
def print_board(board):
    """Display board in a 3x3 grid."""

    # code for text colors
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

    print("\n")
    for i in range(0, 9, 3):
        a, b, c = board[i], board[i+1], board[i+2]
        # Color X as red and O as blue
        a = f"{RED}{a}{RESET}" if a == 'X' else (f"{BLUE}{a}{RESET}" if a == 'O' else a)
        b = f"{RED}{b}{RESET}" if b == 'X' else (f"{BLUE}{b}{RESET}" if b == 'O' else b)
        c = f"{RED}{c}{RESET}" if c == 'X' else (f"{BLUE}{c}{RESET}" if c == 'O' else c)

        print(f" {a} | {b} | {c} ")
        if i < 6:
            print("---+---+---")
    print("\n")

# STEP 2: Create the game rules & helpers
# --- GAME RULES ---

# All winning triplets (rows, columns, diagonals)
LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

def winner(board):
    """Return 'X' or 'O' if someone has three in a row, else None."""
    for a, b, c in LINES:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def moves(board):
    """List of indices that are empty."""
    return [i for i, v in enumerate(board) if v == ' ']

def terminal(board):
    """True if the game is over (win or draw)."""
    return winner(board) is not None or not moves(board)


# STEP 3: Create the utility function
def utility(board, me='O', opp='X'):
    """Score terminal states from AI perspective: +1 win, -1 loss, 0 draw."""
    w = winner(board)
    if w == me:
        return 1
    elif w == opp:
        return -1
    else:
        return 0  # draw or non-terminal (we only call this at terminal)


# STEP 4: Implement the minimax (recursive)
node_count = 0  # counts visited nodes

def minimax(board, player, me='O', opp='X'):
    """Return (best_value, best_move) assuming optimal play by both sides."""
    global node_count
    node_count += 1  # count every call
    if terminal(board):
        return utility(board, me, opp), None

    best_val = -2 if player == me else 2
    best_move = None

    for m in moves(board):
        b2 = board[:]
        b2[m] = player
        next_player = opp if player == me else me
        val, _ = minimax(b2, next_player, me, opp)

        if player == me and val > best_val:
            best_val, best_move = val, m
        elif player == opp and val < best_val:
            best_val, best_move = val, m

    return best_val, best_move


# STEP 5: Create the game loop and conditions
def play_game():
    board = [' '] * 9
    human = 'X'
    ai = 'O'

    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

    print("======================================")
    print("        Welcome to Tic-Tac-Toe!       ")
    print("--------------------------------------")
    print(f"    You are {RED}'X'{RESET} and the AI is {BLUE}'O'{RESET}")
    print("======================================\n")

    print_board(board)

    while True:
        first = input("Do you want to go first? (y/n): ").strip().lower()
        if first in ['y', 'n']:
            break
        else:
            print("Please enter 'y' for yes or 'n' for no.")

    current = human if first == 'y' else ai

    while not terminal(board):
        if current == human:
            try:
                pos = int(input("Enter your move (1-9): ")) - 1
            except ValueError:
                print("Please enter a number 1-9.")
                continue
            if pos not in moves(board):
                print("Invalid move. Try again.")
                continue
            board[pos] = human
        else:
            print("AI is thinking...")

            # timing and node count
            global node_count
            node_count = 0
            start_time = time.time()

            _, m = alphabeta(board, player=ai, alpha=-2, beta=2, me=ai, opp=human)

            end_time = time.time()
            elapsed = end_time - start_time

            print(f"AI chose position {m+1}")
            print(f"Nodes explored: {node_count}")
            print(f"Time taken: {elapsed:.4f} seconds\n")
            # end timing and node counting

            board[m] = ai

        print_board(board)
        current = ai if current == human else human

    w = winner(board)
    print("======================================")
    if w == human:
        print(f"{RED}🎉 You win!{RESET}")
    elif w == ai:
        print(f"{BLUE}🤖 AI wins!{RESET}")
    else:
        print("😐 It's a draw!")
    print("======================================")

    # replay option
    while True:
        print("")
        replay = input("Do you want to play again? (y/n): ").strip().lower()
        if replay in ['y', 'n']:
            break
        else:
            print("Please enter 'y' for yes or 'n' for no.")
    if replay == 'y':
        print("")
        play_game()
    else:
        print("Thanks for playing!")


# STEP 6:  Alpha-Beta Pruning
def alphabeta(board, player, alpha=-2, beta=2, me='O', opp='X'):
    global node_count
    node_count += 1  # count nodes here too
    if terminal(board):
        return utility(board, me, opp), None

    if player == me:
        best = (-2, None)  # MAX
        for m in moves(board):
            b2 = board[:]
            b2[m] = player
            val, _ = alphabeta(b2, opp, alpha, beta, me, opp)
            if val > best[0]:
                best = (val, m)
            alpha = max(alpha, val)
            if alpha >= beta:  # prune
                break
        return best
    else:
        best = (2, None)  # MIN
        for m in moves(board):
            b2 = board[:]
            b2[m] = player
            val, _ = alphabeta(b2, me, alpha, beta, me, opp)
            if val < best[0]:
                best = (val, m)
            beta = min(beta, val)
            if alpha >= beta:  # prune
                break
        return best

if __name__ == "__main__":
    play_game()
