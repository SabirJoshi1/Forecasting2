import numpy as np
from sklearn.metrics import mean_squared_error

def calculate_kpis(forecast_log, val_y):
    forecast = np.expm1(forecast_log)
    actual = np.expm1(val_y)
    rmse = np.sqrt(mean_squared_error(actual, forecast))
    return forecast, actual, rmse

def compute_inventory(forecast):
    safety_stock = forecast.std() * 1.5
    recommended_stock = forecast + safety_stock
    return safety_stock, recommended_stock