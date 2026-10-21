from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QSplitter, QGroupBox, 
                             QFormLayout, QComboBox, QSpinBox, QDoubleSpinBox, QPushButton)
from PyQt6.QtCore import Qt
from ui.network_visualizer import NetworkVisualizer

class ModelTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # --- ORTA PANEL (Çizim Alanı) ---
        self.visualizer = NetworkVisualizer()
        
        # --- SAĞ PANEL (Katman ve Eğitim Ayarları) ---
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 1. Katman Ekleme
        self.layer_group = QGroupBox("Yeni Katman Ekle")
        layer_layout = QFormLayout()
        
        self.combo_layer_type = QComboBox()
        self.combo_layer_type.addItems(["Conv2d", "Linear", "MaxPool2d"])
        self.spin_in_channels = QSpinBox()
        self.spin_in_channels.setRange(1, 4096)
        self.spin_out_channels = QSpinBox()
        self.spin_out_channels.setRange(1, 4096)
        self.spin_out_channels.setValue(16)
        self.spin_kernel = QSpinBox()
        self.spin_kernel.setRange(1, 11)
        self.spin_kernel.setValue(3)
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
        right_layout.addWidget(self.layer_group)
        
        # 2. Eğitim Ayarları
        self.train_group = QGroupBox("Eğitim (Training) Ayarları")
        train_layout = QFormLayout()
        self.spin_lr = QDoubleSpinBox()
        self.spin_lr.setRange(0.00001, 1.0)
        self.spin_lr.setDecimals(5)
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
        right_layout.addWidget(self.train_group)
        right_layout.addStretch()
        
        # 3. Kodu Üret Butonu
        self.btn_generate = QPushButton("Kodu Üret (Generate PyTorch Script)")
        self.btn_generate.setStyleSheet("background-color: #2b78e4; color: white; font-weight: bold; padding: 10px;")
        right_layout.addWidget(self.btn_generate)
        
        splitter.addWidget(self.visualizer)
        splitter.addWidget(right_widget)
        splitter.setSizes([800, 300])
        
        layout.addWidget(splitter)