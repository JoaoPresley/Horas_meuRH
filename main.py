from src.webdriver_manager import WebDriverManager
from src.data_processor import DataProcessor
from config.config import config

def main():
    print("Iniciando o processo de extração e análise de horas...")
    
    driver_manager = WebDriverManager(config)
    try:
        driver_manager.initialize_driver()
        print("Driver inicializado. Realizando login...")
        driver_manager.login()
        print("Login realizado. Navegando para a página de ponto...")
        driver_manager.navigate_to_time_sheet()
        print("Página de ponto acessada. Extraindo HTML...")
        
        html_content = driver_manager.get_page_source()
        if html_content:
            print("HTML extraído. Processando dados...")
            data_processor = DataProcessor(html_content)
            data_processor.extract_data()
            data_processor.calculate_balances()
            
            df_result, saldo_anterior, saldo_mes, saldo_total, saldo_mes_sem_hoje, saldo_total_sem_hoje = data_processor.get_processed_data()
            
            print("\n--- Resultados da Análise ---")
            print(f"\nSaldo Anterior: {saldo_anterior}")
            print(f"Saldo do Mês: {saldo_mes}")
            print(f"Saldo Total: {saldo_total}")
            print(f"Saldo do Mês, desconsiderando o dia de hoje: {saldo_mes_sem_hoje}")
            print(f"Saldo Total, desconsiderando o dia de hoje: {saldo_total_sem_hoje}")

            # Save the processed data to a CSV file for further analysis
            try:
                df_result.to_csv("./data/horas_processadas.csv", index=False, sep=";", encoding="latin-1")
                print(f'{'-' * 64}')
                print("!!! Dados processados salvos em ./data/horas_processadas.csv !!!")
                print(f'{'-' * 64}')
            except Exception as e:
                print(f"Ocorreu um erro inesperado ao tentar salvar os dados em ./data/horas_processadas.csv: {e}")

        else:
            print("Não foi possível extrair o conteúdo HTML.")
            
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        driver_manager.quit_driver()
        print("Processo finalizado.")

if __name__ == "__main__":
    main()
