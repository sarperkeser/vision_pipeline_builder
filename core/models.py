from pydantic import BaseModel, Field
from typing import Optional, Tuple, Dict, Any

class TransformConfig(BaseModel):
    """Kullanıcının seçeceği ön işleme ayarları"""
    resize: Optional[Tuple[int, int]] = Field(default=None, description="(Width, Height) formatında")
    grayscale: bool = False
    normalize: bool = False
    # İleride rotasyon, blur gibi özellikler buraya eklenecek

class DatasetConfig(BaseModel):
    """Veri seti klasör yapısı ve PyTorch DataLoader ayarları"""
    folder_path: str = Field(default="", description="Seçilen ana klasörün yolu")
    batch_size: int = 32
    shuffle: bool = True
    num_workers: int = 0
    transform: TransformConfig = TransformConfig()

class LayerConfig(BaseModel):
    """NodeGraphQt üzerinden tasarlanacak CNN katmanlarının ayarları"""
    layer_id: str
    layer_type: str  # Örn: "Conv2d", "Linear", "MaxPool2d"
    params: Dict[str, Any] = Field(default_factory=dict) 
    # Örn params: {"in_channels": 3, "out_channels": 16, "kernel_size": 3}