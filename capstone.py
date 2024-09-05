import time
import math
import random

# Behind the scenes stuff
originType = ['Musician', 'Detective', 'Surfer']
statNames = ['Intelligence', 'Intuition', 'Charisma']
originStats = [[5, 10, 5], [10, 5, 5], [5, 5, 10]]
pName = ''
pStats = [0, 0, 0]
notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
correctSequence = ['C', 'A', 'D', 'E']

# World building
Locations = ["kitchen", "den", "living Room", "bar"]
activityMenu = ["View stats", "Move location", "Inventory"]
actionMenu = ["Talk to suspect", "Search for clues", "Leave room"]
pianoMenu = ["Look at the key", "Inspect the piano case", "Leave the piano"]
inventory = ["Invitation"]
guests = {
    "Victor Reeves": {
        "role": "Rival composer",
        "motive": "Professional jealousy",
        "location": "den",
        "clue": "Sheet music with angry notes scribbled in the margins",
        "dialogue" : {
            "intro" : "Victor glares at you with undisguised contempt.",
            "options" : {
                1: {"prompt": "Ask about his relationship with Eliza", "response": "Eliza? Hmph. She got lucky. I'm "
                                                                                   "the one with real talent."},
                2: {"prompt": "See what he thinks about Eliza's disappearance", "response": " Clearly it's for "
                                                                                            "attention. Nothing more "
                                                                                            "than that."},
                3: {"prompt": "Comment on the sheet music", "response": "Oh that? I made some... improvements on one "
                                                                        "of Eliza's pieces. That's all."},
            }
        }

    },
    "Sophia Chen": {
        "role": "Ambitious protégé",
        "motive": "Desire for recognition",
        "location": "living room",
        "clue": "Practice schedule with unusually long hours",
        "dialogue" : {
            "intro" : "Sophie gives you a soft smile as you enter the room.",
            "options" : {
                1: {"prompt": "Ask about her relationship with Eliza", "response": "She's amazing. I only wish "
                                                                                   "I could be as good as her."},
                2: {"prompt": "See what he thinks about Eliza's disappearance", "response": " It's just awful! I was "
                                                                                            "hoping to show her one of "
                                                                                            "my new compositions..."},
                3: {"prompt": "Comment on the practice schedule", "response": "I'm trying really hard to be good "
                                                                              "enough. I have to put in these hours"
                                                                              " so Eliza will see that I'm worthy of "
                                                                              "playing for her."},
            }
        }
    },
    "Theodore Blackwood": {
            "role": "Estranged family member",
            "motive": "Split of family fortune",
            "location": "kitchen",
            "clue": "Letter to family lawyer demanding share of fortune",
            "dialogue" : {
                "intro" : "Theodore eyes you suspiciously when he notices your arrival.",
                "options" : {
                    1: {"prompt": "Ask about his relationship with Eliza", "response": "We grew up together."
                                                                                       "There isn't much more to say."},
                    2: {"prompt": "See what he thinks about Eliza's disappearance", "response": "I can't say I don't"
                                                                                                " benefit from her"
                                                                                                " disappearance. "
                                                                                                "The family lawyers"
                                                                                                "will have  \n "
                                                                                                "to rewrite "
                                                                                                "the will when they "
                                                                                                "learn of this."},
                    3: {"prompt": "Comment on the letter", "response": "It's a letter to my lawyer. Regardless of"
                                                                       " her stature, Eliza doesn't deserve the full "
                                                                       "value of our family estate. \n I should have "
                                                                       "my fair share. My lawyer will handle that for "
                                                                       "me."},
                }
        }
    },
    "Olivia Sinclair": {
                "role": "Obsessed Fan",
                "motive": "Wealthy socialite who wants to be close to Eliza",
                "location": "bar",
                "clue": "Several photos of Eliza, threatening letters",
                "dialogue" : {
                    "intro" : "Olivia clearly tries to avoid your gaze when you come in.",
                    "options" : {
                        1: {"prompt": "Ask about his relationship with Eliza", "response": "Eliza? Well, I really like "
                                                                                           "her Obviously."},
                        2: {"prompt": "See what he thinks about Eliza's disappearance", "response": "It's the worst! "
                                                                                                    "What if "
                                                                                                    "something "
                                                                                                    "happened to her?"
                                                                                                    " Maybe she found "
                                                                                                    "out I snuck in "
                                                                                                    "here... Don't "
                                                                                                    "tell anyone!"},
                        3: {"prompt": "Comment on the photos and letters", "response": "Those? I just... I mean, "
                                                                                       "Eliza and I are friends. She"
                                                                                       "loves her. She wanted me here"
                                                                                       " but forgot to send the invite."
                                                                                       " I thought she forgot about "
                                                                                       "me, so I got upset. It's no "
                                                                                       "big deal now."},
            }
        }
    },
    "Eliza Blackwood": {
                "role": "Host of party, renowned musician",
                "motive": "Generate publicity",
                "location": "secret room",
                "clue": "Letter to family lawyer demanding share of fortune",
                "dialogue" : {
                    "intro" : "Eliza smirks as you enter the room.",
                    "options" : {
                        1: {"prompt": "Ask where's she been", "response": "Here, darling. Safe and sound."},
                        2: {"prompt": "Ask why she disappeared", "response": "I had to. What better publicity than "
                                                                             "one of the best artists going missing "
                                                                             "before their newest piece comes out?"},
                        3: {"prompt": "Ask if she'll return to the party", "response": "No, not yet. If I do, then "
                                                                                       "no one will even know that I "
                                                                                       "was gone. Once a few days have "
                                                                                       "passed, then I'll let"
                                                                                       " everyone that I'm okay. "
                                                                                       "Until then, I'll stay here."},
                        4: {"prompt": "Should I go?", "response": "If you don't mind. I trust that you'll keep this "
                                                                  "hush hush. There's no harm in the guests thinking "
                                                                  "I'm gone just a few days, right? If anything, "
                                                                  "it's shown everyone's true colors."},
            }
        }
    },
}

# this will check is a certain item is in the inventory list
def indexInList(item, myList):
    foundIndex = -1
    for i in range(len(myList)):
        if myList[i] == item:
            foundIndex = i
            break
    return foundIndex

# this function presents the menu (inventory, locations) in a nice way
def listToText(myList):
    combinedText = '\n'
    for i in range(len(myList)):
        combinedText += str(i) + ")" + myList[i] + '\n'
    return combinedText + "\n"

def checkMenuRange(question, listName, isCanceable = False):
    index = int(input(question + listToText(listName) + "> "))
    while(True):
        if isCanceable and index == -1:
            return index
        elif index < 0 or index > len(listName) -1:
            index = int(input("Invalid choice. Please try again.\n"))
        else:
            return index

def starline(numRows, numSleep):
    sLine = "*" * 10
    for i in range(numRows):
        print(sLine)
    time.sleep(numSleep)

# condenses unique items in the inventory list, adds a count of each item
def showInventory(inventoryList):
    if len(inventoryList) < 1:
        print("Inventory is empty!")
    uniqInventory = list(set(inventoryList))
    for i in range(len(uniqInventory)):
        print(str(i)+") " + uniqInventory[i] + " ("+str(inventoryList.count(uniqInventory[i]))+")")

def talk_to_guest(guest_name):
    guest = guests[guest_name]
    print(f"\nYou approach {guest_name}. {guest['dialogue']['intro']} ")
    while True:
        print("\nWhat would you like to say?")
        for num, option in guest['dialogue']['options'].items():
            print(f"{num}: {option['prompt']}")
        starline(1,1)
        print("0. End conversation")

        choice = input("> ")
        if choice == "0":
            print(f"You thank {guest_name} and end the conversation.")
            break
        elif choice in [str(num) for num in guest['dialogue']['options'].keys()]:
            response = guest['dialogue']['options'][int(choice)]['response']
            print(f"\n{guest_name}: {response}")
        else:
            print("Invalid choice. Please try again.")

def guestInformation(guest_name):
    if guest_name in guests:
        guest = guests[guest_name]
        print(f"You see {guest_name}. They are the {guest['role']}. You notice: {guest['clue']}.")

def musical_puzzle():
    player_sequence = []
    attempts = 0
    max_attempts = 3

    print("Enter the correct sequence of notes to unlock the secret clue.")
    print("Available notes: C, D, E, F, G, A, B")

    while attempts < max_attempts:
        for i in range(len(correctSequence)):
            note = input(f"Enter note {i+1}: ").upper()
            if note not in notes:
                print("Invalid note. Please try again.")
                continue
            player_sequence.append(note)

        if player_sequence == correctSequence:
            print("Correct!")
            return True
        else:
            print("Incorrect sequence.")
            player_sequence = []
            attempts += 1
            print(f"You have {max_attempts - attempts} attempts remaining.")

    print("You've run out of attempts. The piano keys are hidden by their cover, sealed shut forever.")
    return False
# Defining the character
pName = input("What is your name? > ")
print("Welcome to The Mystery of the Blackwood Disappearance, " + pName + "!")
starline(1,2)
print("Here you will create your character. Choose a class from the options \n "
      "below by telling me which number best suits your character!")
starline(1,2)
for i in range(len(originType)):
    print(originType[i]+":")
    for j in range(len(originStats[i])):
        print(statNames[j],originStats[i][j])
    starline(1,1.5)
pClass = checkMenuRange("Choose your class by inputting the number corresponding to your preferred class.",
                        originType)
print("You have chosen " + originType[pClass] + "!")
pStats = originStats[pClass]
starline(1,3)
print("Welcome!"
      "You are now " + pName + ", a well known " + originType[pClass] + "!"
      " You reside in Connecticut and are currently in your home.")
if originType[pClass] == 'Surfer':
    print("Actually... It's kind of weird that a surfer "
          "lives in Connecticut... but okay."
          "You've built quite a following by traveling the \n"
          "coastlines and venturing to tropical islands. \n"
          "With your only income coming from sponsorships,\n"
          " you've managed to become quite the smooth-talker. \n"
          "Should you run into any trouble on your upcoming \n"
          "journey, you'll have the charisma to charm any potential \n"
          "suspects.")
elif originType[pClass] == 'Detective':
    print("As a seasoned detective you are well-known in \n"
          "the law enforcement world of Connecticut. While in a small\n"
          "state, you've managed to hone your skills and grow your \n"
          "reputation as one of the best. Should you run into\n"
          "any trouble on your upcoming adventure, you'll have the \n"
          "skills to find clues and question suspects.\n")
elif originType[pClass] == 'Musician':
    print("As a musician, you've rubbed elbows with some of the \n"
          "best artists of you generation. Your whole life has \n"
          "been spent waiting for your cue and watching others \n"
          "as they perform their parts. Should you run into any \n"
          "trouble on your upcoming adventure, you'll have the \n"
          "skills to quietly watch and gather clues. You are also \n"
          "pretty lucky!")
starline(1,1)
input("Press enter to continue...")
print(" You sort through your mail. Amongst the junk, you find an invitation. It's addressed as follows: \n"
      "Dear " + pName + ", you are cordially invited to the birthday party of World \n"
                        "Renowned Musician Eliza Blackwood. She will also perform her newest composition. \n"
                        " Please respond in kind.")

exitInput = input("Would you like to accept the invitation? (Yes or no) > ")
if exitInput == "No":
    print("...okay.")
    print("I guess you don't go to the performance. Game over. Boo.")
    starline(2,3)
    exit()
else:
    print("Great! You begin your preparations to travel to Eliza's mansion.")
starline(2,2)
print("You have arrived!")
starline(1,1) 
print("As you make your way up the gravel driveway, you notice the \n "
      "opulent Blackwood Manor looming before you, a grand Victorian edifice \n "
      "silhouetted against the stormy night sky. Lightning flashes, briefly illuminating \n" 
      "the mansion's ornate facade and casting eerie shadows across the manicured grounds.")
starline(1,1)
print("When you arrive, you joined by a few other guests. You recognize a few of them, but others you've never"
      " seen before. You all shuffle into the mansion, ready to find what's awaiting you.")
print("Eliza Blackwood stands at in the foyer, arms wide open. She smiles.")
print("Eliza: 'Welcome everyone! Please, please, come inside. We have quite \n"
      "the celebrations planned. We'll get you some refreshments soon, but first, \n"
      "I'd like to introduce our guests. Victor, please.'")
starline(1,1)
input("Press enter to continue...")
starline(1,1)
print("Victor Reeves, a fellow musician, gives a tight smile to the rest of you.")
print("Eliza: 'And Sophia... a dear protegee.'")
print("An unfamiliar woman with a large smile nods to you. She seems stressed ")
print("Eliza: 'My cousin Theodore.")
print("Theodore Blackwood smiles at the rest of you.")
print("Eliza: 'My good friend " + pName +"!")
print("You wave to the others.")
print("Eliza: And finally, a good... friend, Olivia.")
print("A young girl ignores the rest of you, keeping her sights on Eliza.")
print("Eliza: 'And now, please as you meander and mingle, I will play a new song on the piano.'")
starline(1,1)
input("Press enter to continue...")
starline(1,1)
print("Eliza walks to the side of the foyer, where a piano sits. She sits at it, smiling one last time before "
      "turning her attention to the keys. Her fingers linger on the starting keys, and seconds later you hear "
      "the first few notes of what seems to be a beautiful composition. Suddenly, the lights cut out and the "
      "party guests are plunged into darkness. The music stops.")
print("One of the men gasps, while the others seem to be shocked into silence. \n"
      "You hear someone say, 'Oh no!'")
print("A few more minutes pass, an uncertainty falling over the group. After a few minutes, \n"
      "the lights come back on. Eliza is gone.")
starline(1,1)
input("Press enter to continue...")
starline(1,1)
print("Theodore: 'Where is she?'")
print("Sophia: 'Eliza?'")
print("The others exclaim their surprise. Once the initial shock subsides, the group turns to you.")
print("Why are you all looking at me like that, you ask.")
if originType[pClass] == 'Surfer':
    print("Theodore shrugs. 'You seem pretty lucky,' he says. 'Perhaps you may have some luck finding her.'")
if originType[pClass] == 'Detective':
    print("Olivia balks. 'Aren't you a detective? Shouldn't you start looking for her?'")
if originType[pClass] == 'Musician':
    print("Victor laughs. 'You and her are close, since you're both musicians. Perhaps you might find her quicker \n"
          "than the rest of us.")
print("With a sigh, you nod your head and decide to start looking for your friend, Eliza.")
starline(1,1)

# Stats for me to playtest without doing the whole intro
# pName = 'Maddie'
# pClass = 1
# pStats = originStats[pClass]

# Main Menu! & Inventory
inGameLoop = True
while inGameLoop:
    actChoice = checkMenuRange("What would you like to do?", activityMenu)
    # Stats, travel, inventory
    if actChoice == 0:
        print("Statistics")
        for i in range(len(statNames)):
            print(statNames[i], pStats[i])
        starline(1,1)
    elif actChoice == 1:
        print("Travel")
        travelChoice = checkMenuRange("Where would you like to go?", Locations, True)
        inRoom = True
        while inRoom:
            if travelChoice == 0:
                print("You enter the kitchen.")
                guestInformation("Theodore Blackwood")
                kitchenChoice = checkMenuRange("What would you like to do?", actionMenu)
                if kitchenChoice == 0:
                    talk_to_guest("Theodore Blackwood")
                if kitchenChoice == 1:
                    print("You look around, noting a piece of paper with the letter 'E' written on it stuck to"
                          "the fridge.")
                if kitchenChoice == 2:
                    inRoom = False
            if travelChoice == 1:
                print("You enter the den.")
                guestInformation("Victor Reeves")
                kitchenChoice = checkMenuRange("What would you like to do?", actionMenu)
                if kitchenChoice == 0:
                    talk_to_guest("Victor Reeves")
                if kitchenChoice == 1:
                    print("On the clock, there is a small 'D' etched into the glass.")
                if kitchenChoice == 2:
                    inRoom = False
            if travelChoice == 2:
                print("You enter the living room.")
                guestInformation("Sophia Chen")
                kitchenChoice = checkMenuRange("What would you like to do?", actionMenu)
                if kitchenChoice == 0:
                    talk_to_guest("Sophia Chen")
                if kitchenChoice == 1:
                    print("The TV screen every few minutes flashes with the letter 'A'.")
                if kitchenChoice == 2:
                    inRoom = False
            if travelChoice == 3:
                print("You enter the bar.")
                guestInformation("Olivia Sinclair")
                kitchenChoice = checkMenuRange("What would you like to do?", actionMenu)
                if kitchenChoice == 0:
                    talk_to_guest("Olivia Sinclair")
                if kitchenChoice == 1:
                    print("There are glasses on the bar arranged in shape of the letter 'C'."
                          "There is a piano in the corner of the room.")
                    pianoInput = input("Would you like to look at the piano? > ")
                    if pianoInput == "Yes":
                        piano = True
                        while piano:
                            pianoChoice = checkMenuRange("What would you like to do at the piano?", pianoMenu)
                            if pianoChoice == 0:
                                print("Your fingers linger over the keys.")
                                pianoPlay = input("Would you like to play? > ")
                                if pianoPlay == "Yes":
                                    if musical_puzzle():
                                        piano = False
                                        inRoom = False
                                        inGameLoop = False
                                    else:
                                        print("You do not discover the truth regarding Eliza's disappearance. "
                                              "Try again!")
                                        exit()
                                if pianoPlay == "No":
                                    print("You back away from the keys.")
                            elif pianoChoice == 1:
                                print("You inspect the piano. Nothing seems to be of note until you take a step back. "
                                      "On the legs, there's some sort of code scratched into the wood. It says: "
                                      "B1, L2, D3, K4")
                            elif pianoChoice == 2:
                                print("You back away from the piano and return to your attention to the room.")
                                piano = False
                if kitchenChoice == 2:
                    inRoom = False

    elif actChoice == 2:
        print("Inventory")
        showInventory(inventory)
        starline(1, 3)
print("As the music fades from the piano, the locked door opens. Olivia glances at it, but seemingly doesn't care"
      " enough to ask about it. You enter the secret room. There's a journal on the table that reads: "
      " (dated one week before the party) : \n"
      "Sometimes I wonder if the pressure is worth it. I am constantly forced to change my image or sound "
      "so I'll continue to be liked by society. Perhaps a new type performance will capture their interest.")
print("Then there are indentations on the page, as if someone wrote something on the page before and tore it out.")
print("You take the evidence you've collected and ponder who is responsible for the crime. You think of what the "
      "suspects have claimed and the journal entry. There is only one plausible culprit behind Eliza's "
      "disappearance.")
inSuspect = True
while inSuspect:
    suspectChoice = input("Who do you think is the culprit? > ")
    if suspectChoice == "Eliza":
        starline(1,1)
        print("Correct!")
        starline(1,1)
        inSuspect = False
    else:
        print("Not quite. Try again!")
# After the player correctly identifies Eliza as the suspect
print("You say out loud, seemingly to no one, 'Eliza. I know you're here.'")
print("As you say her name, she lets out a frustrated sigh.")
print("'So, you've figured it out,' she says, stepping out from behind a hidden bookshelf.")
print("'I have to hand it to you, you're quite the detective.")
print()
print("I orchestrated this whole charade to generate publicity for my new composition. \n"
      "The pressure of always needing to be perfect was becoming unbearable.'")
print('"I needed a way to escape it all, even if just for a little while."')
print()
print("'And now that you've found me, what are you going to do? Turn me in to the authorities?'")
print()

elizaChoice = input("What will you do? (1. Turn her in, 2. Let her go) > ")

if elizaChoice == "1":
    print("'I knew you wouldn't understand, Eliza says, shaking her head in disappointment.'")
    print("'Very well, then. I suppose I'll have to face the consequences of my actions.'")
    print()
    print("You escort Eliza out of the hidden room and contact the police, ensuring she is held accountable for her \n"
          "deception.")
    print("The mystery of the Vanishing Virtuoso has been solved.")
elif elizaChoice == "2":
    print("'I see, Eliza says, her eyes widening in surprise. You're letting me go?'")
    print("'Thank you. I promise I'll use this second chance to focus on my music, \n "
          "and not let the pressures of fame consume me again.'")
    print()
    print("You nod in understanding and allow Eliza to slip back through the hidden passage, disappearing from view.")
    print("The mystery remains unsolved, but you've chosen to give Eliza a chance at redemption.")
else:
    print("You hesitate, unsure of how to proceed. Eliza takes advantage of your indecision and quickly slips back \n"
          "through the hidden passage, vanishing from sight.")
    print("The mystery remains unresolved, and Eliza's fate is left uncertain.")

print()
print("The End.")
print(f"Congratulations {pName}! You have completed The Mystery of the Vanishing Virtuoso!")
starline(3,3)