import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QToolBar, QAction, 
                            QFileDialog, QMessageBox, QFontDialog, QStatusBar)
from PyQt5.QtGui import QIcon, QTextCursor, QFont
from PyQt5.QtCore import Qt, QSize

class WordLikeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Word Benzeri Uygulama")
        self.setGeometry(100, 100, 800, 600)
        
       
        self.create_actions()
        
    
        self.create_components()
        self.setup_layout()
        self.connect_signals()
        
        self.current_file = None
        self.text_edit.setFont(QFont("Arial", 12))
    
    def create_actions(self):
        """Tüm aksiyonları burada oluşturuyoruz"""
        
        self.new_action = QAction(QIcon.fromTheme("document-new"), "Yeni", self)
        self.new_action.setShortcut("Ctrl+N")
        
        self.open_action = QAction(QIcon.fromTheme("document-open"), "Aç", self)
        self.open_action.setShortcut("Ctrl+O")
        
        self.save_action = QAction(QIcon.fromTheme("document-save"), "Kaydet", self)
        self.save_action.setShortcut("Ctrl+S")
        
        self.exit_action = QAction("Çıkış", self)
        self.exit_action.setShortcut("Ctrl+Q")
        
        
        self.cut_action = QAction(QIcon.fromTheme("edit-cut"), "Kes", self)
        self.cut_action.setShortcut("Ctrl+X")
        
        self.copy_action = QAction(QIcon.fromTheme("edit-copy"), "Kopyala", self)
        self.copy_action.setShortcut("Ctrl+C")
        
        self.paste_action = QAction(QIcon.fromTheme("edit-paste"), "Yapıştır", self)
        self.paste_action.setShortcut("Ctrl+V")
        
        self.undo_action = QAction(QIcon.fromTheme("edit-undo"), "Geri Al", self)
        self.undo_action.setShortcut("Ctrl+Z")
        
        self.redo_action = QAction(QIcon.fromTheme("edit-redo"), "Yinele", self)
        self.redo_action.setShortcut("Ctrl+Y")
        
        # Biçimlendirme işlemleri
        self.font_action = QAction("Yazı Tipi", self)
        self.font_action.setShortcut("Ctrl+T")
        
        self.bold_action = QAction(QIcon.fromTheme("format-text-bold"), "Kalın", self)
        self.bold_action.setShortcut("Ctrl+B")
        self.bold_action.setCheckable(True)
        
        self.italic_action = QAction(QIcon.fromTheme("format-text-italic"), "İtalik", self)
        self.italic_action.setShortcut("Ctrl+I")
        self.italic_action.setCheckable(True)
        
        self.underline_action = QAction(QIcon.fromTheme("format-text-underline"), "Altı Çizili", self)
        self.underline_action.setShortcut("Ctrl+U")
        self.underline_action.setCheckable(True)
    
    def create_components(self):
        """Arayüz bileşenlerini oluştur"""
        # Merkezde metin editörü
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)
        
        # Durum çubuğu
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Araç çubukları
        self.file_toolbar = QToolBar("Dosya Araçları")
        self.edit_toolbar = QToolBar("Düzenleme Araçları")
        self.format_toolbar = QToolBar("Biçimlendirme Araçları")
        
        # Tüm araç çubuklarını pencereye ekle
        self.addToolBar(self.file_toolbar)
        self.addToolBar(self.edit_toolbar)
        self.addToolBar(self.format_toolbar)
        
        # Menü çubuğu oluştur
        self.create_menus()
        
        # Araç çubuklarına aksiyonları ekle
        self.file_toolbar.addAction(self.new_action)
        self.file_toolbar.addAction(self.open_action)
        self.file_toolbar.addAction(self.save_action)
        
        self.edit_toolbar.addAction(self.cut_action)
        self.edit_toolbar.addAction(self.copy_action)
        self.edit_toolbar.addAction(self.paste_action)
        self.edit_toolbar.addAction(self.undo_action)
        self.edit_toolbar.addAction(self.redo_action)
        
        self.format_toolbar.addAction(self.bold_action)
        self.format_toolbar.addAction(self.italic_action)
        self.format_toolbar.addAction(self.underline_action)
        self.format_toolbar.addAction(self.font_action)
    
    def create_menus(self):
        """Menü çubuğunu oluştur"""
        menubar = self.menuBar()
        
        # Dosya
        file_menu = menubar.addMenu("Dosya")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        
        # Düzen 
        edit_menu = menubar.addMenu("Düzen")
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        
        # Biçim 
        format_menu = menubar.addMenu("Biçim")
        format_menu.addAction(self.font_action)
        format_menu.addAction(self.bold_action)
        format_menu.addAction(self.italic_action)
        format_menu.addAction(self.underline_action)
    
    def setup_layout(self):
        """Arayüz düzenini ayarla"""
        # Araç çubuklarını özelleştirme
        self.file_toolbar.setIconSize(QSize(24, 24))
        self.edit_toolbar.setIconSize(QSize(24, 24))
        self.format_toolbar.setIconSize(QSize(24, 24))
        
        # Durum çubuğu mesajı
        self.status_bar.showMessage("Hazır")
    
    def connect_signals(self):
        """Sinyal-slot bağlantılarını kur"""
        # Dosya
        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.exit_action.triggered.connect(self.close)
        
        # Düzenleme
        self.cut_action.triggered.connect(self.text_edit.cut)
        self.copy_action.triggered.connect(self.text_edit.copy)
        self.paste_action.triggered.connect(self.text_edit.paste)
        self.undo_action.triggered.connect(self.text_edit.undo)
        self.redo_action.triggered.connect(self.text_edit.redo)
        
        # Biçimlendirme 
        self.font_action.triggered.connect(self.set_font)
        self.bold_action.triggered.connect(self.toggle_bold)
        self.italic_action.triggered.connect(self.toggle_italic)
        self.underline_action.triggered.connect(self.toggle_underline)
        
        # Metin değişikliklerini izleme
        self.text_edit.textChanged.connect(self.update_status)
    
    # Slot fonksiyonları
    def new_file(self):
        if self.maybe_save():
            self.text_edit.clear()
            self.current_file = None
            self.setWindowTitle("Word Benzeri Uygulama")
    
    def open_file(self):
        if self.maybe_save():
            file_name, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", "", "Metin Dosyaları (*.txt);;Tüm Dosyalar (*)")
            if file_name:
                with open(file_name, 'r', encoding='utf-8') as f:
                    self.text_edit.setText(f.read())
                self.current_file = file_name
                self.setWindowTitle(f"{file_name} - Word Benzeri Uygulama")
    
    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.text_edit.toPlainText())
            self.status_bar.showMessage("Dosya kaydedildi", 2000)
            return True
        else:
            return self.save_as()
    
    def save_as(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Dosyayı Kaydet", "", "Metin Dosyaları (*.txt);;Tüm Dosyalar (*)")
        if file_name:
            if not file_name.endswith('.txt'):
                file_name += '.txt'
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(self.text_edit.toPlainText())
            self.current_file = file_name
            self.setWindowTitle(f"{file_name} - Word Benzeri Uygulama")
            self.status_bar.showMessage("Dosya kaydedildi", 2000)
            return True
        return False
    
    def maybe_save(self):
        if not self.text_edit.document().isModified():
            return True
        
        ret = QMessageBox.warning(self, "Belge Değişti",
                                "Belgedeki değişiklikler kaydedilmedi.\n"
                                "Kaydetmek istiyor musunuz?",
                                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        
        if ret == QMessageBox.Save:
            return self.save_file()
        elif ret == QMessageBox.Cancel:
            return False
        return True
    
    def set_font(self):
        font, ok = QFontDialog.getFont(self.text_edit.currentFont(), self)
        if ok:
            self.text_edit.setCurrentFont(font)
    
    def toggle_bold(self):
        font = self.text_edit.currentFont()
        font.setBold(self.bold_action.isChecked())
        self.text_edit.setCurrentFont(font)
    
    def toggle_italic(self):
        font = self.text_edit.currentFont()
        font.setItalic(self.italic_action.isChecked())
        self.text_edit.setCurrentFont(font)
    
    def toggle_underline(self):
        font = self.text_edit.currentFont()
        font.setUnderline(self.underline_action.isChecked())
        self.text_edit.setCurrentFont(font)
    
    def update_status(self):
        cursor = self.text_edit.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.status_bar.showMessage(f"Satır: {line}, Sütun: {col}")
    
    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = WordLikeEditor()
    editor.show()
    sys.exit(app.exec_())