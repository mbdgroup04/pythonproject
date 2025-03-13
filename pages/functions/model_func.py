import pickle
import pandas as pd

class model_func:
    def __init__(self):
        self.model_dict = {
        "AAPL": pickle.load(open("models/picklemodel_AAPL.pkl", "rb")),
        "AMZN": pickle.load(open("models/picklemodel_AMZN.pkl", "rb")),
        "GOOG": pickle.load(open("models/picklemodel_GOOG.pkl", "rb")),
        "MSFT": pickle.load(open("models/picklemodel_MSFT.pkl", "rb")),
        "TSLA": pickle.load(open("models/picklemodel_TSLA.pkl", "rb"))
        }
    

    def get_predictions(self, ticker, cl_price:list):
        return self.model_dict[ticker].predict(cl_price)