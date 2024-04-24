import solitaire

dead_ends = 0
total_moves_tried = 0

def simulate_game(board, steps=[], moves_made=0, consecutive_draws=0):
    global dead_ends
    global total_moves_tried

    new_board = board

    if (total_moves_tried % 100 == 0):
        print(f"{moves_made} moves have been made")

    #if (total_moves_tried > 100):
         #board.displayBoard()
         #return

    # Move card to finished if it can be
    for i in range(8):
        if i == 0 and board.pointer < len(board.hand):
            suit = board.hand[board.pointer].suit
            rank = board.hand[board.pointer].rank
        elif board.tableau[i - 1]:
            suit = board.tableau[i - 1][-1].suit
            rank = board.tableau[i - 1][-1].rank
        else:
            continue

        suit_pile = board.suit_to_number[suit]

        #if (board.piles[suit_pile + 8] and (rank - 1) == board.piles[suit_pile + 8][-1]) or rank == 1:
        if (board.check_validity(i, suit_pile + 8)):
            new_board.move(i, suit_pile + 8)
            new_steps = steps + [f"Place {rank} of {suit} from pile {i} to finished"]
            print(f"Place {rank} of {suit} from pile {i} to finished")
            if len(board.hand) + sum([len(board.tableau[i]) for i in range(7)]) == 0:
               print(f"The game has been won on {moves_made} moves. Here are the steps: {steps}")
               return True
            consecutive_draws = 0
            total_moves_tried += 1
            if simulate_game(new_board, new_steps, moves_made + 1, consecutive_draws):
                return True

    # Move card from one tableau to another
    for source in range(1, 8):
        for target in range(1, 8):
            if board.check_validity(source, target):
                new_steps = steps + [f"Move top card {board.tableau[source - 1][board.visibleCardPointers[source - 1]]} and lower from stack {source} to {target}"]
                print(f"Move top card {board.tableau[source - 1][board.visibleCardPointers[source - 1]]} and lower from stack {source} to {target}")
                new_board.move(source, target)
                consecutive_draws = 0
                total_moves_tried += 1
                if simulate_game(new_board, new_steps, moves_made + 1, consecutive_draws):
                    return True



    # Move draw card to tableau if possible
    for target in range(1, 8):
        if board.check_validity(0, target):
            new_steps = steps + [f"Place draw card {board.hand[board.pointer]} on tableau pile {target}"]
            print(f"Place draw card {board.hand[board.pointer]} on tableau pile {target}")
            new_board.move(0, target)
            consecutive_draws = 0
            total_moves_tried += 1
            if simulate_game(new_board, new_steps, moves_made + 1, consecutive_draws):
                return True

    # Draw from pile as long as we haven't done it too many times in a row
    if consecutive_draws < len(board.hand) / 3:
        new_steps = steps + ["Draw from pile"]
        print("Draw from pile")
        new_board.hitHand()
        consecutive_draws = consecutive_draws + 1
        total_moves_tried += 1
        if simulate_game(new_board, new_steps, moves_made + 1, consecutive_draws):
            return True

    # A dead end has been reached
    else:
        dead_ends = dead_ends + 1
        print(f"Dead end {dead_ends} hit at {moves_made} moves")


def main():

    board = solitaire.Solitaire()

    board.displayBoard()

    if not simulate_game(board):
        print(f"{total_moves_tried} moves were tried, and no solution was found")

    board.displayBoard()

if __name__ == "__main__":
    main()
