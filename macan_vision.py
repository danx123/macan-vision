# macan_vision.py

import sys
import requests
import base64
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QListWidget, QLineEdit, QLabel, QSlider, QMessageBox,
    QTabWidget
)
from PyQt5.QtCore import Qt, QUrl, QPoint, QSize
from PyQt5.QtGui import QIcon, QCursor, QPixmap, QPainter
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtSvg import QSvgRenderer

# --- DATA SVG IKON (Diadaptasi dari referensi) ---
SVG_ICONS = {
    "play": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiPjxwb2x5Z29uIHBvaW50cz0iNSAzIDE5IDEyIDUgMjEgNSAzIj48L3BvbHlnb24+PC9zdmc+",
    "stop": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiPjxyZWN0IHg9IjYiIHk9IjYiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiI+PC9yZWN0Pjwvc3ZnPg==",
    "close": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxsaW5lIHgxPSIxOCIgeTE9IjYiIHgyPSI2IiB5Mj0iMTgiPjwvbGluZT48bGluZSB4MT0iNiIgeTE9IjYiIHgyPSIxOCIgeTI9IjE4Ij48L2xpbmU+PC9zdmc+",
    "volume-high": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwb2x5Z29uIHBvaW50cz0iMTEgNSA2IDkgMiA5IDIgMTUgNiAxNSAxMSAxOSAxMSA1Ij48L3BvbHlnb24+PHBhdGggZD0iTTE1LjU0IDguNDZhNSA1IDAgMCAxIDAgNy4wNyI+PC9wYXRoPjwvc3ZnPg==",
    "tv": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxyZWN0IHg9IjIiIHk9IjciIHdpZHRoPSIyMCIgaGVpZ2h0PSIxNSIgcng9IjIiIHJ5PSIyIj48L3JlY3Q+PHBvbHlsaW5lIHBvaW50cz0iMTcgMiAxMiA3IDcgMiI+PC9wb2x5bGluZT48L3N2Zz4=",
    "radio": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxyZWN0IHg9IjMiIHk9IjMiIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgcng9IjIiIHJ5PSIyIj48L3JlY3Q+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMyI+PC9jaXJjbGU+PGxpbmUgeDE9IjUiIHkxPSI1IiB4Mj0iOSIgeTI9IjkiPjwvbGluZT48L3N2Zz4=",
}

# --- FUNGSI HELPER UNTUK IKON SVG ---
def get_icon_from_svg(svg_data_base64, color="#E0E0E0"):
    try:
        svg_data_str = base64.b64decode(svg_data_base64).decode('utf-8')
        svg_data_colored = svg_data_str.replace('currentColor', color)
        renderer = QSvgRenderer(svg_data_colored.encode('utf-8'))
        pixmap = QPixmap(renderer.defaultSize())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)
    except Exception:
        return QIcon()

class MacanVisionApp(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drag_pos = QPoint()
        self.tv_channels = []
        self.radio_stations = []
        self.current_selection = {} # Untuk menyimpan channel/stasiun yang terakhir dipilih

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("Macan Vision")
        self.setObjectName("visionDialog")
        self.setMinimumSize(800, 600)
        self.resize(900, 650)

        # Player media terpusat
        self.player = QMediaPlayer(self)
        self.video_widget = QVideoWidget(self)
        self.video_widget.setObjectName("videoWidget")
        self.player.setVideoOutput(self.video_widget)
        
        self.player.mediaStatusChanged.connect(self.update_status_on_media_change)
        self.player.error.connect(lambda: self.show_error("Gagal memutar. URL mungkin tidak valid atau stream offline."))

        self.setup_ui()
        self.apply_stylesheet() # Terapkan tema default
        
        # Ambil data setelah UI siap
        self.fetch_tv_channels()
        self.fetch_radio_stations()

    def setup_ui(self):
        self.container = QWidget(self)
        self.container.setObjectName("container")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(1, 1, 1, 1)
        container_layout.setSpacing(0)
        
        # --- Title Bar ---
        self.title_bar = self.create_title_bar()
        container_layout.addWidget(self.title_bar)
        
        # --- Content (Tabs, Controls, Status) ---
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(10)

        # --- [FIX] Definisikan status_label SEBELUM tab widget ---
        self.status_label = QLabel("Selamat datang di Macan Vision!")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)

        # --- Tab Widget ---
        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")
        self.tabs.currentChanged.connect(self.on_tab_change)

        # Tab TV
        tv_tab_widget = self.create_tv_tab()
        self.tabs.addTab(tv_tab_widget, "TV Online")
        
        # Tab Radio
        radio_tab_widget = self.create_radio_tab()
        self.tabs.addTab(radio_tab_widget, "Radio Online")
        
        # --- Controls ---
        controls_layout = self.create_controls_layout()

        # Tambahkan widget ke layout
        content_layout.addWidget(self.tabs)
        content_layout.addWidget(self.status_label) # status_label sudah ada
        content_layout.addLayout(controls_layout)
        
        container_layout.addLayout(content_layout)

    def create_title_bar(self):
        title_bar_widget = QWidget()
        title_bar_widget.setFixedHeight(40)
        title_bar_layout = QHBoxLayout(title_bar_widget)
        title_bar_layout.setContentsMargins(15, 0, 5, 0)
        
        app_icon_label = QLabel()
        app_icon_label.setPixmap(get_icon_from_svg(SVG_ICONS["tv"]).pixmap(QSize(22, 22)))
        title_label = QLabel("Macan Vision")
        title_label.setObjectName("titleLabel")
        
        close_button = QPushButton()
        close_button.setObjectName("closeButton")
        close_button.setFixedSize(36, 36)
        close_button.clicked.connect(self.close)
        self.close_button_ref = close_button

        title_bar_layout.addWidget(app_icon_label)
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(close_button)
        return title_bar_widget
        
    def create_tv_tab(self):
        tab_widget = QWidget()
        layout = QHBoxLayout(tab_widget)
        layout.setSpacing(15)

        # Panel Kiri (Video Player)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0,0,0,0)
        left_layout.addWidget(self.video_widget)
        
        # Panel Kanan (Daftar Channel)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0,0,0,0)
        
        self.tv_search_bar = QLineEdit()
        self.tv_search_bar.setPlaceholderText("Cari nama channel TV...")
        self.tv_search_bar.setObjectName("searchBar")
        self.tv_search_bar.textChanged.connect(self.filter_channels)
        
        self.tv_list_widget = QListWidget()
        self.tv_list_widget.setObjectName("channelListWidget")
        self.tv_list_widget.itemDoubleClicked.connect(self.play_selected_tv)

        right_layout.addWidget(self.tv_search_bar)
        right_layout.addWidget(self.tv_list_widget)

        layout.addWidget(left_panel, 3) # Beri rasio lebih besar untuk video
        layout.addWidget(right_panel, 1) # Rasio lebih kecil untuk daftar
        return tab_widget

    def create_radio_tab(self):
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget) # Cukup layout vertikal untuk radio
        
        self.radio_search_bar = QLineEdit()
        self.radio_search_bar.setPlaceholderText("Cari nama radio atau kota...")
        self.radio_search_bar.setObjectName("searchBar")
        self.radio_search_bar.textChanged.connect(self.filter_channels)

        self.radio_list_widget = QListWidget()
        self.radio_list_widget.setObjectName("channelListWidget")
        self.radio_list_widget.itemDoubleClicked.connect(self.play_selected_radio)
        
        layout.addWidget(self.radio_search_bar)
        layout.addWidget(self.radio_list_widget)
        return tab_widget

    def create_controls_layout(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)

        self.play_stop_button = QPushButton()
        self.play_stop_button.setObjectName("mainButton")
        self.play_stop_button.setFixedSize(50, 50)
        self.play_stop_button.clicked.connect(self.play_stop_media)
        
        volume_icon = QLabel()
        volume_icon.setPixmap(get_icon_from_svg(SVG_ICONS["volume-high"]).pixmap(QSize(24, 24)))
        self.volume_icon_ref = volume_icon
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.valueChanged.connect(self.player.setVolume)

        layout.addWidget(self.play_stop_button)
        layout.addStretch()
        layout.addWidget(volume_icon)
        layout.addWidget(self.volume_slider)
        return layout

    def fetch_tv_channels(self):
        self.tv_list_widget.addItem("Mengambil daftar channel TV Indonesia...")
        QApplication.processEvents()
        
        # API dari IPTV-ORG di GitHub, difilter untuk negara Indonesia (ID)
        url = "https://iptv-org.github.io/iptv/channels.json"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            all_channels = response.json()
            
            # Filter hanya untuk Indonesia dan urutkan
            self.tv_channels = [ch for ch in all_channels if ch.get('country') == 'ID']
            self.tv_channels.sort(key=lambda x: x['name'])
            
            self.populate_tv_list()
            self.status_label.setText("Siap. Pilih channel TV untuk ditonton.")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Gagal mengambil daftar TV. Periksa koneksi internet Anda.\nError: {e}")
            self.tv_list_widget.clear()
            self.tv_list_widget.addItem("Gagal memuat daftar.")

    def fetch_radio_stations(self):
        self.radio_list_widget.addItem("Mengambil daftar stasiun radio...")
        QApplication.processEvents()
        
        # API dari radio-browser.info
        url = "https://de1.api.radio-browser.info/json/stations/bycountrycodeexact/ID"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            self.radio_stations = response.json()
            self.radio_stations = [s for s in self.radio_stations if s.get('url_resolved')]
            self.radio_stations.sort(key=lambda x: x['name'])
            self.populate_radio_list()
        except requests.exceptions.RequestException as e:
            self.show_error(f"Gagal mengambil daftar radio. Periksa koneksi internet Anda.\nError: {e}")
            self.radio_list_widget.clear()
            self.radio_list_widget.addItem("Gagal memuat daftar.")

    def populate_tv_list(self):
        self.tv_list_widget.clear()
        for channel in self.tv_channels:
            self.tv_list_widget.addItem(channel['name'])

    def populate_radio_list(self):
        self.radio_list_widget.clear()
        for station in self.radio_stations:
            city = station.get('state', '').strip()
            display_text = station['name']
            if city:
                display_text += f" - {city}"
            self.radio_list_widget.addItem(display_text)

    def filter_channels(self, text):
        query = text.lower()
        
        if self.tabs.currentIndex() == 0: # TV Tab
            for i in range(len(self.tv_channels)):
                channel_name = self.tv_channels[i].get('name', '').lower()
                item = self.tv_list_widget.item(i)
                item.setHidden(query not in channel_name)
        else: # Radio Tab
            for i in range(len(self.radio_stations)):
                station = self.radio_stations[i]
                item = self.radio_list_widget.item(i)
                station_name = station.get('name', '').lower()
                station_city = station.get('state', '').lower()
                item.setHidden(not (query in station_name or query in station_city))

    def play_stream(self, url, name):
        if not url:
            self.show_error("URL stream tidak tersedia.")
            return
        self.player.setMedia(QMediaContent(QUrl(url)))
        self.player.play()
        self.status_label.setText(f"Memutar: {name}")

    def play_selected_tv(self, item):
        index = self.tv_list_widget.row(item)
        # Handle filtering: find the original index
        original_index = -1
        count = -1
        for i in range(len(self.tv_channels)):
            if not self.tv_list_widget.item(i).isHidden():
                count += 1
                if count == index:
                    original_index = i
                    break
        
        if original_index != -1:
            channel = self.tv_channels[original_index]
            self.current_selection = {'type': 'tv', 'data': channel}
            self.play_stream(channel.get('url'), channel.get('name'))


    def play_selected_radio(self, item):
        index = self.radio_list_widget.row(item)
         # Handle filtering: find the original index
        original_index = -1
        count = -1
        for i in range(len(self.radio_stations)):
            if not self.radio_list_widget.item(i).isHidden():
                count += 1
                if count == index:
                    original_index = i
                    break

        if original_index != -1:
            station = self.radio_stations[original_index]
            self.current_selection = {'type': 'radio', 'data': station}
            self.play_stream(station.get('url_resolved'), station.get('name'))

    def play_stop_media(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
        elif self.current_selection:
            # Putar ulang stream yang terakhir dipilih
            data = self.current_selection['data']
            url = data.get('url') if self.current_selection['type'] == 'tv' else data.get('url_resolved')
            name = data.get('name')
            self.play_stream(url, name)
        else:
            self.show_error("Pilih channel atau stasiun dari daftar terlebih dahulu.")

    def on_tab_change(self, index):
        self.player.stop() # Hentikan pemutaran saat berganti tab
        self.status_label.setText("Pilih item untuk diputar.")
        self.current_selection = {} # Reset pilihan terakhir
        if index == 0: # TV Tab
            self.player.setVideoOutput(self.video_widget)
        else: # Radio Tab
            self.player.setVideoOutput(None) # Tidak perlu output video untuk radio


    def update_status_on_media_change(self, status):
        if status == QMediaPlayer.BufferingMedia or status == QMediaPlayer.Connecting:
            self.status_label.setText("Menghubungkan / Buffering...")
        elif status == QMediaPlayer.BufferedMedia:
            if self.current_selection:
                name = self.current_selection['data'].get('name', '')
                self.status_label.setText(f"Memutar: {name}")
        elif status == QMediaPlayer.StalledMedia:
            self.status_label.setText("Stream terhenti. Menunggu buffer...")
        elif status == QMediaPlayer.NoMedia:
             self.status_label.setText("Pemutaran dihentikan.")

        # Update ikon play/stop
        if self.player.state() == QMediaPlayer.PlayingState:
            self.play_stop_button.setIcon(get_icon_from_svg(SVG_ICONS["stop"]))
        else:
            self.play_stop_button.setIcon(get_icon_from_svg(SVG_ICONS["play"]))
    
    def show_error(self, message):
        QMessageBox.warning(self, "Error", message)

    def closeEvent(self, event):
        self.player.stop()
        event.accept()

    # --- FUNGSI UNTUK PEMINDAHAN JENDELA ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.title_bar.underMouse():
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and not self.drag_pos.isNull():
            self.move(event.globalPos() - self.drag_pos)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        self.drag_pos = QPoint()

    # --- FUNGSI UNTUK TEMA ---
    def apply_stylesheet(self):
        theme = {
            "accent": "#0d6efd", "accent_hover": "#0b5ed7", "bg_main": "#181818", 
            "bg_secondary": "#121212", "border": "#2A2A2A", "text_primary": "#E0E0E0", 
            "text_secondary": "#B0B0B0"
        }
        qss = f"""
            #visionDialog, #container {{
                background-color: {theme["bg_main"]}; 
                border-radius: 12px;
                border: 1px solid {theme["border"]};
            }}
            QWidget {{ 
                color: {theme["text_primary"]}; 
                font-family: Segoe UI, sans-serif; 
                font-size: 14px; 
            }}
            #titleLabel {{ font-weight: bold; color: {theme["text_secondary"]}; }}
            #videoWidget {{ background-color: black; border-radius: 8px; }}
            #searchBar, #channelListWidget {{
                background-color: {theme["bg_secondary"]};
                border: 1px solid {theme["border"]};
                border-radius: 6px;
                padding: 6px;
            }}
            #channelListWidget::item {{ padding: 8px; border-radius: 4px; }}
            #channelListWidget::item:selected {{ background-color: {theme["accent"]}; color: #FFFFFF; }}
            #channelListWidget::item:hover:!selected {{ background-color: {theme["border"]}; }}
            #statusLabel {{ color: {theme["text_secondary"]}; padding: 5px;}}
            
            QTabWidget::pane {{ border: none; }}
            QTabBar::tab {{
                background-color: transparent; padding: 8px 15px;
                border-radius: 6px; color: {theme["text_secondary"]};
            }}
            QTabBar::tab:hover {{ background-color: {theme["border"]}; }}
            QTabBar::tab:selected {{ background-color: {theme["accent"]}; color: #FFFFFF; }}

            QSlider::groove:horizontal {{
                border: 1px solid {theme["border"]}; height: 6px; background: {theme["bg_secondary"]};
                margin: 2px 0; border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {theme["text_primary"]}; border: 1px solid {theme["text_primary"]};
                width: 14px; margin: -4px 0; border-radius: 7px;
            }}
            QSlider::handle:horizontal:hover {{ background: {theme["accent"]}; border: 1px solid {theme["accent"]}; }}
            QSlider::sub-page:horizontal {{ background: {theme["accent"]}; border-radius: 3px; }}
            
            QPushButton {{ border: none; background-color: transparent; }}
            #mainButton {{
                background-color: {theme["accent"]}; color: #FFFFFF; border-radius: 25px;
            }}
            #mainButton:hover {{ background-color: {theme["accent_hover"]}; }}
            #closeButton:hover {{ background-color: #E81123; }}
        """
        self.setStyleSheet(qss)
        
        # Perbarui ikon dengan warna tema yang benar
        text_color = theme["text_primary"]
        self.close_button_ref.setIcon(get_icon_from_svg(SVG_ICONS["close"], color=text_color))
        self.volume_icon_ref.setPixmap(get_icon_from_svg(SVG_ICONS["volume-high"], color=text_color).pixmap(QSize(24, 24)))
        self.tabs.setTabIcon(0, get_icon_from_svg(SVG_ICONS["tv"], color=text_color))
        self.tabs.setTabIcon(1, get_icon_from_svg(SVG_ICONS["radio"], color=text_color))
        self.update_status_on_media_change(self.player.mediaStatus())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MacanVisionApp()
    player.show()
    sys.exit(app.exec_())