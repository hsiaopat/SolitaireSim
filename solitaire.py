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
            if file_name.endswith(".txt") and all(char.isdigit() for char in file_name[:-4]):
                self.card_codes = self.generate_card_codes(file_name)
                break
        else:
            raise FileNotFoundError("No suitable file found in the current directory.")


        self.card_codes = self.generate_card_codes(file_name)
        self.mapping = {
            "00": "2H", "01": "3H", "02": "4H", "03": "5H",
            "04": "6H", "05": "7H", "06": "8H", "07": "9H",
            "08": "10H", "09": "JH", "10": "QH", "11": "KH",
            "12": "AH", "13": "2D", "14": "3D", "15": "4D",
            "16": "5D", "17": "6D", "18": "7D", "19": "8D",
            "20": "9D", "21": "10D", "22": "JD", "23": "QD",
            "24": "KD", "25": "AD", "26": "2S", "27": "3S",
            "28": "4S", "29": "5S", "30": "6S", "31": "7S",
            "32": "8S", "33": "9S", "34": "10S", "35": "JS",
            "36": "QS", "37": "KS", "38": "AS", "39": "2C",
            "40": "3C", "41": "4C", "42": "5C", "43": "6C",
            "44": "7C", "45": "8C", "46": "9C", "47": "10C",
            "48": "JC", "49": "QC", "50": "KC", "51": "AC"
        }

        self.tableau = [[] for _ in range(7)]
        self.setup_tableau()

    def generate_card_codes(self, file_name):
        card_codes = [file_name[i:i+2] for i in range(0, len(file_name), 2) if file_name[i:i+2].isdigit()]
        return card_codes

    def setup_tableau(self):
        pile = []
        pileH = []
        pileD = []
        pileS = []
        pileC = []
        index = 0
        count = 1
        for code in self.card_codes:
            card = self.mapping[code]
            rank = card[:-1]
            suit = card[-1]
            visible = False  # All cards are initially visible
            card_obj = self.Card(rank, suit, visible)

            # Add cards to tableau rows with increasing counts
            if index <= 6 and count <= 6:
                self.tableau[index].append(card_obj)
                index += 1

            elif index == 7:
                index = count
                count += 1

            else:
                pile.append(card_obj)
        
        for i in range(len(self.tableau)):
            self.tableau[i][-1].visible = True
            
        pile[-1].visible = True

        self.pile = pile
        self.pileH = pileH
        self.pileD = pileD 
        self.pileS = pileS 
        self.pileC = pileC 

    def play(self):
        print("Welcome to Solitaire!")
        print("Tableau:")
        for pile in self.tableau:
            print([str(card) for card in pile])


        print("\nPile:")
        print([str(card) for card in self.pile])

        print("\nPile of Hearts:")
        print([str(card) for card in self.pileH])

        print("\nPile of Diamonds:")
        print([str(card) for card in self.pileD])

        print("\nPile of Spades:")
        print([str(card) for card in self.pileS])

        print("\nPile of Clubs:")
        print([str(card) for card in self.pileC])
       
        print()
        print("Hacker's Tableau:")
        for pile in self.tableau:
            print([card.visible_str() for card in pile])

        print("\nHacker's Pile:")
        print([card.visible_str() for card in self.pile])

        print("\nHacker's Pile of Hearts:")
        print([card.visible_str() for card in self.pileH])

        print("\nHacker's Pile of Diamonds:")
        print([card.visible_str() for card in self.pileD])

        print("\nHacker's Pile of Spades:")
        print([card.visible_str() for card in self.pileS])

        print("\nHacker's Pile of Clubs:")
        print([card.visible_str() for card in self.pileC])

        

# Example usage
solitaire = Solitaire()
solitaire.play()
