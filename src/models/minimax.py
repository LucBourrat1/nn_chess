import chess


class MiniMax:
    def __init__(self, board):
        self.board = board

    def minimax(self, depth, maximize):
        if self.board.is_checkmate():
            if self.board.turn == chess.WHITE:
                return -10000
            else:
                return 10000
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0
        if maximize:
            best_value = -99999
            for move in self.board.legal_moves:
                self.board.push(move)
                best_value = max(
                    best_value, self.minimax(self.board, depth - 1, not maximize)
                )
                self.board.pop()
            return best_value
        else:
            best_value = 99999
            for move in self.board.legal_moves:
                self.board.push(move)
                best_value = min(
                    best_value, self.minimax(self.board, depth - 1, maximize)
                )
                self.board.pop()
            return best_value

    def get_next_move(self, depth, maximize):
        legals = self.board.legal_moves
        best_move = None
        best_value = -99999
        if not maximize:
            best_value = 99999
        for move in legals:
            self.board.push(move)
            value = self.minimax(self.board, depth - 1, not maximize)
            self.board.pop()
            if maximize:
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
        return (best_move, best_value)
