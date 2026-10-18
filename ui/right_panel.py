from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QComboBox

class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self.properties_group = QGroupBox("Node Özellikleri (Properties)")
        self.form_layout = QFormLayout()

        # Mock (Sahte) Veri Girişleri
        self.input_layer_name = QLineEdit("Conv2d_1")
        self.input_in_channels = QLineEdit("3")
        self.input_out_channels = QLineEdit("16")
        
        self.combo_kernel = QComboBox()
        self.combo_kernel.addItems(["3", "5", "7"])

        self.combo_activation = QComboBox()
        self.combo_activation.addItems(["ReLU", "Sigmoid", "Tanh", "None"])

        self.form_layout.addRow("Katman Adı:", self.input_layer_name)
        self.form_layout.addRow("İnput Channels:", self.input_in_channels)
        self.form_layout.addRow("Output Channels:", self.input_out_channels)
        self.form_layout.addRow("Kernel Size:", self.combo_kernel)
        self.form_layout.addRow("Aktivasyon:", self.combo_activation)

        self.properties_group.setLayout(self.form_layout)
        
        layout.addWidget(self.properties_group)
        layout.addStretch() # Elemanları yukarı yaslamak için alt kısmı iter