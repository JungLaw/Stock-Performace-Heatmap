import src.calculations.technical as tech


def main():
    # Turn ON the new TA engine path for this process
    tech.USE_NEW_TA_ENGINE = True

    db_file = "data/stock_data.db"
    calc = tech.DatabaseIntegratedTechnicalCalculator(db_file=db_file)

    ticker = "AAPL"

    result = calc.calculate_technical_indicators(ticker, save_to_db=False)

    if result is None:
        print("No result.")
        return

    print("Keys:", sorted(result.keys()))
    print("adx_value:", result.get("adx_value"))
    print("plus_di:", result.get("plus_di"))
    print("minus_di:", result.get("minus_di"))
    print("adx_signal:", result.get("adx_signal"))


if __name__ == "__main__":
    main()