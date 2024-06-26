import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QTextEdit, QMessageBox, QComboBox

class SeyahatPlanlama(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seyahat Planlama Uygulaması")
        self.arayuz_olustur()
        self.veritabani_baglantisi_olustur()

    def arayuz_olustur(self):
        self.duzen = QVBoxLayout()
        
        # Heading
        self.heading_label = QLabel("Seyahat Planlama")
        self.heading_label.setStyleSheet("font-size: 30px; color: darkkhaki;")
        self.duzen.addWidget(self.heading_label)

        # Travel (Seyahat) Section
        self.seyahat_rota_label = QLabel("Seyahat Rotası:")
        self.seyahat_rota_label.setStyleSheet("font-size: 20px;")
        self.seyahat_rota_combobox = QComboBox()
        self.seyahat_rota_combobox.addItems(["İstanbul - Ankara", "İzmir - Antalya", "Bodrum - Kapadokya", "Bursa - Trabzon", "Eskişehir - Diyarbakır"])
        self.duzen.addWidget(self.seyahat_rota_label)
        self.duzen.addWidget(self.seyahat_rota_combobox)

        # Accommodation (Konaklama) Section
        self.konaklama_label = QLabel("Konaklama Tesis Adı:")
        self.konaklama_label.setStyleSheet("font-size: 20px;")
        self.konaklama_input = QLineEdit()
        self.duzen.addWidget(self.konaklama_label)
        self.duzen.addWidget(self.konaklama_input)

        # Add some accommodation options
        self.konaklama_options_label = QLabel("Konaklama Seçenekleri:")
        self.konaklama_options_label.setStyleSheet("font-size: 20px;")
        self.konaklama_combobox = QComboBox()
        self.konaklama_combobox.addItem("Hilton (2500 TL)")
        self.konaklama_combobox.addItem("Sheraton (1350 TL)")
        self.konaklama_combobox.addItem("Radisson Blu (950 TL)")
        self.konaklama_combobox.addItem("Marriott (4550 TL)")
        self.konaklama_combobox.addItem("Wyndham (0 TL)")
        self.duzen.addWidget(self.konaklama_options_label)
        self.duzen.addWidget(self.konaklama_combobox)

        # Price Section (hidden)
        self.fiyat_label = QLabel("Fiyat:")
        self.fiyat_label.setStyleSheet("font-size: 20px;")
        self.fiyat_input = QLineEdit()
        self.fiyat_label.hide()
        self.fiyat_input.hide()
        self.duzen.addWidget(self.fiyat_label)
        self.duzen.addWidget(self.fiyat_input)

        self.konaklama_sec_button = QPushButton("Konaklama Seç")
        self.konaklama_sec_button.setStyleSheet("background-color: #228B22;")
        self.konaklama_sec_button.clicked.connect(self.konaklama_sec)
        self.duzen.addWidget(self.konaklama_sec_button)

        # Route (Rota) Section
        self.rota_detay_label = QLabel("Seyahat Rota Detayları:")
        self.rota_detay_label.setStyleSheet("font-size: 20px;")
        self.rota_detay_input = QTextEdit()
        self.duzen.addWidget(self.rota_detay_label)
        self.duzen.addWidget(self.rota_detay_input)

        self.rota_ekle_button = QPushButton("Rota Ekle")
        self.rota_ekle_button.setStyleSheet("background-color: #CD5C5C;")
        self.rota_ekle_button.clicked.connect(self.rota_ekle)
        self.duzen.addWidget(self.rota_ekle_button)

        # Plan List Section
        self.plan_listesi_label = QLabel("Seyahat Planı:")
        self.plan_listesi_label.setStyleSheet("font-size: 20px;")
        self.plan_listesi = QListWidget()
        self.duzen.addWidget(self.plan_listesi_label)
        self.duzen.addWidget(self.plan_listesi)

        self.setLayout(self.duzen)

    def veritabani_baglantisi_olustur(self):
        self.veritabani_baglantisi = sqlite3.connect('seyahat_planlama.db')
        self.cursor = self.veritabani_baglantisi.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Rotalar
                                (id INTEGER PRIMARY KEY,
                                rota TEXT,
                                konaklama TEXT,
                                fiyat INTEGER)''')

        self.veritabani_baglantisi.commit()

    def rota_ekle(self):
        rota = self.seyahat_rota_combobox.currentText()
        konaklama = self.konaklama_combobox.currentText().split(" (")[0]  # Remove price from selection
        fiyat = self.konaklama_combobox.currentText().split(" (")[1][:-4]  # Extract price
        rota_detay = self.rota_detay_input.toPlainText().strip()

        if rota and konaklama and fiyat and rota_detay:
            self.cursor.execute("INSERT INTO Rotalar (rota, konaklama, fiyat) VALUES (?, ?, ?)", (rota, konaklama, fiyat))
            self.veritabani_baglantisi.commit()
            self.plan_listesini_yukle()
            QMessageBox.information(self, "Başarılı", "Rota başarıyla eklendi!")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen rota, konaklama, fiyat ve rota detay bilgilerini girin.")

    def konaklama_sec(self):
        konaklama = self.konaklama_combobox.currentText()
        QMessageBox.information(self, "Konaklama Seçildi", f"Konaklama: {konaklama}")

    def plan_listesini_yukle(self):
        self.plan_listesi.clear()
        self.cursor.execute("SELECT rota, konaklama, fiyat FROM Rotalar")
        rotalar = self.cursor.fetchall()
        for rota in rotalar:
            self.plan_listesi.addItem(f"Rota: {rota[0]} - Konaklama: {rota[1]} - Fiyat: {rota[2]} TL")

    def closeEvent(self, event):
        self.veritabani_baglantisi.close()
        event.accept()

if __name__ == "__main__":
    uygulama = QApplication(sys.argv)
    pencere = SeyahatPlanlama()
    pencere.show()
    sys.exit(uygulama.exec_())
