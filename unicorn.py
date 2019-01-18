#
# Fly Unicorn
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
    backend = qiskit.providers.ibmq.least_busy(qiskit.IBMQ.backends(simulator=False))

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

def oracle(secretProgram, qr, cr, secret):
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
  oracle(guessProgram, qr, cr, secret)

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
  oracle(guessProgram, qr, cr, secret)

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

def miniGame():
  print('An mischievous cloud blocks your way and challenges you to a game!')
  print("If you can guess a magically mystical number before the cloud, you'll be rewarded.\nIf you lose, you'll face a penalty.")

  bonus = 0

  # Read input.
  command = input("Do you want to play his game? [yes,no]: ").lower()
  if command[0] == 'y':
    # Select a random number (returned as an array of bits).
    print("The mischievous cloud blinks his eyes. You hear a crack of thunder. A number has been chosen.")
    secret = random(15)
    secretInt = bitsToInt(secret)
    print("Psst. The secret is " + str(secretInt))

    # Begin the mini-game loop.
    isGuessGameOver = False
    while not isGuessGameOver:
      # Let the player make a guess.
      command = int(input("Guess a number between 0 and 15. [0-15]: "))
      if command == secretInt:
        print("You guessed correct!")
        print("Altitude + 100")
        bonus = 100
        isGuessGameOver = True
      else:
        print("You guessed wrong.")

      # Let the computer make a guess.
      if not isGuessGameOver:
        # The computer's guess is a binary number.
        computerResult = guess(secret)

        print("The mischievous cloud guesses " + str(computerResult) + '.')
        if computerResult == secretInt:
          print("Haha, I win, says the mischievous cloud!")
          print("Altitude - 100")
          bonus = -100
          isGuessGameOver = True

  return bonus

run.isInit = False # Indicate that we need to initialize the IBM Q API in the run() method.
isGameOver = False # Indicates when the game is complete.
altitude = 0 # Current altitude of player. Once goal is reached, the game ends.
goal = 1000 # Max altitude for the player to reach to end the game.
shots = goal + (125 if device == 'real' else 0) # Number of measurements on the quantum machine; when shots == goal, the player reached the goal; we include a buffer on physical quantum computers to account for natural error.
turns = 0 # Total count of turns in the game.

# Generate a random name using a quantum random number generator.
name = getName(randomInt(15)) + ' ' + getName(randomInt(15))

print('===============')
print('  Fly Unicorn')
print('===============')
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
        altitude = altitude + miniGame()
        altitude = altitude if altitude >= 0 else 0

    if not isGameOver and altitude >= goal:
      print('Congratulations! ' + name + ' soars into the castle gates!')
      isGameOver = True

print("The game ended in " + str(turns) + " rounds. Great job!")