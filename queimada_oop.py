import random
import tkinter as tk

LARGURA = 720
ALTURA = 520
TOPO_ARENA = 92
FUNDO_ARENA = 500


class Ball:
    def __init__(self, canvas, x, y, speed, radius=14):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.ids = [
            canvas.create_oval(
                x - 4,
                y - 4,
                x + radius * 2 + 4,
                y + radius * 2 + 4,
                fill="#3b172d",
                outline="",
            ),
            canvas.create_oval(
                x,
                y,
                x + radius * 2,
                y + radius * 2,
                fill="#fb5277",
                outline="#ff9aab",
                width=2,
            ),
            canvas.create_oval(
                x + 5,
                y + 4,
                x + 11,
                y + 10,
                fill="#ffe1e7",
                outline="",
            ),
        ]

    def move(self):
        self.y += self.speed
        for item_id in self.ids:
            self.canvas.move(item_id, 0, self.speed)

    def off_screen(self):
        return self.y > ALTURA

    def center(self):
        return (self.x + self.radius, self.y + self.radius)

    def destroy(self):
        for item_id in self.ids:
            self.canvas.delete(item_id)


class Player:
    def __init__(self, canvas, x, y, width=48, height=34):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.ids = [
            canvas.create_oval(x + 2, y + height - 2, x + width - 2, y + height + 9, fill="#12364a", outline=""),
            canvas.create_rectangle(
                x, y + 5, x + width, y + height, fill="#102f43", outline="#4ce5d2", width=2
            ),
            canvas.create_rectangle(x + 7, y, x + width - 7, y + 8, fill="#4ce5d2", outline=""),
            canvas.create_rectangle(x + 11, y + 14, x + width - 11, y + 20, fill="#c6fff5", outline=""),
            canvas.create_oval(x + 5, y + 16, x + 9, y + 20, fill="#79ffdc", outline=""),
            canvas.create_oval(x + width - 9, y + 16, x + width - 5, y + 20, fill="#79ffdc", outline=""),
        ]

    def move_to(self, x):
        offset = x - self.x
        self.x = x
        for item_id in self.ids:
            self.canvas.move(item_id, offset, 0)

    def bounds(self):
        return (self.x, self.y, self.width, self.height)


class Game:
    def __init__(self, root):
        self.root = root
        root.title("Queimada | Dodge")
        root.resizable(False, False)
        root.configure(bg="#080e1d")

        self.canvas = tk.Canvas(root, width=LARGURA, height=ALTURA, bg="#080e1d", highlightthickness=0)
        self.canvas.pack()

        self.draw_arena()

        self.player_width = 48
        self.player_height = 34
        self.player = Player(
            self.canvas,
            (LARGURA - self.player_width) / 2,
            FUNDO_ARENA - self.player_height,
            self.player_width,
            self.player_height,
        )

        self.left_pressed = False
        self.right_pressed = False

        self.score = 0
        self.balls = []
        self.game_running = True

        self.score_text = self.canvas.create_text(
            LARGURA - 42,
            38,
            text="000",
            fill="#7cf7dc",
            font=("Segoe UI", 25, "bold"),
            anchor="e",
        )
        self.game_over_items = []

        root.bind("<KeyPress>", self.on_key_press)
        root.bind("<KeyRelease>", self.on_key_release)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.reset_game()

    def draw_arena(self):
        self.canvas.create_rectangle(0, 0, LARGURA, 82, fill="#0d1729", outline="")
        self.canvas.create_line(0, 81, LARGURA, 81, fill="#1c2a40", width=2)
        self.canvas.create_text(
            28, 27, text="QUEIMADA", fill="#f3f7ff", font=("Segoe UI", 19, "bold"), anchor="w"
        )
        self.canvas.create_text(
            29, 55, text="DESVIE E SOBREVIVA", fill="#7f91ac", font=("Segoe UI", 9, "bold"), anchor="w"
        )
        self.canvas.create_text(
            LARGURA - 111,
            22,
            text="PONTOS",
            fill="#7f91ac",
            font=("Segoe UI", 9, "bold"),
            anchor="e",
        )
        self.canvas.create_rectangle(
            20, TOPO_ARENA, LARGURA - 20, FUNDO_ARENA, fill="#0b1425", outline="#1c2a40", width=2
        )

        for y in range(TOPO_ARENA + 24, FUNDO_ARENA, 48):
            self.canvas.create_line(22, y, LARGURA - 22, y, fill="#111e32")
        for x in range(68, LARGURA - 20, 72):
            self.canvas.create_line(x, TOPO_ARENA + 2, x, FUNDO_ARENA - 2, fill="#101c2f")

        self.canvas.create_text(
            LARGURA / 2,
            ALTURA - 9,
            text="←  →   MOVER",
            fill="#657792",
            font=("Segoe UI", 9, "bold"),
        )

    def reset_game(self):
        self.game_running = True
        self.score = 0
        for b in self.balls:
            b.destroy()
        self.balls.clear()

        self.player.move_to((LARGURA - self.player_width) / 2)
        self.update_score()

        for item_id in self.game_over_items:
            self.canvas.delete(item_id)
        self.game_over_items.clear()

        self.root.after(900, self.spawn_ball)
        self.root.after(16, self.game_loop)

    def update_score(self):
        self.canvas.itemconfig(self.score_text, text=f"{self.score:03}")

    @staticmethod
    def rect_circle_collision(rect_x, rect_y, rect_w, rect_h, circle_x, circle_y, radius):
        closest_x = max(rect_x, min(circle_x, rect_x + rect_w))
        closest_y = max(rect_y, min(circle_y, rect_y + rect_h))
        dx = circle_x - closest_x
        dy = circle_y - closest_y
        return (dx * dx + dy * dy) <= (radius * radius)

    def end_game(self):
        self.game_running = False
        self.game_over_items = [
            self.canvas.create_rectangle(
                0, TOPO_ARENA, LARGURA, FUNDO_ARENA, fill="#070d18", stipple="gray50", outline=""
            ),
            self.canvas.create_rectangle(
                190, 166, 530, 362, fill="#111d31", outline="#2a3c55", width=2
            ),
            self.canvas.create_rectangle(190, 166, 530, 171, fill="#fb5277", outline=""),
            self.canvas.create_text(
                LARGURA / 2,
                211,
                text="FIM DE JOGO",
                fill="#f5f7ff",
                font=("Segoe UI", 22, "bold"),
            ),
            self.canvas.create_text(
                LARGURA / 2,
                255,
                text=f"Sua pontuação: {self.score:03}",
                fill="#9eafc7",
                font=("Segoe UI", 13),
            ),
            self.canvas.create_rectangle(
                258, 290, 462, 334, fill="#4ce5d2", outline="", tags="restart"
            ),
            self.canvas.create_text(
                LARGURA / 2,
                312,
                text="JOGAR NOVAMENTE",
                fill="#08201f",
                font=("Segoe UI", 10, "bold"),
                tags="restart",
            ),
        ]

    def spawn_ball(self):
        if not self.game_running:
            return
        x = random.randint(24, LARGURA - 24 - 28)
        speed = 15 + random.random() * 3 + self.score * 0.03
        b = Ball(self.canvas, x, TOPO_ARENA, speed)
        self.balls.append(b)
        self.root.after(900, self.spawn_ball)

    def game_loop(self):
        if not self.game_running:
            return

        # movimento
        if self.left_pressed and self.player.x > 22:
            new_x = max(22, self.player.x - 5)
            self.player.move_to(new_x)
        if self.right_pressed and self.player.x < LARGURA - 22 - self.player.width:
            new_x = min(LARGURA - 22 - self.player.width, self.player.x + 5)
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
        if not self.game_running and event.keysym in ("Return", "space"):
            self.reset_game()
            return
        if event.keysym == "Left":
            self.left_pressed = True
        elif event.keysym == "Right":
            self.right_pressed = True

    def on_key_release(self, event):
        if event.keysym == "Left":
            self.left_pressed = False
        elif event.keysym == "Right":
            self.right_pressed = False

    def on_canvas_click(self, event):
        if not self.game_running and 258 <= event.x <= 462 and 290 <= event.y <= 334:
            self.reset_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()