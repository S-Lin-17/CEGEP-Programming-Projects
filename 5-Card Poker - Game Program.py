import random
import time

class Card(object):
    def __init__(self, name, value, suit, symbol):
        self.name = name
        self.value = value
        self.suit = suit
        self.symbol = symbol

    def __repr__(self): # Make cards visible as strings for a human
        return self.symbol

class PokerPts(object):
    def __init__(self, cards):
        self.cards = cards

    def values_sum(self):
        SUM = 0
        for card in self.cards:
            SUM += card.value 
        return SUM

class Deck(object):
    def shuffle(self, times=1):
        random.shuffle(self.cards)
        print("Deck is shuffled.")

    def deal(self):
        return self.cards.pop(0) # Remove self 

class Card_Pile(Deck):
    def __init__(self):
        self.cards = []
        suits = {"Hearts":"♡", "Spades":"♠", "Diamonds":"♢", "Clubs":"♣"}
        values = {"A": 1,
                  "2": 2,
                  "3": 3,
                  "4": 4,
                  "5": 5,
                  "6": 6,
                  "7": 7,
                  "8": 8,
                  "9": 9,
                  "10": 10,
                  "J": 11,
                  "Q": 12,
                  "K": 13}

        for name in values:
            for suit in suits:
                symbol_Icon = suits[suit]
                if 2 <= values[name] < 11:
                    symbol = str(values[name])+symbol_Icon
                else:
                    symbol = name[0]+symbol_Icon
                self.cards.append( Card(name, values[name], suit, symbol) )

            
class Player(object):
  def __init__(self):
    self.cards = []

  def addCard(self,card):
    self.cards.append(card)

player = Player() # Initializes Player() class for the player (user)
CPU = Player()

# Player's initial amount of money
P_Money = 50.0

# Initial entrance fee (At Round 1-5)
Ent_Fee = 5.0
Round = 1

exit_program = False
print("Welcome to the 5-Card Sum Poker game!")

while not exit_program:

    print("")
    print("Round {}".format(Round))
    print("You have ${:.2f}".format(P_Money))

    # Entrance fee increase every 5 rounds 
    if Round % 5 == 0:
        Ent_Fee += 5.0
        print("The entrance fee has increased by $5.00")
    elif Round % 5 == 4: # Warns the Player that the entrance fee will increase the next round
        print("The entrance fee will increase by $5.00 the next round!")

    print("The current entrance fee is ${:.2f}".format(Ent_Fee))
    
    user_input = input("Enter 'Start' to begin the game or 'Exit' to close the game: ")

    if user_input == 'Start':
        
        P_Money -= Ent_Fee
        print("Your current balance is ${:.2f}".format(P_Money))

        deck = Card_Pile() # Initializes Deck() class
        deck.shuffle()

        # Giving cards to both Player and CPU hands
        for i in range(0,5):
            player.addCard(deck.deal()) # From Deck class *after shuffle
            CPU.addCard(deck.deal()) 

        print("")
        print("Current deck:")
        print(player.cards)
        print("") # Leaving space for Player to easily recognize the deck

        time.sleep(2)

        # Player Bet System
        PBet_Invalid = True
        while True:
            if PBet_Invalid == False:
                break
    
            PBet_in = input("How much do you want to bet: ")

            # Error if anything is entered other than a number with/without decimal
            try:
                PBet = float(PBet_in) # PBet is the Player's real bet

                if PBet > P_Money: # If bet exceeds Player's money
                    print("Your bet exceeds your current balance! Enter a smaller bet.")
                    # Will loop back to the bet prompt

                else:
                    PBet_Invalid = False # Will break the loop
            except:
                print("Input Error: make sure that your input is comprised of only integers or decimals.")

      
        invalid = True
        while invalid:
            discard_inp = input(
"""Which cards would you like to discard? Type '1' for 1st card, '2' for 2nd card, etc.
Please separate with commas.
If you don't want to discard, type 'Keep'
If you want to discard everything, type 'All'
"""
)

            if discard_inp == 'Keep':
                break

            elif discard_inp == 'All':
                player.cards = [] # Deck is erased to add in new cards
                for i in range(0,5):
                    player.addCard(deck.deal()) 
                break

            else:
                try: # Used to check if user has inputted the right amount of cards, the right numbers and right format

                    # Had to look online for this part of the code
                    inputList = [int(inp.strip()) for inp in discard_inp.split(",") if inp]

                    for inp in inputList:
                      if inp > 6:
                        continue 
                      if inp < 1:
                        continue 

                    for inp in inputList:
                      player.cards[inp-1] = deck.deal()
                    invalid = False

                except:
                    print("Input Error: use commas to separate the cards you want to hold and use the right numbers.")


        print("")
        print("The Dealer's initial deck:")
        print(CPU.cards)
        print("")

        # CPU discards cards with values less than 8
        cardIndex = 0
        for card in CPU.cards:
            if card.value < 8:
                CPU.cards[cardIndex] = deck.deal()
                cardIndex += 1
            else:
                cardIndex += 1

        
        time.sleep(3) # More delay

        print("")
        print("Your new deck:")
        print(player.cards) # New hand for Player

        print("")
        print("The Dealer's new deck:")
        print(CPU.cards) # Dealer's new deck
        print("")
        
        time.sleep(3) # More delay
    
        # Calculating sum of values of hands by calling "values_sum" method from PokerPts class
        P1 = PokerPts(player.cards)
        CPU1 = PokerPts(CPU.cards)
        P_SUM = P1.values_sum()
        CPU_SUM = CPU1.values_sum()
        print("Your total sum is:      {}".format(P_SUM))
        print("The Dealer's sum is:    {}".format(CPU_SUM))
        print("")

        time.sleep(2) # More delay

        # Determining the winner
        if P_SUM > CPU_SUM:
            print("You win!")
            price = PBet * 1.2 + Ent_Fee
            P_Money += price
            print("You've won ${:.2f}".format(price))

        elif P_SUM < CPU_SUM:
            print("You lose...")
            P_Money -= PBet

        else: # If P_SUM == CPU_SUM
            print("It's a tie!")
            print("You get your entrance fee back.")
            P_Money += Ent_Fee


        # Player status
        if P_Money == 0:
            print("You don't have any money left!")
            print("Game Over")
            exit_program = True
        elif P_Money < Ent_Fee:
            print("Your current balance (${:.2f}) is under the entrance fee (${:.2f}). You don't have enough money!".format(P_Money,Ent_Fee))
            print("Game Over")
            exit_program = True
        else:
            player.cards = [] # Resetting the Player's hand
            CPU.cards = [] # Resetting the Dealer's hand
            Round += 1
      

    elif user_input == 'Exit':
        exit_program = True

    else:
        print("Invalid input. Please make sure to write 'Start' or 'Exit'.")

print("Thank you for playing 5-card Sum Poker! Have a nice day!")

time.sleep(5) # Program stays open for 5 seconds before closing











    
