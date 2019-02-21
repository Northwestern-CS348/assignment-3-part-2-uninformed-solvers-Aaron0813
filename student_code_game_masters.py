from game_master import GameMaster
from read import *
from util import *
import read


class TowerOfHanoiGame(GameMaster):
    def __init__(self):
        super().__init__()
        # use list to store states
        # self.states = [[] for i in range(3)]

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        # use ask to get state
        asks = []
        asks.append(read.parse_input("fact: (on ?disk peg1)"))
        asks.append(read.parse_input("fact: (on ?disk peg2)"))
        asks.append(read.parse_input("fact: (on ?disk peg3)"))
        answers = []
        for i in asks:
            answers.append(self.kb.kb_ask(i))

        tuples = []
        for num in range(len(answers)):
            if answers[num]:
                temp_list = []
                for i in answers[num]:
                    for j in i.bindings:
                        temp_list.append(int(str(j.constant)[-1:]))
                temp_list.sort()
                tuples.append(tuple(temp_list))
            else:
                tuples.append(tuple())
        return (tuple(tuples))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### delete obj in previous peg, add it to current peg
        ### movable disk1 peg1 peg2
        print("\n\n================")
        sl = movable_statement.terms
        print("Term " + str(sl))
        # print(sl)
        pre_fact = Fact(["on", sl[0], sl[1]])
        next_fact = Fact(["on", sl[0], sl[2]])

        # step 1: remove previous fact
        #  disk1 could be
        #  (1) the only one on peg1, -- add empty fact and retract Top fact
        #  (2) or just the top of peg1 -- retract Top fact, and change the disk below it to be top
        self.kb.kb_retract(pre_fact)
        self.kb.kb_retract(Fact(["top", sl[0], sl[1]]))

        ask_fact = Fact(["on", "?disk", sl[1]])
        answer = self.ask_sort(ask_fact)

        if answer:
            for a in answer:
                # print(type(a))
                print(a)
            # print(type(answer[0]))
            # print("answer = " + str((answer[0].bindings[0]).constant))
            # print(type(sl[1]))
            inferred_fact = Fact(["top", answer[0], sl[1]])
            print("inferred_fact = " + str(inferred_fact.statement))
            self.kb.kb_assert(inferred_fact)
        else:
            inferred_fact = Fact(["empty", sl[1]])
            print("inferred_fact = " + str(inferred_fact.statement))
            self.kb.kb_assert(inferred_fact)

        # step 2: add next fact
        #  peg2 could be
        #  (1) empty previous --  retract empty fact and add Top fact
        #  (2) has other disks -- retract previous Top fact, and and add Top fact
        ask_fact = Fact(["on", "?disk", sl[2]])
        answer = self.ask_sort(ask_fact)
        if answer:
            for a in answer:
                # print(type(a))
                print(a)
            inferred_fact = Fact(["top", answer[0], sl[2]])
            print("inferred_fact = " + str(inferred_fact.statement))
            self.kb.kb_retract(inferred_fact)
        else:
            inferred_fact = Fact(["empty", sl[2]])
            self.kb.kb_retract(inferred_fact)

        self.kb.kb_assert(next_fact)
        self.kb.kb_assert(Fact(["top", sl[0], sl[2]]))

    def ask_sort(self, fact):
        answers = self.kb.kb_ask(fact)
        sorted_ans = []
        if answers:
            for a in answers:
                sorted_ans.append(str(a.bindings[0].constant))
            sorted_ans.sort()
            return sorted_ans
        else:
            return False

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))


class Puzzle8Game(GameMaster):
    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input(
            'fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        # 如果没有,结果为false,就可以标注为empty
        ### Student code goes here
        asks = []
        # fact: (location tile1 pos1 pos1)
        ask = []
        ask.append(read.parse_input("fact: (location ?tile pos1 pos1)"))
        ask.append(read.parse_input("fact: (location ?tile pos1 pos2)"))
        ask.append(read.parse_input("fact: (location ?tile pos1 pos3)"))
        asks.append(ask)

        ask = []
        ask.append(read.parse_input("fact: (location ?tile pos2 pos1)"))
        ask.append(read.parse_input("fact: (location ?tile pos2 pos2)"))
        ask.append(read.parse_input("fact: (location ?tile pos2 pos3)"))
        asks.append(ask)

        ask = []
        ask.append(read.parse_input("fact: (location ?tile pos3 pos1)"))
        ask.append(read.parse_input("fact: (location ?tile pos3 pos2)"))
        ask.append(read.parse_input("fact: (location ?tile pos3 pos3)"))
        asks.append(ask)

        # for j in asks:
        #     for i in j:
        #         print(i)

        return asks
        # asks.append(read.parse_input("fact: (on ?disk peg2)"))
        # asks.append(read.parse_input("fact: (on ?disk peg3)"))
        # answers = []
        # for i in asks:
        #     answers.append(self.kb.kb_ask(i))

        # tuples = []
        # for num in range(len(answers)):
        #     if answers[num]:
        #         temp_list = []
        #         for i in answers[num]:
        #             for j in i.bindings:
        #                 temp_list.append(int(str(j.constant)[-1:]))
        #         temp_list.sort()
        #         tuples.append(tuple(temp_list))
        #     else:
        #         tuples.append(tuple())
        # return (tuple(tuples))
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
