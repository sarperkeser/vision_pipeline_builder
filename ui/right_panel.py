from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QFormLayout, 
                             QComboBox, QPushButton, QSpinBox, QDoubleSpinBox)

class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # 1. Katman Ekleme Grubu
        self.layer_group = QGroupBox("Yeni Katman Ekle")
        layer_layout = QFormLayout()

        self.combo_layer_type = QComboBox()
        self.combo_layer_type.addItems(["Conv2d", "Linear", "MaxPool2d"])

        self.spin_in_channels = QSpinBox() # Sadece ilk başta aktif
        self.spin_in_channels.setRange(1, 4096)
        self.spin_in_channels.setValue(3)

        self.spin_out_channels = QSpinBox()
        self.spin_out_channels.setRange(1, 4096)
        self.spin_out_channels.setValue(16)

        self.spin_kernel = QSpinBox()
        self.spin_kernel.setRange(1, 11)
        self.spin_kernel.setValue(3)
        self.spin_kernel.setSingleStep(2) # 1, 3, 5, 7 diye artar

        self.combo_activation = QComboBox()
        self.combo_activation.addItems(["None", "ReLU", "Sigmoid", "Tanh", "Softmax"])

        layer_layout.addRow("Katman Tipi:", self.combo_layer_type)
        layer_layout.addRow("In Channels:", self.spin_in_channels)
        layer_layout.addRow("Out/Features:", self.spin_out_channels)
        layer_layout.addRow("Kernel Size:", self.spin_kernel)
        layer_layout.addRow("Aktivasyon:", self.combo_activation)

        self.btn_add_layer = QPushButton("Katmanı Modele Ekle")
        self.btn_add_layer.setStyleSheet("background-color: #28a745; color: white; padding: 8px; font-weight: bold;")
        layer_layout.addRow(self.btn_add_layer)

        self.layer_group.setLayout(layer_layout)
        layout.addWidget(self.layer_group)

        # 2. Eğitim Ayarları Grubu
        self.train_group = QGroupBox("Model Eğitim (Training) Ayarları")
        train_layout = QFormLayout()

        self.spin_lr = QDoubleSpinBox()
        self.spin_lr.setRange(0.00001, 1.0)
        self.spin_lr.setDecimals(5)
        self.spin_lr.setSingleStep(0.001)
        self.spin_lr.setValue(0.001)

        self.spin_epochs = QSpinBox()
        self.spin_epochs.setRange(1, 1000)
        self.spin_epochs.setValue(10)

        self.combo_optimizer = QComboBox()
        self.combo_optimizer.addItems(["Adam", "SGD", "RMSprop"])

        train_layout.addRow("Learning Rate:", self.spin_lr)
        train_layout.addRow("Epoch Sayısı:", self.spin_epochs)
        train_layout.addRow("Optimizer:", self.combo_optimizer)

        self.train_group.setLayout(train_layout)
        layout.addWidget(self.train_group)

        layout.addStretch()

        # 3. Kodu Üret Butonu
        self.btn_generate = QPushButton("Kodu Üret (Generate PyTorch Script)")
        self.btn_generate.setStyleSheet("background-color: #2b78e4; color: white; font-weight: bold; padding: 10px;")
        layout.addWidget(self.btn_generate)