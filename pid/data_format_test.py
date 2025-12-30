from data_format import MinMaxQuantizer as MinMaxQuant
import numpy as np
import plt

data_min = -1.6
data_max = 5.7
quant_bits = 8
quantizer = MinMaxQuant(data_min, data_max, quant_bits)
quant_data = quantizer.quantized(-0.56)
print(quant_data)

orig = np.arange(data_min, data_max, 0.1)
quant = [quantizer.quantized(i) for i in orig]
dequant = [quantizer.dequantize(i) for i in quant]
error = [orig[i] - dequant[i] for i in range(len(quant))]
plt.plot_scatter(orig, error, './fig/quant_error.pdf')