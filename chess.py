from abc import ABC, abstractmethod
import copy

class Move:
    def __init__(self, start_row, start_col, end_row, end_col, piece_moved=None, piece_captured=None, en_passant= False):
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.piece_moved = piece_moved
        self.piece_captured = piece_captured
        self.en_passant = en_passant

class Piece(ABC):
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col

    @abstractmethod
    def get_moves(self, board):
        pass

    def is_enemy(self, other):
        return other and self.color != other.color

class Pawn(Piece):
    def get_moves(self, board):
        moves = []
        direction = 1 if self.color=="white" else -1
        r = self.row + direction
        c = self.col

        if 0 <= r < 8 and board.grid[r][c] is None:
            moves.append(Move(self.row, self.col, r, c))
            
            if (self.color=="white" and self.row==1) or (self.color=="black" and self.row==6):
                r2 = r + direction
                if 0 <= r2 < 8 and board.grid[r2][c] is None:
                    moves.append(Move(self.row, self.col, r2, c))

        for dc in [-1,1]:
            nc = c+dc
            if 0<=nc<8:
                target = board.grid[r][nc]
                if target and self.is_enemy(target):
                    moves.append(Move(self.row, self.col, r, nc))

        if board.en_passant_target:  
            er, ec = board.en_passant_target  
            if r == er and abs(c - ec) == 1:  
                moves.append(Move(self.row, self.col, er, ec, en_passant=True)) 
        return moves

class Rook(Piece):
    def get_moves(self, board):
        moves = []
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        for dr,dc in directions:
            r,c = self.row+dr, self.col+dc
            while 0<=r<8 and 0<=c<8:
                target = board.grid[r][c]
                if target is None:
                    moves.append(Move(self.row,self.col,r,c))
                elif self.is_enemy(target):
                    moves.append(Move(self.row,self.col,r,c))
                    break
                else:
                    break
                r+=dr
                c+=dc
        return moves

class Knight(Piece):
    def get_moves(self, board):
        moves=[]
        for dr,dc in [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
            r,c = self.row+dr, self.col+dc
            if 0<=r<8 and 0<=c<8:
                target = board.grid[r][c]
                if target is None or self.is_enemy(target):
                    moves.append(Move(self.row,self.col,r,c))
        return moves

class Pawshop(Piece):
    def get_moves(self,board):
        moves = []
        for dr,dc in [(1,1),(-1,-1),(-1,1),(1,-1)]:
            r,c = self.row + dr, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.grid[r][c]
                if target is None or self.is_enemy(target):
                    moves.append(Move(self.row,self.col,r,c))
        return moves

class Dumb(Piece):  # не ходит никуда
    def get_moves(self, board):
        return []  # статичная фигура

class Grasshopper(Piece):  # ходит как король на 2 клетки, может перепрыгивать фигуры
    def get_moves(self, board):
        moves = []
        for dr in [-2, 0, 2]:
            for dc in [-2, 0, 2]:
                if dr == 0 and dc == 0:
                    continue
                r = self.row + dr
                c = self.col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = board.grid[r][c]
                    # перепрыгивает через фигуры, поэтому не проверяем промежуточные клетки
                    if target is None or self.is_enemy(target):
                        moves.append(Move(self.row, self.col, r, c))
        return moves
    
class Bishop(Piece):
    def get_moves(self, board):
        moves=[]
        for dr,dc in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            r,c=self.row+dr,self.col+dc
            while 0<=r<8 and 0<=c<8:
                target=board.grid[r][c]
                if target is None:
                    moves.append(Move(self.row,self.col,r,c))
                elif self.is_enemy(target):
                    moves.append(Move(self.row,self.col,r,c))
                    break
                else:
                    break
                r+=dr
                c+=dc
        return moves

class Queen(Piece):
    def get_moves(self, board):
        return Rook(self.color,self.row,self.col).get_moves(board) + \
               Bishop(self.color,self.row,self.col).get_moves(board)

class King(Piece):
    def get_moves(self, board):
        moves=[]
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr==0 and dc==0:
                    continue
                r,c=self.row+dr,self.col+dc
                if 0<=r<8 and 0<=c<8:
                    target=board.grid[r][c]
                    if target is None or self.is_enemy(target):
                        moves.append(Move(self.row,self.col,r,c))
        return moves

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup()
        self.en_passant_target = None

    def setup(self):
        self.grid[0] = [Rook("white",0,0),Knight("white",0,1),Bishop("white",0,2),
                        Queen("white",0,3),King("white",0,4),Bishop("white",0,5),
                        Knight("white",0,6),Rook("white",0,7)]
        self.grid[1] = [
            Dumb("white",1,0),  
            Pawn("white",1,1),
            Pawn("white",1,2),
            Pawn("white",1,3),
            Pawn("white",1,4),
            Pawn("white",1,5),
            Pawshop("white",1,6),
            Grasshopper("white",1,7)
        ]
        self.grid[7] = [Rook("black",7,0),Knight("black",7,1),Bishop("black",7,2),
                        Queen("black",7,3),King("black",7,4),Bishop("black",7,5),
                        Knight("black",7,6),Rook("black",7,7)]
        self.grid[6] = [
            Dumb("black",6,0), 
            Pawn("black",6,1),
            Pawn("black",6,2),
            Pawn("black",6,3),
            Pawn("black",6,4),
            Pawn("black",6,5),
            Pawshop("black",6,6),
            Grasshopper("black",6,7)
        ]

    def move_piece(self, move):
        piece = self.grid[move.start_row][move.start_col]
        move.piece_moved = piece
        if move.en_passant:
            direction = 1 if piece.color=="white" else -1  
            captured_row = move.end_row - direction  
            move.piece_captured = self.grid[captured_row][move.end_col]  
            self.grid[captured_row][move.end_col] = None  
        else:
            move.piece_captured = self.grid[move.end_row][move.end_col]
        self.grid[move.end_row][move.end_col]=piece
        self.grid[move.start_row][move.start_col]=None
        piece.row=move.end_row
        piece.col=move.end_col
        self.en_passant_target = None 
        if isinstance(piece, Pawn) and abs(move.start_row - move.end_row) == 2: 
            middle_row = (move.start_row + move.end_row) // 2 
            self.en_passant_target = (middle_row, move.start_col)

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "white"
        self.move_history = []
    def legal_moves(self, piece):
        moves = []
        for move in piece.get_moves(self.board):
            board_copy = copy.deepcopy(self.board)
            board_copy.move_piece(move)
            if not self.is_check(piece.color, board_copy):
                moves.append(move)
        return moves
    
    def threatened_squares(self, color):
        """Возвращает список координат фигур color, которые находятся под угрозой"""
        enemy_color = "black" if color == "white" else "white"
        threatened = set()
        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece and piece.color == enemy_color:
                    for move in piece.get_moves(self.board):
                        target = self.board.grid[move.end_row][move.end_col]
                        if target and target.color == color:
                            threatened.add((move.end_row, move.end_col))
        return threatened

    def make_move(self, move):
        self.board.move_piece(move)
        self.move_history.append(copy.deepcopy(move))
        piece = move.piece_moved
        if isinstance(piece, Pawn):
            last_row = 7 if piece.color == "white" else 0
            if piece.row == last_row:
                while True:
                    print("Пешка достигла края доски. В какую фигуру хотите превратиться? (R, N, B, Q, W, G, D)")
                    choice = input().strip().upper()
                    new_piece = None
                    if choice == "R":
                        new_piece = Rook(piece.color, piece.row, piece.col)
                    elif choice == "N":
                        new_piece = Knight(piece.color, piece.row, piece.col)
                    elif choice == "B":
                        new_piece = Bishop(piece.color, piece.row, piece.col)
                    elif choice == "Q":
                        new_piece = Queen(piece.color, piece.row, piece.col)
                    elif choice == "W":
                        new_piece = Pawshop(piece.color, piece.row, piece.col)
                    elif choice == "G":
                        new_piece = Grasshopper(piece.color, piece.row, piece.col)
                    elif choice == "D":
                        new_piece = Dumb(piece.color, piece.row, piece.col)

                    if new_piece:
                        self.board.grid[piece.row][piece.col] = new_piece
                        print(f"Пешка превращена в {choice}")
                        break
                    print("Некорректный выбор, попробуйте снова")
        self.turn="black" if self.turn=="white" else "white"

    def undo(self, n=1):
        for _ in range(n):
            if not self.move_history:
                break
            last_move = self.move_history.pop()
            self.board.grid[last_move.start_row][last_move.start_col]=last_move.piece_moved
            self.board.grid[last_move.end_row][last_move.end_col]=last_move.piece_captured
            last_move.piece_moved.row=last_move.start_row
            last_move.piece_moved.col=last_move.start_col
            self.turn="black" if self.turn=="white" else "white"

    def is_check(self, color, board=None):
        if board is None:
            board=self.board
        king=None
        for r in range(8):
            for c in range(8):
                piece=board.grid[r][c]
                if isinstance(piece, King) and piece.color==color:
                    king=piece
        if king is None:
            return False
        for r in range(8):
            for c in range(8):
                piece=board.grid[r][c]
                if piece and piece.color!=color:
                    for move in piece.get_moves(board):
                        if move.end_row==king.row and move.end_col==king.col:
                            return True
        return False

def print_board(board):
    print("  a b c d e f g h")
    for r in range(7,-1,-1):
        row=[]
        for c in range(8):
            piece=board.grid[r][c]
            if piece is None:
                row.append("·")
            else:
                symbol={"white": {"Pawn":"P","Rook":"R","Knight":"N","Bishop":"B","Queen":"Q","King":"K","Pawshop":"W","Dumb":"D","Grasshopper":"G"},
                        "black": {"Pawn":"p","Rook":"r","Knight":"n","Bishop":"b","Queen":"q","King":"k","Pawshop":"w","Dumb":"d","Grasshopper":"g"}}[piece.color][piece.__class__.__name__]
                row.append(symbol)
        print(r+1," ".join(row),r+1)
    print("  a b c d e f g h")

def coords_to_alg(row, col):
    return chr(ord('a')+col)+str(row+1)

def alg_to_coords(s):
    col=ord(s[0])-ord('a')
    row=int(s[1])-1
    return row,col

game=Game()

while True:
    print_board(game.board)
    print(f"Ход {game.turn}")
    threatened = game.threatened_squares(game.turn)
    if threatened:
        print("Фигуры под угрозой:", " ".join([coords_to_alg(r, c) for r, c in threatened]))

    movable_pieces=[]
    for r in range(8):
        for c in range(8):
            piece=game.board.grid[r][c]
            if piece and piece.color==game.turn:
                if game.legal_moves(piece):
                    movable_pieces.append(piece)

    if not movable_pieces:
        if game.is_check(game.turn):
            print(f"Мат! Победили {'black' if game.turn=='white' else 'white'}")
        else:
            print("Пат")
        break
    elif game.is_check(game.turn):
        print("Шах")

    print("Выберите фигуру для хода:")
    print(" ".join([coords_to_alg(p.row,p.col) for p in movable_pieces]))

    while True:
        start_input=input()
        if start_input=="undo":
            print("На сколько ходов откатить?")
            n=int(input())
            game.undo(n)
            break
        r1,c1=alg_to_coords(start_input)
        piece=game.board.grid[r1][c1]
        if piece in movable_pieces:
            break
        print("Неверная фигура, выберите снова:")

    if start_input=="undo":
        continue

    moves=game.legal_moves(piece)
    print("Выберите поле на которое хотите походить:")
    print(" ".join([coords_to_alg(m.end_row,m.end_col) for m in moves]))

    while True:
        end_input=input()
        r2,c2=alg_to_coords(end_input)
        move=next((m for m in moves if m.end_row==r2 and m.end_col==c2), None)
        if move:
            break
        print("Недопустимый ход, выберите снова:")

    game.make_move(move)

    enemy="black" if game.turn=="white" else "white"
    if game.is_check(enemy):
        print(f"{enemy} под шахом")