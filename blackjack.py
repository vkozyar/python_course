# Mini-project #6 - Blackjack
# http://www.codeskulptor.org/#user44_oBbSrX14YK_24.py

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
play_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = list()

    def __str__(self):
        str_self = ""
        for card in self.cards:
            str_self = str_self + str(card) + " "
        return str_self
    
    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        hand_value = 0
        ace_true = False
        for card in self.cards:
            if card.get_rank() == 'A':
                #print "there was A"
                ace_true = True
            hand_value += VALUES[card.get_rank()]
            
            if hand_value < 11 and ace_true == True:
                hand_value += 10
        #print "hand_value = ", hand_value
        return hand_value
        
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 82 # the width of card + 10 pixels
            
        # draw a hand on the canvas, use the draw method fo        

        
# define deck class 
class Deck:
    def __init__(self):
        self.decks = list()
        for i in SUITS:
            for j in RANKS:
                self.decks.append(Card(i,j))
        
    def shuffle(self):
        random.shuffle(self.decks) 

    def deal_card(self):
        return self.decks.pop()
            
    def __str__(self):
        str_self =  ""
        for deck in self.decks:
            str_self = str(deck) + " "
        print str_self
        return str_self

#define event handlers for buttons
def deal():
    global in_play, dealer, player, deck_keeper, outcome
    in_play = False
    outcome = ""

    # your code goes here
    
    deck_keeper = Deck()
    deck_keeper.shuffle()
    dealer = Hand()
    player = Hand()
    
    dealer.add_card(deck_keeper.deal_card())
    dealer.add_card(deck_keeper.deal_card())
    player.add_card(deck_keeper.deal_card())
    player.add_card(deck_keeper.deal_card())
    
    print "dealer cards:", dealer
    print "player cards:", player
    
    
    in_play = True

def hit():
    global in_play, score, outcome
    if player.get_value() < 21 and in_play == True:
        player.add_card(deck_keeper.deal_card())
        
    if player.get_value() >= 21 and in_play == True:
        outcome = "You have busted!"
        score -= 1
        print "You have busted!"
        in_play = False
        
    
    # replace with your code below
    
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    # replace with your code below
    global outcome, in_play, player, dealer, score, play_score, deal_score
    
    while dealer.get_value() < 17:
        dealer.add_card(deck_keeper.deal_card())
    
    if in_play == True:
        if player.get_value() > dealer.get_value() or dealer.get_value() > 21:
            print "Player Win"
            outcome = "Player Win!"
            #in_play = False
            score += 1
        else:
            score -= 1
            outcome = "Dealer Win!"
            
    in_play = False
       
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome, in_play, score, play_score, deal_score

    play_score = player.get_value()
    deal_score = dealer.get_value()
    
    #canvas.draw_text("Game", [240, 50], 50 ,"Pink")
    
    player.draw(canvas, [100, 400])
    dealer.draw(canvas, [100, 150])
    
    #Print message about player win/lost
    canvas.draw_text(outcome, [210, 100], 30 ,"Black")
    
    # for card back
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (136,199), CARD_BACK_SIZE)
    
    # player_score just for test
    #canvas.draw_text( "Player score = " + str(play_score), [200, 550], 20 ,"Black")
    # dealer_score just for test
    #canvas.draw_text( "Dealer score = " + str(deal_score), [30, 550], 20 ,"Black")
    canvas.draw_text( "Score = " + str(score), [350, 550], 20 ,"Black")
    
    # Just test crad drawing
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
