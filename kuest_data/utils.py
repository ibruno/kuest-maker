import json
import pandas as pd

from kuest_utils.postgres_utils import fetch_sheet_df

def pretty_print(txt, dic):
    print("\n", txt, json.dumps(dic, indent=4))

def _filter_question(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty or "question" not in df.columns:
        return pd.DataFrame()
    question = df["question"].fillna("").astype(str)
    return df[question != ""].reset_index(drop=True)


def get_sheet_df():
    """
    Fetch market configuration and hyperparameters from Postgres.
    """
    df = _filter_question(fetch_sheet_df("Selected Markets"))
    df2 = _filter_question(fetch_sheet_df("All Markets"))

    if df.empty or df2.empty:
        result = pd.DataFrame()
    else:
        result = df.merge(df2, on="question", how="inner")

    params_df = fetch_sheet_df("Hyperparameters")
    records = params_df.to_dict(orient="records") if not params_df.empty else []
    hyperparams, current_type = {}, None

    for r in records:
        # Update current_type only when we have a non-empty type value
        # Handle both string and NaN values from pandas
        type_value = r.get("type")
        if type_value and str(type_value).strip() and str(type_value) != "nan":
            current_type = str(type_value).strip()
        
        # Skip rows where we don't have a current_type set
        if current_type and r.get("param") is not None:
            # Convert numeric values to appropriate types
            value = r.get("value")
            try:
                # Try to convert to float if it's numeric
                if isinstance(value, str) and value.replace(".", "").replace("-", "").isdigit():
                    value = float(value)
                elif isinstance(value, (int, float)):
                    value = float(value)
            except (ValueError, TypeError):
                pass  # Keep as string if conversion fails

            hyperparams.setdefault(current_type, {})[r["param"]] = value

    return result, hyperparams
