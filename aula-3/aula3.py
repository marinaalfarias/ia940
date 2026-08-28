import os
import librosa
import matplotlib.pyplot as plt
import numpy as np


def analisar_sinal(caminho_arquivo):
    # 1. Carrega o arquivo usando o caminho passado na função
    data, sr = librosa.load(caminho_arquivo, sr=None)

    # 2. Garante áudio mono e normalizado
    if data.ndim > 1:
        data = data[:, 0]
    data = data / np.max(np.abs(data))

    t = np.arange(len(data)) / sr

    # 3. Janelas de tempo
    # Em Python, slice(start, stop) usa índices em amostras, não segundos.
    inicio_ataque = int(0.450 *sr)
    fim_ataque = int(0.500 * sr)

    if fim_ataque <= inicio_ataque:
        raise ValueError("A janela de ataque ficou vazia. Verifique a duração e a taxa de amostragem.")

    idx_total = slice(0, len(data))
    idx_ataque = slice(inicio_ataque, fim_ataque)

    inicio_sustentado = len(data) // 2
    fim_sustentado = inicio_sustentado + int(0.100 * sr)
    if fim_sustentado <= inicio_sustentado:
        raise ValueError("A janela sustentada ficou vazia. Verifique a duração e a taxa de amostragem.")

    idx_sustentado = slice(inicio_sustentado, fim_sustentado)

    escalas = [
        ("Duração Total", idx_total),
        ("Primeiros 50 ms (Ataque)", idx_ataque),
        ("100 ms (Fase Sustentada)", idx_sustentado),
    ]

    fig, axes = plt.subplots(3, 2, figsize=(14, 9))

    for i, (label, idx) in enumerate(escalas):
        t_segmento = t[idx]
        x_segmento = data[idx]

        # --- Domínio do Tempo ---
        axes[i, 0].plot(t_segmento * 1000, x_segmento, color="b")
        axes[i, 0].set_title(f"Tempo: {label}")
        axes[i, 0].set_xlabel("Tempo (ms)")
        axes[i, 0].set_ylabel("Amplitude")
        axes[i, 0].grid(True)

        # --- Domínio da Frequência (FFT) ---
        n = len(x_segmento)
        fft_magnitude = np.abs(np.fft.rfft(x_segmento)) / n
        frequencias = np.fft.rfftfreq(n, d=1 / sr)

        axes[i, 1].plot(frequencias, fft_magnitude, color="r")
        axes[i, 1].set_title(f"Frequência: {label}")
        axes[i, 1].set_xlabel("Frequência (Hz)")
        axes[i, 1].set_ylabel("Magnitude")
        axes[i, 1].set_xlim(0, 4000)
        axes[i, 1].grid(True)

    plt.tight_layout()
    plt.show()


# Garante o caminho relativo correto baseado na pasta onde está o script
diretorio_script = os.path.dirname(os.path.abspath(__file__))
caminho_mp3 = os.path.join(diretorio_script, "audio.mp3")

# Executa a análise
analisar_sinal(caminho_mp3)