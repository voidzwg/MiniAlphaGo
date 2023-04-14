#!/usr/bin/Anaconda3/python
# -*- coding: utf-8 -*-
# MCTS.py

from copy import deepcopy
import random, math

class Node:
    def __init__(self, state, color, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.color = color
        self.children = []
        self.score = 0
        self.visits = 0
    
    def add_child(self):
        if self.is_fully_expanded():
            return None
        possible_actions = list(self.state.get_legal_actions(self.color))
        for child in self.children:
            if child.action in possible_actions:
                possible_actions.remove(child.action)
        action = random.choice(possible_actions)
        child_state = deepcopy(self.state)
        child_state._move(action, self.color)
        child_color = self._opponent()
        if len(list(child_state.get_legal_actions(child_color))) == 0:
            child_color = self.color
        child = Node(child_state, child_color, self, action)
        self.children.append(child)
        return child
    
    def expand(self):
        moves = self.state.get_legal_actions(self.color)
        for move in moves:
            new_board = deepcopy(self.state)
            new_board._move(move, self.color)
            next_color = 'X' if self.color == 'O' else 'O'
            child = Node(new_board, next_color, self, move)
            self.children.append(child)
    
    def update(self, score):
        self.visits += 1
        self.score += score
    
    def is_fully_expanded(self):
        return len(self.children) == len(list(self.state.get_legal_actions(self.color)))
    
    def choose_best_child(self, c):
        return max(self.children, key=lambda x: x.uct_value(c))

    def uct_value(self, c):
        if self.visits == 0:
            return float('inf')
        else:
            return self.score / self.visits + c * math.sqrt(math.log(self.parent.visits) / self.visits)
    
    def rollout_policy_random(self, legal_actions):
        return random.choice(legal_actions)
    
    def _action(self, board, color):
        possible_choice = list(board.get_legal_actions(color))
        if len(possible_choice) != 0:
            return self.rollout_policy_random(possible_choice)
        else:
            return None
    
    def _opponent(self):
        return 'X' if self.color == 'O' else 'O'
    
    def rollout(self):
        """
        采用随机落子的方式模拟
        """
        current_player = self._opponent()
        board = deepcopy(self.state)
        stop = 0
        while True:
            action = self._action(board, current_player)
            if action is not None:
                board._move(action, current_player)
                if stop != 0:
                    stop = 0
                current_player = self._opponent() if current_player == self.color else self.color
            else:
                stop += 1
            if stop == 6:
                break
        
        winner, diff = board.get_winner()
        if winner == 0 and self.color == "X" or winner == 1 and self.color == "O":
            return 1
        else:
            return 0
    
    def backpropagate(self, score):
        node = self
        while node is not None:
            node.update(score)
            node = node.parent

    
class MCTS:
    """
    MonteCarloTreeSearch
    """
    def __init__(self, node, color):
        self.root = node
        self.color = color
    
    def choose_best_action(self, simulation_limit=1000, c=1.414):
        for i in range(simulation_limit):
            leaf = self.select(self.root, c)
            if not (len(list(leaf.state.get_legal_actions('X'))) == 0 \
                and len(list(leaf.state.get_legal_actions('O'))) == 0):
                leaf.expand()
            simulation_result = leaf.rollout()
            leaf.backpropagate(simulation_result)
        return self.root.choose_best_child(c).action
    
    def select(self, node, c):
        while node.children:
            node = node.choose_best_child(c)
        return node
        
    
    def choose_node(self, node, c):
        while node.is_fully_expanded():
            node = node.choose_best_child(c)
        b_list = list(node.state.get_legal_actions('X'))
        w_list = list(node.state.get_legal_actions('O'))
        is_over = len(b_list) == 0 and len(w_list) == 0
        
        if is_over:
            return node
        else:
            return node.add_child()