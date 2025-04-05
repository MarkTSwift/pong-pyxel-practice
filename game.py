import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

class App:
    def __init__(self):
        self.state = "title"
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="ポン")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if self.state == "title":
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
                self.state = "game"

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
        pyxel.cls(pyxel.COLOR_GREEN)
        self.draw_center_line()

    def draw_center_line(self):
        for y in range(0, SCREEN_HEIGHT, 4):
            pyxel.line(SCREEN_WIDTH // 2, y, SCREEN_WIDTH // 2, y + 1, pyxel.COLOR_WHITE)

App()