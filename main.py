import sys
import datetime
import configparser
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QComboBox,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QDialog,
    QApplication,
    QCalendarWidget,
)
from PySide6.QtCore import Slot
from connection.client_logic import ClientConnector
from pathlib import Path


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        layout = QVBoxLayout()
        self.create_labeled_widget(QComboBox(self), "reciever", "Recipiente: ")
        self.get_emails()
        rec_layout = self.create_hor_layout(self.reciever, self.reciever_label)
        self.create_labeled_widget(QLineEdit(), "send_date", "Data de envio: (dd/mm)")
        date_layout = self.create_hor_layout(self.send_date, self.send_date_label)
        self.create_labeled_widget(
            QLineEdit(), "send_time", "Horario de envio: (hh:mm)"
        )
        time_layout = self.create_hor_layout(self.send_time, self.send_time_label)
        self.create_labeled_widget(QLineEdit(), "subject", "Assunto: ")
        subject_layout = self.create_hor_layout(self.subject, self.subject_label)
        self.create_labeled_widget(QPlainTextEdit(), "message", "Mensagem")
        self.send = QPushButton("Enviar")
        self.send.clicked.connect(self.send_data)
        self.calendar = QCalendarWidget()
        self.show_calendar = QPushButton("Calendário")
        self.show_calendar.clicked.connect(self.open_calendar)
        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.send)
        self.buttons.addWidget(self.show_calendar)
        self.configure_layout_layouts(
            layout, rec_layout, date_layout, time_layout, subject_layout
        )
        self.configure_layout_widgets(layout, self.message_label, self.message)
        self.configure_layout_layouts(layout, self.buttons)
        self.setLayout(layout)
        self.setWindowTitle("Lembretes")
        self.resize(500, 300)
        self.today = datetime.date.today()

    def create_hor_layout(self, widget: QWidget, label: QLabel):
        hor_layout = QHBoxLayout()
        hor_layout.addWidget(label)
        hor_layout.addWidget(widget)
        return hor_layout

    def create_labeled_widget(
        self, widget: QWidget, field_name: str, label_message: str
    ):
        label_name = f"{field_name}_label"
        label = QLabel(label_message)
        setattr(self, field_name, widget)
        setattr(self, label_name, label)

    def configure_layout_widgets(self, layout: QVBoxLayout, *args):
        for widget in args:
            layout.addWidget(widget)

    def configure_layout_layouts(
        self, layout: QVBoxLayout, *args: QHBoxLayout | QVBoxLayout
    ):
        for widget in args:
            layout.addLayout(widget)

    @Slot()
    def send_data(self):

        data = self.get_data()
        if self.validate_data(data):
            self.format_datetime(data)
            if ClientConnector.send_message(data, SERVER):
                self.confirmation()
            else:
                pop_up = QDialog(self)
                layout = QVBoxLayout(pop_up)
                confirmation = QPushButton("OK")
                confirmation.clicked.connect(pop_up.accept)
                text = QPlainTextEdit("Não foi possivel conectar ao servidor")
                text.setReadOnly(True)
                layout.addWidget(text)
                layout.addWidget(confirmation)
                pop_up.setWindowTitle("Erro de Conexão")
                pop_up.setLayout(layout)
                pop_up.resize(200, 100)
                pop_up.exec()

    @Slot()
    def open_calendar(self):
        self.calendar.show()

    def confirmation(self):
        pop_up = QDialog(self)
        layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        confirmation = QPushButton("Agendar outra mensagem")
        confirmation.clicked.connect(pop_up.accept)
        text = QPlainTextEdit("Mensagem agendada.")
        closing = QPushButton("Fechar")
        closing.clicked.connect(sys.exit)
        text.setReadOnly(True)
        layout.addWidget(text)
        h_layout.addWidget(confirmation)
        h_layout.addWidget(closing)
        layout.addLayout(h_layout)
        pop_up.setWindowTitle("Confirmaçao de Envio")
        pop_up.setLayout(layout)
        pop_up.resize(200, 100)
        pop_up.exec()
        if pop_up.result():
            self.send_date.clear()
            self.send_time.clear()
            self.subject.clear()
            self.message.clear()

    def get_data(self) -> list[str]:

        data = []
        data.append(self.reciever.currentText())
        data.append(self.send_date.text())
        data.append(self.send_time.text())
        data.append(self.subject.text())
        message = self.message.document()
        data.append(str(message.toRawText()))
        return data

    def validate_data(self, data: list[str]):
        send_date = data[1]
        try:
            send_date_dateclass = datetime.date(
                day=int(send_date[:2]),
                month=int(send_date[3:]),
                year=self.today.year
            )
            if send_date_dateclass < self.today:
                raise ValueError
            if not ((send_date[2] == "/") or (send_date[2] == "-")):
                raise IndentationError
        except IndentationError:
            pop_up = QDialog(self)
            layout = QVBoxLayout(pop_up)
            confirmation = QPushButton("OK")
            confirmation.clicked.connect(pop_up.accept)
            text = QPlainTextEdit("Erro de formatação.\nExpectativa: dd/mm")
            text.setReadOnly(True)
            layout.addWidget(text)
            layout.addWidget(confirmation)
            pop_up.setWindowTitle("Erro de Formatação")
            pop_up.setLayout(layout)
            pop_up.resize(200, 100)
            pop_up.exec()
            return False

        except ValueError:
            pop_up = QDialog(self)
            layout = QVBoxLayout(pop_up)
            confirmation = QPushButton("OK")
            confirmation.clicked.connect(pop_up.accept)
            text = QPlainTextEdit("Data invalida.")
            text.setReadOnly(True)
            layout.addWidget(text)
            layout.addWidget(confirmation)
            pop_up.setWindowTitle("Data Invalida")
            pop_up.setLayout(layout)
            pop_up.resize(200, 100)
            pop_up.exec()
            return False

        send_time = data[2]
        try:
            datetime.time(
                hour=int(send_time[:2]),
                minute=int(send_time[3:]))
            if send_time[2] != ":":
                raise IndentationError

        except IndentationError:
            pop_up = QDialog(self)
            layout = QVBoxLayout(pop_up)
            confirmation = QPushButton("OK")
            confirmation.clicked.connect(pop_up.accept)
            text = QPlainTextEdit("Formatação invalida.")
            text.setReadOnly(True)
            layout.addWidget(text)
            layout.addWidget(confirmation)
            pop_up.setWindowTitle("Erro de Formatação")
            pop_up.setLayout(layout)
            pop_up.resize(200, 100)
            pop_up.exec()
            return False

        except ValueError:
            pop_up = QDialog(self)
            layout = QVBoxLayout(pop_up)
            confirmation = QPushButton("OK")
            confirmation.clicked.connect(pop_up.accept)
            text = QPlainTextEdit("Hora invalida")
            text.setReadOnly(True)
            layout.addWidget(text)
            layout.addWidget(confirmation)
            pop_up.setWindowTitle("Hora Invalida")
            pop_up.setLayout(layout)
            pop_up.resize(200, 100)
            pop_up.exec()
            return False

        return True

    def format_datetime(self, data: list[str]):

        send_date = data[1]
        send_time = data[2]
        data[1] = str(
            datetime.date(
                day=int(send_date[:2]),
                month=int(send_date[3:]),
                year=self.today.year,
            )
        )
        data[2] = str(datetime.time(
            hour=int(send_time[:2]),
            minute=int(send_time[3:])
            ))

        return data

    def get_emails(self):
        emails = EMAILS.split(",")
        for email in emails:
            email = email.strip()
            self.reciever.addItem(email)

if __name__ == "__main__":
    path = Path(__file__).parent/"config/config.ini"
    config = configparser.ConfigParser()
    config.read(path)
    PORT = config.get("SERVER", "port")
    HOST = config.get("SERVER", "host")
    SERVER = (HOST, int(PORT))
    EMAILS = config.get("EMAILS", "emails")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
