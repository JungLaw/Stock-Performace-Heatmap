# signals_loader.py

import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


class RulesRepository:
    """
    Loads and manages access to hierarchical master_rules.json.

    Structure assumed (based on your Step A/B/C):
      {
        "version": "...",
        "categories": {
          "Trend": {
            "SMA": {
              "params": [[10], [20], ...],
              "feature_scopes": {
                "heatmap": { "10": { ...rule_block... }, ... },
                "overlay": { ... },
                "alerts": { ... },
                "custom": { ... },
                "tiles": { ... },
                "MVA": { ... },
                "basic_signals": { ... }
              },
              "metadata": { ... }
            },
            ...
          },
          ...
        }
      }
    """

    def __init__(self, rules: Dict[str, Any]):
        self.rules = rules
        self.categories: Dict[str, Dict[str, Any]] = rules.get("categories", {})
        # Build flat index: indicator_name_lower -> (category_name, indicator_dict)
        self._indicator_index: Dict[str, Tuple[str, Dict[str, Any]]] = {}
        self._build_index()

    @classmethod
    def from_file(cls, path: str | Path) -> "RulesRepository":
        path = Path(path)
        with path.open("r", encoding="utf-8") as f:
            rules = json.load(f)
        return cls(rules)

    def _build_index(self) -> None:
        for cat_name, indicators in self.categories.items():
            for ind_name, ind_data in indicators.items():
                key = ind_name.lower()
                self._indicator_index[key] = (cat_name, ind_data)

    # ---------- basic accessors ----------

    def get_indicator(self, indicator_name: str) -> Optional[Dict[str, Any]]:
        """
        Returns the indicator block by its name (case-insensitive), across all categories.
        """
        key = indicator_name.lower()
        entry = self._indicator_index.get(key)
        if entry is None:
            return None
        _, ind = entry
        return ind

    def get_indicator_with_category(self, indicator_name: str) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        Returns (category_name, indicator_block) for the given indicator name.
        """
        key = indicator_name.lower()
        return self._indicator_index.get(key)

    def get_feature_scope(
        self,
        indicator_name: str,
        feature_scope: str = "heatmap"
    ) -> Optional[Dict[str, Any]]:
        """
        Returns the feature_scopes[feature_scope] dict:
          { param_key: rule_block, ... }
        """
        ind = self.get_indicator(indicator_name)
        if not ind:
            return None
        scopes = ind.get("feature_scopes", {})
        return scopes.get(feature_scope)

    def get_rule_block(
        self,
        indicator_name: str,
        feature_scope: str,
        param_key: str
    ) -> Optional[Dict[str, Any]]:
        """
        Returns the rule block for a given (indicator, scope, param_key).
        Example for heatmap:
          repo.get_rule_block("RSI", "heatmap", "14")
        """
        feature = self.get_feature_scope(indicator_name, feature_scope)
        if not feature:
            return None
        return feature.get(param_key)

    def list_indicators(self) -> Dict[str, str]:
        """
        Returns a dict: indicator_name -> category_name
        """
        return {ind: cat for ind, (cat, _) in self._indicator_index.items()}

    def list_params(self, indicator_name: str) -> list[str]:
        """
        Return the list of param keys derived from params (e.g. ["10","14","21","30"])
        """
        ind = self.get_indicator(indicator_name)
        if not ind:
            return []
        param_list = ind.get("params", [])
        keys = []
        for p in param_list:
            # p is a list like [14] or [12,26,9] or [20,2.0]
            key = "_".join(str(x) for x in p)
            keys.append(key)
        return keys