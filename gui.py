import sys
import pandas as pd

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)


class JournalArticlesApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Journal Articles Scraper")
        self.resize(1100, 600)

        # Load dataset
        try:
            self.df = pd.read_csv("journal_articles_cleaned.csv")
        except Exception as e:
            QMessageBox.critical(
                self,
                "File Error",
                "CSV file nahi mili!\n"
                "journal_articles_cleaned.csv ko "
                "Python file ke same folder mein rakho.\n\n"
                + str(e)
            )
            self.df = pd.DataFrame()

        self.filtered_df = self.df.copy()

        # Main layout
        layout = QVBoxLayout()

        # Heading
        heading = QLabel("Journal Articles Scraper")
        heading.setStyleSheet(
            "font-size: 22px; font-weight: bold; padding: 8px;"
        )
        layout.addWidget(heading)

        # Dataset information
        self.info_label = QLabel(
            f"Total articles: {len(self.df)}"
        )
        layout.addWidget(self.info_label)

        # Search area
        search_layout = QHBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(
            "Search article title..."
        )
        search_layout.addWidget(self.search_box)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_articles)
        search_layout.addWidget(search_button)

        reset_button = QPushButton("Show All")
        reset_button.clicked.connect(self.reset_search)
        search_layout.addWidget(reset_button)

        layout.addLayout(search_layout)

        # Table
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        # Display only first 100 articles initially
        self.setLayout(layout)
        self.show_data(self.df.head(100))

    def show_data(self, data):
        # Disable sorting while filling the table
        self.table.setSortingEnabled(False)
        self.table.clear()

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data.columns))
        self.table.setHorizontalHeaderLabels(
            list(data.columns)
        )

        for row in range(len(data)):
            for col in range(len(data.columns)):
                value = data.iloc[row, col]

                if pd.isna(value):
                    value = ""

                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)

        self.info_label.setText(
            f"Showing {len(data)} articles "
            f"out of {len(self.df)} total articles"
        )

    def search_articles(self):
        query = self.search_box.text().strip()

        if query == "":
            self.show_data(self.df.head(100))
            return

        # Search in article titles
        results = self.df[
            self.df["Title"].astype(str).str.contains(
                query,
                case=False,
                na=False,
                regex=False
            )
        ]

        self.filtered_df = results

        # Limit displayed results for performance
        self.show_data(results.head(100))

    def reset_search(self):
        self.search_box.clear()
        self.filtered_df = self.df.copy()
        self.show_data(self.df.head(100))


if __name__ == "__main__":

    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    window = JournalArticlesApp()
    window.show()

    app.exec_()