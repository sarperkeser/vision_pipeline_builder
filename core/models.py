from pydantic import BaseModel, Field
from typing import Optional, Tuple, List

class TransformConfig(BaseModel):
    grayscale: bool = False
    normalize: bool = False

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