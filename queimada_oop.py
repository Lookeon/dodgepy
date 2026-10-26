import random
import tkinter as tk

LARGURA = 600
ALTURA = 400


class Ball:
    def __init__(self, canvas, x, y, speed, radius=15, color="#ef4444", outline="#b91c1c"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.id = canvas.create_oval(x, y, x + radius * 2, y + radius * 2, fill=color, outline=outline)

    def move(self):
        self.y += self.speed
        self.canvas.move(self.id, 0, self.speed)

    def off_screen(self):
        return self.y > ALTURA

    def center(self):
        return (self.x + self.radius, self.y + self.radius)

    def destroy(self):
        try:
            self.canvas.delete(self.id)
        except tk.TclError:
            pass


class Player:
    def __init__(self, canvas, x, y, width=40, height=40, color="#22c55e", outline="#14532d"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id = canvas.create_rectangle(x, y, x + width, y + height, fill=color, outline=outline, width=2)

    def move_to(self, x):
        self.x = x
        self.canvas.coords(self.id, self.x, self.y, self.x + self.width, self.y + self.height)

    def bounds(self):
        return (self.x, self.y, self.width, self.height)


class Game:
    def __init__(self, root):
        self.root = root
        root.title("Queimada (OOP)")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=LARGURA, height=ALTURA, bg="#0f172a", highlightthickness=0)
        self.canvas.pack()

        self.score_label = tk.Label(root, text="Pontuação: 0", font=("Arial", 18), fg="white", bg="#111827")
        self.score_label.pack(pady=(5, 0))

        self.player_width = 40
        self.player_height = 40
        self.player = Player(self.canvas, 280, 340, self.player_width, self.player_height)

        self.left_pressed = False
        self.right_pressed = False

        self.score = 0
        self.balls = []
        self.game_running = True

        self.game_over_text = None
        self.final_score_text = None
        self.restart_button = None

        root.bind("<KeyPress>", self.on_key_press)
        root.bind("<KeyRelease>", self.on_key_release)

        self.reset_game()

    def reset_game(self):
        self.game_running = True
        self.score = 0
        for b in self.balls:
            b.destroy()
        self.balls.clear()

        self.player.move_to(280)
        self.update_score()

        if self.game_over_text is not None:
            self.canvas.delete(self.game_over_text)
            self.game_over_text = None
        if self.final_score_text is not None:
            self.canvas.delete(self.final_score_text)
            self.final_score_text = None
        if self.restart_button is not None:
            self.restart_button.destroy()
            self.restart_button = None

        self.root.after(900, self.spawn_ball)
        self.root.after(16, self.game_loop)

    def update_score(self):
        self.score_label.config(text=f"Pontuação: {self.score}")

    @staticmethod
    def rect_circle_collision(rect_x, rect_y, rect_w, rect_h, circle_x, circle_y, radius):
        closest_x = max(rect_x, min(circle_x, rect_x + rect_w))
        closest_y = max(rect_y, min(circle_y, rect_y + rect_h))
        dx = circle_x - closest_x
        dy = circle_y - closest_y
        return (dx * dx + dy * dy) <= (radius * radius)

    def end_game(self):
        self.game_running = False
        self.game_over_text = self.canvas.create_text(
            LARGURA / 2,
            120,
            text="Fim de jogo",
            fill="white",
            font=("Arial", 28, "bold"),
        )
        self.final_score_text = self.canvas.create_text(
            LARGURA / 2,
            170,
            text=f"Pontuação final: {self.score}",
            fill="white",
            font=("Arial", 20),
        )

        self.restart_button = tk.Button(
            self.root,
            text="Jogar novamente",
            command=self.reset_game,
            font=("Arial", 12, "bold"),
            bg="#f59e0b",
            fg="#111827",
            padx=18,
            pady=8,
        )
        self.restart_button.pack(pady=(10, 0))

    def spawn_ball(self):
        if not self.game_running:
            return
        x = random.randint(0, LARGURA - 30)
        speed = 15 + random.random() * 3 + self.score * 0.03
        b = Ball(self.canvas, x, 0, speed)
        self.balls.append(b)
        self.root.after(900, self.spawn_ball)

    def game_loop(self):
        if not self.game_running:
            return

        # movimento
        if self.left_pressed and self.player.x > 0:
            new_x = max(0, self.player.x - 5)
            self.player.move_to(new_x)
        if self.right_pressed and self.player.x < LARGURA - self.player.width:
            new_x = min(LARGURA - self.player.width, self.player.x + 5)
            self.player.move_to(new_x)

        # bolas
        for b in list(self.balls):
            b.move()
            cx, cy = b.center()
            rx, ry, rw, rh = self.player.bounds()
            if self.rect_circle_collision(rx, ry, rw, rh, cx, cy, b.radius):
                self.end_game()
                return
            if b.off_screen():
                b.destroy()
                try:
                    self.balls.remove(b)
                except ValueError:
                    pass
                self.score += 1
                self.update_score()

        self.root.after(16, self.game_loop)

    def on_key_press(self, event):
        if event.keysym == "Left":
            self.left_pressed = True
        elif event.keysym == "Right":
            self.right_pressed = True

    def on_key_release(self, event):
        if event.keysym == "Left":
            self.left_pressed = False
        elif event.keysym == "Right":
            self.right_pressed = False


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()