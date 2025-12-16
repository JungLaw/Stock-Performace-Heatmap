# delete_check_technical_optionc.py
import pandas as pd
from src.calculations.technical import DatabaseIntegratedTechnicalCalculator

def main():
    # Adjust db path if needed – use the same one as performance/volume
    db_file = "data/stock_data.db"
    tech_calc = DatabaseIntegratedTechnicalCalculator(db_file=db_file)

    ticker = "AAPL"  # or any symbol you usually test with

    df_ind = tech_calc.calculate_optionc_indicators(ticker, save_to_db=False)

    if df_ind is None:
        print("Failed to compute Option-C indicators.")
        return

    print(df_ind.columns)
    print(df_ind.tail())

if __name__ == "__main__":
    main()