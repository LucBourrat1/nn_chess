import chess
import copy


class MiniMax:
    def __init__(self, board):
        self.board = copy.deepcopy(board)
        self.pieceSquareTable = [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20, 0, 0, 0, 0, -20, -40],
            [-30, 0, 10, 15, 15, 10, 0, -30],
            [-30, 5, 15, 20, 20, 15, 5, -30],
            [-30, 0, 15, 20, 20, 15, 0, -30],
            [-30, 5, 10, 15, 15, 10, 5, -30],
            [-40, -20, 0, 5, 5, 0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50],
        ]

    def eval(self):
        scoreWhite = 0
        scoreBlack = 0
        for i in range(0, 8):
            for j in range(0, 8):
                squareIJ = chess.square(i, j)
                pieceIJ = self.board.piece_at(squareIJ)
                if str(pieceIJ) == "P":
                    scoreWhite += 100 + self.pieceSquareTable[i][j]
                if str(pieceIJ) == "N":
                    scoreWhite += 310 + self.pieceSquareTable[i][j]
                if str(pieceIJ) == "B":
                    scoreWhite += 320 + self.pieceSquareTable[i][j]
                if str(pieceIJ) == "R":
                    scoreWhite += 500 + self.pieceSquareTable[i][j]
                if str(pieceIJ) == "Q":
                    scoreWhite += 900 + self.pieceSquareTable[i][j]
                if str(pieceIJ) == "p":
                    scoreBlack += 100 + self.pieceSquareTable[i][j]
                if str(pieceIJ) == "n":
                    scoreBlack += 310 + self.pieceSquareTable[i][j]
                if str(pieceIJ) == "b":
                    scoreBlack += 320 + self.pieceSquareTable[i][j]
                if str(pieceIJ) == "r":
                    scoreBlack += 500 + self.pieceSquareTable[i][j]
                if str(pieceIJ) == "q":
                    scoreBlack += 900 + self.pieceSquareTable[i][j]
        return scoreWhite - scoreBlack

    def minimax(self, depth, maximize):
        if self.board.is_checkmate():
            if self.board.turn == chess.WHITE:
                return -10000
            else:
                return 10000
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0
        if depth == 0:
            return self.eval()
        if maximize:
            best_value = -99999
            for move in self.board.legal_moves:
                self.board.push(move)
                best_value = max(best_value, self.minimax(depth - 1, not maximize))
                self.board.pop()
            return best_value
        else:
            best_value = 99999
            for move in self.board.legal_moves:
                self.board.push(move)
                best_value = min(best_value, self.minimax(depth - 1, maximize))
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
            value = self.minimax(depth - 1, not maximize)
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
