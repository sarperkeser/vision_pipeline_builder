from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QRadialGradient, QFont
from PyQt6.QtCore import Qt, QPointF

class NetworkVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.layers = []
        self.img_w = 224
        self.img_h = 224
        self.channels = 3
        self.has_dataset = False
        self.setStyleSheet("background-color: #1a1a24; border: 1px solid #333;")

        # Dinamik Çizim Alanı (Zoom ve Pan) Değişkenleri
        self.scale_factor = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.last_pos = None

    def update_input_params(self, width: int, height: int, channels: int = 3, has_dataset: bool = False):
        """Sol panelden gelen değişimlerde tetiklenir."""
        self.img_w = width
        self.img_h = height
        self.channels = channels
        self.has_dataset = has_dataset
        self.update()

    def set_layers(self, layers):
        self.layers = layers
        self.update()

    # --- YAKINLAŞTIRMA VE KAYDIRMA (ZOOM & PAN) OLAYLARI ---
    
    def wheelEvent(self, event):
        """Fare tekerleği ile Zoom In / Zoom Out yapar."""
        if not self.has_dataset: return
        zoom_in_factor = 1.15
        zoom_out_factor = 1.0 / zoom_in_factor

        # Tekerlek yukarı mı aşağı mı kaydırıldı?
        if event.angleDelta().y() > 0:
            self.scale_factor *= zoom_in_factor
        else:
            self.scale_factor *= zoom_out_factor

        self.update()

    def mousePressEvent(self, event):
        """Fare sol tıklandığında başlangıç noktasını kaydeder."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_pos = event.position()

    def mouseMoveEvent(self, event):
        """Fare basılı tutup sürüklendiğinde tuvali kaydırır (Pan)."""
        if self.last_pos is not None and event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.position() - self.last_pos
            self.pan_x += delta.x()
            self.pan_y += delta.y()
            self.last_pos = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        """Fare tıkı bırakıldığında sürüklemeyi sonlandırır."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_pos = None

    # --- ÇİZİM MOTORU ---

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self.has_dataset:
            painter.setPen(QColor("#888"))
            painter.setFont(QFont("Arial", 13, QFont.Weight.Bold))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, 
                             "Tasarım Alanı\n\nÇizimi görmek için lütfen önce sol panelden\nbir 'Veri Seti' klasörü seçin.\n\n(Çizim aktifleştiğinde farenizin tekerleği ile\nyakınlaşıp, sürükleyerek gezinebilirsiniz.)")
            return

        # Zoom ve Pan değerlerini çizim motoruna uygula
        painter.translate(self.pan_x, self.pan_y)
        painter.scale(self.scale_factor, self.scale_factor)

        # 1 NODE = 512 DEĞER KURALI
        total_values = self.img_w * self.img_h * self.channels
        total_nodes = max(1, total_values // 512)

        visual_layers = []
        
        # Giriş Katmanı Tanımı (Maksimum sınır tamamen kaldırıldı)
        visual_layers.append({
            "name": f"Input ({total_nodes:,} Node)\n[{total_values:,} Değer]", 
            "nodes": total_nodes, 
            "color": "#2575fc"
        })

        # Gizli ve Çıkış Katmanları (Maksimum sınır tamamen kaldırıldı)
        for i, layer in enumerate(self.layers):
            nodes_count = layer.out_channels if layer.out_channels else 5
            if i == len(self.layers) - 1:
                visual_layers.append({"name": "Output", "nodes": nodes_count, "color": "#7f00ff"})
            else:
                visual_layers.append({"name": f"Hidden {i+1}", "nodes": nodes_count, "color": "#00f2fe"})

        # Sonsuz tuval için düğümler ve katmanlar arası "sabit" boşluklar
        x_spacing = 300  # Katmanlar arası yatay boşluk
        y_spacing = 35   # Aynı katmandaki düğümler arası dikey boşluk

        # Tuvali dikey eksende ortalamak için en uzun katmanın yüksekliğini bul
        max_nodes = max([layer["nodes"] for layer in visual_layers])
        max_height = max_nodes * y_spacing

        node_positions = []

        # Koordinat Hesaplamaları
        for i, layer_info in enumerate(visual_layers):
            x = (i + 1) * x_spacing
            nodes_in_layer = layer_info["nodes"]
            
            # Katmandaki düğümleri dikeyde ortala
            start_y = (max_height - (nodes_in_layer * y_spacing)) / 2 + 100
            
            layer_positions = []
            for j in range(nodes_in_layer):
                y = start_y + (j * y_spacing)
                # Hassas çizim ve zoom için QPointF (Ondalıklı) kullanıyoruz
                layer_positions.append(QPointF(float(x), float(y)))
                
            node_positions.append(layer_positions)

        # Bağlantı Çizgileri
        for i in range(len(node_positions) - 1):
            current_layer_pos = node_positions[i]
            next_layer_pos = node_positions[i + 1]
            next_color = QColor(visual_layers[i + 1]["color"])
            
            # Dinamik Saydamlık: Düğüm sayısı arttıkça çizgiler katı siyah bir bloğa dönüşmesin diye saydamlaşır
            alpha = max(2, 45 - (len(current_layer_pos) // 10)) 
            next_color.setAlpha(alpha)

            pen = QPen(next_color, 1.0)
            painter.setPen(pen)

            for pt1 in current_layer_pos:
                for pt2 in next_layer_pos:
                    painter.drawLine(pt1, pt2)

        # Düğümleri (Node) Çiz
        radius = 12.0
        for i, layer_info in enumerate(visual_layers):
            color_hex = layer_info["color"]
            positions = node_positions[i]

            # Katman Başlıkları
            painter.setPen(QColor("#ffffff"))
            painter.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            if positions:
                painter.drawText(int(positions[0].x()) - 100, int(positions[0].y()) - 50, 200, 40, 
                                 Qt.AlignmentFlag.AlignCenter, layer_info["name"])

            # Küre (Gradient) Çizimleri
            for pt in positions:
                grad = QRadialGradient(pt, radius)
                grad.setColorAt(0, QColor("#ffffff"))
                grad.setColorAt(0.3, QColor(color_hex))
                grad.setColorAt(1, QColor(color_hex).darker(150))
                
                painter.setBrush(QBrush(grad))
                painter.setPen(QPen(QColor("#2b2b36"), 1))
                painter.drawEllipse(pt, radius, radius)