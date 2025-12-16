from src.calculations.technical import DatabaseIntegratedTechnicalCalculator
from src.calculations.signal_classifier import run_optionc_heatmap

def main():
    calc = DatabaseIntegratedTechnicalCalculator()
    df = calc.calculate_optionc_indicators("AAPL", save_to_db=False)

    assert df is not None and not df.empty, "Option-C indicator DF is empty"

    for t in ["MU", "SPY", "NVDA"]:
        df = calc.calculate_optionc_indicators(t, save_to_db=False)
        #scores = run_optionc_heatmap(df)      
        scores = run_optionc_heatmap(
            df,
            rules_path="src/config/master_rules_normalized.json",
            indicators=["RSI", "MACD", "Stochastic", "ADX", "ROC", "Williams_R"],  #"WILLR"
            )
        print(scores.keys())
        assert scores

    assert scores, "No scores returned"
    for ind, params in scores.items():
        for p, s in params.items():
            assert not s.isna().all(), f"All-NaN scores for {ind} {p}"

    #print("Option C smoke test passed.")
    print("Option A (Momentum Expansion) smoke test passed.")

    # TEST 2: Short-term Indicators Check
    rolling = calc.calculate_rule_engine_signals_optionc(
        ticker="AAPL",
        feature_scope="heatmap",
        save_to_db=False,
        indicators=["RSI", "MACD", "Stochastic", "ADX", "ROC", "Williams_R"],
        return_type="rolling"
    )

    print(rolling["status"])
    print(rolling["short_term"]["indicators"])

    print("TYPE:", type(rolling))
    if isinstance(rolling, dict):
        print("TOP-LEVEL KEYS:", list(rolling.keys())[:30])
        # If it looks like scores, show one sample
        if rolling and all(isinstance(v, dict) for v in rolling.values()):
            k0 = next(iter(rolling.keys()))
            print("SAMPLE INDICATOR KEY:", k0)
            k1 = next(iter(rolling[k0].keys())) if rolling[k0] else None
            print("SAMPLE PARAM KEY:", k1)
    else:
        print("VALUE:", rolling)
   

if __name__ == "__main__":
    main()
