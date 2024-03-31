import chess
import copy
import math
from chess import Board
import random


class TreeNode:
    def __init__(self, board: Board):
        self.M = 0
        self.V = 0
        self.visited_moves_and_nodes = []
        self.non_visited_legal_moves = []
        self.board = board
        self.parent = None
        for m in self.board.legal_moves:
            self.non_visited_legal_moves.append(m)

    def is_mcts_leaf_node(self):
        return len(self.non_visited_legal_moves) != 0

    def is_terminal_node(self):
        return (
            len(self.non_visited_legal_moves) == 0
            and len(self.visited_moves_and_nodes) == 0
        )


class Mcts:
    def __init__(self, board: chess.Board, player):
        self.board = copy.deepcopy(board)
        self.player = player
        self.opponent = chess.BLACK if self.player == chess.WHITE else chess.WHITE

    def uct_value(self, node, parent):
        val = node.M + 1.4142 * math.sqrt(math.log(parent.V) / node.V)
        return val

    def select(self, node: TreeNode):
        if node.is_mcts_leaf_node() or node.is_terminal_node():
            return node
        else:
            max_uct_child = None
            max_uct_value = -1000000.0
            for move, child in node.visited_moves_and_nodes:
                uct_val_child = self.uct_value(child, node)
                if uct_val_child > max_uct_value:
                    max_uct_child = child
                    max_uct_value = uct_val_child
            if max_uct_child == None:
                raise ValueError("could not identify child with best uct value")
            else:
                return self.select(max_uct_child)

    def expand(self, node: TreeNode):
        move_to_expand = node.non_visited_legal_moves.pop()
        board = node.board.copy()
        board.push(move_to_expand)
        child_node = TreeNode(board)
        child_node.parent = node
        node.visited_moves_and_nodes.append((move_to_expand, child_node))
        return child_node

    def simulate(self, node: TreeNode):
        board = node.board.copy()
        while board.outcome(claim_draw=True) == None:
            ls = []
            for m in board.legal_moves:
                ls.append(m)
            move = random.choice(ls)
            board.push(move)
        payout = 0.5  # TODO check if correct initialisation
        o = board.outcome(claim_draw=True)
        if o.winner == self.player:
            payout = 1
        if o.winner == self.opponent:
            payout = 0.5  # TODO should be 0 here for loss?
        if o.winner == None:
            payout = 0  # TODO should be 0.5 here for draw?
        return payout

    def backpropagate(self, node: TreeNode, payout):
        node.M = ((node.M * node.V) + payout) / (node.V + 1)
        node.V = node.V + 1
        if node.parent != None:
            return self.backpropagate(node.parent, payout)

    def get_next_moves(self, n_iter):
        root = TreeNode(self.board)
        for i in range(0, n_iter):
            node = self.select(root)
            if not node.is_terminal_node():
                node = self.expand(node)
            payout = self.simulate(node)
            self.backpropagate(node, payout)
        root.visited_moves_and_nodes.sort(key=lambda x: x[1].V, reverse=True)
        print(
            [
                (m.uci(), child.M, child.V)
                for m, child in root.visited_moves_and_nodes[:10]
            ]
        )
