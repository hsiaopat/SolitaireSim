import solitaire
from copy import deepcopy

dead_ends = 0
total_moves_tried = 0
used_boards = set()
boards_repeated = 0
board_printed = False

def simulate_game(board, steps=[], numbered_steps=[], moves_made=0, consecutive_draws=0, verbose=True, output=""):
    global dead_ends
    global total_moves_tried
    global used_boards
    global board_printed, boards_repeated

    i = 0

    if verbose and total_moves_tried % 10 == 0:
        board.displayBoard()
    #elif total_moves_tried > 160:
    #    return False

    if board_printed:
        return False

    if (dead_ends > 500):
        return False

    # if (len(board.hand) == 0 and not board_printed):
    #     board.displayBoard()
    #     board_printed = True

    if verbose and (total_moves_tried % 100 == 0):
        print(f"{moves_made} moves have been made")

    #if (total_moves_tried > 100):
         #board.displayBoard()
         #return

    # Move card to finished if it can be
    for i in range(8):
        if verbose: print(i, end="")
        if i == 0 and board.pointer < len(board.hand) and board.pointer >= 0:
            suit = board.hand[board.pointer].suit
            rank = board.hand[board.pointer].rank
        elif i > 0 and board.tableau[i - 1]:
            suit = board.tableau[i - 1][-1].suit
            rank = board.tableau[i - 1][-1].rank
        else:
            continue

        suit_pile = board.suit_to_number[suit]

        #if (board.piles[suit_pile + 8] and (rank - 1) == board.piles[suit_pile + 8][-1]) or rank == 1:
        if (board.check_validity(i, suit_pile + 8)):
            new_board = deepcopy(board)
            new_board.move(i, suit_pile + 8)
            board_string = new_board.board_to_string()
            if board_string not in used_boards:
                used_boards.add(board_string)
                new_steps = steps + [f"Place {rank} of {suit} from pile {i} to finished"]
                if i != 0:
                    new_numbered_steps = numbered_steps + [f"{i} {suit_pile + 8} {board.visibleCardPointers[i - 1]}"]
                else:
                     new_numbered_steps = numbered_steps + [f"{i} {suit_pile + 8} {-1}"]
                if verbose: print(f"Place {rank} of {suit} from pile {i} to finished")
                if verbose: print(len(new_board.hand), [len(new_board.tableau[j]) for j in range(7)], total_moves_tried)
                if len(new_board.hand) + sum([len(new_board.tableau[j]) for j in range(7)]) == 0:
                   print(f"The game has been won on {moves_made} moves.\n")
                   if output != "":
                       with open(output, "w") as f:
                           for step in numbered_steps:
                               f.write(f"{step}\n")
                   if verbose: print(f"Here are the steps: {new_steps}")
                   return True
                consecutive_draws = 0
                total_moves_tried += 1
                if simulate_game(new_board, new_steps, new_numbered_steps, moves_made + 1, consecutive_draws, verbose=verbose, output=output):
                    return True
            else:
                boards_repeated += 1

    # Move card from one tableau to another
    for source in range(1, 8):
        for target in range(1, 8):
            if board.check_validity(source, target):
                new_board = deepcopy(board)
                new_board.move(source, target)
                board_string = new_board.board_to_string()
                if board_string not in used_boards:
                    used_boards.add(board_string)
                    new_steps = steps + [f"Move top card {board.tableau[source - 1][board.visibleCardPointers[source - 1]]} and lower from stack {source} to {target}"]
                    new_numbered_steps = numbered_steps + [f"{source} {target} {board.visibleCardPointers[source - 1]}"]
                    if verbose: print(f"Move top card {board.tableau[source - 1][board.visibleCardPointers[source - 1]]} and lower from stack {source} to {target}")
                    consecutive_draws = 0
                    total_moves_tried += 1
                    if simulate_game(new_board, new_steps, new_numbered_steps, moves_made + 1, consecutive_draws, verbose=verbose, output=output):
                        return True
            else:
                boards_repeated += 1



    # Move draw card to tableau if possible
    for target in range(1, 8):
        if board.check_validity(0, target):
            new_board = deepcopy(board)
            new_board.move(0, target)
            board_string = new_board.board_to_string()
            if board_string not in used_boards:
                used_boards.add(board_string)
                new_steps = steps + [f"Place draw card {board.hand[board.pointer]} on tableau pile {target}"]
                new_numbered_steps = numbered_steps + [f"0 {target} -1"]
                if verbose: print(f"Place draw card {board.hand[board.pointer]} on tableau pile {target}")
                consecutive_draws = 0
                total_moves_tried += 1
                if simulate_game(new_board, new_steps, new_numbered_steps, moves_made + 1, consecutive_draws, verbose=verbose, output=output):
                    return True
            else:
                boards_repeated += 1

    # Draw from pile as long as we haven't done it too many times in a row
    if consecutive_draws < len(board.hand) / board.draw_num:
        new_board = deepcopy(board)
        reshuffle = new_board.hitHand()
        board_string = new_board.board_to_string()
        if board_string not in used_boards:
            used_boards.add(board_string)
            new_steps = steps + ["Draw from pile"]
            new_numbered_steps = numbered_steps + [f"-1 -1 -1"]
            if reshuffle:
                new_numbered_steps = new_numbered_steps + [f"-1 -1 -1"]                
            if verbose: print("Draw from pile")
            consecutive_draws = consecutive_draws + 1
            total_moves_tried += 1
            if simulate_game(new_board, new_steps, new_numbered_steps, moves_made + 1, consecutive_draws, verbose=verbose, output=output):
                return True
        else:
            boards_repeated += 1

    # A dead end has been reached
    else:
        dead_ends = dead_ends + 1
        #board.displayBoard()
        if verbose: print(f"Dead end {dead_ends} hit at {moves_made} moves")
        return False

def test_multiple(num_games):
    global dead_ends
    global total_moves_tried
    global used_boards, boards_repeated

    for _ in range(20):
        dead_ends = 0
        total_moves_tried = 0
        boards_repeated = 0
        used_boards = set()
        board = solitaire.Solitaire(random_game=True, draw_num=3)
        #board.displayBoard()
        if not simulate_game(board, verbose=False):
            print(f"{total_moves_tried} moves were tried, and no solution was found\n")

        #print(boards_repeated)
        #board.displayBoard()

    #board.displayBoard()

    #board.displayBoard()

def solve_board(output):
    board = solitaire.Solitaire(most_recent=True, random_game=False, draw_num=1)
    board.displayBoard()
    if not simulate_game(board, verbose=False, output=output):
        with open(output, "w") as f:
            # Write how many moves were tried with the algorithm if it isn't solved
            f.write(f"{total_moves_tried}\n")
            print("Nothing found")
    else:
        print("Done")

def main():
    #test_multiple(20)
    solve_board("output.txt")


if __name__ == "__main__":
    main()
