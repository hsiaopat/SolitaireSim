import solitaire


def simulate_game(board, steps=[], dead_ends=0, moves_made=0, consecutive_draws=0):

    '''
    if (moves_made % 100 == 0):
        print(f"{moves_made} moves have been made")


    if card can be finished:
       finish card on new_board
       new_steps = steps + [f"Place {card} from {stack} in finished"]
       if game has been won:
           print(f"The game has been won on {moves_made} moves. Here are the steps: {steps}")
           return
       flip over new card if needed
       consecutive_draws = 0
       make_moves(new_board, new_steps, dead_ends, moves_made + 1, consecutive_draws)

    if card can be moved from one stack to another:
        move stack on new_board
        new_steps = steps + [f"Move {card} from stack {stack1} to {stack2}"]
        flip over new card
        consecutive_draws = 0
        make_moves(new_board, new_steps, dead_ends, moves_made + 1, consecutive_draws)

    if draw card can be placed on tableau:
        place card on new_board
        new_steps = steps + [f"Place {card} on stack {stack}"]
        consecutive_draws = 0
        make_moves(new_board, new_steps, dead_ends, moves_made + 1, consecutive_draws)

    if consecutive_draws < size(draw_pile) / 3:
        new_steps = steps + ["Draw from pile"]
        consecutive_draws = consecutive_draws + 1
        make_moves(new_board, steps + ["draw pile"], dead_ends, moves_made + 1, consecutive_draws)

    else:
        dead_end = dead_end + 1
        print(f"Dead end {dead_end} hit at {moves_made} moves)

    '''

def main():
    simulate_game(board)

if __name__ == "__main__":
    main()
