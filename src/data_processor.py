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
            match = re.match(r'(\d{2}/\d{2})\s+([a-zA-ZçÇãÃéÉáÁóÓúÚíÍ]+)-feira\s+.*?(?:(\d{2}:\d{2})\s+Entrada\s+1)?\s*?(?:(\d{2}:\d{2})\s+Saída\s+1)?\s*?(?:(\d{2}:\d{2})\s+Entrada\s+2)?\s*?(?:(\d{2}:\d{2})\s+Saída\s+2)?', text)
            
            if match:
                day_data = {
                    'Data': match.group(1),
                    'Dia': match.group(2),
                    'Batida_1': match.group(3) if match.group(3) else '00:00',
                    'Batida_2': match.group(4) if match.group(4) else '00:00',
                    'Batida_3': match.group(5) if match.group(5) else '00:00',
                    'Batida_4': match.group(6) if match.group(6) else '00:00',
                }
                data.append(day_data)
            else:
                # Handle cases where the regex might not match perfectly, e.g., weekends with no punches
                # or different text formats. For now, we'll just append a basic structure.
                # A more robust solution would involve more complex regex or parsing logic.
                day_data = {
                    'Data': text.split(' ')[0] if text else '',
                    'Dia': text.split(' ')[1] if text and len(text.split(' ')) > 1 else '',
                    'Batida_1': '00:00',
                    'Batida_2': '00:00',
                    'Batida_3': '00:00',
                    'Batida_4': '00:00',
                }
                data.append(day_data)

        self.df = pd.DataFrame(data)
        
        # Convert time columns to timedelta
        time_cols = ['Batida_1', 'Batida_2', 'Batida_3', 'Batida_4']
        for col in time_cols:
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
