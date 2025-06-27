import unittest

import pandas as pd
import matplotlib
import matplotlib

from customer_segmentation.utils import functions


class TestPlots(unittest.TestCase):
    def test_plot_time_series(self):
        matplotlib.use("Agg")  # Backend, damit kein GUI-Fenster geöffnet wird
        df = pd.DataFrame(
            {"date": pd.date_range("2020-01-01", periods=3), "values": [1, 2, 3]}
        )
        try:
            functions.plot_time_series(df, x="date", y=["values"])
        except Exception as e:
            self.fail(f"Function raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
