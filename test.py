import sys
from tkinter import Tk, Button
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Window")
        self.setGeometry(100, 100, 300, 200)

        btn = QPushButton("Click me", self)
        btn.setGeometry(50, 50, 200, 50)
        btn.clicked.connect(self.button_clicked)

    def button_clicked(self):
        print("Button clicked!")


def main():
    # Khởi tạo ứng dụng PyQt5
    app = QApplication(sys.argv)

    # Tạo cửa sổ Tkinter
    root = Tk()
    root.geometry("200x100")
    root.title("Tkinter Window")

    # Tạo nút trong cửa sổ Tkinter
    btn_tkinter = Button(root, text="Tkinter Button")
    btn_tkinter.pack()

    # Tạo cửa sổ PyQt5
    window = MainWindow()
    window.show()

    # Chạy vòng lặp ứng dụng PyQt5
    sys.exit(app.exec_())

    # Chạy vòng lặp ứng dụng Tkinter
    root.mainloop()


if __name__ == "__main__":
    main()
