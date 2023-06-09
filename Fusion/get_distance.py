import math

def calculate_distance(ptx, gtx, grx, wavelength, received_power):

    ptx_mw = 10 ** ((ptx - 30) / 10)  # Potencia de transmisión en mW
    received_power_mw = 10 ** ((received_power - 30) / 10)  # Potencia recibida en mW
    distance = (wavelength / (4 * math.pi)) * math.sqrt(ptx_mw * gtx * grx / received_power_mw)

    return distance


ptx = 20  
gtx = 10  
grx = 5  
wavelength = 0.125  
received_power = -71.99 

distance = calculate_distance(ptx, gtx, grx, wavelength, received_power)
print("Distance is", distance, "metros")



