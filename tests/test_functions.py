import unittest
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 


class TestPlotTimeSeries(unittest.TestCase):
    def test_function_runs(self):
        # Dummy-Dataframe
        import pandas as pd
        import matplotlib
        matplotlib.use('Agg')  # Backend, damit kein GUI-Fenster geöffnet wird
        df = pd.DataFrame({"date": pd.date_range('2020-01-01', periods=3), "values": [1,2,3]})
        try:
            plot_time_series(df, x='date', y=['values'])
        except Exception as e:
            self.fail(f"Function raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()


def plot_time_series(df: pd.DataFrame, x: str, y: list, n_cols = 2) -> None:
   
    size = [(i, j) for i in range(len(y)-1) for j in range(len(y)-1) if j <= 1 and i <= 1]    
    rows = len(size) // n_cols

    _, axes = plt.subplots(rows, n_cols, figsize=(len(size)**2, len(size)+2))  
  
    for s, col in zip(size, y):
        i, j = s      
        sns.lineplot(data=df, x=x, y=col, ax=axes[i, j])
        axes[i, j].set_title(f'{col} | {x}')
        axes[i, j].xaxis.set_major_locator(mdates.MonthLocator(interval=2)) 
        axes[i, j].xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
        axes[i, j].set_xlabel("")
       
    plt.tight_layout()
    plt.show()