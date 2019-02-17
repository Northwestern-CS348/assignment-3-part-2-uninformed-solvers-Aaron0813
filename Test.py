import unittest, inspect
from multiprocessing.pool import ThreadPool
from multiprocessing.context import TimeoutError
from student_code_game_masters import Puzzle8Game


p8 = Puzzle8Game()
p8.read('puzzle8_top_right_empty.txt')
for i in p8.getGameState():
    print(i)
print(p8.getGameState())