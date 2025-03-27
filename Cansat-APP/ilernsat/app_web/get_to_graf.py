import re
import time
temperaturas = []
temp_pattern = r"Temp:\s*([\d\.]+)C"
x = ""
def filtrar_temperaturas():
    with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/lora_output.csv") as f_data:
        while True:
            global x
            try:
                Data = f_data.readlines()
                if len(Data) != x:
                    if re.search("CANSAT", Data[-1]) and re.search("Sv/h", Data[-1]):
                        print("OK")
                        match = re.search(temp_pattern, Data[-1])
                        temperaturas.append(float(match.group(1)))
                        x = len(Data)

                    elif re.search("CANSAT", Data[-3]) and re.search("Sv/h", Data[-3]):
                        print("OK 2")
                        match = re.search(temp_pattern, Data[-3])
                        temperaturas.append(float())
                        x = len(Data)
            except Exception as e:
                    print(f"Esperando datos LORA [NO DATA] {e} " )
            time.sleep(1)

if __name__ == '__main__':
    filtrar_temperaturas()
