# Dependency injection
# Я добавил промежуточный менеджер CleanerBotManager, который напрямую работает функциональным ядром.
# CleanerBotManager инжектится в CleanerBot. CleanerBot - вызывает специально сконфигурированные для него методы
# менеджера. С помощью CleanerBotManager можно менять реальзацию методов и функциональное ядро, без изменений CleanerBot
# Плюсы:
# Может быть много различных реализаций менеджеров, это позволит более гибко настраивать бота
# Минусы:
# Дополнительная абстракция и усложнение кода
import pure_robot


class CleanerBotManager:
    def __init__(self):
        self.__state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

    def get_status(self):
        return f"Clean: {self.__state.state}\nAngle: {self.__state.angle}\nPos X: {self.__state.x}\nPos Y: {self.__state.y}"

    def make(self, program):
        self.__state = pure_robot.make(
            pure_robot.transfer_to_cleaner,
            program,
            self.__state
        )


class CleanerBot:
    def __init__(self, manager: CleanerBotManager):
        self.bot_manager = manager

    def make(self, program):
        self.bot_manager.make(program)

    def get_status(self):
        print(self.bot_manager.get_status())


bot = CleanerBot(CleanerBotManager())

bot.make([
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
])

bot.get_status()
