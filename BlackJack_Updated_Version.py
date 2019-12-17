from random import shuffle

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
value={'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

#Objects of the game
class Cards():
    #Card Object , define what is a card and the type of it
    '''
    Tasks:
    #represent cards
    '''
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank

    def __str__(self):
        return self.suit + ' of ' + self.rank

class Deck():
    #Deck Object ,define what is a Deck , store the cards of the game
    
    '''
    Tasks:

    #Manage the cards during the game
    #Store Them
    #Distribute Them
    '''

    def __init__(self):
        self.deck=[Cards(suit,rank) for suit in suits for rank in ranks]

    def __str__(self):
        names=''
        for card in self.deck:
            names+='\n'+card.__str__()
        return names

    def shuffle(self):
        shuffle(self.deck)

    def distribute(self):
        single_card=self.deck.pop()
        return single_card
    
class Hand():
    #Hand Object ,define what is a Hand , store the cards belonging to each player
    '''
    Tasks:
    #Track Cards
    #Managing value of Hand
    #pull of deck
    '''

    def __init__(self,deck):
        self.handvalue=0
        self.handcards=[]
        self.ace=0

        for i in range(0,2):
            self.handcards.append(deck.distribute())
            self.handvalue+= value[self.handcards[i].rank]

            if self.handcards[i].rank =='Ace':
                self.ace+=1


    def __str__(self,):
        holded_cards=''

        for single_card in self.handcards:
            holded_cards+='\n'+single_card.__str__()
        return holded_cards

    def pull(self,card):
        self.handcards.append(card)
        self.handvalue+=value[card.rank]

    
    def ace_value_correction(self):
        if self.handvalue > 21:
            if self.ace > 0 :
                self.handvalue-=10
                self.ace-=1


    
class BankAccount():
    #Define Account of each player 

    '''
    Tasks:
    #Control Chips of each player
    #Updating Amount in relate to bet
        '''
    def __init__(self):
        self.chips=100
        self.bet=0

    def placebet(self):
        self.chips-=self.bet
    
    def win(self):
        self.chips+=2*self.bet
    
    def tie(self):
        self.chips+=self.bet
    def refill(self):
        self.chips=100



#Function to operate the game 
def betPlacer(bank):
    #place bet
    #check if it suply the condition of player chips
    #update chips
    while True:
        try:
            bank.bet=int(input('Enter your bet: '))
        except ValueError:
            print('Error occur , please try again by entering intenger')
        else:
            if bank.bet > bank.chips:
                print('your resourses are not satisfaying to place such bet , try again')
            else:
                bank.placebet()
                break



def action(deck,player_hand):
    #Takes user decision in order to determinate if it should keep pulling cards from deck 
    global game
    try:
        choice=input('\nPlease choose "h" for hit and "s" for stand: ')

        if choice=='h':
           player_hand.pull(deck.distribute())
        else:
            game=False

    except ValueError:
        print('Please Enter h or s')

def show_some(player,dealer):
    #shows card during the game
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.handcards[1])
    print("\nPlayer's Hand:", *player.handcards, sep='\n ')

def reveal_hidden_card(dealer):
    #show cards at the end of the game
    print("\nDealer's Hand:", *dealer.handcards, sep='\n ')


def game_process():
    #process start running at each start of the game by user decision
    try:
        decider=input('In order to start a game press any key or press "E" to exit the game:  ')
    except ValueError:
        print('Input error occur , you should enter only Y or N for Yes/No')
    else:
        if decider.lower() !='e':
            return True
        else:
            return False

   
player_bank=BankAccount()

while game_process():
    game=True
    deck=Deck()
    deck.shuffle()
    player_hand=Hand(deck)
    dealer_hand=Hand(deck)

    print('\nWelcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')
    betPlacer(player_bank)
    show_some(player_hand,dealer_hand)

    while game: #actual game take place
        action(deck,player_hand) #ask if user want to hit
        player_hand.ace_value_correction() #in case user exceed 21 there will be chcek for aces in order to try and reduce value by changing it to 1
        show_some(player_hand,dealer_hand)


        if game==False: #in case player decide to stop hit cards
            while dealer_hand.handvalue < 17:
                dealer_hand.pull(deck.distribute())
                dealer_hand.ace_value_correction()
            reveal_hidden_card(dealer_hand)
        
        if player_hand.handvalue > 21:
            print(f'You are busted , your current chip balance is {player_bank.chips}')
            break
    
        elif dealer_hand.handvalue > 21:
            player_bank.win()
            print(f'Dealer is busted , your win and your chip balance is {player_bank.chips}')
            break

    if player_hand.handvalue <= 21 and dealer_hand.handvalue <=21:
        if player_hand.handvalue > dealer_hand.handvalue:
            player_bank.win()
            print(f'Player Win , your chips balance is {player_bank.chips}')
        elif player_hand.handvalue < dealer_hand.handvalue:
            print(f'Dealer Win , Player chips balance now is {player_bank.chips}')
        elif player_hand.handvalue == dealer_hand.handvalue:
            player_bank.tie()
            print(f'Its Tie, Player chips balance now is {player_bank.chips}')

    if player_bank.chips == 0:
        player_bank.refill()
        print(f'You are out of money , here take another 100 if you want keep gambling')