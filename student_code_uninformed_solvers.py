from solver import *
from queue import Queue


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.init()

    def init(self):
        self.generate_children()

    def generate_children(self):
        movable_actions = self.gm.getMovables()
        for move in movable_actions:
            self.gm.makeMove(move)
            child_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
            if child_state in self.visited:
                self.gm.reverseMove(move)
                continue
            self.currentState.children.append(child_state)
            child_state.parent = self.currentState
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
        # check current state
        self.visited[current_state] = True

        if current_state.state == self.victoryCondition:
            return True

        # if current node still has some children can be visited-visit it
        while current_state.nextChildToVisit < len(current_state.children):
            # get next child
            new_state = current_state.children[current_state.nextChildToVisit]
            current_state.nextChildToVisit += 1
            # not visit, then make move and go to this state
            if new_state not in self.visited:
                self.visited[new_state] = False
                self.gm.makeMove(new_state.requiredMovable)
                self.currentState = new_state
                self.generate_children()
                return False

        # this node does not have children to visit, go back
        if current_state.requiredMovable:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = Queue()
        self.queue.put(self.currentState)
        self.is_init = False

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
            required_moves = self.generate_move_path(target_state)

            for move in required_moves:
                self.gm.makeMove(move)
            # 这个语句的位置也忒精细了吧,搞不好就错了,啧啧啧,受不了
            self.currentState = target_state
            self.visited[target_state] = True
            if target_state.state == self.victoryCondition:
                return True

            movable_actions = self.gm.getMovables()

            for move in movable_actions:
                self.gm.makeMove(move)
                new_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                self.currentState.children.append(new_state)
                new_state.parent = self.currentState

                if new_state in self.visited:
                    self.gm.reverseMove(move)
                    continue
                self.queue.put(new_state)
                self.visited[new_state] = False
                self.gm.reverseMove(move)

    def generate_move_path(self, target_state):
        paths = []
        current_state = target_state
        while current_state.parent:
            move = current_state.requiredMovable
            paths.insert(0, move)
            current_state = current_state.parent
        return paths

    def go_back_to_root(self, ):
        current_state = self.currentState
        while current_state.parent is not None:
            move = current_state.requiredMovable
            self.gm.reverseMove(move)
            current_state = current_state.parent
