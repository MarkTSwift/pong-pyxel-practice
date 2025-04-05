import pyxel

pyxel.init(160, 120, title="Hello Pyxel")

def update():
    pass

def draw():
    pyxel.cls(0)
    pyxel.text(50, 60, "Hello, Pyxel!", 7)

pyxel.run(update, draw)