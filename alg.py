#1 
class Board:
    def __init__(self):
        self.field = [[' ' for i in range(3)] for i in range(3)]
        self.prev_turn = 1
    def display(self):
        for i in self.field:
            print(*i, sep = '|')
            print('-'*5)
    def make_move(self,i,j,sign):
        self.display()
        flag = 0
        if self.prev_turn != sign and self.field[i] == ' ':
            self.field[i][j]= sign
            self.prev_turn = sign
            if self.field[i][j] == self.field[i][(j+1)%3] == self.field[i][(j+2)%3]:
                flag = 1
            elif self.field[i][j] == self.field[(i+1)%3][j] == self.field[(i+2)%3][j]:
                flag = 1
            elif i == j and self.field[i][j] == self.field[(i+1)%3][(j+1)%3] == self.field[(i+2)%3][(j+2)%3]:
                flag = 1
            if flag == 1:
                return "win"
            else:
                return "move completed"





