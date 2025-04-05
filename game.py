import pyxel
import random

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

LEFT_PADDLE_SPEED = 4
RIGHT_PADDLE_SPEED = 3

LEFT_MATCH_POINT = 10
RIGHT_MATCH_POINT = 10

def is_colliding(ax, ay, aw, ah, bx, by, bw, bh):
    return (
        ax < bx + bw and
        ax + aw > bx and
        ay < by + bh and
        ay + ah > by
    )

class App:
    def __init__(self):
        self.state = "title"
        self.left_paddle_y = SCREEN_HEIGHT // 2 - 10
        self.right_paddle_y = SCREEN_HEIGHT // 2 - 10

        self.score_left = 0
        self.score_right = 0

        # ボール
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_dx = 1  # 横移動速度
        self.ball_dy = 1  # 縦移動速度

        self.winner = None

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

            # ボールが左の壁を越えた（右側の得点）
            if self.ball_x < 0:
                self.score_right += 1
                self.reset_ball()

            # ボールが右の壁を越えた（左側の得点）
            if self.ball_x > SCREEN_WIDTH:
                self.score_left += 1
                self.reset_ball       ()

            #勝利判定
            if self.score_left >= LEFT_MATCH_POINT:
                self.winner = "left"
                self.state = "result"

            if self.score_right >= RIGHT_MATCH_POINT:
                self.winner = "right"
                self.state = "result"

        elif self.state == "result":
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SHIFT):
                self.reset_game()
                self.state = "game"

        # ボールの移動
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # 上下の壁にぶつかったら跳ね返る
        if self.ball_y <= 0 or self.ball_y >= SCREEN_HEIGHT - 4:
            self.ball_dy *= -1

        # ボールのサイズ
        paddle_width = 4
        ball_size = 4
        paddle_height = 20

        # 左パドルとの当たり判定
        paddle_top = self.left_paddle_y
        paddle_bottom = self.left_paddle_y + paddle_height
        paddle_center = (paddle_top + paddle_bottom) // 2

        if is_colliding(self.ball_x, self.ball_y, ball_size, ball_size,
                        10, self.left_paddle_y, paddle_width, paddle_height):
            self.ball_dx = abs(self.ball_dx)  # 右に跳ね返す
            # 当たった位置でdyを変化させる
            if self.ball_y < paddle_top + 5:
                self.ball_dy -= 1
            elif self.ball_y > paddle_bottom - 5:
                self.ball_dy += 1
            else:
                # 中央ヒット！スピードアップ！
                self.ball_dx *= 1.05
                self.ball_dx = min(self.ball_dx, 5)
            self.ball_dy = max(-3, min(3, self.ball_dy))  # 上限を制限

        # 右パドルとの当たり判定
        paddle_top = self.right_paddle_y
        paddle_bottom = self.right_paddle_y + paddle_height
        paddle_center = (paddle_top + paddle_bottom) // 2

        if is_colliding(self.ball_x, self.ball_y, ball_size, ball_size,
                        SCREEN_WIDTH - 14, self.right_paddle_y, paddle_width, paddle_height):
            self.ball_dx = -abs(self.ball_dx)  # 左に跳ね返す

            if self.ball_y < paddle_top + 5:
                self.ball_dy -= 1
            elif self.ball_y > paddle_bottom - 5:
                self.ball_dy += 1
            else:
                # 中央ヒット！スピードアップ！
                self.ball_dx *= 1.05
                self.ball_dx = min(self.ball_dx, 5)
            self.ball_dy = max(-3, min(3, self.ball_dy))  # 上限を制限

    def reset_ball(self):
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_dx = 2 * (-1 if pyxel.rndi(0, 1) == 0 else 1)  # ランダムな左右方向
        self.ball_dy = pyxel.rndi(-2, 2)

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        if self.state == "title":
            self.draw_title_screen()
        elif self.state == "game":
            self.draw_game_screen()
        elif self.state == "result":
            self.draw_result_screen()

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

        # ボールの描画（4x4ピクセルの白い四角）
        pyxel.rect(self.ball_x, self.ball_y, 4, 4, pyxel.COLOR_RED)

        score_text = f"{self.score_left}      {self.score_right}"
        pyxel.text(SCREEN_WIDTH // 2 - len(score_text) * 2, 10, score_text, pyxel.COLOR_YELLOW)

    def draw_center_line(self):
        for y in range(0, SCREEN_HEIGHT, 4):
            pyxel.line(SCREEN_WIDTH // 2, y, SCREEN_WIDTH // 2, y + 1, pyxel.COLOR_WHITE)

    def draw_result_screen(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)

        if self.winner == "left":
            lines = ["LEFT", "WIN"]
        else:
            lines = ["RIGHT", "WIN"]

        for i, text in enumerate(lines):
            pyxel.text(SCREEN_WIDTH // 2 - len(text) * 2, 50 + i * 10, text, pyxel.COLOR_WHITE)

        pyxel.text(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 20, "Press Enter to Restart", pyxel.COLOR_CYAN)

    def reset_game(self):
        self.score_left = 0
        self.score_right = 0
        self.reset_ball()

App()