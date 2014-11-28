import RPi.GPIO as GPIO
import time
import csv  # Exporting and importing cracked aps
import os  # File management
GPIO.setmode(GPIO.BCM)

# software Settings
debug = False
wheelSpeed = 1
pauseBetweenLetters = 1.5
sequence = [0,'a','b','c','d','e','f','g'] #can contain chars or step positions


# physical settings
letterCount = 95
fullturnSteps = 1600
dirPin = 2
stepPin = 3
ledPin = 4
invertedDir = True


# internal / calculated
stepsPerLetter = fullturnSteps / letterCount
currentStep = 0
direction = 1
startTime = time.time()
totalSteps = 0

# GPIO setup.
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(stepPin, 0)
GPIO.output(ledPin, 0)


# rotates the wheel according to the given sequence
def playSequence(seq):
    for letter in seq:
		gotoLetter(letter)
		GPIO.output(ledPin, 1)
		time.sleep(pauseBetweenLetters)
		GPIO.output(ledPin, 0)


# advances one step in the current direction
def step():
	global wheelSpeed, stepPin, direction, currentStep
	GPIO.output(stepPin, 1)
	GPIO.output(stepPin, 0)
	time.sleep(wheelSpeed / 1000.0)
	currentStep += direction
	currentStep = currentStep%fullturnSteps
	if(debug == True):
		print("currentStep: " + str(currentStep))


# advances by the given number of steps in the current direction
def move(steps):
	global totalSteps
	if steps > 0:
		setDirection(1)
	else:
		setDirection(-1)
	for i in range(0, abs(steps)):
		step()
	totalSteps += steps


# goto given step (using current direction)
def moveTo(targetStep):
	global currentStep
	while(currentStep % fullturnSteps != targetStep):
		step()


# goto given letter, using the current direction, then reverse direction
def gotoLetter(letter):
	global stepsPerLetter, direction
	if type(letter) is int:
		moveTo(letter)
	elif(len(letter) > 1):
		moveTo(int(letter) * stepsPerLetter)
	else:
		moveTo((ord(letter) - 32) * stepsPerLetter)
	direction = -1 * direction
	setDirPin()

# set direction to -1 or 1
def setDirection(dir):
	global direction
	direction = int(min(max(dir, -1), 1))
	setDirPin()
	# if(debug == True):
		# print("direction: " + str(direction))

def setDirPin():
	if(invertedDir == False):
		GPIO.output(dirPin, max(0,direction))
	else:
		GPIO.output(dirPin, 1-max(0,direction))	

# calibration process
def calibrate():
	global currentStep
	done = 'notDone'
	while done == 'notDone':
		done = commandReader(raw_input("calibrate ('h' for help): "))
	currentStep = 0
	print('\ncalibration done.\n')


# recording new sequence (and saving it)
def recordSequence():
	global sequence
	done = 'notDone'
	newSequence = []
	while done != 'exit':
		done = commandReader(raw_input("rotate wheel by... (h for help): "))
		if(done == 'done'):
			print("added one position to sequence: " + str(currentStep))
			newSequence.append(currentStep)
	if(len(newSequence) > 0):
		filename = raw_input("save this sequence as: ")
		if(len(filename) > 0):
			savedFile = open(filename + '.csv', 'w')
			savedFile.write(str(newSequence))
			savedFile.close()
		sequence = newSequence
	print("new sequence: " + str(sequence))


# reads and executes user commands
def commandReader(command):
	try:
		command = int(command)
		move(command)
		return 'notDone'
	except:
		if command == 'h':
			print("\n- Use the commands below to adjust the wheel position:")
			print("\t'q': -1  |  'Q': -10\n\t'w': +1  |  'W': +10\n\t x : +x  |  -x : -x")
			print("\t'e': exit")
			print("\t<_|: validate the position\n")
		elif command == 'q':
			move(-1)
		elif command == 'w':
			move(1)
		elif command == 'Q':
			move(-10)
		elif command == 'W':
			move(10)
		elif command == '':
			return 'done'
		elif command == 'e':
			return 'exit'
		else:
			print("wrong command")
		return 'notDone'

def load_cracked(self):
    result = []
    if not os.path.exists('cracked.csv'): return result
    with open('cracked.csv', 'rb') as csvfile:
        targetreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in targetreader:
            result.append(row)
            sequence.append(0) # 'id' char
            sequence.append(list(row[1]))
            sequence.append(17) # 'pw' char
            sequence.append(list(row[3]))
    return result

setDirPin()
# os.system("/home/pi/wifite.py -all -wep &")

# main loop
try:
	print('\n')
	calibrate()
	if(raw_input("record new sequence? (y/n)") == "y"):
		recordSequence()
	if(raw_input("load cracked? (y/n)") == "y"):
		print(load_cracked())

	while True:
		playSequence(sequence)

# program end
except KeyboardInterrupt:
	print("\n\nprogram exited\n")
except Exception, e:
	print("\n\nprogram crashed\n#############################\n" + str(e) + "\n#############################\n")
finally:
	print("gpio cleaned")
	GPIO.cleanup()
