from pydantic import BaseModel, Field
from typing import Optional, Tuple, List

class TransformConfig(BaseModel):
    grayscale: bool = False
    normalize: bool = False
    
    h_flip: bool = False
    v_flip: bool = False
    rotation: int = 0
    
    color_jitter: bool = False
    jitter_brightness: float = 0.2
    jitter_contrast: float = 0.2
    jitter_saturation: float = 0.2
    
    gaussian_blur: bool = False
    blur_kernel: int = 3 # PyTorch'ta kernel size genelde 3, 5, 7 gibi tek sayılar olur

class DatasetConfig(BaseModel):
    folder_path: str = ""
    batch_size: int = 32
    shuffle: bool = True
    input_size: Tuple[int, int] = Field(default=(224, 224), description="(Width, Height)")
    num_classes: int = 0
    transform: TransformConfig = TransformConfig()

class LayerConfig(BaseModel):
    layer_type: str
    in_channels: Optional[int] = None
    out_channels: Optional[int] = None
    kernel_size: Optional[int] = None
    activation: str = "None"

class TrainConfig(BaseModel):
    learning_rate: float = 0.001
    epochs: int = 10
    optimizer: str = "Adam"