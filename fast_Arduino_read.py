import serial
import wave
import time
import datetime as dt

port = 'COM4'
filename = 'output.wav'
baudrate = 115200
time_rec = 240
inc_factor = 50
# inc_factor = 5

sample_rate = 10000
num_channels = 1
sampwidth = 2

ser = serial.Serial(port, baudrate, timeout=1)  # Установка таймаута для чтения

frame_count = 0  # Для подсчета количества обработанных кадров

with wave.open(filename, 'w') as wf:
    wf.setnchannels(num_channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(sample_rate)
    
    a = []

    try:
        print('Считывание данных с микрофона', flush=True)
        time_sec = time_rec
        end_time = time.time() + time_rec
        while time.time() < end_time:
            if abs(time_sec + time.time() - end_time) < 0.1:
                print(dt.timedelta(seconds=time_sec), flush=True)
                time_sec -= 1
            if ser.in_waiting > 0:
                data = ser.readline().strip()
                try:
                    value = int(data) * inc_factor
                    # wf.writeframes(value.to_bytes(2, byteorder='little', signed=True))
                    a.append(value.to_bytes(2, byteorder='little', signed=True))
                    frame_count += 1
                except ValueError:
                    continue
    except KeyboardInterrupt:
        print("Прервано пользователем", flush=True)
    finally:
        print('Окончание считывания данных с микрофона', flush=True)
        ser.close()
    
    # Количество дополнительных записей, чтобы привести длину звуквого файла к требуемой time_rec
    # num = 1
    num = int(time_rec * sample_rate / frame_count)
    print(f'Начало записи в файл {filename}', flush=True)
    for i in range(frame_count):
        for j in range(num):
            wf.writeframes(a[i])

print("Запись завершена", flush=True)
print(f"Количество обработанных кадров: {frame_count}", flush=True)
# print(f"Ожидаемая длительность записи: {frame_count / sample_rate} секунд", flush=True)
