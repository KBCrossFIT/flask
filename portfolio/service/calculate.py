import pandas as pd
import FinanceDataReader as fdr
from flask import Flask, request, jsonify
from config import api_key
import openai

from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier

# OpenAI API Key 설정
openai.api_key = api_key

app = Flask(__name__)



