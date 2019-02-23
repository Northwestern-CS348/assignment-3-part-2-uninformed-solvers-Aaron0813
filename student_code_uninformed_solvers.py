from solver import *
from queue import Queue


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.generate_children(self.currentState)

    def generate_children(self, current_state):
        moves = self.gm.getMovables()
        for move in moves:
            self.gm.makeMove(move)
            new_state = GameState(self.gm.getGameState(), current_state.depth + 1, move)
            if new_state in self.visited:
                self.gm.reverseMove(move)
                continue
            self.currentState.children.append(new_state)
            new_state.parent = current_state
            # self.visited[new_state] = False
            self.gm.reverseMove(move)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        current_state = self.currentState
        print(current_state.state)
        self.visited[current_state] = True
        if current_state.state == self.victoryCondition:
            return True
        while current_state.nextChildToVisit < len(current_state.children):
            next_state = current_state.children[current_state.nextChildToVisit]
            current_state.nextChildToVisit += 1
            if next_state not in self.visited:
                self.visited[next_state] = False
                self.gm.makeMove(next_state.requiredMovable)
                self.currentState = next_state
                self.generate_children(next_state)
                return False
        if current_state.parent:
            self.gm.reverseMove(current_state.requiredMovable)
            self.currentState = current_state.parent
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.is_init = False
        self.queue = Queue()
        self.queue.put(self.currentState)

    def go_back_to_root(self, ):
        current_state = self.currentState
        print(current_state.state)
        while current_state.parent is not None:
            move = current_state.requiredMovable
            self.gm.reverseMove(move)
            current_state = current_state.parent

    def go_to_next_state(self, target_state):
        moves = []
        current_state = target_state
        while current_state.parent:
            moves.insert(0, current_state.requiredMovable)
            current_state = current_state.parent

        for move in moves:
            self.gm.makeMove(move)

        self.currentState = target_state

    def generate_children(self, current_state):
        moves = self.gm.getMovables()
        for move in moves:
            self.gm.makeMove(move)
            new_state = GameState(self.gm.getGameState(), current_state.depth + 1, move)
            if new_state in self.visited:
                self.gm.reverseMove(move)
                continue
            self.currentState.children.append(new_state)
            new_state.parent = current_state
            self.queue.put(new_state)
            self.visited[new_state] = False
            self.gm.reverseMove(move)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm. --- 有点没看懂

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if not self.is_init:
            self.is_init = True
            self.solveOneStep()
        if self.queue:
            target_state = self.queue.get()
            self.go_back_to_root()
            self.go_to_next_state(target_state)

            current_state = self.currentState
            self.visited[current_state] = True
            if current_state.state == self.victoryCondition:
                return True
            self.generate_children(current_state)
        return False


