#!/usr/bin/env python3

import random

suits={'c':'clubs','h':'hearts','d':'diamonds','s':"spades"}

class Card:
    def __init__(self,rank,suit):
        self.rank=rank      #card rank: 1=ace, 13=king
        self.suit=suit      #'c','d','h','s': The card's real suit
        self.effectivesuit=suit     #always equals suit, except for 8's
    def __repr__(self):
        #produce printable representation of this card
        q=[None,"A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        if self.rank != 8:
            return q[self.rank]+" of "+suits[self.suit]
        else:
            return q[self.rank]+" of "+suits[self.suit]+" ("+suits[self.effectivesuit]+")"
        
#create a deck of 52 cards along with a waste pile with one card.
def make_deck():
    deck=[]    #the deck (draw pile)
    for r in range(1,14):
        for s in 'cshd':
            deck.append( Card(r,s) )
    random.shuffle(deck)
    waste = [deck.pop()]      #the waste pile
    return deck,waste
        
#deal a hand; return a list of cards representing the hand
def deal_hand(deck):
    #if there are not enough cards left to deal a hand, 
    #this will throw an error
    tmp=[]
    for i in range(5):
        tmp.append(deck.pop())
    return tmp
    
#draws one card and return it. If the deck is exhausted,
#shuffle the waste pile and make it the new deck.
#If the waste pile has only one card and the deck
#is exhausted, return None
def draw_card(deck,waste):
    if len(deck) == 0 and len(waste) == 1:
        return None
        
    if len(deck) == 0:
        deck[:] = waste[:-1]
        waste[:] = [waste[-1]]
        random.shuffle(deck)
        
    return deck.pop()
    
#c = card to play; waste=the waste pile
#Return true if c may legally be played to waste.
def is_legal_play(c,waste):
    wastetop = waste[-1]
    if c.rank == 8:
        return True
    if c.suit == wastetop.effectivesuit:
        return True
    if c.rank == wastetop.rank:
        return True
    return False
    
 
#display the table
def show_table(deck,waste,hands,turn):
    print("============================")
    print(len(deck),"cards in deck;",len(waste),"cards in waste pile")
    for i in range(len(hands)):
        if i != turn:
            print("Opponent",i,"has",len(hands[i]),"cards")
    print("Top card of waste pile:",waste[-1])
    for i in range(len(hands[turn])):
        print(i+1," => ",hands[turn][i])
            
def main():

    deck,waste = make_deck()
    
    numplayers = 2
    
    hands=[]
    for i in range(numplayers):
        hands.append(deal_hand(deck))
        
    turn=0      #which player goes next

    while 1:
        
        #display the table
        show_table(deck,waste,hands,turn)
        
        #get the user's choice
        idx = input("Play which card? (Enter number, or 'd' to draw) ")
        if idx == 'd':
            c = draw_card(deck,waste)
            if not c:
                print("Oh, too bad. You tried to take a card and there wasn't one. You lose.")
                return
            else:
                hands[turn].append(c)
        else:
            try:
                idx = int(idx)-1
            except ValueError:
                idx=-1
            
            if idx < 0 or idx >= len(hands[turn]):
                print("Not a valid index")
            elif not is_legal_play(hands[turn][idx],waste):
                print("Not a valid play")
            else:
                c = hands[turn].pop(idx)
                s='*'
                if c.rank == 8:
                    while len(s) == 0 or s not in "cshd":
                        s = input("What suit (c,h,s, or d)? ").strip()
                    c.effectivesuit = s
                    
                waste.append(c)
                if len(hands[turn]) == 0:
                    print("Player",turn,"wins!")
                    return
                turn = (turn + 1 ) % numplayers
                
        
main()
