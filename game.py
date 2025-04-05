import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="ポン")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

    def draw(self):
        pyxel.cls(pyxel.COLOR_GREEN)
        pyxel.text(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2, "PONG!", pyxel.COLOR_YELLOW)

App()