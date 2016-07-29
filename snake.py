from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random
import sys


class SnakeGame(QMainWindow):
    def __init__(self):
        super(SnakeGame, self).__init__()
        self.sboard = Board(self)

        self.statusbar = self.statusBar()
        self.sboard.msg2statusbar[str].connect(self.statusbar.showMessage)

        self.setCentralWidget(self.sboard)
        self.setWindowTitle('Snake')
        self.resize(800, 600)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

        self.sboard.start()
        self.show()


class Board(QFrame):
    msg2statusbar = pyqtSignal(str)
    SPEED = 50
    WIDTHINBLOCKS = 80
    HEIGHTINBLOCKS = 60

    def __init__(self, parent):
        super(Board, self).__init__(parent)
        self.timer = QBasicTimer()
        self.snake = [[5, 10], [5, 11], [5, 12]]
        self.snake2 = [[30, 10], [30, 11], [30, 12]]
        self.current_x_head = self.snake[0][0]
        self.current_y_head = self.snake[0][1]
        self.current_x_head2 = self.snake2[0][0]
        self.current_y_head2 = self.snake2[0][1]
        self.food = []
        self.grow_snake = False
        self.grow_snake2 = False
        self.board = []
        self.direction = 1
        self.direction2 = 1
        self.drop_food()
        self.setFocusPolicy(Qt.StrongFocus)


    def square_width(self):
        return self.contentsRect().width() / Board.WIDTHINBLOCKS

    def square_height(self):
        return self.contentsRect().height() / Board.HEIGHTINBLOCKS

    def start(self):
        self.msg2statusbar.emit(str(len(self.snake) - 2))
        self.msg2statusbar.emit(str(len(self.snake2) - 2))
        self.timer.start(Board.SPEED, self)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter2 = QPainter(self)
        painter_food = QPainter(self)
        rect = self.contentsRect()
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()

        for pos in self.snake:
            self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())
        for pos in self.snake2:
            self.draw_square2(painter2, rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())
        for pos in self.food:
            self.draw_food(painter_food, rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())
            
    def draw_square(self, painter, x, y):
        color = QColor(0, 0, 255, 127)
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)

    def draw_square2(self, painter2, x, y):
        color = QColor(255, 0, 0, 127)
        painter2.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)
        
    def draw_food(self, painter_food, x, y):
        color = QColor(255, 0, 255, 127)
        painter_food.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left:
            if self.direction != 2:
                if self.grow_snake2:
                    self.direction = 2
                else:
                    self.direction = 1
        elif key == Qt.Key_Right:
            if self.direction != 1:
                if self.grow_snake2:
                    self.direction = 1
                else:
                    self.direction = 2
        elif key == Qt.Key_Down:
            if self.direction != 4:
                self.direction = 3
        elif key == Qt.Key_Up:
            if self.direction != 3:
                self.direction = 4
                
        if key == Qt.Key_Q:
            if self.direction2 != 2:
                if self.grow_snake:
                    self.direction2 = 2
                else:
                    self.direction2 = 1
        elif key == Qt.Key_D:
            if self.direction2 != 1:
                if self.grow_snake:
                    self.direction2 = 1
                else:
                    self.direction2 = 2
        elif key == Qt.Key_S:
            if self.direction2 != 4:
                self.direction2 = 3
        elif key == Qt.Key_Z:
            if self.direction2 != 3:
                self.direction2 = 4
        

    def move_snake(self):
        if self.direction == 1:
            self.current_x_head, self.current_y_head = self.current_x_head - 1, self.current_y_head
            if self.current_x_head < 0:
                self.current_x_head = Board.WIDTHINBLOCKS - 1
        if self.direction == 2:
            self.current_x_head, self.current_y_head = self.current_x_head + 1, self.current_y_head
            if self.current_x_head == Board.WIDTHINBLOCKS:
                self.current_x_head = 0
        if self.direction == 3:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head + 1
            if self.current_y_head == Board.HEIGHTINBLOCKS:
                self.current_y_head = 0
        if self.direction == 4:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head - 1
            if self.current_y_head < 0:
                self.current_y_head = Board.HEIGHTINBLOCKS

        head = [self.current_x_head, self.current_y_head]
        self.snake.insert(0, head)
        if len(self.snake)<=120:
            self.msg2statusbar.emit(str(len(self.snake)-2))
        else:
            self.snake.pop()

    def move_snake2(self):
        if self.direction2 == 1:
            self.current_x_head2, self.current_y_head2 = self.current_x_head2 - 1, self.current_y_head2
            if self.current_x_head2 < 0:
                self.current_x_head2 = Board.WIDTHINBLOCKS - 1
        if self.direction2 == 2:
            self.current_x_head2, self.current_y_head2 = self.current_x_head2 + 1, self.current_y_head2
            if self.current_x_head2 == Board.WIDTHINBLOCKS:
                self.current_x_head2 = 0
        if self.direction2 == 3:
            self.current_x_head2, self.current_y_head2 = self.current_x_head2, self.current_y_head2 + 1
            if self.current_y_head2 == Board.HEIGHTINBLOCKS:
                self.current_y_head2 = 0
        if self.direction2 == 4:
            self.current_x_head2, self.current_y_head2 = self.current_x_head2, self.current_y_head2 - 1
            if self.current_y_head2 < 0:
                self.current_y_head2 = Board.HEIGHTINBLOCKS

        head2 = [self.current_x_head2, self.current_y_head2]
        self.snake2.insert(0, head2)
        if len(self.snake2)<=120:
            self.msg2statusbar.emit(str(len(self.snake2)-2))
        else:
            self.snake2.pop()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.move_snake()
            self.move_snake2()
            self.is_food_collision()
            self.is_suicide()
            self.update()

    def is_suicide(self):
        for i in range(1, len(self.snake)):
            if ((self.snake[i] == self.snake[0]) | (self.snake[0] == self.snake2[i])):
                self.msg2statusbar.emit(str("Player 2 win"))
                self.snake = [[x, y] for x in range(0, 81) for y in range(0, 61)]
                self.timer.stop()
                self.update()

        for i in range(1, len(self.snake2)):
            if ((self.snake2[i] == self.snake2[0]) | (self.snake2[0] == self.snake[i])):
                self.msg2statusbar.emit(str("Player 1 win"))
                self.snake2 = [[x, y] for x in range(0, 81) for y in range(0, 61)]
                self.timer.stop()
                self.update()

    def is_food_collision(self):
        for pos in self.food:
            if pos == self.snake[0]:
                self.food.remove(pos)
                self.grow_snake = True
                
            elif pos == self.snake2[0]:
                self.food.remove(pos)
                self.grow_snake2 = True

    def drop_food(self):
        x = random.randint(3, 58)
        y = random.randint(3, 38)
        
        for pos in self.snake: 
            if pos == [x, y]:
                self.drop_food()

        for pos in self.snake2: 
            if pos == [x, y]:
                self.drop_food()
                
        self.food.append([x, y])


def main():
    app = QApplication([])
    launch_game = SnakeGame()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
