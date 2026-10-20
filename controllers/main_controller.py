import os
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from core.worker import DatasetScanner
from core.models import DatasetConfig, TransformConfig, LayerConfig, TrainConfig
from core.generator import CodeGenerator

class MainController:
    def __init__(self, view):
        self.view = view
        self.scanner = None
        self.selected_folder = ""
        self.generator = CodeGenerator()
        self.layers = []

        # Buton Bağlantıları
        self.view.left_panel.btn_select_folder.clicked.connect(self.select_folder)
        self.view.right_panel.btn_add_layer.clicked.connect(self.add_layer)
        self.view.right_panel.btn_generate.clicked.connect(self.generate_code)

        # Sol paneldeki W ve H değer değişikliklerini doğrudan çizime bağla
        self.view.left_panel.spin_img_width.valueChanged.connect(self.on_input_dimension_changed)
        self.view.left_panel.spin_img_height.valueChanged.connect(self.on_input_dimension_changed)

    def on_input_dimension_changed(self):
        """Sol paneldeki Input Size kutucukları değiştiğinde anında tetiklenir."""
        w = self.view.left_panel.spin_img_width.value()
        h = self.view.left_panel.spin_img_height.value()
        
        # Eğer bir klasör yolu seçiliyse True, boşsa False döner
        has_data = bool(self.selected_folder)
        
        # Ortadaki visualizer'ı güncelle ve klasör seçilip seçilmediğini bildir
        self.view.middle_panel.visualizer.update_input_params(
            width=w, 
            height=h, 
            channels=3, 
            has_dataset=has_data
        )

    def on_scan_completed(self, data):
        """İlk klasör seçimi/taraması bittiğinde otomatik tetiklenir."""
        if data.get("status") == "error":
            QMessageBox.critical(self.view, "Hata", f"Klasör okunurken hata oluştu: {data['message']}")
            return

        num_classes = len(data['classes'])
        self.view.left_panel.lbl_num_classes.setText(f"{num_classes} Sınıf Bulundu")

        # Klasör seçildiği an ortadaki paneli güncel değerlerle tekrar çizdir
        self.on_input_dimension_changed()

        QMessageBox.information(
            self.view, 
            "Tarama Tamamlandı", 
            f"Otomatik Tespit Edildi:\n- Sınıf Sayısı: {num_classes}\n- Toplam Görsel: {data['total_images']}"
        )
        self.show_preview(data)
    def select_folder(self):
        """Klasör seçme diyalogunu açar ve taramayı başlatır."""
        folder_path = QFileDialog.getExistingDirectory(self.view, "Veri Seti Ana Klasörünü Seç")
        if folder_path:
            self.selected_folder = folder_path
            self.view.left_panel.tree_view.setRootIndex(
                self.view.left_panel.file_model.index(folder_path)
            )

            # Arka plan tarayıcısını başlat
            self.scanner = DatasetScanner(folder_path)
            self.scanner.scan_completed.connect(self.on_scan_completed)
            self.scanner.start()

    # def on_scan_completed(self, data):
    #     """Arka plan taraması bittiğinde çalışır."""
    #     if data.get("status") == "error":
    #         QMessageBox.critical(self.view, "Hata", f"Klasör okunurken hata oluştu: {data['message']}")
    #         return

    #     QMessageBox.information(
    #         self.view, 
    #         "Tarama Tamamlandı", 
    #         f"Sınıf (Class) Sayısı: {len(data['classes'])}\nToplam Görsel: {data['total_images']}"
    #     )
    #     self.show_preview(data)
    # def on_scan_completed(self, data):
    #         """Arka plan taraması bittiğinde otomatik çalışır."""
    #         if data.get("status") == "error":
    #             QMessageBox.critical(self.view, "Hata", f"Klasör okunurken hata oluştu: {data['message']}")
    #             return

    #         num_classes = len(data['classes'])
            
    #         # Sol paneldeki sınıf sayısı etiketini otomatik güncelle
    #         self.view.left_panel.lbl_num_classes.setText(f"{num_classes} Sınıf Bulundu")

    #         QMessageBox.information(
    #             self.view, 
    #             "Tarama Tamamlandı", 
    #             f"Otomatik Tespit Edildi:\n- Sınıf (Class) Sayısı: {num_classes}\n- Toplam Görsel: {data['total_images']}"
    #         )
    #         self.show_preview(data)
            
    def show_preview(self, data):
        """Bulunan ilk görseli orta paneldeki alana yansıtır."""
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

    def add_layer(self):
        """Sağ paneldeki değerleri okuyup listeye katman olarak ekler."""
        l_type = self.view.right_panel.combo_layer_type.currentText()
        in_ch = self.view.right_panel.spin_in_channels.value()
        out_ch = self.view.right_panel.spin_out_channels.value()
        kernel = self.view.right_panel.spin_kernel.value()
        activation = self.view.right_panel.combo_activation.currentText()

        # İlk katman değilse, in_channels değerini bir önceki katmanın out_channels değerine eşitle
        actual_in = in_ch if len(self.layers) == 0 else self.layers[-1].out_channels

        # Katman objesini oluştur
        new_layer = LayerConfig(
            layer_type=l_type,
            in_channels=actual_in,
            out_channels=out_ch,
            kernel_size=kernel if l_type == "Conv2d" else None,
            activation=activation
        )
        self.layers.append(new_layer)

        # Orta paneldeki listeye yazdır
        display_text = f"[{len(self.layers)}] {l_type} | In: {actual_in} -> Out: {out_ch}"
        if l_type == "Conv2d":
            display_text += f" | Kernel: {kernel}x{kernel}"
        if activation != "None":
            display_text += f" ---> Aktivasyon: {activation}"

        #self.view.middle_panel.layer_list.addItem(display_text)
        # Orta paneldeki görselleştiriciyi yeni katmanlarla güncelle ve yeniden çizdir
        self.view.middle_panel.visualizer.set_layers(self.layers)

        # İlk katman eklendikten sonra In Channels girdi alanını kilitle
        self.view.right_panel.spin_in_channels.setDisabled(True)
        self.view.right_panel.spin_in_channels.setValue(out_ch)


    def generate_code(self):
        """Tüm state'i toplayıp Jinja şablonuyla PyTorch koduna dönüştürür."""
        if not self.selected_folder:
            QMessageBox.warning(self.view, "Uyarı", "Lütfen önce bir veri seti klasörü seçin!")
            return
        if len(self.layers) == 0:
            QMessageBox.warning(self.view, "Uyarı", "Lütfen modele en az 1 katman ekleyin!")
            return

        try:
            # Sol panelden Input Size ve otomatik algılanan Sınıf Sayısını al
            img_w = self.view.left_panel.spin_img_width.value()
            img_h = self.view.left_panel.spin_img_height.value()
            
            # Sınıf sayısını etiketten sayısal olarak ayıkla
            num_classes_text = self.view.left_panel.lbl_num_classes.text().split()[0]
            num_classes = int(num_classes_text) if num_classes_text.isdigit() else 0

            dataset_conf = DatasetConfig(
                folder_path=self.selected_folder,
                batch_size=self.view.left_panel.spin_batch_size.value(),
                shuffle=self.view.left_panel.check_shuffle.isChecked(),
                input_size=(img_w, img_h),
                num_classes=num_classes,
                transform=TransformConfig()
            )

            train_conf = TrainConfig(
                learning_rate=self.view.right_panel.spin_lr.value(),
                epochs=self.view.right_panel.spin_epochs.value(),
                optimizer=self.view.right_panel.combo_optimizer.currentText()
            )

            # Kodu üret
            final_code = self.generator.generate_script(dataset_conf, self.layers, train_conf)

            # Kaydetme penceresi aç
            save_path, _ = QFileDialog.getSaveFileName(
                self.view, "PyTorch Scriptini Kaydet", "model_train.py", "Python Files (*.py)"
            )
            if save_path:
                with open(save_path, "w", encoding="utf-8") as file:
                    file.write(final_code)
                QMessageBox.information(self.view, "Başarılı", "Kod başarıyla üretildi ve kaydedildi!")

        except Exception as e:
            QMessageBox.critical(self.view, "Hata", f"Kod üretilirken hata oluştu:\n{str(e)}")



    # def generate_code(self):
    #     """Tüm state'i toplayıp Jinja şablonuyla PyTorch koduna dönüştürür."""
    #     if not self.selected_folder:
    #         QMessageBox.warning(self.view, "Uyarı", "Lütfen önce bir veri seti klasörü seçin!")
    #         return
    #     if len(self.layers) == 0:
    #         QMessageBox.warning(self.view, "Uyarı", "Lütfen modele en az 1 katman ekleyin!")
    #         return

    #     try:
    #         dataset_conf = DatasetConfig(
    #             folder_path=self.selected_folder,
    #             batch_size=self.view.left_panel.spin_batch_size.value(),
    #             shuffle=self.view.left_panel.check_shuffle.isChecked(),
    #             transform=TransformConfig()
    #         )

    #         train_conf = TrainConfig(
    #             learning_rate=self.view.right_panel.spin_lr.value(),
    #             epochs=self.view.right_panel.spin_epochs.value(),
    #             optimizer=self.view.right_panel.combo_optimizer.currentText()
    #         )

    #         # Kodu üret
    #         final_code = self.generator.generate_script(dataset_conf, self.layers, train_conf)

    #         # Kaydetme penceresi aç
    #         save_path, _ = QFileDialog.getSaveFileName(
    #             self.view, "PyTorch Scriptini Kaydet", "model_train.py", "Python Files (*.py)"
    #         )
    #         if save_path:
    #             with open(save_path, "w", encoding="utf-8") as file:
    #                 file.write(final_code)
    #             QMessageBox.information(self.view, "Başarılı", "Kod başarıyla üretildi ve kaydedildi!")

    #     except Exception as e:
    #         QMessageBox.critical(self.view, "Hata", f"Kod üretilirken hata oluştu:\n{str(e)}")