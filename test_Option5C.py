from src.calculations.technical import DatabaseIntegratedTechnicalCalculator
from src.calculations.signal_classifier import run_optionc_heatmap

def main():
    calc = DatabaseIntegratedTechnicalCalculator()
    df = calc.calculate_optionc_indicators("AAPL", save_to_db=False)

    assert df is not None and not df.empty, "Option-C indicator DF is empty"

    for t in ["MU", "SPY", "NVDA"]:
        df = calc.calculate_optionc_indicators(t, save_to_db=False)
        scores = run_optionc_heatmap(df)
        assert scores
    #scores = run_optionc_heatmap(df)
    #scores = run_optionc_heatmap(df, rules_path="src/config/master_rules_normalized.json")

    assert scores, "No scores returned"
    for ind, params in scores.items():
        for p, s in params.items():
            assert not s.isna().all(), f"All-NaN scores for {ind} {p}"

    print("Option C smoke test passed.")

if __name__ == "__main__":
    main()
