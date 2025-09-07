import math
from statistics import median

class PriceSuggestorAgent:
    CONDITION_MULTIPLIER = {"Like New": 1.0, "Good": 0.9, "Fair": 0.75}
    CATEGORY_BASE = {
        "Mobile": 0.30, "Laptop": 0.30, "Electronics": 0.28,
        "Camera": 0.25, "Furniture": 0.20, "Fashion": 0.40
    }

    def __init__(self, df):
        self.df = df.copy()

    def _find_similar(self, category, brand=None):
        subset = self.df[self.df['category'].str.lower() == category.lower()]
        if brand:
            same_brand = subset[subset['brand'].str.lower() == brand.lower()]
            if len(same_brand) >= 2:
                return same_brand
        return subset

    def _baseline_price(self, similar_df):
        prices = similar_df['asking_price'].dropna().tolist()
        if prices:
            return float(median(prices))
        return None

    def _annual_depr(self, category):
        return self.CATEGORY_BASE.get(category, 0.30)

    def suggest(self, payload):
        category = payload.get("category")
        brand = payload.get("brand")
        age_months = int(payload.get("age_months", 0))
        condition = payload.get("condition", "Good")

        similar = self._find_similar(category, brand)
        baseline = self._baseline_price(similar)

        if not baseline:
            return {"error": f"No comparable data found for category '{category}'"}

        annual_depr = self._annual_depr(category)
        years = age_months / 12.0
        remaining_value = baseline * ((1 - annual_depr) ** years)
        remaining_value *= self.CONDITION_MULTIPLIER.get(condition, 0.9)

        lower = max(math.floor(remaining_value * 0.85), math.floor(baseline * 0.10))
        upper = math.ceil(remaining_value * 1.10)

        return {
            "fair_price_range": f"₹{lower:,} – ₹{upper:,}",
            "estimated_value_point": f"₹{int(round(remaining_value)):,}",
            "reasoning": (
                f"Baseline price from similar '{category}' listings "
                f"(brand: {brand if brand else 'any'}): ₹{baseline:,.0f}. "
                f"Applied {annual_depr*100:.0f}% annual depreciation over {age_months} months "
                f"and condition adjustment '{condition}'."
            )
        }
