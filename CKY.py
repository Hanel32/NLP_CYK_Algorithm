# -*- coding: utf-8 -*-
"""
Created on Sat Nov 04 18:38:43 2017

@author: Carson
"""

#CKY implementation for CSCE 489 Special Topics class.
#Allow for command line arguments to be passed.

import sys
import numpy as np

def buildTree(score, back):
    print "\nNew span: 1"
    for i in range(len(score)):
        print "\nIndices: " + str(i) + " " + str(i+1)
        for item, pt in zip(score[i][i+1],back[i][i+1]):
            if item > 0. and not pt == None:
                    prob = "P(" + str(pt[1]) + ") = " + str(item)
                    b    = " (BackPointer = (" + str(pt[0]) + ", " + str(pt[2]) + ", " + str(pt[3]) + ")"
                    print prob + b
    for span in range(2, len(score)+2):
        print "\nNew span: " + str(span)
        for begin in range(0, len(score)+1-span):
            end = begin + span
            print "\nIndicies: " + str(begin) + " " + str(end)
            for item, pt in zip(score[begin][end],back[begin][end]):
                if item > 0. and not pt == None:
                    prob = "P(" + str(pt[1]) + ") = " + str(item)
                    b    = " (BackPointer = (" + str(pt[0]) + ", " + str(pt[2]) + ", " + str(pt[3]) + ")"
                    print prob + b
                    
    return

def CKY(grammar, sentences):
    #
    #
    #NOTE!!!!!!!! CHANGE SENTS BACK!
    #
    #
    #build grammar dict
    keyI  = {}
    c     = 0
    for key in grammar:
        if key not in keyI:
            keyI[key] = c
            c+= 1
    c     = 0
    for sentence in sentences:
        sentence = sentence.split()
        #Probabilistic scores
        score = np.zeros((len(sentence),len(sentence)+1, len(grammar)))
        #Back-pointers to parent data
        back  = len(sentence)*[(len(sentence)+1)*[len(grammar)*[None]]]
        
        i = 0
        for word in sentence:
            print "\nSpan: " + word
            for A in grammar:
                if(word in grammar[A][""].keys()):
                    score[i][i+1][keyI[A]] = grammar[A][""][word]
                    print "P(" + str(A) + " " + str(word) + ") = " + str(grammar[A][""][word])
                else:
                    score[i][i+1][keyI[A]] = 0.
            #Handle Unary probabilities
            added = True
            while(added):
                #print "Word: " + word
                added = False
                for A in grammar:
                    for B in grammar:
                        #print "I (expect 0 1 2 3): " + str(i) + "," + str(i+1)
                        if(score[i][i+1][keyI[B]] > 0 and B in grammar[A][""].keys()):
                            temp = float(score[i][i+1][keyI[B]])
                            prob = float(grammar[A][""][B]) * temp
                            #print "P(" + str(B) + ")->" + str(A) + " = " + str(prob) 
                            if(prob > score[i][i+1][keyI[A]]):
                                score[i][i+1][keyI[A]] = prob
                                back[i][i+1][keyI[A]]  = B#words[word]
                                print "P(" + str(A) + " " + str(word) + ") = " + str(prob)
                                added = True
            i += 1
        for span in range(2, len(sentence)+2):
            for begin in range(0, len(sentence)+1-span):
                #print "Begin (expected 0, 1, 2, 0, 1, 0)" + str(begin)
                end = begin + span
                #print "End   (expected 2, 3, 4, 3, 4, 4)" + str(end)
                print "\nLocation: " + str(begin) + " " + str(end)
                for split in range(begin, end):
                    for A in grammar:
                        for B in grammar:
                            for C in grammar:
                                lop  = float(score[begin][split][keyI[C]])
                                mop  = float(score[split][end][keyI[B]])
                                if(C in grammar.keys() and B in grammar[C].keys() and A in grammar[C][B].keys()):
                                    rop  = float(grammar[C][B][A])
                                else:
                                    rop  = 0.
                                
                                prob = lop*mop*rop 
                                if(prob > score[begin][end][keyI[A]]):
                                    score[begin][end][keyI[A]] = prob
                                    back[begin][end][keyI[A]]  = (split, A, B, C)#words[word]
                                    print "P(" + str(A) + ")->" + str(C) + "+" + str(B) + " " + str(prob)
                added = True
                while(added):
                    print "Handling unaries!"
                    added = False
                    for A in grammar:
                        for B in grammar:
                            if(B in grammar[A][""]):
                                lop  = float(grammar[A][""][B])
                            else:
                                lop  = 0.
                            rop = float(score[begin][end][keyI[B]])
                            prob = lop * rop
                            if(prob > score[begin][end][keyI[A]]):
                                #print "Prob Unary: " + str(prob)
                                print "UNARY Location: " + str(begin) + " " + str(end) + " " + A
                                print "P(" + str(C) + ")->" + str(A) + "+" + str(B) + " " + str(prob) + "\n"
                                score[begin][end][keyI[A]] = prob
                                back[begin][end][keyI[A]]  = 0#words[word]
                                added = True
    
    return buildTree(score, back)
        
def checkDigit(digit):
    try:
        float(digit)
        return True
    except ValueError:
        return False

def parseGrammar(rules):
    print "Building grammar..."
    grammar = {}
    
    #Want to break it up into rules/evalunts.
    #For example, for all N rules, want all words that are nouns to be keys
    #From there, also want N->Word->Probability to be built into the grammar dictionary.
    #Idea: parse dictionary as keys -> term.prob and split on the period to get the probability
    for line in rules:
        line = line.split()
        rulesList = []
        rule = []
        for item in line:
            if(not checkDigit(item)):
                rule.append(item)
                line = line[1:]
            else:
                rule.append(item)
                rulesList.append(rule)
                line = line[1:]
                rule = []
        for rule in rulesList:
            if(len(rule) < 3 or len(rule) > 4):
                print "Improper grammar form! Rule not added"
                print rule
            else:
                if(len(rule) == 3):
                    nont = rule[0]
                    if nont not in grammar:
                        grammar[nont] = {}
                    if ""   not in grammar[nont]:
                        grammar[nont][""] = {}
                    term = rule[1]
                    if term not in grammar[nont][""]:
                        grammar[nont][""][term] = {}
                    prob = rule[2]
                    grammar[nont][""][term] = prob
                    rulesList = rulesList[1:]
                if(len(rule) == 4):
                    nona = rule[1]
                    if nona not in grammar:
                        grammar[nona] = {}
                    nonb = rule[2]
                    if nonb not in grammar[nona]:
                        grammar[nona][nonb] = {}
                    term = rule[0]
                    if term not in grammar[nona][nonb]:
                        grammar[nona][nonb][term] = {}
                    prob = rule[3]
                    grammar[nona][nonb][term] = prob
                    rulesList = rulesList[1:]
    return grammar

#About confirmFiles:
#  Confirms that the commandline arguments being sent are valid.
#  TODO: Make sure to come back and verify the OS path to the file.
def confirmFiles():
    confirmed = True
    
    if(len(sys.argv) != 3):
        print "Invalid number of file names provided! Program ending..."
        confirmed = False 
    if(sys.argv[0] != "CKY.py"):
        print "Not entirely sure how you're running the program..."
        confirmed = False
    if(sys.argv[1] != "grammar_rules.txt"):
        print "The second file should be grammar_rules.txt..."
        confirmed = False
    if(sys.argv[2] != "sents.txt"):
        print "The third file should be sents.txt"
        confirmed = False
    if(confirmed):
        print "All commandline arguments confirmed! Continuing to parsing phase..."
    return confirmed

def main():
    #NOTE: When implementing CKY, only parse a singular sentence at a time
    grammar      = {}
    #sents        = []
    validProgram = confirmFiles()
    print "Back from confirmation, result: "
    print validProgram
    if(validProgram):
        grammarF    = open(sys.argv[1])
        grammar     = parseGrammar(grammarF)
        print "Grammar built! Score sentence(s)..."
        #sents       = parseSents(sys.argv[2])
        sents       = open(sys.argv[2])
        sent        = []
        for item in sents:
            sent.append(item)
        parseRecord = CKY(grammar, sent)
    else:
        print "Unfortunately, you've provided some incorrect command line arguments..."
        
        
main()
        
        
