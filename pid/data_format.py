"""
TODO:

1. Add more quantization scheme

"""

import numpy as np
import struct
from typing import Union, List, Tuple, Optional
from enum import Enum
import json


class MinMaxQuantizer:
    def __init__(self, data_min, data_max, quant_bits, round_type = "nearest", quant_zero_point = True):
        """
        Min-Max Quantizer

        Args:
            data_min: minimal data range
            data_max: maximal data range
            quant_bits: bit number after quantization
            quant_zero_point: bool, whether to quantize zero point
        """
        self.min_val = data_min
        self.max_val = data_max
        self.quant_bits = quant_bits
        self.quant_zero_point = quant_zero_point
        self.round_type = round_type
        
        # Calculate scaling factor
        self.q_min = 0
        self.q_max = (1 << self.quant_bits) - 1
        
        if self.max_val == self.min_val:
            self.scale = 1.0
        else:
            self.scale = (self.max_val - self.min_val) / (self.q_max - self.q_min)
        
        # Calculate zero point
        if self.quant_zero_point:
            self.zero_point = self.q_min - self.min_val / self.scale
            self.zero_point = np.round(self.zero_point)
            self.zero_point = np.clip(self.zero_point, self.q_min, self.q_max)
        else:
            self.zero_point = 0


    def _round(self, x):
        if self.round_type == "nearest":
            return np.round(x)
        elif self.config.round_type == "floor":
            return np.floor(x)
        elif self.config.round_type == "ceil":
            return np.ceil(x)
        else:
            raise ValueError(f"不支持的舍入类型: {self.config.round_type}")
        

    def quantized(self, data) -> np.ndarray:
        """
        Args:
            data: input float data

        Returns:
            quant_data: output quantized data
            quant_info: quantized info
        """
        quantized = data / self.scale + self.zero_point
        quantized = self._round(quantized)
        quantized = np.clip(quantized, self.q_min, self.q_max).astype(np.uint8)
        
        return quantized
    
    def dequantize(self, quantized:np.ndarray):
        scale = self.scale
        zero_point = self.zero_point
        return (quantized.astype(np.float32) - zero_point) * scale