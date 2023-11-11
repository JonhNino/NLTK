import pyaudio
import wave

def record_audio_to_file(file_path, record_seconds):
    # Configuración básica
    chunk = 1024  # Grabar en trozos de 1024 muestras
    sample_format = pyaudio.paInt16  # 16 bits por muestra
    channels = 1  # Cambiar a 1 canal para micrófono mono
    fs = 44100  # Grabar a 44100 muestras por segundo

    p = pyaudio.PyAudio()  # Crear interfaz con PortAudio

    print('Grabando')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Inicializar la lista de frames de audio

    # Almacenar datos en trozos durante el tiempo de grabación establecido
    for _ in range(0, int(fs / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Terminar la grabación
    stream.stop_stream()
    stream.close()
    p.terminate()

    print('Grabación finalizada')

    # Guardar los datos grabados como un archivo WAV
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

# Utilizar la función para grabar audio
record_audio_to_file('output.wav', 300)  # Grabar por 300 segundos