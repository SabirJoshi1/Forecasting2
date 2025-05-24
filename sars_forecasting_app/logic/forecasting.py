import numpy as np
from statsmodels.tsa.arima.model import ARIMA

def train_arimax_model(log_sales, exog, split=(0.8, 0.9)):
    n = len(log_sales)
    train_end, val_end = int(n * split[0]), int(n * split[1])
    train_y, val_y = log_sales[:train_end], log_sales[train_end:val_end]
    train_exog, val_exog = exog[:train_end], exog[train_end:val_end]

    model = ARIMA(train_y, order=(2, 1, 2), exog=train_exog)
    model_fit = model.fit()
    forecast_log = model_fit.forecast(steps=len(val_y), exog=val_exog)

    return forecast_log, val_y, model_fit, train_end, val_end