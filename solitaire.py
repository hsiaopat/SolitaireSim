import os
import random

class Solitaire:
    class Card:
        def __init__(self, rank, suit, color, visible=False):
            self.rank = rank
            self.suit = suit
            self.color = color
            self.visible = visible

        def __str__(self):
            #if self.visible:
            return f"{self.rank} of {self.suit}"
            #else:
            #    return "Hidden Card"

        def visible_str(self):
            return f"{self.rank} of {self.suit}"

        def flip(self):
            self.visible = not self.visible

    def __init__(self, most_recent=False, random_game=False, draw_num=3):
        self.draw_num = draw_num

        # Get a list of files in the current directory
        files_in_directory = os.listdir("gameFiles")

        # Use this option to play the most recent file
        if most_recent:
            for file_name in files_in_directory:
                if len(file_name) == 104 and all(char.isdigit() for char in file_name[:-4]):
                    self.card_codes = self.generate_card_codes(file_name)
                    print(f"File Name: {file_name}")
                    break
            else:
                raise FileNotFoundError("No suitable file found in the current directory.")

        # Gives you choice of files in the directory
        elif not random_game:
            possible_files = []
            # Look for a file with the desired format (containing numbers from 01 to 51)
            for file_name in files_in_directory:
                if len(file_name) == 104 and all(char.isdigit() for char in file_name[:-4]):
                    possible_files.append(file_name)

            if len(possible_files) > 0:
                print(f"Possible files: {possible_files}")
                file_num = int(input("Enter which number game you would like out of these (0 indexed): "))
                self.card_codes = self.generate_card_codes(possible_files[file_num])
                print(f"File Name: {possible_files[file_num]}")
            else:
                raise FileNotFoundError("No suitable file found in the current directory.")


            # Unshuffled (easily solvable) example
            #self.card_codes = self.generate_card_codes("00010203040506070809101112131415161718192021222324252627282930313233343536373839404142434445464748495051")

            # Solvable game example
            #self.card_codes = self.generate_card_codes("31501835474539091638200206085123244837321327142911280146440025172243124249363041051019070334261540332104")

            # Quick dead end example
            #self.card_codes = self.generate_card_codes("20480530061643441801243336142207452710460911023100353223045140493442150312211917472637381339290825415028")

        # Games are randomized
        else:
            order = [i for i in range(52)]
            random.shuffle(order)
            game_name = "".join([f"{card:02d}" for card in order])
            print(f"Game name: {game_name}")
            self.card_codes = self.generate_card_codes(game_name)



        self.mapping = {
            0:"C", 1: "D", 2: "H", 3: "S"
        }

        self.suit_to_number = {
            "C": 0, "D": 1, "H": 2, "S": 3
        }


        self.tableau = [[] for _ in range(7)]
        self.setup_tableau()
        self.pointer = len(self.hand)



    def generate_card_codes(self, file_name):
        card_codes = []
        i = len(file_name) - 1
        while i > 0:
            # Check if the current two characters form a valid two-digit number
            if file_name[i-1:i+1].isdigit():
                card_codes.append(file_name[i-1:i+1])
                i -= 2  # Move two characters back for the next two-digit number
            else:
                i -= 1  # Move one character back if it's not a valid two-digit number
        return card_codes

    def check_validity(self, source, target, verbose=False):
        # Check if the move is valid based on the tableau
        #print("visible Card pointers")
        #print(self.visibleCardPointers)

        if source == target:
            if verbose: print("Error: You selected the same location")
            return False

        if source < 0 or source > 11 or target < 0 or target > 11:
            if verbose: print("Error: Not valid location to move")
            return False

        if target <= 8 and target > 0:
            if len(self.tableau[source - 1]) == 0:
                if verbose: print("Error: No cards in pile")
                return False

        # If the target is one of the piles
        if target >= 8 and target <= 11:
            target_suit = self.mapping[target - 8]  # Get the suit of the target pile
            if source <= 7:  # If moving from tableau or hand to pile
                if source != 0: # Moving from tableau
                    if self.tableau[source - 1]:  # Check if tableau source pile is not empty
                        card_suit = self.tableau[source - 1][-1].suit  # Get the suit of the card being moved
                        card_rank = self.tableau[source - 1][-1].rank
                    else:
                        if verbose: print("Error: Source tableau pile is empty")
                        return False
                else: # Moving from hand
                    if (self.pointer >= len(self.hand)):
                        if verbose: print("Error: Need to draw cards")
                        return False
                    elif self.hand and self.pointer >= 0:
                        card_suit = self.hand[self.pointer].suit
                        card_rank = self.hand[self.pointer].rank
                    else:
                        if verbose: print("Error: Source pile is empty")
                        return False

                if card_suit != target_suit:  # Check if suits match
                    if verbose: print("Error: Card suit does not match pile suit")
                    return False
                if self.piles[target]:
                    prev_rank = self.piles[target][-1].rank
                else:
                    prev_rank = 0

                if card_rank == prev_rank + 1:
                    return True
                else:
                    if verbose: print("Error: Card is not next in pile")
                    return False
            else:  # If moving from one pile to another pile
                return True  # Pile to pile move is always valid
        else:  # If moving to the tableau
            if source > 0:  # If moving from tableau to tableau
                if self.tableau[source - 1]:  # Check if source tableau pile is not empty
                    try:
                        source_card = self.tableau[source - 1][self.visibleCardPointers[source - 1]]  # Get the card being moved
                    except:
                        self.displayBoard()
                        print(source, self.visibleCardPointers)
                    if self.tableau[target - 1]:  # Check if target tableau pile is not empty
                        target_card = self.tableau[target - 1][-1]  # Get the top card of the target pile
                        if source_card.color != target_card.color:  # Check if colors alternate
                            if source_card.rank == target_card.rank - 1:  # Check if ranks are consecutive
                                return True
                            else:
                                if verbose: print("Error: Card rank is not one less than target card rank")
                                return False
                        else:
                            if verbose: print("Error: Card color does not alternate")
                            return False
                    else:  # If target tableau pile is empty, check if source card is one less than the last card in the pile
                        if source_card.rank == 13:  # King can be placed on an empty pile
                            if self.visibleCardPointers[source - 1] != 0:
                                return True
                            else: # Pointless move of king
                                if verbose: print("Error: Moving king from open spot to open spot does nothing")
                                return False
                        else:
                            if verbose: print("Error: Only king can be placed on an empty tableau pile")
                            return False
                else:
                    if verbose: print("Error: Source tableau pile is empty")
                    return False
            else:  # If moving from hand to tableau
                if (self.pointer >= len(self.hand)):
                    if verbose: print("Error: Need to draw cards")
                    return False
                elif self.hand and self.pointer >= 0:  # Check if source pile is not empty
                    source_card = self.hand[self.pointer]  # Get the card being moved
                    if self.tableau[target - 1]:  # Check if target tableau pile is not empty
                        target_card = self.tableau[target - 1][-1]  # Get the top card of the target pile
                        if source_card.color != target_card.color:  # Check if colors alternate
                            if source_card.rank == target_card.rank - 1:  # Check if ranks are consecutive
                                return True
                            else:
                                if verbose: print("Error: Card rank is not one less than target card rank")
                                return False
                        else:
                            if verbose: print("Error: Card color does not alternate")
                            return False
                    else:
                        if source_card.rank == 13:
                            return True
                        elif verbose:
                            print("Error: Only king can be placed on an empty tableau pile")
                            return False
                else:
                    if verbose: print("Error: Source pile is empty")
                    return False

    def move(self, source, target):
        # 0 = hand
        # 1 = col 1
        # 2 = col 2
        # 3 = col 3
        # 4 = col 4
        # 5 = col 5
        # 6 = col 6
        # 7 = col 7
        # 8 = clubs pile
        # 9 = diamonds pile
        # 10 = hearts pile
        # 11 = spades pile
        #check for error

        #check if source is in tableau then move pointer

        if not self.check_validity(source, target, verbose=False):
            #print(f"Move from {source} to {target} is not possible")
            return

        # Move card to desired location
        if source == 0:  # If the source is the hand
            card = self.hand.pop(self.pointer)
            if target >= 1 and target <= 7:
                self.tableau[target - 1].append(card)
                # Flip the card behind it if any
                if self.pointer > 0:
                    self.hand[self.pointer - 1].flip()

                if self.visibleCardPointers[target - 1] < 0:
                    self.visibleCardPointers[target - 1] = 0
            # If it was in the hand, move the pointer
            #self.pointer -= 1
            else:
                self.piles[target].append(card)

            # Update the hand if necessary
            if self.pointer < 0:
                self.pointer = 0

        # Else, flip card behind it over
        elif source <= 11 and source >= 8: #source is in the piles
            cards = self.piles[source][self.visibleCardPointers:]
            self.tableau[target-1].extend(cards)
            self.visibleCardPointers[target - 1] -= 1
        elif target <= 11 and target >= 8: #tableau to pile
            card = self.tableau[source-1].pop()
            self.piles[target].append(card)
            if self.visibleCardPointers[source - 1] >= len(self.tableau[source - 1]):
                self.visibleCardPointers[source - 1] -= 1
        else: #tableau to tableau
            cards = self.tableau[source - 1][self.visibleCardPointers[source - 1]:]
            self.tableau[source - 1] = self.tableau[source - 1][:self.visibleCardPointers[source - 1]]
            self.tableau[target - 1].extend(cards)
            self.visibleCardPointers[source - 1] -= 1
            if (self.visibleCardPointers[target - 1] < 0):
                self.visibleCardPointers[target - 1] = 0



    def hitHand(self):
        if self.pointer == 0:
            self.pointer = len(self.hand) - self.draw_num
        elif self.pointer <= self.draw_num:
            self.pointer = 0
        else:
            self.pointer -= self.draw_num

        if self.pointer < 0:
            self.pointer = 0


    def setup_tableau(self):
        hand = []
        pileH = []
        pileD = []
        pileS = []
        pileC = []
        piles = {}
        index = 0
        count = 1
        visibleCardPointers = [i for i in range(7)]

        #set up pointers for tableaus
        for code in self.card_codes:
            rank = int(code) // 4 + 1
            suit = int(code) % 4
            if suit ==  0 or suit == 3:
                color = "black"
            else:
                color = "red"
            suit = self.mapping[suit]
            visible = False  # All cards are initially visible
            card_obj = self.Card(rank, suit, color, visible)

            # Add cards to tableau rows with increasing counts
            if index <= 6 and count <= 7:
                self.tableau[index].append(card_obj)
                index += 1

                if index == 7:
                    index = count
                    count += 1

            else:
                hand.append(card_obj)


            #Solitaire.displayBoard(self)

        for i in range(len(self.tableau)):
            self.tableau[i][-1].visible = True

        hand[-1].visible = True

        self.hand = hand
        self.piles = piles
        self.piles[8] = pileC
        self.piles[9] = pileD
        self.piles[10] = pileH
        self.piles[11] = pileS
        self.visibleCardPointers = visibleCardPointers

    def play(self):
        print("Welcome to Solitaire!")
        print()
        print("Directions: To move a card from two locations, ")

        print("Tableau:")
        for pile in self.tableau:
            print([str(card) for card in pile])


        print("\nPile:")
        print([str(card) for card in self.hand])

        print("\nPile of Clubs:")
        print([str(card) for card in self.piles[8]])

        print("\nPile of Diamonds:")
        print([str(card) for card in self.piles[9]])

        print("\nPile of Hearts:")
        print([str(card) for card in self.piles[10]])

        print("\nPile of Spades:")
        print([str(card) for card in self.piles[11]])

        print()


    def displayBoard(self):
        print("Hacker's Tableau:")
        for pile in self.tableau:
            print([card.visible_str() for card in pile])
        print(f"Visible Card Pointers: {self.visibleCardPointers}")

        print("\nHacker's Pile:")
        print([card.visible_str() for card in self.hand])
        print(f"Current available card: #{self.pointer}, or {len(self.hand) - self.pointer} from right")

        print("\nHacker's Pile of Clubs: ", end="")
        print([card.visible_str() for card in self.piles[8]], end="")

        print("\nHacker's Pile of Diamonds: ", end="")
        print([card.visible_str() for card in self.piles[9]], end="")

        print("\nHacker's Pile of Hearts: ", end="")
        print([card.visible_str() for card in self.piles[10]], end="")

        print("\nHacker's Pile of Spades: ", end="")
        print([card.visible_str() for card in self.piles[11]], end="\n\n")
        #print("------------------------------------------------------\n")


    def board_to_string(self):
        board_string = ""

        for card in self.hand:
            board_string += f"{(card.rank - 1) * 4 + self.suit_to_number[card.suit]:02d}"

        for pile in self.tableau:
            board_string += "|"
            for card in pile:
                board_string += f"{(card.rank - 1) * 4 + self.suit_to_number[card.suit]:02d}"

        board_string += f"|{self.pointer}"

        return board_string


    def playGame(self):
        # self.move(1, 9)
        # self.move(2, 1)
        # self.move(3, 1)
        # self.move(7, 8)
        # self.move(4, 8)
        # self.move(5, 8)
        # self.move(0, 3)
        # self.hitHand()
        # self.move(0, 10)
        # self.hitHand()
        # self.hitHand()
        # self.move(0, 9)
        # self.hitHand()
        # self.hitHand()
        # self.hitHand()
        # self.hitHand()
        self.displayBoard()
        game_over = False

        while not game_over:
            source, target = [int(i) for i in (input("Enter a source and target pile, '0 0' to draw from the deck, or '-1 -1' to quit: ")).split()]
            if target == 0:
                self.hitHand()
            elif target == -1:
                break
            else:
                self.move(source, target)

            self.displayBoard()

# Example usage
if __name__ == "__main__":
    solitaire = Solitaire(random_game=True, draw_num=1)
    print(solitaire.board_to_string())
    #solitaire.displayBoard()

    solitaire.playGame()

    '''
    print("7,8")
    solitaire.move(7, 8)
    #solitaire.displayBoard()

    print("3,2")
    solitaire.move(3, 2)
    #solitaire.displayBoard()

    print("1,9")
    solitaire.move(1, 9)
    #solitaire.displayBoard()

    print("2,1")
    solitaire.move(2, 1)
    #solitaire.displayBoard()

    solitaire.move(4, 8)
    solitaire.displayBoard()
    '''
