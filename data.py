from typing import Dict, List, Any

import pandas as pd
from ex import db


def get_data(set=None):
    pass


def get_csv(data: pd.DataFrame):
    return data.to_csv()
