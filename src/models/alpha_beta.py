import chess
import copy


class AlphaBeta:
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
        self.counts = 0

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

    def alpha_beta(self, depth, alpha, beta, maximize):
        self.counts += 1
        if self.board.is_checkmate():
            if self.board.turn == chess.WHITE:
                return -10000
            else:
                return 10000
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0
        if depth == 0:
            return self.eval()
        legals = self.board.legal_moves
        if maximize:
            best_value = -99999
            for move in legals:
                self.board.push(move)
                best_value = max(
                    best_value, self.alpha_beta(depth - 1, alpha, beta, not maximize)
                )
                self.board.pop()
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    return best_value
            return best_value
        else:
            best_value = 99999
            for move in legals:
                self.board.push(move)
                best_value = min(
                    best_value, self.alpha_beta(depth - 1, alpha, beta, not maximize)
                )
                self.board.pop()
                beta = min(beta, best_value)
                if beta <= alpha:
                    return best_value
            return best_value

    def get_next_move(self, depth, maximize):
        legals = self.board.legal_moves
        best_move = None
        best_value = -9999
        if not maximize:
            best_value = 9999
        for move in legals:
            self.board.push(move)
            value = self.alpha_beta(depth - 1, -10000, 10000, not maximize)
            self.board.pop()
            if maximize:
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
        self.board.push(best_move)
        return best_move, best_value, self.counts
