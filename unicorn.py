#
# Flying Unicorn
# A simple quantum game where the player has to fly a unicorn to the castle.
#

import math
import qiskit
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import IBMQ
import numpy as np
import operator
import time
import ast
from configparser import RawConfigParser
from randomint import random, randomInt, bitsToInt

# Selects the environment to run the game on: simulator or real
device = 'real';

def run(program, type, shots = 100):
  if type == 'real':
    if not run.isInit:
        # Setup the API key for the real quantum computer.
        parser = RawConfigParser()
        parser.read('config.ini')

        # Read configuration values.
        proxies = ast.literal_eval(parser.get('IBM', 'proxies')) if parser.has_option('IBM', 'proxies') else None
        verify = (True if parser.get('IBM', 'verify') == 'True' else False) if parser.has_option('IBM', 'verify') else True
        token = parser.get('IBM', 'key')

        IBMQ.enable_account(token = token, proxies = proxies, verify = verify)
        run.isInit = True

    # Set the backend server.
    provider = IBMQ.get_provider()
    backend = provider.get_backend('ibmq_qasm_simulator')
    #backend = qiskit.providers.ibmq.least_busy(qiskit.IBMQ.backends(simulator=False))

    # Execute the program on the quantum machine.
    print("Running on", backend.name())
    start = time.time()
    job = qiskit.execute(program, backend)
    result = job.result().get_counts()
    stop = time.time()
    print("Request completed in " + str(round((stop - start) / 60, 2)) + "m " + str(round((stop - start) % 60, 2)) + "s")
    return result
  else:
    # Execute the program in the simulator.
    print("Running on the simulator.")
    start = time.time()
    job = qiskit.execute(program, qiskit.Aer.get_backend('qasm_simulator'), shots=shots)
    result = job.result().get_counts()
    stop = time.time()
    print("Request completed in " + str(round((stop - start) / 60, 2)) + "m " + str(round((stop - start) % 60, 2)) + "s")
    return result

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

def oracle(secretProgram, qr, secret):
  # Convert the list of 1's and 0's in secret into an array.
  secret = np.asarray(secret)

  # Find all bits with a value of 0.
  indices = np.where(secret == 0)[0]

  # Invert the bits associated with a value of 0.
  for i in range(len(indices)):
    # We want to read bits, starting with the right-most value as index 0.
    index = int(len(secret) - 1 - indices[i])
    # Invert the qubit.
    secretProgram.x(qr[index])

def guess(secret):
  # Apply 4-bit Grover's search to identify a target array of bits amongst all combinations of bits in 1 program execution.
  # Create 2 qubits for the input array.
  qr = QuantumRegister(4)
  # Create 2 registers for the output.
  cr = ClassicalRegister(4)
  guessProgram = QuantumCircuit(qr, cr)

  # Place the qubits into superposition to represent all possible values.
  guessProgram.h(qr)

  # Run oracle on key. Invert the 0-value bits.
  oracle(guessProgram, qr, secret)

  # Apply Grover's algorithm with a triple controlled Pauli Z-gate (cccZ).
  guessProgram.cu1(np.pi / 4, qr[0], qr[3])
  guessProgram.cx(qr[0], qr[1])
  guessProgram.cu1(-np.pi / 4, qr[1], qr[3])
  guessProgram.cx(qr[0], qr[1])
  guessProgram.cu1(np.pi/4, qr[1], qr[3])
  guessProgram.cx(qr[1], qr[2])
  guessProgram.cu1(-np.pi/4, qr[2], qr[3])
  guessProgram.cx(qr[0], qr[2])
  guessProgram.cu1(np.pi/4, qr[2], qr[3])
  guessProgram.cx(qr[1], qr[2])
  guessProgram.cu1(-np.pi/4, qr[2], qr[3])
  guessProgram.cx(qr[0], qr[2])
  guessProgram.cu1(np.pi/4, qr[2], qr[3])

  # Reverse the inversions by the oracle.
  oracle(guessProgram, qr, secret)

  # Amplification.
  guessProgram.h(qr)
  guessProgram.x(qr)

  # Apply Grover's algorithm with a triple controlled Pauli Z-gate (cccZ).
  guessProgram.cu1(np.pi/4, qr[0], qr[3])
  guessProgram.cx(qr[0], qr[1])
  guessProgram.cu1(-np.pi/4, qr[1], qr[3])
  guessProgram.cx(qr[0], qr[1])
  guessProgram.cu1(np.pi/4, qr[1], qr[3])
  guessProgram.cx(qr[1], qr[2])
  guessProgram.cu1(-np.pi/4, qr[2], qr[3])
  guessProgram.cx(qr[0], qr[2])
  guessProgram.cu1(np.pi/4, qr[2], qr[3])
  guessProgram.cx(qr[1], qr[2])
  guessProgram.cu1(-np.pi/4, qr[2], qr[3])
  guessProgram.cx(qr[0], qr[2])
  guessProgram.cu1(np.pi/4, qr[2], qr[3])

  # Reverse the amplification.
  guessProgram.x(qr)
  guessProgram.h(qr)

  # Measure the result.
  guessProgram.barrier(qr)
  guessProgram.measure(qr, cr)

  # Obtain a measurement and check if it matches the password (without error).
  results = run(guessProgram, device)
  print(results)
  answer = max(results.items(), key=operator.itemgetter(1))[0]

  # Convert the binary number to an array of characters.
  arrResult = list(answer)
  # Convert the array of characters to an array of integers (1's and 0's).
  arrResultInt = [int(i) for i in arrResult]
  # Convert the result to an integer.
  return bitsToInt(arrResultInt)

def miniGame(altitude):
  print("\n=====================\n-[ Altitude " + str(altitude) + " feet ]-\nA mischievous quantum cloud blocks your way and challenges you to a game!")
  print("He has stolen a magical unicorn jewel from the castle!\nIf you can guess which jewel is the real one before the cloud, you'll be rewarded.\nIf you lose, you'll face a penalty.")

  bonus = 0

  # Read input.
  command = input("Do you want to play his game? [yes,no]: ").lower()
  if command[0] == 'y':
    # Select a random number (returned as an array of bits).
    print("The mischievous cloud blinks his eyes. You hear a crack of thunder. A unicorn jewel has been chosen.")
    secret = random(15) # 1-14
    secretInt = bitsToInt(secret)
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
        # The computer's guess is a binary number from the total 1-14 range. Thew quantum player doesn't need an advantage of range to make it easier!
        computerResult = guess(secret)

        # Convert the search result index into a jewel name within the selected range.
        computerJewelIndex = computerResult - low + 1

        print("The mischievous cloud guesses " + getJewel(computerJewelIndex) + '.')
        if computerResult == secretInt:
          print("Haha, I win, says the mischievous cloud!\nDon't say I didn't warn you! After all, I live in the quantum world! =)")
          print("Altitude - 100")
          bonus = -100
          isGuessGameOver = True

  # Return the new altitude + bonus (or penalty).
  return (altitude + bonus) if (altitude + bonus) >= 0 else 0

run.isInit = False # Indicate that we need to initialize the IBM Q API in the run() method.
isGameOver = False # Indicates when the game is complete.
altitude = 0 # Current altitude of player. Once goal is reached, the game ends.
errorBuffer = (0 if device == 'real' else 0) # Amount to add to measurements on real quantum computer to account for error rate, otherwise player can never reach goal due to measurement error even at 100% invert of qubit.
goal = 1024 - errorBuffer # Max altitude for the player to reach to end the game.
shots = goal + errorBuffer # Number of measurements on the quantum machine; when shots == goal, the player reached the goal; we include a buffer on physical quantum computers to account for natural error.
turns = 0 # Total count of turns in the game.

# Generate a random name using a quantum random number generator.
name = getName(randomInt(15)) + ' ' + getName(randomInt(15))

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
  # Setup a qubit to represent the unicorn.
  unicorn = QuantumRegister(1)
  unicornClassic = ClassicalRegister(1)
  program = QuantumCircuit(unicorn, unicornClassic);

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

    # Calculate the amount of NOT to apply to the qubit, based on the percent of the new altitude from the goal.
    frac = (altitude + modifier) / goal
    if frac >= 1:
      # The unicorn is at or beyond the goal, so just invert the 0-qubit to a 1-qubit for 100% of goal.
      # Note: On a real quantum machine the error rate is likely to cause NOT(0) to not go all the way to 1, staying around 1=862 and 0=138, etc.
      program.x(unicorn)
    elif frac > 0:
      # Apply a percentage of the NOT operator to the unicorn (qubit), cooresponding to how high the unicorn is.
      program.u3(frac * math.pi, 0.0, 0.0, unicorn)

    # Collapse the qubit superposition by measuring it, forcing it to a value of 0 or 1.
    program.measure(unicorn, unicornClassic);

    # Execute on quantum machine.
    counts = run(program, device, shots)
    print(counts)

    # Set the altitude based upon the number of 1 counts in the quantum results.
    altitude = counts['1'] if '1' in counts else 0

    # Did the player reach the castle?
    if altitude >= goal:
      print('Congratulations! ' + name + ' soars into the castle gates!')
      isGameOver = True
    elif altitude > 0:
      # Check if we should play a mini-game.
      if randomInt(15) > 10:
        # Play the mini-game and then apply a bonus or penalty to altitude.
        altitude = miniGame(altitude)

    if not isGameOver and altitude >= goal:
      print('Congratulations! ' + name + ' soars into the castle gates!')
      isGameOver = True

print("The game ended in " + str(turns) + " rounds. " + ("You won, great job! :)" if altitude >= goal else "Better luck next time. :("))
