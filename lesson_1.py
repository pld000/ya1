class CleanerBot:
    cleaningState = None

    def move(self, distance):
        print(f"POS {distance}")

    def turn(self, angle):
        print(f"ANGLE {angle}")

    def setCleaningState(self, state):
        self.cleaningState = state
        print(f"STATE {state}")

    def start(self):
        print(f"START WITH {self.cleaningState}")

    def stop(self):
        print("STOP")

    def getCleaningState(self):
        return self.cleaningState


def activateCleanerBot(cleanerBot: CleanerBot):
    return {
        'move': cleanerBot.move,
        'turn': cleanerBot.turn,
        'set': cleanerBot.setCleaningState,
        'start': cleanerBot.start,
        'stop': cleanerBot.stop
    }

bot = activateCleanerBot(CleanerBot())
while True:
    commands = input("Commands: ").split(',')
    for command in commands:
        command_name, _, param = command.strip().partition(' ')
        if command_name == "exit" or command_name == "quit" or command_name == "q":
            break

        if command_name == 'stop' or command_name == "start":
            bot[command_name]()
        else:
            bot[command_name](param)



