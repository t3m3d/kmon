from random import randint, choice
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QColor, QPainter, QFont, QLinearGradient, QRadialGradient
from PySide6.QtWidgets import QWidget


class CRTPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Matrix / CRT settings
        self.bg_color = QColor(0, 8, 0)
        self.glow_color = QColor(80, 255, 120)
        self.text_color = QColor(120, 255, 120)
        self.dim_text_color = QColor(40, 120, 40)

        self.scanline_color = QColor(0, 20, 0, 120)
        self.vignette_color = QColor(0, 0, 0, 180)

        self.font = QFont("Consolas")
        self.font.setStyleHint(QFont.Monospace)
        self.font.setPointSize(11)

        # Matrix rain config
        self.columns = []
        self.column_width = 12      # pixels per column (approx)
        self.char_height = 14       # pixels per row (approx)
        self.speed_min = 3
        self.speed_max = 8
        self.trail_length_min = 10
        self.trail_length_max = 25

        self.characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*+-/"

        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rain)
        self.timer.start(50)  # ~20 FPS

        # Flicker phase
        self.flicker_phase = 0

        self.setMinimumSize(250, 200)

    # ----- Public API -----

    def start_matrix_rain(self):
        if not self.timer.isActive():
            self.timer.start(50)

    def stop_matrix_rain(self):
        if self.timer.isActive():
            self.timer.stop()

    # ----- Matrix rain logic -----

    class Column:
        def __init__(self, x_index, y, speed, trail_length, characters):
            self.x_index = x_index      # column index (multiplied by column_width)
            self.y = y                  # current "head" y offset in pixels
            self.speed = speed          # pixels per frame
            self.trail_length = trail_length  # number of characters in trail
            self.characters = characters

        def step(self, height):
            self.y += self.speed
            if self.y - self.trail_length * 14 > height:
                # Reset to top with random offset and speed
                self.y = randint(-200, 0)
                self.speed = randint(3, 8)
                self.trail_length = randint(10, 25)

        def char_at(self, index):
            # index 0 = head, higher index = older trail
            return choice(self.characters)

    def update_rain(self):
        # Update flicker
        self.flicker_phase = (self.flicker_phase + 1) % 1000

        # Initialize columns based on current width
        width = self.width()
        height = self.height()
        num_columns = max(1, width // self.column_width)

        if not self.columns or len(self.columns) != num_columns:
            self.columns = []
            for i in range(num_columns):
                start_y = randint(-400, 0)
                speed = randint(self.speed_min, self.speed_max)
                trail_len = randint(self.trail_length_min, self.trail_length_max)
                self.columns.append(
                    CRTPanel.Column(
                        x_index=i,
                        y=start_y,
                        speed=speed,
                        trail_length=trail_len,
                        characters=self.characters,
                    )
                )

        # Step each column
        for col in self.columns:
            col.step(height)

        self.update()

    # ----- Painting -----

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        w = rect.width()
        h = rect.height()

        # Draw outer bezel
        self._paint_bezel(painter, rect)

        # Inner CRT screen area
        margin = 12
        screen_rect = QRectF(
            rect.left() + margin,
            rect.top() + margin,
            rect.width() - 2 * margin,
            rect.height() - 2 * margin,
        )

        # Draw CRT background with subtle radial glow
        self._paint_crt_background(painter, screen_rect)

        # Apply slight curvature (fake it with a gradient mask / shading)
        self._paint_crt_curvature(painter, screen_rect)

        # Draw matrix rain inside the screen area
        painter.save()
        painter.setClipRect(screen_rect.adjusted(4, 4, -4, -4))
        self._paint_matrix_rain(painter, screen_rect)
        painter.restore()

        # Scanlines and vignette on top
        self._paint_scanlines(painter, screen_rect)
        self._paint_vignette(painter, screen_rect)

        # Subtle global flicker
        self._paint_flicker(painter, screen_rect)

        painter.end()

    def _paint_bezel(self, painter, rect):
        bezel_grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
        bezel_grad.setColorAt(0.0, QColor(15, 15, 15))
        bezel_grad.setColorAt(0.5, QColor(5, 5, 5))
        bezel_grad.setColorAt(1.0, QColor(20, 20, 20))

        painter.setBrush(bezel_grad)
        painter.setPen(QColor(40, 40, 40))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 18, 18)

    def _paint_crt_background(self, painter, screen_rect):
        # Base dark green background
        painter.save()
        painter.setClipRect(screen_rect)

        painter.setBrush(self.bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(screen_rect, 12, 12)

        # Radial glow in the center
        center = screen_rect.center()
        radius = screen_rect.width() * 0.7
        glow = QRadialGradient(center, radius)
        glow.setColorAt(0.0, QColor(0, 40, 0))
        glow.setColorAt(0.5, QColor(0, 20, 0))
        glow.setColorAt(1.0, QColor(0, 5, 0))

        painter.setBrush(glow)
        painter.drawRoundedRect(screen_rect, 12, 12)

        painter.restore()

    def _paint_crt_curvature(self, painter, screen_rect):
        # Fake curvature with a vertical gradient highlight
        curve_grad = QLinearGradient(
            screen_rect.topLeft(), screen_rect.topRight()
        )
        curve_grad.setColorAt(0.0, QColor(0, 0, 0, 90))
        curve_grad.setColorAt(0.5, QColor(255, 255, 255, 20))
        curve_grad.setColorAt(1.0, QColor(0, 0, 0, 90))

        painter.save()
        painter.setClipRect(screen_rect)
        painter.setBrush(curve_grad)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(screen_rect.adjusted(2, 2, -2, -2), 14, 14)
        painter.restore()

    def _paint_matrix_rain(self, painter, screen_rect):
        painter.save()
        painter.setFont(self.font)

        # Clip rect for safe drawing inside screen
        left = int(screen_rect.left()) + 8
        top = int(screen_rect.top()) + 8
        right = int(screen_rect.right()) - 8
        bottom = int(screen_rect.bottom()) - 8

        height = bottom - top

        for col in self.columns:
            x = left + col.x_index * self.column_width

            # Head of the column
            head_y = col.y
            # Draw from head up to trail length
            for i in range(col.trail_length):
                y = head_y - i * self.char_height
                if y < top - 20 or y > bottom + 20:
                    continue

                ch = col.char_at(i)

                if i == 0:
                    # Bright head
                    color = self.glow_color
                else:
                    # Fade trail
                    fade = max(0, 255 - i * 12)
                    color = QColor(
                        self.text_color.red(),
                        self.text_color.green(),
                        self.text_color.blue(),
                        fade,
                    )

                painter.setPen(color)
                painter.drawText(x, y, ch)

        painter.restore()

    def _paint_scanlines(self, painter, screen_rect):
        painter.save()
        painter.setClipRect(screen_rect)

        line_spacing = 3
        y = int(screen_rect.top())
        while y < screen_rect.bottom():
            painter.setPen(self.scanline_color)
            painter.drawLine(
                int(screen_rect.left()), y,
                int(screen_rect.right()), y
            )
            y += line_spacing

        painter.restore()

    def _paint_vignette(self, painter, screen_rect):
        painter.save()
        painter.setClipRect(screen_rect)

        vignette = QRadialGradient(
            screen_rect.center(), max(screen_rect.width(), screen_rect.height())
        )
        vignette.setColorAt(0.7, QColor(0, 0, 0, 0))
        vignette.setColorAt(1.0, self.vignette_color)

        painter.setBrush(vignette)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(screen_rect, 12, 12)

        painter.restore()

    def _paint_flicker(self, painter, screen_rect):
        # Very subtle brightness modulation
        flicker_intensity = 8  # max alpha
        phase = self.flicker_phase % 60
        if phase < 10:
            alpha = flicker_intensity
        elif phase < 20:
            alpha = flicker_intensity // 2
        else:
            alpha = 0

        if alpha <= 0:
            return

        painter.save()
        painter.setClipRect(screen_rect)
        painter.setBrush(QColor(255, 255, 255, alpha))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(screen_rect, 12, 12)
        painter.restore()
