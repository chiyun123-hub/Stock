import os

# Trust the corporate TLS-inspection root cert (see .certs/combined_ca_bundle.pem)
os.environ["CURL_CA_BUNDLE"] = os.path.join(os.path.dirname(__file__), ".certs", "combined_ca_bundle.pem")

import yfinance as yf

os.makedirs("data", exist_ok=True)

# Download 5 years of daily AAPL data
df = yf.download("AAPL", period="5y", interval="1d")
df.to_csv("data/aapl_5y.csv")

print("Saved data/aapl_5y.csv")
