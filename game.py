import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

LEFT_PADDLE_SPEED = 4
RIGHT_PADDLE_SPEED = 3

class App:
    def __init__(self):
        self.state = "title"
        self.left_paddle_y = SCREEN_HEIGHT // 2 - 10
        self.right_paddle_y = SCREEN_HEIGHT // 2 - 10

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="ポン")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if self.state == "title":
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
                self.state = "game"

        elif self.state == "game":
            # 左側のパドル
            if pyxel.btn(pyxel.KEY_W):
                self.left_paddle_y -= LEFT_PADDLE_SPEED
            if pyxel.btn(pyxel.KEY_S):
                self.left_paddle_y += LEFT_PADDLE_SPEED

            # 画面外に出ないように制限
            self.left_paddle_y = max(0, min(SCREEN_HEIGHT - 20, self.left_paddle_y))

            # 左側のパドル
            if pyxel.btn(pyxel.KEY_UP):
                self.right_paddle_y -= RIGHT_PADDLE_SPEED
            if pyxel.btn(pyxel.KEY_DOWN):
                self.right_paddle_y += RIGHT_PADDLE_SPEED

            # 画面外に出ないように制限
            self.right_paddle_y = max(0, min(SCREEN_HEIGHT - 20, self.right_paddle_y))

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        if self.state == "title":
            self.draw_title_screen()
        elif self.state == "game":
            self.draw_game_screen()

    def draw_title_screen(self):
        pyxel.cls(pyxel.COLOR_GREEN)
        pyxel.text(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2, "PONG!", pyxel.COLOR_YELLOW)
        pyxel.text(SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT - 15, "Made by: Mark T Swift", pyxel.COLOR_LIGHT_BLUE)

    def draw_game_screen(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        self.draw_center_line()

        # 左側のバーを描画
        pyxel.rect(10, self.left_paddle_y, 4, 20, pyxel.COLOR_WHITE)
        # 右側のバーを描画
        pyxel.rect(SCREEN_WIDTH - 14, self.right_paddle_y, 4, 20, pyxel.COLOR_WHITE)

    def draw_center_line(self):
        for y in range(0, SCREEN_HEIGHT, 4):
            pyxel.line(SCREEN_WIDTH // 2, y, SCREEN_WIDTH // 2, y + 1, pyxel.COLOR_WHITE)

App()