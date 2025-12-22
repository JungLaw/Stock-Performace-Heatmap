from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple

import pandas_ta_classic as ta


# ----------------------------------------------------------------------
# Default indicator configuration (single source of parameter truth)
# ----------------------------------------------------------------------
DEFAULT_CONFIG: Dict[str, Any] = {
    "RSI": [10, 14, 21, 30],  
    "MACD": [
        (12, 26, 9),
        (5, 34, 1), 
        (8, 17, 5), 
        (20, 50, 10), 
    ],
    "STOCH": [
        (14, 3, 3),
        (5, 3, 3),
        (21, 5, 5),
    ],
    "SMA": [10, 20, 50, 100, 200],
    # Expanded to satisfy BullBearPower(10/13/21) dependencies (EMA_10/13/21)
    "EMA": [10, 13, 20, 21, 50],   # [5, 10, 13, 20, 50, 100, 200]
    
    "BB": [
        (20, 2.0),
    ],
    # Trend / volatility
    "ADX": [14],   # ADX_14, DIp_14, DIn_14

    # Expanded to satisfy BullBearPower(10/13/21) dependencies (ATR/ATRP_10/13/21)
    "ATR": [10, 12, 13, 14, 21],   # add 10/13/21; keep 12/14
    "ATRP": [10, 12, 13, 14, 21],  # (ATR% vs price); add 10/13/21; keep 12/14 
    
    # Momentum / oscillators
    "CCI": [20],   # CCI_20 (window 20)
    "ROC": [9, 12, 20, 50],   
    "WILLR": [5, 14, 20],

    # Option B (Volume + ERI)
    # B1 — Core Volume
    "MFI": [10, 14, 30],
    # CMF "30" is now activated per your direction; keep alongside rulebook params
    "CMF": [10, 21, 30, 50],
    # OBV has a param key "0" in the rulebook, but computation is single-series
    "OBV": [0],
    # Required aliases by rulebook: OBV_smooth and OBV_smooth_20
    "OBV_SMOOTH": [20],
}


# ----------------------------------------------------------------------
# Canonical price series helper (Adj Close preferred)
# ----------------------------------------------------------------------
def _get_price_series(df: pd.DataFrame) -> pd.Series:
    """
    Canonical price series:
    - Use 'Adj Close' when available
    - Fallback to 'Close' otherwise

    This must stay aligned with performance.py.
    """
    if "Adj Close" in df.columns:
        return df["Adj Close"]
    return df["Close"]


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def compute_all_indicators(
    df: pd.DataFrame,
    config: Dict[str, Any] | None = None,
) -> pd.DataFrame:
    """
    Compute technical indicators using pandas-ta-classic as the math engine,
    with canonical Option C naming and canonical price selection
    (Adj Close preferred, else Close).

    Indicators controlled by `config` (or DEFAULT_CONFIG when None):

        - RSI_n                      → RSI_14, RSI_30, ...
        - MACD_fast_slow_signal_*    → MACD_12_26_9_line/_signal/_hist, ...
        - STOCHK/STOCHD              → STOCHK_14_3_3, STOCHD_14_3_3, ...
        - SMA_n                      → SMA_20, SMA_50, SMA_200, ...
        - EMA_n                      → EMA_20, EMA_50, ...
        - BB_period_std_*            → BB_20_2_mid/_upper/_lower, ...
        - ATR_n                      → ATR_14, ...
        - ATRP_n                     → ATRP_14, ...
        - ADX_n, DIp_n, DIn_n        → ADX_14, DIp_14, DIn_14, ...
        - CCI_n                      → CCI_20, ...
        - ROC_n                      → ROC_10, ...

    `config` is expected to follow the DEFAULT_CONFIG structure.
    """
    df = df.copy()

    # Use provided config or fall back to default
    cfg: Dict[str, Any] = config or DEFAULT_CONFIG

    # Canonical price series (Adj Close preferred)
    price = _get_price_series(df)

    # ====================================================
    # RSI (pandas_ta_classic.rsi)
    # ====================================================
    for period in cfg.get("RSI", []):
        p_i = int(period)
        rsi_series = ta.rsi(price, length=p_i)
        df[f"RSI_{p_i}"] = rsi_series

    # ====================================================
    # MACD (pandas_ta_classic.macd)
    # ====================================================
    for fast, slow, signal in cfg.get("MACD", []):
        fast_i, slow_i, signal_i = int(fast), int(slow), int(signal)
        prefix = f"MACD_{fast_i}_{slow_i}_{signal_i}"

        macd_df = ta.macd(
            price,
            fast=fast_i,
            slow=slow_i,
            signal=signal_i,
        )

        # pandas-ta / pandas-ta-classic typically uses:
        #   MACD_12_26_9   → MACD line
        #   MACDs_12_26_9  → signal line
        #   MACDh_12_26_9  → histogram
        line_col = f"MACD_{fast_i}_{slow_i}_{signal_i}"
        sig_col_lower = f"MACDs_{fast_i}_{slow_i}_{signal_i}"
        sig_col_upper = f"MACDS_{fast_i}_{slow_i}_{signal_i}"
        hist_col_lower = f"MACDh_{fast_i}_{slow_i}_{signal_i}"
        hist_col_upper = f"MACDH_{fast_i}_{slow_i}_{signal_i}"

        macd_line = macd_df[line_col] if line_col in macd_df.columns else macd_df.iloc[:, 0]

        if sig_col_lower in macd_df.columns:
            macd_signal = macd_df[sig_col_lower]
        elif sig_col_upper in macd_df.columns:
            macd_signal = macd_df[sig_col_upper]
        else:
            # Fallback: try second column
            macd_signal = macd_df.iloc[:, 1] if macd_df.shape[1] > 1 else macd_line * 0.0

        if hist_col_lower in macd_df.columns:
            macd_hist = macd_df[hist_col_lower]
        elif hist_col_upper in macd_df.columns:
            macd_hist = macd_df[hist_col_upper]
        else:
            # Fallback: try third column
            macd_hist = macd_df.iloc[:, 2] if macd_df.shape[1] > 2 else macd_line * 0.0

        df[f"{prefix}_line"] = macd_line
        df[f"{prefix}_signal"] = macd_signal
        df[f"{prefix}_hist"] = macd_hist

    # ====================================================
    # Stochastic (pandas_ta_classic.stoch)
    # ====================================================
    stoch_params: List[Tuple[int, int, int]] = cfg.get("STOCH", [])
    if {"High", "Low"}.issubset(df.columns):
        for k_period, d_period, smooth_k in stoch_params:
            k_i, d_i, s_i = int(k_period), int(d_period), int(smooth_k)

            stoch_df = ta.stoch(
                high=df["High"],
                low=df["Low"],
                close=price,  # use canonical price (Adj Close preferred)
                k=k_i,
                d=d_i,
                smooth_k=s_i,
            )
            # pandas-ta naming: STOCHk_14_3_3, STOCHd_14_3_3
            k_src = f"STOCHk_{k_i}_{d_i}_{s_i}"
            d_src = f"STOCHd_{k_i}_{d_i}_{s_i}"

            k_series = stoch_df[k_src] if k_src in stoch_df.columns else stoch_df.iloc[:, 0]
            d_series = stoch_df[d_src] if d_src in stoch_df.columns else stoch_df.iloc[:, 1]

            df[f"STOCHK_{k_i}_{d_i}_{s_i}"] = k_series
            df[f"STOCHD_{k_i}_{d_i}_{s_i}"] = d_series
    else:
        # If High/Low missing, still create the configured columns as NA
        for k_period, d_period, smooth_k in stoch_params:
            k_i, d_i, s_i = int(k_period), int(d_period), int(smooth_k)
            df[f"STOCHK_{k_i}_{d_i}_{s_i}"] = pd.NA
            df[f"STOCHD_{k_i}_{d_i}_{s_i}"] = pd.NA

    # ====================================================
    # SMA (pandas_ta_classic.sma)
    # ====================================================
    for window in cfg.get("SMA", []):
        w_i = int(window)
        sma_series = ta.sma(price, length=w_i)
        df[f"SMA_{w_i}"] = sma_series

    # ====================================================
    # EMA (pandas_ta_classic.ema)
    # ====================================================
    for span in cfg.get("EMA", []):
        s_i = int(span)
        ema_series = ta.ema(price, length=s_i)
        df[f"EMA_{s_i}"] = ema_series

    # BullBearPower rules reference redundant EMA_<len>_<len> names (e.g., EMA_13_13)
    # Create *only the required* aliases (no extra computation), to keep the DF lean.
    for s_i in (10, 13, 21):
        base = f"EMA_{s_i}"
        alias = f"EMA_{s_i}_{s_i}"
        if base in df.columns and alias not in df.columns:
            df[alias] = df[base]

    # ====================================================
    # Bull/Bear Power (Elder Ray style components) + BBP composite
    # ====================================================
    # We compute:
    #   BullPower_<len> = High - EMA_<len>
    #   BearPower_<len> = Low  - EMA_<len>
    #   BBP_<len>       = BullPower_<len> + BearPower_<len>
    #
    # For rulebook/rolling compatibility, also alias:
    #   BullBearPower_<len> = BBP_<len>
    #
    # Note: This is intentionally minimal: no ATR normalization, no slopes.
    if {"High", "Low"}.issubset(df.columns):
        for s_i in (10, 13, 21):
            ema_col = f"EMA_{s_i}"
            if ema_col not in df.columns:
                # If config changes, ensure the columns still exist (avoid KeyError)
                df[f"BullPower_{s_i}"] = pd.NA
                df[f"BearPower_{s_i}"] = pd.NA
                df[f"BBP_{s_i}"] = pd.NA
                df[f"BullBearPower_{s_i}"] = pd.NA
                continue

            bull = df["High"] - df[ema_col]
            bear = df["Low"] - df[ema_col]
            bbp = bull + bear

            df[f"BullPower_{s_i}"] = bull
            df[f"BearPower_{s_i}"] = bear
            df[f"BBP_{s_i}"] = bbp

            # Alias used by rolling meta / rulebook variable naming
            df[f"BullBearPower_{s_i}"] = df[f"BBP_{s_i}"]
    else:
        for s_i in (10, 13, 21):
            df[f"BullPower_{s_i}"] = pd.NA
            df[f"BearPower_{s_i}"] = pd.NA
            df[f"BBP_{s_i}"] = pd.NA
            df[f"BullBearPower_{s_i}"] = pd.NA

    # ====================================================
    # Bollinger Bands (pandas_ta_classic.bbands)
    # ====================================================
    for period, num_std in cfg.get("BB", []):
        p_i = int(period)
        n_std = float(num_std)

        bb_df = ta.bbands(price, length=p_i, std=n_std)

        # pandas-ta naming: BBL_20_2.0, BBM_20_2.0, BBU_20_2.0
        std_tag_str = f"{n_std:.1f}"
        mid_src = f"BBM_{p_i}_{std_tag_str}"
        upper_src = f"BBU_{p_i}_{std_tag_str}"
        lower_src = f"BBL_{p_i}_{std_tag_str}"

        mid = bb_df[mid_src] if mid_src in bb_df.columns else bb_df.iloc[:, 1]
        upper = bb_df[upper_src] if upper_src in bb_df.columns else bb_df.iloc[:, 2]
        lower = bb_df[lower_src] if lower_src in bb_df.columns else bb_df.iloc[:, 0]

        # Option C naming uses integer std tag (e.g. BB_20_2_mid)
        std_tag_int = int(round(n_std))
        df[f"BB_{p_i}_{std_tag_int}_mid"] = mid
        df[f"BB_{p_i}_{std_tag_int}_upper"] = upper
        df[f"BB_{p_i}_{std_tag_int}_lower"] = lower

    # ====================================================
    # ATR and ATRP (pandas_ta_classic.atr)
    # ====================================================
    if {"High", "Low"}.issubset(df.columns):
        for length in cfg.get("ATR", []):
            l_i = int(length)
            atr_series = ta.atr(
                high=df["High"],
                low=df["Low"],
                close=price,
                length=l_i,
            )
            df[f"ATR_{l_i}"] = atr_series

        # ATRP = ATR% (ATR relative to price)
        for length in cfg.get("ATRP", []):
            l_i = int(length)
            atr_col = f"ATR_{l_i}"
            if atr_col not in df.columns:
                # Compute ATR on the fly if not already done
                atr_series = ta.atr(
                    high=df["High"],
                    low=df["Low"],
                    close=price,
                    length=l_i,
                )
                df[atr_col] = atr_series
            atr_series = df[atr_col]

            # ATRP = 100 * ATR / price, with infinities mapped to NaN
            atrp = (atr_series / price) * 100.0
            atrp = atrp.replace([np.inf, -np.inf], np.nan)

            df[f"ATRP_{l_i}"] = atrp
    else:
        # If High/Low missing, still create the configured columns as NA
        for length in cfg.get("ATR", []):
            l_i = int(length)
            df[f"ATR_{l_i}"] = pd.NA
        for length in cfg.get("ATRP", []):
            l_i = int(length)
            df[f"ATRP_{l_i}"] = pd.NA

    # ====================================================
    # ADX + DIp/DIn (pandas_ta_classic.adx)
    # ====================================================
    if {"High", "Low"}.issubset(df.columns):
        for length in cfg.get("ADX", []):
            l_i = int(length)
            adx_df = ta.adx(
                high=df["High"],
                low=df["Low"],
                close=price,
                length=l_i,
            )
            # Typical pandas-ta columns: ADX_14, DMP_14, DMN_14
            adx_src = f"ADX_{l_i}"
            dmp_src = f"DMP_{l_i}"
            dmn_src = f"DMN_{l_i}"

            # Be defensive: fall back to first/other columns if names differ
            adx_series = adx_df[adx_src] if adx_src in adx_df.columns else adx_df.iloc[:, 0]
            dmp_series = dmp_series = (
                adx_df[dmp_src] if dmp_src in adx_df.columns else adx_df.iloc[:, 1]
            )
            dmn_series = dmn_series = (
                adx_df[dmn_src] if dmn_src in adx_df.columns else adx_df.iloc[:, 2]
            )

            # ADX itself
            df[f"ADX_{l_i}"] = adx_series

            # pandas-ta's DMP/DMN are already DI+ and DI− style values (0–100 range),
            # so we map them directly to Option C DIp/DIn without rescaling.
            df[f"DIp_{l_i}"] = dmp_series
            df[f"DIn_{l_i}"] = dmn_series
    else:
        for length in cfg.get("ADX", []):
            l_i = int(length)
            df[f"ADX_{l_i}"] = pd.NA
            df[f"DIp_{l_i}"] = pd.NA
            df[f"DIn_{l_i}"] = pd.NA

    # ====================================================
    # CCI (Commodity Channel Index) - pandas_ta_classic.cci
    # ====================================================
    if {"High", "Low"}.issubset(df.columns):
        for length in cfg.get("CCI", []):
            l_i = int(length)
            # ta.cci returns a Series named like CCI_length_constant; we just
            # reassign it to Option C name CCI_<length>.
            cci_series = ta.cci(
                high=df["High"],
                low=df["Low"],
                close=price,
                length=l_i,
            )
            df[f"CCI_{l_i}"] = cci_series
    else:
        for length in cfg.get("CCI", []):
            l_i = int(length)
            df[f"CCI_{l_i}"] = pd.NA

    # ====================================================
    # ROC (Rate of Change) - pandas_ta_classic.roc
    # ====================================================
    for length in cfg.get("ROC", []):
        l_i = int(length)
        roc_series = ta.roc(
            close=price,
            length=l_i,
        )
        # pandas-ta names this ROC_<length>; we mirror that in Option C.
        df[f"ROC_{l_i}"] = roc_series

    # ====================================================
    # Williams %R (WILLR) - pandas_ta_classic.willr
    # ====================================================
    high_col = "High" if "High" in df.columns else "high"
    low_col = "Low" if "Low" in df.columns else "low"

    if high_col in df.columns and low_col in df.columns:
        high = df[high_col]
        low = df[low_col]

        for length in cfg.get("WILLR", []):
            l_i = int(length)
            # pandas_ta_classic function name may differ by version
            if hasattr(ta, "willr"):
                willr_series = ta.willr(
                    high=high,
                    low=low,
                    close=price,
                    length=l_i,
                )
            else:
                willr_series = ta.williams_r(
                    high=high,
                    low=low,
                    close=price,
                    length=l_i,
                )

            df[f"WILLR_{l_i}"] = willr_series
    else:
        logger.warning("WILLR skipped: High/Low columns not present")

    # ====================================================
    # Option B — Core Volume Indicators (MFI / CMF / OBV)
    # ====================================================
    # NOTE: Daily-only volume semantics are enforced at the data-fetch layer;
    # here we just require Volume to exist. If missing, create NA outputs.

    vol_col = "Volume" if "Volume" in df.columns else ("volume" if "volume" in df.columns else None)

    # --- MFI ---
    # Requires High/Low and Volume.
    if {"High", "Low"}.issubset(df.columns) and vol_col is not None:
        for length in cfg.get("MFI", []):
            l_i = int(length)
            if hasattr(ta, "mfi"):
                mfi_series = ta.mfi(
                    high=df["High"],
                    low=df["Low"],
                    close=price,
                    volume=df[vol_col],
                    length=l_i,
                )
            else:
                # If classic build differs, fail soft with NA series (keeps app stable)
                mfi_series = pd.Series(pd.NA, index=df.index)
            df[f"MFI_{l_i}"] = mfi_series
    else:
        for length in cfg.get("MFI", []):
            l_i = int(length)
            df[f"MFI_{l_i}"] = pd.NA

    # --- CMF ---
    # Requires High/Low and Volume.
    if {"High", "Low"}.issubset(df.columns) and vol_col is not None:
        for length in cfg.get("CMF", []):
            l_i = int(length)
            if hasattr(ta, "cmf"):
                cmf_series = ta.cmf(
                    high=df["High"],
                    low=df["Low"],
                    close=price,
                    volume=df[vol_col],
                    length=l_i,
                )
            else:
                cmf_series = pd.Series(pd.NA, index=df.index)
            df[f"CMF_{l_i}"] = cmf_series
    else:
        for length in cfg.get("CMF", []):
            l_i = int(length)
            df[f"CMF_{l_i}"] = pd.NA

    # --- OBV ---
    # OBV is single-series; rulebook param key is "0".
    if vol_col is not None:
        if hasattr(ta, "obv"):
            obv_series = ta.obv(close=price, volume=df[vol_col])
        else:
            obv_series = pd.Series(pd.NA, index=df.index)
        # Ensure OBV lands in a float-capable column to avoid pandas dtype warnings
        if "OBV" in df.columns:
            df["OBV"] = pd.to_numeric(df["OBV"], errors="coerce").astype("float64")
        obv_series = pd.to_numeric(obv_series, errors="coerce").astype("float64")
        df["OBV"] = obv_series

        # Required OBV smoothing aliases: OBV_smooth and OBV_smooth_20
        smooth_periods = cfg.get("OBV_SMOOTH", [20])
        # Canonical: OBV_smooth_20 is EMA(20) of OBV, and OBV_smooth aliases to it.
        for sp in smooth_periods:
            sp_i = int(sp)
            if df["OBV"].isna().all():
                df[f"OBV_smooth_{sp_i}"] = pd.NA
            else:
                df[f"OBV_smooth_{sp_i}"] = ta.ema(df["OBV"], length=sp_i)
        if "OBV_smooth_20" in df.columns:
            df["OBV_smooth"] = df["OBV_smooth_20"]
        else:
            # if config changed, still ensure OBV_smooth exists
            first = int(smooth_periods[0]) if smooth_periods else 20
            alias_col = f"OBV_smooth_{first}"
            df["OBV_smooth"] = df[alias_col] if alias_col in df.columns else pd.NA
    else:
        df["OBV"] = pd.NA
        df["OBV_smooth_20"] = pd.NA
        df["OBV_smooth"] = pd.NA

    return df
