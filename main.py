import random
from collections import deque
from functools import partial

commands = [
("mov", +0), #ускорится на speed
("rot", +0), #повернуть на случайный угол
("rep", +0), #размножится
("atk", +0), #атаковать
("eat", +0), #кушать
("sen", +0), #проверить сенсор 0(Столкновение с стеной) если True выполнить следующую инструкцию иначе пропустить
("sen", +1), #проверить сенсор 1(Столкновение с бактерией) если True выполнить следующую инструкцию иначе пропустить
("sen", +2), #проверить сенсор 2(Столкновение с едой) если True выполнить следующую инструкцию иначе пропустить
("mem", +0), #записать в ячейку 0
("mem", +1), #записать в ячейку 1
("mem", +2), #записать в ячейку 2
("mem", +3), #записать в ячейку 3
("mem", +4), #записать в ячейку 4
("mem", +5), #записать в ячейку 5
("mem", +6), #записать в ячейку 6
("mem", +7), #записать в ячейку 7
("mem", +8), #записать в ячейку 8
("mem", +9), #записать в ячейку 9
("mod", +1), #увеличить значение ячейки на 1
("mod", -1), #уменьшить значение ячейки на 1
("set", +0), #выбрать ячейку 0
("set", +1), #выбрать ячейку 1
("set", +2), #выбрать ячейку 2
("inc", -1), #выбрать ячейку назад
("inc", +1), #выбрать следующую ячейку
("ifj", +0), #сравнить значение с 0 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
("ifj", +1), #сравнить значение с 1 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
("ifj", +2), #сравнить значение с 2 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
("ifj", +3), #сравнить значение с 3 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
("ifj", +4), #сравнить значение с 4 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
("ifj", +5), #сравнить значение с 5 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
("ifj", +6), #сравнить значение с 6 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
("ifj", +7), #сравнить значение с 7 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
("ifj", +8), #сравнить значение с 8 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
("ifj", +9), #сравнить значение с 9 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
("jmp", -3), #перепрыгнуть на 3 действия назад
("jmp", -2), #перепрыгнуть на 2 действия назад
("jmp", +2), #перепрыгнуть на 2 действия вперёд
("jmp", +3), #перепрыгнуть на 3 действия вперёд
("slp", +1), #подождать 1 действие
("slp", +2), #подождать 2 действие
("slp", +3), #подождать 3 действие
("non", +0), #существует для отладки и не используется
("gt0", +0), #переместится в начало, не реализован
("gtm", +0), #переместитя на значение переменной, не реализован
]

class Comand_Quet:
    reproduct_shance = 0.01
    __slots__ = ("index", "quet", "lens", "main")
    
    def __init__(self, lens: int, main: "Intelect", quet: None | list = None) -> None:
        self.index = 0 #обозначает какая команда сейчас выбрана
        self.quet = [random.randint(0, len(main.command_handler.command_defs)) for x in range(lens)] if quet is None else quet
        self.lens = lens
        self.main = main
        
    def move(self, number: int) -> None:
        '''перемещает индекс на число, не давая выйти за пределы(зацикленно)'''
        self.index = (self.index + number) % self.lens
        
    def run_command(self) -> None:
        '''исполняет команду которая сейчас выбрана'''
        self.main.command_handler.command_defs[self.quet[self.index]-1](self.main)
        
    def copy(self) -> deque[int]:
        '''копирует список команд с мутациями'''
        if random.random() < 1 - self.reproduct_shance:
            return
        copy = self.quet.copy()
        for x in range(random.randint(1, self.lens//4)):
            copy[random.randint(0, self.lens-1)] = random.randint(0, len(self.main.command_handler.command_defs))
        return copy
        
class Command_Handler:
    __slots__ = ("command_defs", "excluded")
    
    def __init__(self) -> None:
        '''создаёт список команд с их аргументами из большого блока с исключениями'''
        self.excluded = ["non", "gt0", "gtm"] #Исключенные команды
        self.command_defs = [self.generate(func, cod) for func, cod in commands if not(func in self.excluded)]
    
    def generate(self, func_name: str, arg: int) -> partial:
        '''преобразует название команды и её аргумент в python обьект'''
        try:
            res = eval("Command_Handler."+func_name)
            return partial(res, cod=arg)
        except Exception as error:
            return partial(Command_Handler.non, cod=func_name)
        
    @staticmethod
    def non(agent: "Intelect", cod: int) -> None:
        '''Для отладки'''
        print("Отладка или ошибка", f"Ошибка вызвана {cod=}")
        agent.command_quet.move(1)
    
    @staticmethod
    def mov(agent: "Intelect", cod: int) -> None:
        '''добавляет флаг движения'''
        agent.flags.append(1)
        agent.command_quet.move(1)
        
    @staticmethod
    def rot(agent: "Intelect", cod: int) -> None:
        '''добавляет флаг вращения'''
        agent.flags.append(2)
        agent.command_quet.move(1)
        
    @staticmethod
    def rep(agent: "Intelect", cod: int) -> None:
        '''добавляет флаг размножения'''
        agent.flags.append(3)
        agent.command_quet.move(1)
        
    @staticmethod
    def atk(agent: "Intelect", cod: int) -> None:
        '''добавляет флаг атаки'''
        agent.flags.append(4)
        agent.command_quet.move(1)
        
    @staticmethod
    def eat(agent: "Intelect", cod: int) -> None:
        '''добавляет флаг еды'''
        agent.flags.append(5)
        agent.command_quet.move(1)
        
    @staticmethod
    def sen(agent: "Intelect", cod: int) -> None:
        '''команда посмотреть на сенсор'''
        if cod in agent.sensor:
            agent.command_quet.move(1)
        else:
            agent.command_quet.move(2)
            
    @staticmethod
    def mem(agent: "Intelect", cod: int) -> None:
        '''запомнить число в выбраной ячейке памяти'''
        agent.memory[agent.memory_index] = cod
        agent.command_quet.move(1)
        
    @staticmethod
    def mod(agent: "Intelect", cod: int) -> None:
        '''изменить значение в выбранной ячейке в диапазоне 0-9 на -1 или 1'''
        agent.memory[agent.memory_index] = (agent.memory[agent.memory_index] + cod)%10
        agent.command_quet.move(1)
        
    @staticmethod
    def set(agent: "Intelect", cod: int) -> None:
        '''выбрать ячейку памяти'''
        agent.memory_index = cod
        agent.command_quet.move(1)
        
    @staticmethod
    def inc(agent: "Intelect", cod: int) -> None:
        '''выбрать следуйщую или предыдущую ячеййку памяти не выходя за границы'''
        agent.memory_index = (agent.memory_index + cod)%agent.memory_len
        agent.command_quet.move(1)
        
    @staticmethod
    def ifj(agent: "Intelect", cod: int) -> None:
        '''сравнить значение ячейки и cod'''
        if agent.memory[agent.memory_index] == cod:
            agent.command_quet.move(1)
        else:
            agent.command_quet.move(2)
            
    @staticmethod
    def jmp(agent: "Intelect", cod: int) -> None:
        '''перепрыгнуть на несколько комманд назад или вперёд'''
        if agent.recursion == agent.max_loop:
            agent.recursion = -2
            agent.command_quet.move(1)
            return
        if agent.recursion >= 0:
            agent.command_quet.move(cod)
        agent.recursion += 1
        
    @staticmethod
    def slp(agent: "Intelect", cod: int) -> None:
        '''подождать несколько комманд ничего не делая'''
        agent.sleep += cod
        agent.command_quet.move(1)
        
    @staticmethod
    def gt0(agent: "Intelect", cod: int) -> None:
        '''переместится в начало очереди команд'''
        if agent.recursion == agent.max_loop:
            agent.recursion = 0
            agent.command_quet.move(1)
            return
        if agent.recursion >= 0:
            agent.command_quet.index = 0
        agent.recursion += 1

class Intelect:
    __slots__ = ("memory", "memory_len", "sleep", "memory_index", "recursion", "max_loop", "steps", "sensor", "flags", "command_handler", "command_quet")
    
    def __init__(self, memory_len: int, data: None | Comand_Quet = None) -> None:
        self.memory = [0]*memory_len
        self.memory_len = memory_len
        self.sleep = 0
        self.memory_index = 0
        self.recursion = 0
        self.max_loop = 5 #максимальное количество повторений
        self.steps = 0
        self.sensor = deque() #если сработал сенсор добавится число в очередь
        self.flags = deque() #если бактерия хочет совершить действие то добавляет его в очередь на исполнение
        self.command_handler = Command_Handler()
        self.command_quet = Comand_Quet(60, self, data)
        
    def copy(self) -> None:
        '''создаёт копию себя с мутацией'''
        return Intelect(self.memory_len, self.command_quet.copy())
        
    def step(self) -> None:
        '''выполняет шаг симуляции'''
        if random.random() < 0.015 + self.steps/20000:
            self.flags.append(0) #даёт команду смерти
        self.steps += 1
        if self.sleep > 0:
            self.sleep -= 1
            return
        self.command_quet.run_command()
        if self.steps%100==0 and len(self.sensor) > 0:
            self.sensor.pop() #забыть сенсор
        return len(self.flags) > 0 #сообщает есть ли действия на исполнения self.flags

def hand_flags(agent: Intelect) -> None:
    '''обрабатывает действия бактерии'''
    for flag in agent.flags:
        if flag==1:
            #print("move", len(g))
            pass
        elif flag==2:
            #print("rotate", len(g))
            pass
        elif flag==3:
            agents.append(agent.copy())
        elif flag==4:
            #print("attack", len(g))
            pass
        elif flag==5:
            #print("eat", len(g))
            pass
        elif flag==0:
            agents.remove(agent)
            break
        else : 
            agent.flags.clear()

def tick() -> None:
    '''исполняет шаг симуляции для всех бактерий'''
    for agent in agents:
        if agent.step(): 
            hand_flags(agent)


if __name__ == "__main__":
    agents = [Intelect(3) for x in range(200)]
    
    for x in range(30):
        tick()
