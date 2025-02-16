import math
import random
import re
from collections import deque
from functools import partial

commands = """
mov +0, ускорится на speed
rot +0, повернуть на случайный угол
rep +0, размножится
atk +0, атаковать
eat +0, кушать
sen +0, проверить сенсор 0(Столкновение с стеной) если True выполнить следующую инструкцию иначе пропустить
sen +1, проверить сенсор 1(Столкновение с бактерией) если True выполнить следующую инструкцию иначе пропустить
sen +2, проверить сенсор 2(Столкновение с едой) если True выполнить следующую инструкцию иначе пропустить
mem +0, записать в ячейку 0
mem +1, записать в ячейку 1
mem +2, записать в ячейку 2
mem +3, записать в ячейку 3
mem +4, записать в ячейку 4
mem +5, записать в ячейку 5
mem +6, записать в ячейку 6
mem +7, записать в ячейку 7
mem +8, записать в ячейку 8
mem +9, записать в ячейку 9
mod +1, увеличить значение ячейки на 1
mod -1, уменьшить значение ячейки на 1
set +0, выбрать ячейку 0
set +1, выбрать ячейку 1
set +2, выбрать ячейку 2
inc -1, выбрать ячейку назад
inc +1, выбрать следующую ячейку
ifj +0, сравнить значение с 0 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
ifj +1, сравнить значение с 1 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
ifj +2, сравнить значение с 2 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
ifj +3, сравнить значение с 3 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
ifj +4, сравнить значение с 4 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
ifj +5, сравнить значение с 5 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
ifj +6, сравнить значение с 6 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
ifj +7, сравнить значение с 7 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
ifj +8, сравнить значение с 8 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
ifj +9, сравнить значение с 9 и выполнить следуещее действие, иначе перепрыгнуть на 1 действие
jmp -3, перепрыгнуть на 3 действия назад
jmp -2, перепрыгнуть на 2 действия назад
jmp +2, перепрыгнуть на 2 действия вперёд
jmp +3, перепрыгнуть на 3 действия вперёд
slp +1, подождать 1 действие
slp +2, подождать 2 действие
slp +3, подождать 3 действие

"""
#gt0 +0, переместится в начало
#gtm +0, переместится 

class Comand_Quet:
    reproduct_shance = 0.01
    
    def __init__(self, lens, main:"Intelect", quet: None | list = None):
        self.index = 0
        self.quet = [random.randint(0, len(main.command_handler.command_defs)) for x in range(lens)] if quet is None else quet
        self.lens = lens
        self.main = main
        
    def move(self, number):
        self.index = (self.index + number) % self.lens
        
    def run_command(self):
        self.main.command_handler.command_defs[self.quet[self.index]-1](self.main)
        
    def copy(self):
        if random.random() < 1 - self.reproduct_shance:
            return
        copy = self.quet.copy()
        for x in range(random.randint(1, self.lens//4)):
            copy[random.randint(0, self.lens-1)] = random.randint(0, len(self.main.command_handler.command_defs))
        return copy
        
class Command_Handler:
    
    def __init__(self):
        self.command_defs = [self.generate(match.group(1), int(match.group(2))) for match in re.finditer(r"(\w+)\s*([+-]\d+)", commands)]
    
    def generate(self, func_name, arg):
        try:
            res = eval("Command_Handler."+func_name)
            return partial(res, cod=arg)
        except Exception as s:
            return lambda: -1
    
    @staticmethod
    def mov(agent:"Intelect", cod):
        agent.flags.append(1)
        agent.command_quet.move(1)
        
    @staticmethod
    def rot(agent:"Intelect", cod):
        agent.flags.append(2)
        agent.command_quet.move(1)
        
    @staticmethod
    def rep(agent:"Intelect", cod):
        agent.flags.append(3)
        agent.command_quet.move(1)
        
    @staticmethod
    def atk(agent:"Intelect", cod):
        agent.flags.append(4)
        agent.command_quet.move(1)
        
    @staticmethod
    def eat(agent:"Intelect", cod):
        agent.flags.append(5)
        agent.command_quet.move(1)
        
    @staticmethod
    def sen(agent:"Intelect", cod):
        if agent.sensor[cod]:
            agent.command_quet.move(1)
        else:
            agent.command_quet.move(2)
            
    @staticmethod
    def mem(agent:"Intelect", cod):
        agent.memory[agent.memory_index] = cod
        agent.command_quet.move(1)
        
    @staticmethod
    def mod(agent:"Intelect", cod):
        agent.memory[agent.memory_index] = (agent.memory[agent.memory_index] + cod)%10
        agent.command_quet.move(1)
        
    @staticmethod
    def set(agent:"Intelect", cod):
        agent.memory_index = cod
        agent.command_quet.move(1)
        
    @staticmethod
    def inc(agent:"Intelect", cod):
        agent.memory_index = (agent.memory_index + cod)%agent.memory_len
        agent.command_quet.move(1)
        
    @staticmethod
    def ifj(agent:"Intelect", cod):
        if agent.memory[agent.memory_index] == cod:
            agent.command_quet.move(1)
        else:
            agent.command_quet.move(2)
            
    @staticmethod
    def jmp(agent:"Intelect", cod):
        if agent.recursion == agent.max_loop:
            agent.recursion = -2
            agent.command_quet.move(1)
            return
        if agent.recursion >= 0:
            agent.command_quet.move(cod)
        agent.recursion += 1
        
    @staticmethod
    def slp(agent:"Intelect", cod):
        agent.sleep += cod
        agent.command_quet.move(1)
        
    @staticmethod
    def gt0(agent:"Intelect", cod):
        if agent.recursion == self.max_loop:
            agent.recursion = 0
            agent.command_quet.move(1)
            return
        if agent.recursion >= 0:
            agent.command_quet.index = 0
        agent.recursion += 1

class Intelect:
    
    def __init__(self, memory_len, data: None | Comand_Quet = None):
        self.memory = [0]*memory_len
        self.memory_len = memory_len
        self.sleep = 0
        self.memory_index = 0
        self.recursion = 0
        self.max_loop = 5
        self.steps = 0
        self.sensor = [False, False, False]
        self.flags = deque()
        self.command_handler = Command_Handler()
        self.command_quet = Comand_Quet(60, self, data)
        
    def copy(self):
        return Intelect(self.memory_len, self.command_quet.copy())
        
    def step(self):
        if random.random() < 0.015 + self.steps/20000:
            self.flags.append(0)
        self.steps += 1
        if self.sleep > 0:
            self.sleep -= 1
            return
        self.command_quet.run_command()
        return len(self.flags) > 0

def hand_flags(f):
    for flag in f.flags:
        if flag==1:
            #print("move", len(g))
            pass
        elif flag==2:
            #print("rotate", len(g))
            pass
        elif flag==3:
            g.append(f.copy())
        elif flag==4:
            #print("attack", len(g))
            pass
        elif flag==5:
            #print("eat", len(g))
            pass
        elif flag==0:
            g.remove(f)
            break
        else : 
            f.flags.clear()

def tick():
    for f in g:
        if f.step(): 
            hand_flags(f)


if __name__ == "__main__":
    parse_func = [(match.group(1), int(match.group(2))) for match in re.finditer(r"(\w+)\s*([+-]\d+)", commands)]
    g = [Intelect(3) for x in range(200)]
    
    for x in range(30):
        tick()

#print({hex(i):(x.split()[0],int(x.split()[1])) for i,x in enumerate(filter(lambda x: x != "", [x[:6] for x in commands.split("\n")]))})


