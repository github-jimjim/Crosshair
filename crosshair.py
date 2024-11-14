from PyQt5.QtWidgets import QApplication, QLabel, QMenu
from PyQt5.QtGui import QPixmap, QGuiApplication, QContextMenuEvent, QImage
from PyQt5.QtCore import Qt
from PIL import Image, ImageOps
import sys
import configparser

class CrosshairOverlay(QLabel):
    def __init__(self, image_path, size, color):
        super().__init__()

        img = Image.open(image_path).convert("RGBA")

        if color:
            img = self.apply_color(img, color)

        img = img.resize((size, size), Image.Resampling.LANCZOS)

        qt_img = self.pil_to_qimage_with_alpha(img)
        pixmap = QPixmap.fromImage(qt_img)

        self.setPixmap(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.resize(pixmap.size())
        self.center_on_screen()

    def apply_color(self, img, color):
        colored_img = Image.new("RGBA", img.size, color)
        mask = img.split()[3]
        img_colored = Image.composite(colored_img, img, mask)
        return img_colored

    def pil_to_qimage_with_alpha(self, img):
        """Konvertiert ein PIL-Image in ein QImage unter Beibehaltung der Transparenz."""
        data = img.tobytes("raw", "RGBA")
        qimage = QImage(data, img.size[0], img.size[1], QImage.Format_RGBA8888)
        return qimage

    def center_on_screen(self):
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        exit_action = menu.addAction("Exit")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == exit_action:
            QApplication.quit()

def read_settings_from_ini():
    config = configparser.ConfigParser()
    ini_file = 'config.ini'
    if not config.read(ini_file):
        config['Settings'] = {'Size': '200', 'Color': '#FFFFFF'}
        with open(ini_file, 'w') as configfile:
            config.write(configfile)
        size = 200
        color = '#FFFFFF'
    else:
        size = config.getint('Settings', 'Size', fallback=200)
        color = config.get('Settings', 'Color', fallback='#FFFFFF')
    
    return size, color

def main():
    app = QApplication(sys.argv)

    image_path = "useable_crosshair.png"
    size, color = read_settings_from_ini()

    overlay = CrosshairOverlay(image_path, size, color)
    overlay.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
