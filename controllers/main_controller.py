import os
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

# Anlık filtreleme için Pillow (PIL)
from PIL import Image, ImageEnhance, ImageFilter

from core.worker import DatasetScanner
from core.models import DatasetConfig, TransformConfig, LayerConfig, TrainConfig
from core.generator import CodeGenerator

class MainController:
    def __init__(self, view):
        self.view = view
        self.scanner = None
        self.selected_folder = ""
        self.original_img_path = None # Orijinal görseli hafızada tutacağız
        self.generator = CodeGenerator()
        self.layers = []

        # Sol Panel Bağlantıları
        self.view.left_panel.btn_select_folder.clicked.connect(self.select_folder)
        self.view.left_panel.spin_img_width.valueChanged.connect(self.on_input_dimension_changed)
        self.view.left_panel.spin_img_height.valueChanged.connect(self.on_input_dimension_changed)

        # Model Sekmesi Bağlantıları
        self.view.model_tab.btn_add_layer.clicked.connect(self.add_layer)
        self.view.model_tab.btn_generate.clicked.connect(self.generate_code)

        # Data Sekmesi Bağlantıları (Anlık Augmentation Tetikleyicileri)
        self.view.data_tab.check_hflip.stateChanged.connect(self.apply_augmentations_to_preview)
        self.view.data_tab.check_vflip.stateChanged.connect(self.apply_augmentations_to_preview)
        self.view.data_tab.spin_rotation.valueChanged.connect(self.apply_augmentations_to_preview)
        self.view.data_tab.check_color_jitter.stateChanged.connect(self.apply_augmentations_to_preview)
        self.view.data_tab.check_gaussian_blur.stateChanged.connect(self.apply_augmentations_to_preview)

        self.view.data_tab.spin_brightness.valueChanged.connect(self.apply_augmentations_to_preview)
        self.view.data_tab.spin_contrast.valueChanged.connect(self.apply_augmentations_to_preview)
        self.view.data_tab.spin_saturation.valueChanged.connect(self.apply_augmentations_to_preview)
        self.view.data_tab.spin_blur_kernel.valueChanged.connect(self.apply_augmentations_to_preview)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self.view, "Veri Seti Ana Klasörünü Seç")
        if folder_path:
            self.selected_folder = folder_path
            self.view.left_panel.tree_view.setRootIndex(self.view.left_panel.file_model.index(folder_path))
            
            # Seçim yapıldığında doğrudan Veri sekmesine geç
            self.view.tabs.setCurrentIndex(0)

            self.scanner = DatasetScanner(folder_path)
            self.scanner.scan_completed.connect(self.on_scan_completed)
            self.scanner.start()

    def on_input_dimension_changed(self):
        w = self.view.left_panel.spin_img_width.value()
        h = self.view.left_panel.spin_img_height.value()
        has_data = bool(self.selected_folder)
        self.view.model_tab.visualizer.update_input_params(width=w, height=h, channels=3, has_dataset=has_data)

    def on_scan_completed(self, data):
        if data.get("status") == "error":
            QMessageBox.critical(self.view, "Hata", f"Klasör okunurken hata oluştu: {data['message']}")
            return

        num_classes = len(data['classes'])
        self.view.left_panel.lbl_num_classes.setText(f"{num_classes} Sınıf Bulundu")
        self.on_input_dimension_changed()
        
        # Önizleme için klasördeki ilk resmi bul
        self.find_and_load_first_image(data)

    def find_and_load_first_image(self, data):
        """Klasördeki ilk resmi bulur ve orijinal yolunu hafızaya kaydeder."""
        if data['classes'] and data['total_images'] > 0:
            first_class_dir = os.path.join(data['folder'], data['classes'][0])
            for f in os.listdir(first_class_dir):
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.original_img_path = os.path.join(first_class_dir, f)
                    self.apply_augmentations_to_preview() # Orijinali ekrana bas
                    break

    def apply_augmentations_to_preview(self):
        """PIL kullanarak seçilen noise'leri fotoğrafa anında uygular."""
        if not self.original_img_path: return
        
        try:
            img = Image.open(self.original_img_path).convert("RGB")
            
            h_flip = self.view.data_tab.check_hflip.isChecked()
            v_flip = self.view.data_tab.check_vflip.isChecked()
            rotation = self.view.data_tab.spin_rotation.value()
            
            if h_flip: img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if v_flip: img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            if rotation > 0: img = img.rotate(rotation, expand=False)
            
            # COLOR JITTER DİNAMİK DEĞERLERİ
            if self.view.data_tab.check_color_jitter.isChecked():
                b_val = self.view.data_tab.spin_brightness.value()
                c_val = self.view.data_tab.spin_contrast.value()
                s_val = self.view.data_tab.spin_saturation.value()
                
                # Önizlemede etkiyi net görebilmek için orijinal olan 1.0 değerinin üzerine ekliyoruz
                img = ImageEnhance.Brightness(img).enhance(1.0 + b_val)
                img = ImageEnhance.Contrast(img).enhance(1.0 + c_val)
                img = ImageEnhance.Color(img).enhance(1.0 + s_val)
                
            # GAUSSIAN BLUR DİNAMİK DEĞERİ
            if self.view.data_tab.check_gaussian_blur.isChecked():
                k_val = self.view.data_tab.spin_blur_kernel.value()
                img = img.filter(ImageFilter.GaussianBlur(radius=k_val))

            data = img.tobytes("raw", "RGB")
            qimage = QImage(data, img.width, img.height, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            
            label_size = self.view.data_tab.preview_label.size()
            scaled_pixmap = pixmap.scaled(label_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.view.data_tab.preview_label.setPixmap(scaled_pixmap)

        except Exception as e:
            print("Önizleme oluşturulurken hata:", e)
    # def apply_augmentations_to_preview(self):
    #     """PIL kullanarak seçilen noise'leri fotoğrafa anında uygular."""
    #     if not self.original_img_path: return
        
    #     try:
    #         # Resmi PIL ile aç
    #         img = Image.open(self.original_img_path).convert("RGB")
            
    #         # Arayüzden değerleri oku
    #         h_flip = self.view.data_tab.check_hflip.isChecked()
    #         v_flip = self.view.data_tab.check_vflip.isChecked()
    #         rotation = self.view.data_tab.spin_rotation.value()
    #         c_jitter = self.view.data_tab.check_color_jitter.isChecked()
    #         g_blur = self.view.data_tab.check_gaussian_blur.isChecked()

    #         # Efektleri sırayla uygula
    #         if h_flip: img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    #         if v_flip: img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            
    #         # DÜZELTME: expand=False yapılarak resmin tuval boyutunun büyümesi engellendi (PyTorch standardı)
    #         if rotation > 0: img = img.rotate(rotation, expand=False)
            
    #         if c_jitter:
    #             img = ImageEnhance.Color(img).enhance(1.5)
    #             img = ImageEnhance.Contrast(img).enhance(1.2)
    #         if g_blur:
    #             img = img.filter(ImageFilter.GaussianBlur(radius=2))

    #         # PIL imajını PyQt QPixmap formatına çevir
    #         data = img.tobytes("raw", "RGB")
    #         qimage = QImage(data, img.width, img.height, QImage.Format.Format_RGB888)
    #         pixmap = QPixmap.fromImage(qimage)

    #         # Önizleme alanının güvenli boyutunu al
    #         label_size = self.view.data_tab.preview_label.size()
            
    #         # DÜZELTME: SmoothTransformation ile köşeli pikseller yumuşatıldı
    #         scaled_pixmap = pixmap.scaled(
    #             label_size, 
    #             Qt.AspectRatioMode.KeepAspectRatio, 
    #             Qt.TransformationMode.SmoothTransformation
    #         )
            
    #         self.view.data_tab.preview_label.setPixmap(scaled_pixmap)

    #     except Exception as e:
    #         print("Önizleme oluşturulurken hata:", e)

    def add_layer(self):
        l_type = self.view.model_tab.combo_layer_type.currentText()
        in_ch = self.view.model_tab.spin_in_channels.value()
        out_ch = self.view.model_tab.spin_out_channels.value()
        kernel = self.view.model_tab.spin_kernel.value()
        activation = self.view.model_tab.combo_activation.currentText()

        actual_in = in_ch if len(self.layers) == 0 else self.layers[-1].out_channels

        new_layer = LayerConfig(
            layer_type=l_type,
            in_channels=actual_in,
            out_channels=out_ch,
            kernel_size=kernel if l_type == "Conv2d" else None,
            activation=activation
        )
        self.layers.append(new_layer)

        self.view.model_tab.visualizer.set_layers(self.layers)
        self.view.model_tab.spin_in_channels.setDisabled(True)
        self.view.model_tab.spin_in_channels.setValue(out_ch)

    def generate_code(self):
        if not self.selected_folder:
            QMessageBox.warning(self.view, "Uyarı", "Lütfen önce bir klasör seçin!")
            return
        if len(self.layers) == 0:
            QMessageBox.warning(self.view, "Uyarı", "Lütfen modele en az 1 katman ekleyin!")
            return

        try:
            # Transform ayarlarını UI'dan al
            t_config = TransformConfig(
                h_flip=self.view.data_tab.check_hflip.isChecked(),
                v_flip=self.view.data_tab.check_vflip.isChecked(),
                rotation=self.view.data_tab.spin_rotation.value(),
                color_jitter=self.view.data_tab.check_color_jitter.isChecked(),
                jitter_brightness=self.view.data_tab.spin_brightness.value(),
                jitter_contrast=self.view.data_tab.spin_contrast.value(),
                jitter_saturation=self.view.data_tab.spin_saturation.value(),
                gaussian_blur=self.view.data_tab.check_gaussian_blur.isChecked(),
                blur_kernel=self.view.data_tab.spin_blur_kernel.value()
            )

            dataset_conf = DatasetConfig(
                folder_path=self.selected_folder,
                batch_size=self.view.left_panel.spin_batch_size.value(),
                shuffle=self.view.left_panel.check_shuffle.isChecked(),
                input_size=(self.view.left_panel.spin_img_width.value(), self.view.left_panel.spin_img_height.value()),
                num_classes=int(self.view.left_panel.lbl_num_classes.text().split()[0]) if self.view.left_panel.lbl_num_classes.text().split()[0].isdigit() else 0,
                transform=t_config
            )

            train_conf = TrainConfig(
                learning_rate=self.view.model_tab.spin_lr.value(),
                epochs=self.view.model_tab.spin_epochs.value(),
                optimizer=self.view.model_tab.combo_optimizer.currentText()
            )

            final_code = self.generator.generate_script(dataset_conf, self.layers, train_conf)

            save_path, _ = QFileDialog.getSaveFileName(self.view, "PyTorch Script Kaydet", "model_train.py", "Python (*.py)")
            if save_path:
                with open(save_path, "w", encoding="utf-8") as file:
                    file.write(final_code)
                QMessageBox.information(self.view, "Başarılı", "Kod üretildi!")
        except Exception as e:
            QMessageBox.critical(self.view, "Hata", str(e))