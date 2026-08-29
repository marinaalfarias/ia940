import os
import librosa
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

def analisar_sinal(caminho_arquivo):
    # 1. Carrega o arquivo usando o caminho passado na função
    data, sr = librosa.load(caminho_arquivo, sr=None)

    # 2. Garante áudio mono e normalizado
    if data.ndim > 1:
        data = data[:, 0]
    data = data / np.max(np.abs(data))

    t = np.arange(len(data)) / sr
    idx_total = slice(0, len(data))
    fig, axes = plt.subplots(1, 2, figsize=(14, 9))

    escalas = [
        ("Duração Total", idx_total),
    ]

    for i, (label, idx) in enumerate(escalas):
        t_segmento = t[idx]
        x_segmento = data[idx]

        # --- Domínio do Tempo ---
        axes[0].plot(t_segmento * 1000, x_segmento, color="b")
        axes[0].set_title(f"Tempo: {label}")
        axes[0].set_xlabel("Tempo (ms)")
        axes[0].set_ylabel("Amplitude")
        axes[0].grid(True)

        # --- Domínio da Frequência (FFT) ---
        n = len(x_segmento)
        fft_magnitude = np.abs(np.fft.rfft(x_segmento)) / n
        frequencias = np.fft.rfftfreq(n, d=1 / sr)

        axes[1].plot(frequencias, fft_magnitude, color="r")
        axes[1].set_title(f"Frequência: {label}")
        axes[1].set_xlabel("Frequência (Hz)")
        axes[1].set_ylabel("Magnitude")
        axes[1].set_xlim(0, 4000)
        axes[1].grid(True)

    plt.tight_layout()
    plt.show()
    
    picos, _ = find_peaks(fft_magnitude, height=0.02)

    print(f"Quantidade de componentes senoidais: {len(picos)}")
    print(f"Frequências encontradas (Hz): {frequencias[picos]}")


# Garante o caminho relativo correto baseado na pasta onde está o script
diretorio_script = os.path.dirname(os.path.abspath(__file__))
caminho_mp3_1 = os.path.join(diretorio_script, "harmonico.wav")
caminho_mp3_2 = os.path.join(diretorio_script, "percussivo.wav")

# Executa a análise
analisar_sinal(caminho_mp3_1)
analisar_sinal(caminho_mp3_2)