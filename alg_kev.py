import solitaire

def simulate_game(board, steps=[], dead_ends=0, moves_made=0, consecutive_draws=0):
    global prev_t_to_t_move  # Declare prev_t_to_t_move as a global variable
    print("Top card of waste:", board.piles[0][1] if board.piles[0] else "Empty")
    moveMade = False

    # RULE 1: tableau to pile.
    if not moveMade:
        for i in range(8):
            for j in range(8, 12):
                print(i, j)
                if board.check_validity(i, j):
                    board.move(i, j)
                    print(i, j)
                    moveMade = True
                    return

    # RULE 2: Move between tableaus.
    if not moveMade:
        for i in range(8):
            for j in range(8):
                # Check if the move is valid and not the same as the previous tableau-to-tableau move
                if board.check_validity(i, j) and prev_t_to_t_move != (i, j) and prev_t_to_t_move != (j, i):
                    board.move(i, j)
                    print(i, j)
                    prev_t_to_t_move = (i, j)  # Update prev_t_to_t_move with the current move
                    print(prev_t_to_t_move)
                    moveMade = True
                    return

    # RULE 3: Move from waste to tableaus.
    if not moveMade and board.piles[0]:
        for i in range(8):
            if board.check_validity(12, i):
                board.move(12, i)
                print('RULE #3')
                print(12, i)
                moveMade = True
                return

    # RULE 4: Hit hand if no move has been made.
    if not moveMade:
        board.hitHand()
        print("Hand hit")

    return

def main():
    global prev_t_to_t_move
    prev_t_to_t_move = (-1, -1)
    board = solitaire.Solitaire()

    board.displayBoard()

    for _ in range(20):
        simulate_game(board)
        board.displayBoard()

if __name__ == "__main__":
    main()
