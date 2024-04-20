import os

class Solitaire:
    class Card:
        def __init__(self, rank, suit, color, visible=False):
            self.rank = rank
            self.suit = suit
            self.color = color
            self.visible = visible

        def __str__(self):
            if self.visible:
                return f"{self.rank} of {self.suit}"
            else:
                return "Hidden Card"
        def visible_str(self):
                return f"{self.rank} of {self.suit}"
        
        def flip(self):
            self.visible = not self.visible

    def __init__(self):
         # Get a list of files in the current directory
        files_in_directory = os.listdir()

        # Look for a file with the desired format (containing numbers from 01 to 51)
        for file_name in files_in_directory:
            if len(file_name) == 104 and all(char.isdigit() for char in file_name[:-4]):
                self.card_codes = self.generate_card_codes(file_name)
                print("File Name: ")
                print(file_name)
                break  
        else:
            raise FileNotFoundError("No suitable file found in the current directory.")


        self.card_codes = self.generate_card_codes(file_name)
        self.mapping = {
            0:"C", 1: "D", 2: "H", 3: "S" 
        }


        self.tableau = [[] for _ in range(7)]
        self.setup_tableau()
        self.pointer = len(self.hand)-1
    
        

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
    
    def check_validity(self, source, target):
        # Check if the move is valid based on the tableau
        if source == target:
            print("Error: You selected the same location")
            return False
        
        if source < 0 or source > 11 or target < 0 or target > 11:
            print("Error: Not valid location to move")
            return False
        
        # If the target is one of the piles
        if target >= 8 and target <= 11:
            target_suit = self.mapping[target - 8]  # Get the suit of the target pile
            if source <= 7:  # If moving from tableau to pile
                if self.tableau[source - 1]:  # Check if tableau source pile is not empty
                    card_suit = self.tableau[source - 1][-1].suit  # Get the suit of the card being moved
                    if card_suit == target_suit:  # Check if suits match
                        return True
                    else:
                        print("Error: Card suit does not match pile suit")
                        return False
                else:
                    print("Error: Source tableau pile is empty")
                    return False
            else:  # If moving from one pile to another pile
                return True  # Pile to pile move is always valid
        else:  # If moving to the tableau
            if source <= 7:  # If moving from tableau to tableau
                if self.tableau[source - 1]:  # Check if source tableau pile is not empty
                    source_card = self.tableau[source - 1][-1]  # Get the card being moved
                    if self.tableau[target - 1]:  # Check if target tableau pile is not empty
                        target_card = self.tableau[target - 1][-1]  # Get the top card of the target pile
                        if source_card.color != target_card.color:  # Check if colors alternate
                            if source_card.rank == target_card.rank - 1:  # Check if ranks are consecutive
                                return True
                            else:
                                print("Error: Card rank is not one less than target card rank")
                                return False
                        else:
                            print("Error: Card color does not alternate")
                            return False
                    else:  # If target tableau pile is empty, check if source card is one less than the last card in the pile
                        if source_card.rank == 13:  # King can be placed on an empty pile
                            return True
                        else:
                            print("Error: Only king can be placed on an empty tableau pile")
                            return False
                else:
                    print("Error: Source tableau pile is empty")
                    return False
            else:  # If moving from pile to tableau
                if self.tableau[target - 1]:  # Check if target tableau pile is not empty
                    target_card = self.tableau[target - 1][-1]  # Get the top card of the target pile
                    if self.piles[source]:  # Check if source pile is not empty
                        source_card = self.piles[source][-1]  # Get the card being moved
                        if source_card.rank == target_card.rank - 1:  # Check if ranks are consecutive
                            return True
                        else:
                            print("Error: Card rank is not one less than target card rank")
                            return False
                    else:
                        print("Error: Source pile is empty")
                        return False
                else:
                    print("Error: Target tableau pile is empty")
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
        

        # Move card to desired location
        if source == 0:  # If the source is the hand
            card = self.hand.pop(self.pointer)
            if target >= 1 and target <= 7:
                self.tableau[target - 1].append(card)
                # Flip the card behind it if any
                if self.pointer > 0:
                    self.hand[self.pointer - 1].flip()
            # If it was in the hand, move the pointer
            self.pointer -= 1
            
            # Update the hand if necessary
            if self.pointer < 0:
                self.pointer = 0

        # Else, flip card behind it over
        elif source <= 11 and source >= 8:
            card = self.piles[source].pop()
            self.tableau[target-1].append(card)
        elif target <= 11 and target >= 8:
            card = self.tableau[source-1].pop()
            self.piles[target].append(card)
        else:
            card = self.tableau[source-1].pop()
            self.tableau[target-1].append(card)

    
    def hitHand(self):
        self.pointer -= 3
        if self.pointer == 0:
            self.pointer = len(self.hand) - 3
        elif self.pointer < 0:
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
            if index <= 6 and count <= 6:
                self.tableau[index].append(card_obj)
                index += 1

                if index == 7:
                    index = count
                    count += 1

            else:
                hand.append(card_obj)
        
        for i in range(len(self.tableau)):
            self.tableau[i][-1].visible = True
            
        hand[-1].visible = True

        self.hand = hand
        self.piles = piles
        self.piles[8] = pileC 
        self.piles[9] = pileD 
        self.piles[10] = pileH
        self.piles[11] = pileS 

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

        print("\nHacker's Pile:")
        print([card.visible_str() for card in self.hand])

        print("\nHacker's Pile of Clubs:")
        print([card.visible_str() for card in self.piles[8]])

        print("\nHacker's Pile of Diamonds:")
        print([card.visible_str() for card in self.piles[9]])

        print("\nHacker's Pile of Hearts:")
        print([card.visible_str() for card in self.piles[10]])

        print("\nHacker's Pile of Spades:")
        print([card.visible_str() for card in self.piles[11]])

# Example usage
solitaire = Solitaire()
solitaire.displayBoard()
if solitaire.check_validity(7,8):
    solitaire.move(7,8)
    solitaire.displayBoard()
if solitaire.check_validity(3,8):
    solitaire.move(3,8)
    solitaire.displayBoard()

