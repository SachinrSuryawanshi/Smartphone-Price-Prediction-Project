from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class SmartphoneInputSchema(BaseModel):
    Brand: str = Field(..., description="Brand name", examples=["samsung"])
    OS: str = Field(..., description="Operating System", examples=["android"])
    Notches: str = Field(..., description="Screen notch style", examples=["punch hole"])
    ProcessorName: str = Field(..., description="Chipset family", examples=["snapdragon"])
    rating: float = Field(..., ge=0.0, le=100.0, description="Spec score rating", examples=[82.0])
    Speed: float = Field(..., ge=0.5, le=5.0, description="Clock speed in GHz", examples=[2.4])
    Core: float = Field(..., ge=1.0, le=16.0, description="CPU cores", examples=[8.0])
    Ram: float = Field(..., ge=1.0, le=64.0, description="RAM in GB", examples=[8.0])
    Rom: float = Field(..., ge=8.0, le=2048.0, description="Storage in GB", examples=[128.0])
    Inches: float = Field(..., ge=3.0, le=10.0, description="Screen size in inches", examples=[6.67])
    Xaxis: float = Field(..., ge=320.0, le=4000.0, description="Horizontal screen resolution", examples=[1080.0],)
    Yaxis: float = Field(..., ge=320.0, le=4000.0, description="Vertical screen resolution", examples=[2400.0],)
    Hz: float = Field(..., ge=30.0, le=240.0, description="Refresh rate in Hz", examples=[120.0])
    Capacity: float = Field(..., ge=1000.0, le=15000.0, description="Battery capacity in mAh", examples=[5000.0])
    Watt: float = Field(..., ge=5.0, le=300.0, description="Charging wattage in W", examples=[45.0])
    RearCamera: float = Field(..., ge=0.0, le=1.0, description="Has rear camera flag", examples=[1.0])
    RearMP: float = Field(..., ge=0.0, le=300.0, description="Primary rear camera MP", examples=[50.0])
    FrontMP: float = Field(..., ge=0.0, le=100.0, description="Front selfie camera MP", examples=[16.0])
    RearCameraCount: float = Field(..., ge=0.0, le=6.0, description="Total rear camera sensors", examples=[3.0])
    Sim: float = Field(..., ge=1.0, le=3.0, description="Supported SIM count", examples=[2.0])
    FiveG: int = Field(..., alias="5G", ge=0, le=1, description="5G connectivity flag", examples=[1],)
    NFC: int = Field(..., ge=0, le=1, description="NFC connectivity flag", examples=[1])
    IrBlaster: int = Field(..., ge=0, le=1, description="IR Blaster flag", examples=[0])
    FastCharging: int = Field(..., ge=0, le=1, description="Fast charging flag", examples=[1])
    HasMemoryCard: int = Field(..., ge=0, le=1, description="MicroSD slot available", examples=[0])
    IsHybrid: int = Field(..., ge=0, le=1, description="Hybrid SIM slot", examples=[0])
    ExtraSupport: float = Field(..., ge=0.0, description="Expandable storage capacity (GB)", examples=[0.0])


    class Config:
        populate_by_name = True


class BatchSmartphoneInputSchema(BaseModel):
  devices: List[SmartphoneInputSchema]