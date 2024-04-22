import solitaire


def simulate_game(board, steps=[], dead_ends=0, moves_made=0, consecutive_draws=0):

    new_board = board

    if (moves_made % 100 == 0):
        print(f"{moves_made} moves have been made")

    # Move card to finished if it can be
    for i in range(8):
        if i == 0:
            suit = board.hand[board.pointer].suit
            rank = board.hand[board.pointer].rank
        elif board.tableau[i - 1]:
            suit = board.tableau[i - 1][-1].suit
            rank = board.tableau[i - 1][-1].rank

        suit_pile = board.suit_to_number[suit]

        if (board.piles[suit_pile + 8] and (rank - 1) == board.piles[suit_pile + 8][-1]) or rank == 1:
            new_board.move(i, suit_pile + 8)
            new_steps = steps + [f"Place {rank} of {suit} from pile {i} to finished"]
            print(f"Place {rank} of {suit} from pile {i} to finished")
            if len(board.hand) + sum([len(board.tableau[i]) for i in range(7)]) == 0:
               print(f"The game has been won on {moves_made} moves. Here are the steps: {steps}")
               return
            consecutive_draws = 0
            simulate_game(new_board, new_steps, dead_ends, moves_made + 1, consecutive_draws)

    '''
    if card can be moved from one stack to another:
        move stack on new_board
        new_steps = steps + [f"Move {card} from stack {stack1} to {stack2}"]
        flip over new card
        consecutive_draws = 0
        simulate_game(new_board, new_steps, dead_ends, moves_made + 1, consecutive_draws)

    '''

    # Move draw card to tableau if possible
    print(board.hand[board.pointer])
    suit = board.hand[board.pointer].suit
    rank = board.hand[board.pointer].rank
    for i in range(1, 8):
        if board.check_validity(0, i):
            new_board.move(0, i)
            new_steps = steps + [f"Place draw card {card} on tableau pile {stack}"]
            print(f"Place draw card {card} on tableau pile {stack}")
            consecutive_draws = 0
            simulate_game(new_board, new_steps, dead_ends, moves_made + 1, consecutive_draws)

    # Draw from pile as long as we haven't done it too many times in a row
    if consecutive_draws < len(board.hand) / 3:
        new_steps = steps + ["Draw from pile"]
        print("Draw from pile")
        new_board.hitHand()
        consecutive_draws = consecutive_draws + 1
        simulate_game(new_board, new_steps, dead_ends, moves_made + 1, consecutive_draws)

    # A dead end has been reached
    else:
        dead_ends = dead_ends + 1
        print(f"Dead end {dead_ends} hit at {moves_made} moves")


def main():
    board = solitaire.Solitaire()

    board.displayBoard()

    simulate_game(board)

    board.displayBoard()

if __name__ == "__main__":
    main()
