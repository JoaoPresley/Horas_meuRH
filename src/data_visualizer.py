import matplotlib.pyplot as plt
import os


class DataVisualizer:
    def __init__(self, estilo='seaborn-v0_8-muted', titulo="Saldo do mês"):
        plt.style.use(estilo)
        self.titulo = titulo
        self.fig = None
        self.ax = None

    def _horas_decimais(self, hora_str):
        s = str(hora_str).replace('"', '').strip()
        negativo = s.startswith('-')
        s_limpo = s.replace('-', '')
        h, m = map(float, s_limpo.split(':'))
        decimal = h + (m / 60)
        return -decimal if negativo else decimal

    def criar_grafico_saldos(self, saldo_anterior, saldo_mes, saldo_total):
        # 1. Preparação dos dados
        labels = ["Anterior", "Atual", "Total"]
        strings_originais = [saldo_anterior, saldo_mes, saldo_total]
        valores_decimais = [self._horas_decimais(s) for s in strings_originais]
        cores = ['#3498db' if v >= 0 else '#e74c3c' for v in valores_decimais]

        # 2. Configuração do Canvas (Figure e Axes)
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        # Ajuste de escala dinâmico
        padding = 5
        self.ax.set_ylim(min(valores_decimais) - padding, max(valores_decimais) + padding)

        # 3. Estética
        self.ax.set_title(self.titulo, fontsize=16, fontweight='bold', pad=20)
        self.ax.set_ylabel('Horas Decimais', fontsize=12)
        self.ax.grid(axis='y', linestyle='--', alpha=0.3)
        self.ax.axhline(0, color='black', linestyle='-', linewidth=1.2)

        # Remover bordas para um visual mais limpo
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        # 4. Desenho das barras
        barras = self.ax.bar(labels, valores_decimais, color=cores, width=0.6)

        # 5. Adição de Labels (ax.text)
        for bar, label_txt in zip(barras, strings_originais):
            yval = bar.get_height()
            va = 'bottom' if yval >= 0 else 'top'
            offset = 0.5 if yval >= 0 else -0.5

            self.ax.text(
                bar.get_x() + bar.get_width() / 2,
                yval + offset,
                label_txt,
                ha='center',
                va=va,
                fontsize=14,
                fontweight='bold'
            )

        plt.tight_layout()
        return self.fig  # Retorna a figura se precisar usar em outro lugar

    def salvar(self, caminho="./data/grafico_horas.png"):
        if self.fig:
            # Garante que a pasta existe
            os.makedirs(os.path.dirname(caminho), exist_ok=True)
            self.fig.savefig(caminho, dpi=300)
            plt.close(self.fig)  # Fecha para liberar memória
            print(f"Gráfico salvo com sucesso em: {caminho}")
        else:
            print("Erro: O gráfico precisa ser criado antes de salvar.")