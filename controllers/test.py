

import os
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# YENİ İMPORTLAR
from core.worker import DatasetScanner
from core.models import DatasetConfig, TransformConfig, LayerConfig
from core.generator import CodeGenerator

class MainController:
    def __init__(self, view):
        self.view = view
        self.scanner = None
        self.selected_folder = "" # Seçilen klasörü hafızada tutmak için
        self.generator = CodeGenerator() # Motorumuzu başlattık
        
        # Buton bağlantıları
        self.view.left_panel.btn_select_folder.clicked.connect(self.select_folder)
        self.view.right_panel.btn_generate.clicked.connect(self.generate_code) # YENİ BAĞLANTI
        
    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self.view, "Veri Seti Ana Klasörünü Seç")
        if folder_path:
            self.selected_folder = folder_path
            self.view.left_panel.tree_view.setRootIndex(self.view.left_panel.file_model.index(folder_path))
            
            self.scanner = DatasetScanner(folder_path)
            self.scanner.scan_completed.connect(self.on_scan_completed)
            self.scanner.start()
            
    def on_scan_completed(self, data):
        if data.get("status") == "error":
            QMessageBox.critical(self.view, "Hata", f"Klasör okunurken hata oluştu: {data['message']}")
            return
            
        QMessageBox.information(self.view, "Tarama Tamamlandı", 
            f"Sınıf (Class) Sayısı: {len(data['classes'])}\nToplam Görsel: {data['total_images']}")
        self.show_preview(data)

    def show_preview(self, data):
        if data['classes'] and data['total_images'] > 0:
            first_class_dir = os.path.join(data['folder'], data['classes'][0])
            for f in os.listdir(first_class_dir):
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(first_class_dir, f)
                    pixmap = QPixmap(img_path)
                    label_size = self.view.middle_panel.preview_label.size()
                    scaled_pixmap = pixmap.scaled(label_size, Qt.AspectRatioMode.KeepAspectRatio)
                    self.view.middle_panel.preview_label.setPixmap(scaled_pixmap)
                    break

    # YENİ METOT: Kodu Üretme Süreci
    def generate_code(self):
        if not self.selected_folder:
            QMessageBox.warning(self.view, "Uyarı", "Lütfen önce bir veri seti klasörü seçin!")
            return

        try:
            # 1. UI'dan Verileri Topla ve Pydantic'e Dönüştür
            # Transform ayarları (Şimdilik mock, boyut 224x224 diyelim)
            transform_conf = TransformConfig(resize=(224, 224), grayscale=False)
            
            # Dataset ayarları
            dataset_conf = DatasetConfig(
                folder_path=self.selected_folder,
                batch_size=self.view.left_panel.spin_batch_size.value(),
                shuffle=self.view.left_panel.check_shuffle.isChecked(),
                transform=transform_conf
            )
            
            # Sağ paneldeki Layer ayarları
            layer_conf = LayerConfig(
                layer_id=self.view.right_panel.input_layer_name.text(),
                layer_type="Conv2d",
                params={
                    "in_channels": int(self.view.right_panel.input_in_channels.text()),
                    "out_channels": int(self.view.right_panel.input_out_channels.text()),
                    "kernel_size": int(self.view.right_panel.combo_kernel.currentText()),
                    "activation": self.view.right_panel.combo_activation.currentText()
                }
            )

            # 2. Kodu Üret
            final_code = self.generator.generate_script(dataset_conf, layer_conf)

            # 3. Kullanıcıya Kayıt Yeri Sor
            save_path, _ = QFileDialog.getSaveFileName(
                self.view, "PyTorch Scriptini Kaydet", "model_train.py", "Python Files (*.py)"
            )
            
            if save_path:
                with open(save_path, "w", encoding="utf-8") as file:
                    file.write(final_code)
                QMessageBox.information(self.view, "Başarılı", "Kod başarıyla üretildi ve kaydedildi!")

        except Exception as e:
            QMessageBox.critical(self.view, "Hata", f"Kod üretilirken bir hata oluştu:\n{str(e)}")