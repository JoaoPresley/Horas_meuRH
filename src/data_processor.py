from bs4 import BeautifulSoup
import pandas as pd
import re

class DataProcessor:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.df = None
        self.saldo_anterior = None
        self.saldo_mes = None
        self.saldo_total = None

    def _formata_timedelta_to_hh_mm(self, td):
        total_seconds = int(td.total_seconds())
        sign = "-" if total_seconds < 0 else ""
        total_seconds = abs(total_seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{sign}{hours:02d}:{minutes:02d}"

    def extract_data(self):
        lines = self.soup.tbody.find_all('tr')
        data = []
        for line in lines:
            text = line.get_text(separator=' ')
            # Regex para extrair Data, Dia e as Batidas
            # Exemplo: '15/04 quarta-feira qua. 07:25 Entrada 1 09:45 Saída 1 13:30 Entrada 2 17:05 Saída 2 Resumo diário Incluir batida Solicitar abono Enviar atestado'
            match = re.search(r'(\d{2}/\d{2})\s+([a-zA-ZçÇãÃéÉáÁóÓúÚíÍ]+)', text, re.IGNORECASE)
            
            if match:
                # Dia do ponto, ex: 01/04
                day_schedule = match.group(1)
                # Dia da semana, ex: quarta
                day = match.group(2)

                # Regex para encontrar todos os pontos do dia, podem haver mais que 4 ou menos se houve batida erradas ou horas extras.
                hours = re.findall(r'\d{2}:\d{2}', text, re.IGNORECASE)

                #Preenche o dict que será inserio no data com os dias e depois as horas
                day_data = {"Data": day_schedule, "Dia": day}

                # Percorre todas as batidas as nomeando.
                for i in range(len(hours)):
                    col_name = f"Batida_{i+1}"
                    day_data[col_name] = hours[i]

                data.append(day_data)
            else:
                raise ValueError(f"Não foi possível encontrar o padrão de data e dia no texto: '{text[:50]}...'")


        self.df = pd.DataFrame(data)
        
        # Convert time columns to timedelta
        time_cols = self.df.columns[2:]
        for col in time_cols:
            # Antes de transformar para timedelta precisa tratar os NaN
            self.df[col] = self.df[col].fillna("00:00")
            #Agora sim concatena e transforma
            self.df[col] = pd.to_timedelta(self.df[col] + ':00')

        # Extract Saldo Anterior
        saldo_anterior_tag = self.soup.find('h6') # Assuming h6 contains the previous balance
        if saldo_anterior_tag:
            self.saldo_anterior = saldo_anterior_tag.text.strip()[1:] # Remove leading 'R' or similar
        else:
            self.saldo_anterior = '00:00'

    def calculate_balances(self):
        if self.df is None:
            self.extract_data()

        self.df["Saldo_diario"] = pd.to_timedelta("00:00:00")
        for i in range(1, len(self.df.columns[2:]), 2):
            col1 = f"Batida_{i}"
            col2 = f"Batida_{i+1}"
            self.df["Saldo_diario"] += self.df[col2] - self.df[col1]

        self.df["Meta_horas"] = self.df["Dia"].apply(lambda x: pd.to_timedelta("00:00:00") if x.lower() in ("sábado","domingo") else pd.to_timedelta("08:00:00"))
        self.df["Saldo_Extra"] = self.df["Saldo_diario"] - self.df["Meta_horas"]

        self.saldo_mes = self._formata_timedelta_to_hh_mm(self.df["Saldo_Extra"].sum())
        
        # Calculate Saldo Total
        try:
            td_saldo_mes = pd.to_timedelta(self.saldo_mes + ":00")
            td_saldo_anterior = pd.to_timedelta(self.saldo_anterior + ":00")
            self.saldo_total = self._formata_timedelta_to_hh_mm(td_saldo_mes + td_saldo_anterior)
        except Exception as e:
            print(f"Erro ao calcular saldo total: {e}")
            self.saldo_total = "Erro"

    def get_processed_data(self):
        return self.df, self.saldo_anterior, self.saldo_mes, self.saldo_total
