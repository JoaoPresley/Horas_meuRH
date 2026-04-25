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
            
            df_result, saldo_anterior, saldo_mes, saldo_total = data_processor.get_processed_data()
            
            print("\n--- Resultados da Análise ---")
            print("DataFrame de Saldo Diário:")
            print(df_result.head(10).to_markdown(index=False))
            print(f"\nSaldo Anterior: {saldo_anterior}")
            print(f"Saldo do Mês: {saldo_mes}")
            print(f"Saldo Total: {saldo_total}")

            # Save the processed data to a CSV file for further analysis
            df_result.to_csv("./data/horas_processadas.csv", index=False)
            print("\nDados processados salvos em ./data/horas_processadas.csv")

        else:
            print("Não foi possível extrair o conteúdo HTML.")
            
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        driver_manager.quit_driver()
        print("Processo finalizado.")

if __name__ == "__main__":
    main()
