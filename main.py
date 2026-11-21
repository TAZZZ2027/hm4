from __future__ import annotations
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
import sys
import numpy as np
from pathlib import Path
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from about import AboutWindow


class IceCreamChartWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.temperatures = []
        self.profits = []
        self.icecream = []
        self.selected_file = ''

        self.setWindowTitle("Scoops & Stats 🍦")
        self.resize(1100, 760)
        self.setMinimumSize(760, 540)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(28, 24, 28, 28)
        main_layout.setSpacing(18)

        action_bar = QWidget()
        action_bar.setObjectName("actionBar")
        action_layout = QHBoxLayout(action_bar)
        action_layout.setContentsMargins(22, 16, 22, 16)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(3)

        heading = QLabel("Scoops & Stats 🍨")
        heading.setObjectName("heading")
        title_layout.addWidget(heading)

        self.file_button = QPushButton("🍧  Choose File")
        self.file_button.setObjectName("chooseFileButton")
        self.file_button.clicked.connect(self.Choose_file_fun)
        action_layout.addWidget(self.file_button)

        self.about_button = QPushButton("About")
        self.about_button.setObjectName("aboutButton")
        self.about_button.clicked.connect(self.show_about)
        action_layout.addWidget(self.about_button)
        main_layout.addWidget(action_bar)

        chart_panel = QWidget()
        chart_panel.setObjectName("chartPanel")
        chart_layout = QVBoxLayout(chart_panel)
        chart_layout.setContentsMargins(18, 18, 18, 14)
        chart_layout.setSpacing(10)


        self.figure = Figure(figsize=(8, 5), dpi=100, facecolor="#FFFDF7")
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setObjectName("chartCanvas")
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        chart_layout.addWidget(self.toolbar)
        chart_layout.addWidget(self.canvas, stretch=1)
        main_layout.addWidget(chart_panel, stretch=1)

        self.plot_placeholder()


    def Choose_file_fun(self):
      self.selected_file = "Ice Cream.csv" 
      if self.selected_file:
        with open(self.selected_file, 'r') as f:
            next(f)
            for l in f:
                self.icecream = l.split(',')
                self.temperatures.append(float(self.icecream[0]))
                self.profits.append(float(self.icecream[1]))
        self.plot_ice_cream()

    def plot_ice_cream(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.scatter(self.temperatures, self.profits, s=1)

        m, b = np.polyfit(self.temperatures, self.profits, 1)
        x_vals = np.array(self.temperatures)
        y_line = m * x_vals + b
        ax.plot(x_vals, y_line, color="red", label=f"y = {m:.2f}x + {b:.2f}")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.set_title("Ice Cream Profits vs. Temperature")
        ax.set_xlabel("Temperature")
        ax.set_ylabel("Profits")
        ax.legend()

        self.figure.tight_layout()
        self.canvas.draw()


    def show_about(self) -> None:
        if not hasattr(self, "about_window"):
            self.about_window = AboutWindow()
        self.about_window.show()
        self.about_window.raise_()
        self.about_window.activateWindow()

    def plot_placeholder(self) -> None:
        axes = self.figure.add_subplot(111)
        days = [1, 2, 3, 4, 5, 6, 7]
        scoops = [2, 3, 2.5, 4, 3.5, 5, 4.5]
        axes.plot(days, scoops, color="#FF6B8B", marker="o", linewidth=3)
        axes.fill_between(days, scoops, color="#FF6B8B", alpha=0.12)
        axes.set_title("A week of imaginary scoops", color="#554B45", pad=14)
        axes.set_xlabel("Sunny day")
        axes.set_ylabel("Scoops enjoyed")
        axes.set_xticks(days)
        axes.grid(True, color="#EADFD3", linewidth=0.8, alpha=0.8)
        axes.set_facecolor("#FFFDF7")
        axes.spines[["top", "right"]].set_visible(False)
        axes.spines[["left", "bottom"]].set_color("#EADFD3")
        axes.tick_params(colors="#766B63")
        axes.xaxis.label.set_color("#766B63")
        axes.yaxis.label.set_color("#766B63")
        self.figure.tight_layout()
        self.canvas.draw()


def main() -> int:
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    stylesheet_path = Path(__file__).with_name("style.qss")
    app.setStyleSheet(stylesheet_path.read_text(encoding="utf-8"))

    window = IceCreamChartWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())