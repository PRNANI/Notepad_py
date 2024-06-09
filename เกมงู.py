import tkinter as tk
import random

# กำหนดค่าสำหรับเกม
WIDTH = 600
HEIGHT = 400
SQUARE_SIZE = 20
DELAY = 150  # เพิ่มค่า DELAY เพื่อลดความเร็วของงู

class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food = self.create_food()
        self.score = 0

        self.bind("<KeyPress>", self.change_direction)

        self.delay = DELAY
        self.game_over = False
        self.paused = False

        self.update()

    def create_food(self):
        x = random.randint(0, (WIDTH-SQUARE_SIZE) // SQUARE_SIZE) * SQUARE_SIZE
        y = random.randint(0, (HEIGHT-SQUARE_SIZE) // SQUARE_SIZE) * SQUARE_SIZE
        return self.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill="red")

    def move(self):
        if not self.paused:
            head_x, head_y = self.snake[0]

            if self.direction == "Left":
                new_head = (head_x - SQUARE_SIZE, head_y)
            elif self.direction == "Right":
                new_head = (head_x + SQUARE_SIZE, head_y)
            elif self.direction == "Up":
                new_head = (head_x, head_y - SQUARE_SIZE)
            elif self.direction == "Down":
                new_head = (head_x, head_y + SQUARE_SIZE)

            self.snake.insert(0, new_head)

            if self.check_collision():
                self.game_over = True
                return

            if new_head == (self.canvas.coords(self.food)[0], self.canvas.coords(self.food)[1]):
                self.score += 1
                self.canvas.delete(self.food)
                self.food = self.create_food()
            else:
                self.canvas.delete(self.snake.pop())

            for segment in self.snake:
                self.canvas.create_rectangle(segment[0], segment[1], segment[0] + SQUARE_SIZE, segment[1] + SQUARE_SIZE, fill="green")

            self.after(self.delay, self.move)

    def check_collision(self):
        head_x, head_y = self.snake[0]

        return (
            head_x < 0 or
            head_y < 0 or
            head_x >= WIDTH or
            head_y >= HEIGHT or
            (head_x, head_y) in self.snake[1:]
        )

    def change_direction(self, event):
        if event.keysym in ["Left", "Right", "Up", "Down"]:
            new_direction = event.keysym
            opposite_directions = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}

            if new_direction != opposite_directions[self.direction]:
                self.direction = new_direction
                self.paused = False  # แก้ไขตรงนี้เพื่อให้งูเคลื่อนที่ได้เมื่อมีการกดปุ่มเพียงครั้งเท่านั้น

    def update(self):
        if not self.game_over:
            self.move()
            self.title(f"Snake | Score: {self.score}")
            self.after(100, self.update)
        else:
            self.canvas.create_text(WIDTH/2, HEIGHT/2, text=f"Game Over! Your Score: {self.score}", fill="white", font=("Helvetica", 24))

if __name__ == "__main__":
    game = SnakeGame()
    game.mainloop()

