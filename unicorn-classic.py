#
# Flying Unicorn
# A simple quantum game where the player has to fly a unicorn to the castle.
# Classic implementation (non-quantum).
#

import random
import math

def getName(index):
  names = {
    1: 'Golden',
    2: 'Sparkle',
    3: 'Twilight',
    4: 'Rainbow',
    5: 'Mist',
    6: 'Bow',
    7: 'Cloud',
    8: 'Sky',
    9: 'Magic',
    10: 'Pixel',
    11: 'Sprite',
    12: 'Mansion',
    13: 'Dark',
    14: 'Light',
    15: 'Crimson'
  }

  return names.get(index, 'Mystery')

def getJewel(index):
  names = {
    1: 'amethyst',
    2: 'sapphire',
    3: 'emerald',
    4: 'jade',
  }

  return names.get(index, 'Mystery')

# Get the status for the current state of the unicorn.
def status(altitude):
  if altitude == 0:
    return 'is waiting for you on the ground'
  elif altitude <= 100:
    return 'is floating gently above the ground'
  elif altitude <= 200:
    return 'is hovering just above the evergreen sea of trees'
  elif altitude <= 300:
    return 'is approaching the first misty cloud layer'
  elif altitude <= 400:
    return 'has soared through the misty pink clouds'
  elif altitude <= 500:
    return 'is well above the misty clouds'
  elif altitude <= 600:
    return 'You can barely see the evergreen sea of trees from this high up'
  elif altitude <= 700:
    return 'is soaring through the sky'
  elif altitude <= 800:
    return 'You can see the first glimpse of the golden castle gates just above you'
  elif altitude <= 900:
    return 'is nearly at the mystical castle gates'
  elif altitude < 1000:
    return 'swiftly glides through the mystical castle gate. You\'re almost there'
  else:
    return 'A roar emits from the crowd of excited sky elves, waiting to greet you'

def action(command):
  command = command.lower()[0]

  switcher = {
    'u': 150,
    'd': -150,
    'q': 0
  }

  return switcher.get(command, -1)

def guess():
  return random.randint(1, 14)

def bound(value, low, high):
   diff = high - low
   return (value % diff + diff) % diff

def miniGame(altitude):
  print("\n=====================\n-[ Altitude " + str(altitude) + " feet ]-\nA mischievous quantum cloud blocks your way and challenges you to a game!")
  print("He has stolen a magical unicorn jewel from the castle!\nIf you can guess which jewel is the real one before the cloud, you'll be rewarded.\nIf you lose, you'll face a penalty.")

  bonus = 0

  # Read input.
  command = input("Do you want to play his game? [yes,no]: ").lower()
  if command[0] == 'y':
    # Select a random number (returned as an array of bits).
    print("The mischievous cloud blinks his eyes. You hear a crack of thunder. A unicorn jewel has been chosen.")
    secret = random.randint(1, 14) # 1-14
    secretInt = secret
    low = 1
    high = 14
    print("Psst. The secret is " + str(secretInt))

    # Give the player a chance against the quantum algorithm by breaking the guesses into ranges of 4 choices (25% chance).
    if secretInt < 5:
      low = 1
      high = 4
    elif secretInt < 9:
      low = 5
      high = 8
    elif secretInt < 13:
      low = 9
      high = 12
    else:
      low = 13
      high = 14

    # Begin the mini-game loop.
    isGuessGameOver = False
    round = 0
    while not isGuessGameOver:
      # Let the player make a guess.
      round = round + 1
      jewels = []
      for i in range(high - low + 1):
        jewels.append(getJewel(i + 1))

      # Select a jewel.
      command = ''
      while not command.lower() in jewels:
        command = input("Round " + str(round) + ". Which unicorn jewel is the real one? [" + ','.join(jewels) + "]: ").lower()

      # Make the selected index 1-based to match our secret number and be within the selected range.
      index = low + jewels.index(command) if command in jewels else -1

      # Check if the player guesses the correct number.
      if index == secretInt:
        print("You guessed correct!")
        print("Altitude + 100")
        bonus = 100
        isGuessGameOver = True
      else:
        print("You guessed wrong.")

      # Let the computer make a guess.
      if not isGuessGameOver:
        # The computer's guess is a number from 1-14.
        computerResult = guess()

        # Bound the result to the range of possible jewels (i.e., 1-4).
        computerJewelIndex = bound(computerResult, low, high + 1)
        if computerJewelIndex == 0:
          computerJewelIndex = 4

        # Get the matching jewel name.
        jewelName = getJewel(computerJewelIndex)

        # Finally, get the index of the matching jewel within range and use this as the computer's guess within range.
        computerResult = low + jewels.index(jewelName)

        print("The mischievous cloud guesses " + getJewel(computerJewelIndex) + '.')
        if computerResult == secretInt:
          print("Haha, I win, says the mischievous cloud!\nDon't say I didn't warn you!")
          print("Altitude - 100")
          bonus = -100
          isGuessGameOver = True

  # Return the new altitude + bonus (or penalty).
  return (altitude + bonus) if (altitude + bonus) >= 0 else 0

isGameOver = False # Indicates when the game is complete.
altitude = 0 # Current altitude of player. Once goal is reached, the game ends.
goal = 1024 # Max altitude for the player to reach to end the game.
turns = 0 # Total count of turns in the game.

# Generate a random name using a quantum random number generator.
name = getName(random.randint(1, 16)) + ' ' + getName(random.randint(1, 16))

print('================')
print(' Flying Unicorn')
print('================')
print('')
print('Your majestic unicorn, ' + name + ', is ready for flight!')
print('After a long night of preparation and celebration, it\'s time to visit the castle in the clouds.')
print('Use your keyboard to fly up or down on a quantum computer, as you ascend your way into the castle.')
print('')

# Begin main game loop.
while not isGameOver:
  # Setup a variable to represent the unicorn.
  unicorn = 0

  # Get input from the user.
  command = ''
  while not command.lower() in ['u', 'd', 'q', 'up', 'down', 'quit']:
    # Read input.
    command = input("\n=====================\n-[ Altitude " + str(altitude) + " feet ]-\n" + name + " " + status(altitude) + ".\n[up,down,quit]: ").lower()

  # Process input.
  modifier = action(command)
  if modifier == 0:
    isGameOver = True
  elif modifier == -1:
    print("What?")
  else:
    if modifier > 0:
      print("You soar into the sky.")
    elif modifier < 0:
      if altitude > 0:
        print("You dive down lower.")
      else:
        print("Your unicorn can't fly into the ground!")

    turns = turns + 1

    unicorn
    # Calculate the amount of NOT to apply to the qubit, based on the percent of the new altitude from the goal.
    frac = (altitude + modifier) / goal
    if frac >= 1:
      # The unicorn is at or beyond the goal, so just invert the 0-qubit to a 1-qubit for 100% of goal.
      # Note: On a real quantum machine the error rate is likely to cause NOT(0) to not go all the way to 1, staying around 1=862 and 0=138, etc.
      unicorn = 1
    elif frac > 0:
      # Apply a percentage of the distance of the unicorn to the goal (0-1), cooresponding to how high the unicorn is.
      unicorn = frac * math.pi

    # Execute on quantum machine.
    counts = random.randint(50, 151) # 50-150
    print(counts)

    # Set the altitude based upon the number of 1 counts in the result.
    altitude = counts

    # Did the player reach the castle?
    if altitude >= goal:
      print('Congratulations! ' + name + ' soars into the castle gates!')
      isGameOver = True
    elif altitude > 0:
      # Check if we should play a mini-game.
      if random.randint(1, 16) > 10:
        # Play the mini-game and then apply a bonus or penalty to altitude.
        altitude = miniGame(altitude)

    if not isGameOver and altitude >= goal:
      print('Congratulations! ' + name + ' soars into the castle gates!')
      isGameOver = True

print("The game ended in " + str(turns) + " rounds. " + ("You won, great job! :)" if altitude >= goal else "Better luck next time. :("))