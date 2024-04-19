import os

class Solitaire:
    class Card:
        def __init__(self, rank, suit, visible=False):
            self.rank = rank
            self.suit = suit
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
        #check validity of move based on tableau
        source = 1
        target = 1

        if source != target and (source <= 11 and source >= 8 and target <= 11 and target >= 8):
            print("Not valid")
            return False
        if source == target:
            print("Error: You selected the same location")
            return False
        
        if source < 0 or source > 11 or target < 0 or target > 11:
            print("Error: Not valid location to move")
            return False
        
        return
    
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
            suit = self.mapping[suit]
            visible = False  # All cards are initially visible
            card_obj = self.Card(rank, suit, visible)

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

        
    def displayBoard(self):
        print("Hacker's Tableau:")
        for pile in self.tableau:
            print([card.visible_str() for card in pile])

# Example usage
solitaire = Solitaire()
solitaire.play()
solitaire.move(7,8)
solitaire.play()
