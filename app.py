from flask import Flask, render_template_string, request
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    stock_ticker = request.form.get('ticker', 'PETR4.SA')
    stock = yf.Ticker(stock_ticker)
    info = stock.info
    
    # Get historical market data for the last 52 weeks
    hist = stock.history(period="52wk")
    
    # Plot the closing values
    plt.figure(figsize=(10, 5))
    plt.plot(hist.index, hist['Close'], label='Close Price')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title(f'Closing Prices for {stock_ticker} (Last 52 Weeks)')
    plt.legend()
    
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Encode the plot to base64 string
    plot_data = base64.b64encode(buf.read()).decode('utf-8')
    
    # Select key information about the health of the company
    key_info = {
        'Market Cap': info.get('marketCap'),
        'Enterprise Value': info.get('enterpriseValue'),
        'Trailing P/E': info.get('trailingPE'),
        'Forward P/E': info.get('forwardPE'),
        'PEG Ratio': info.get('pegRatio'),
        'Price/Sales': info.get('priceToSalesTrailing12Months'),
        'Price/Book': info.get('priceToBook'),
        'Enterprise Value/Revenue': info.get('enterpriseToRevenue'),
        'Enterprise Value/EBITDA': info.get('enterpriseToEbitda'),
        'Profit Margin': info.get('profitMargins'),
        'Operating Margin': info.get('operatingMargins'),
        'Return on Assets': info.get('returnOnAssets'),
        'Return on Equity': info.get('returnOnEquity'),
        'Revenue': info.get('totalRevenue'),
        'Gross Profit': info.get('grossProfits'),
        'EBITDA': info.get('ebitda'),
        'Net Income': info.get('netIncomeToCommon')
    }
    
    # Create a summary of the stock based on key information
    summary = f"""
    The stock {stock_ticker} has a market capitalization of {key_info['Market Cap']} and an enterprise value of {key_info['Enterprise Value']}.
    It has a trailing P/E ratio of {key_info['Trailing P/E']} and a forward P/E ratio of {key_info['Forward P/E']}.
    The PEG ratio is {key_info['PEG Ratio']}, indicating its growth potential.
    The price-to-sales ratio is {key_info['Price/Sales']} and the price-to-book ratio is {key_info['Price/Book']}.
    The company has an enterprise value to revenue ratio of {key_info['Enterprise Value/Revenue']} and an enterprise value to EBITDA ratio of {key_info['Enterprise Value/EBITDA']}.
    The profit margin is {key_info['Profit Margin']} and the operating margin is {key_info['Operating Margin']}.
    The return on assets is {key_info['Return on Assets']} and the return on equity is {key_info['Return on Equity']}.
    The total revenue is {key_info['Revenue']}, with a gross profit of {key_info['Gross Profit']} and an EBITDA of {key_info['EBITDA']}.
    The net income to common shareholders is {key_info['Net Income']}.
    """
    
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Stock Information</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <style>
                body {
                    padding: 20px;
                }
                .card {
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="text-center">Stock Information</h1>
                <form method="post" class="text-center mb-4">
                    <input type="text" name="ticker" placeholder="Enter Stock Ticker" class="form-control" style="max-width: 300px; margin: 0 auto;">
                    <button type="submit" class="btn btn-primary mt-2">Get Info</button>
                </form>
                <div class="card">
                    <div class="card-body">
                        <h2>Closing Prices (Last 52 Weeks)</h2>
                        <img src="data:image/png;base64,{{ plot_data }}" alt="Closing Prices">
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h2>Key Information for {{ stock_ticker }}</h2>
                        <ul class="list-group">
                            {% for key, value in key_info.items() %}
                                <li class="list-group-item">
                                    <strong>{{ key }}:</strong> {{ value }}
                                </li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h2>Summary</h2>
                        <p>{{ summary }}</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
    ''', stock_ticker=stock_ticker, key_info=key_info, plot_data=plot_data, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
