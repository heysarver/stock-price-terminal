import yfinance as yf
import shutil
import curses

def fetch_stock_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    historical_data = stock.history().tail(2)
    current_price = round(historical_data['Close'].iloc[-1], 2)
    previous_price = round(historical_data['Close'].iloc[-2], 2)
    price_change = round(current_price - previous_price, 2)
    percent_change = "{:.2f}".format((price_change / previous_price) * 100)
    return current_price, price_change, percent_change

def display_stock_data(stdscr):
    stock_symbols = ['AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'SPY', 'QQQ', 'IWM']
    stock_symbols.sort()
    half_length = len(stock_symbols) // 2
    first_half_symbols = stock_symbols[:half_length]
    second_half_symbols = stock_symbols[half_length:]
    previous_data = {symbol: (0, 0, 0) for symbol in stock_symbols}
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.nodelay(True)
    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
        stdscr.clear()
        terminal_width, _ = shutil.get_terminal_size((20, 20))
        stdscr.addstr(0, 0, "#" * terminal_width, curses.color_pair(3))
        stdscr.addstr(1, 0, "## Welcome to the Stock Data Terminal User Interface ##".center(terminal_width), curses.color_pair(3))
        stdscr.addstr(2, 0, "#" * terminal_width, curses.color_pair(3))
        stdscr.addstr(3, 0, "| Ticker    Price     Change    % Change  | Ticker    Price     Change    % Change  |".center(terminal_width), curses.color_pair(3))
        stdscr.addstr(4, 0, "#" * terminal_width, curses.color_pair(3))
        stock_data_list = []
        for i in range(half_length):
            stock1_data = fetch_stock_data(first_half_symbols[i])
            stock2_data = fetch_stock_data(second_half_symbols[i])
            stock_data_list.append((first_half_symbols[i], stock1_data, second_half_symbols[i], stock2_data))
        for idx, stock_data in enumerate(stock_data_list, start=5):
            price_color1 = curses.color_pair(1) if stock_data[1][0] > previous_data[stock_data[0]][0] else curses.color_pair(2)
            price_color2 = curses.color_pair(1) if stock_data[3][0] > previous_data[stock_data[2]][0] else curses.color_pair(2)
            change_color1 = curses.color_pair(1) if stock_data[1][1] >= 0 else curses.color_pair(2)
            change_color2 = curses.color_pair(1) if stock_data[3][1] >= 0 else curses.color_pair(2)
            start_col = ((terminal_width - 86) // 2)
            stdscr.addstr(idx, start_col, "| ", curses.color_pair(3))
            stdscr.addstr(idx, start_col + 2, f"{stock_data[0]:<9}", curses.color_pair(3))
            stdscr.addstr(idx, start_col + 12, f"{stock_data[1][0]:<9.2f}", price_color1)
            stdscr.addstr(idx, start_col + 22, f"{stock_data[1][1]:<9.2f} {stock_data[1][2]}%", change_color1)
            stdscr.addstr(idx, start_col + 42, "| ", curses.color_pair(3))
            stdscr.addstr(idx, start_col + 44, f"{stock_data[2]:<9}", curses.color_pair(3))
            stdscr.addstr(idx, start_col + 54, f"{stock_data[3][0]:<9.2f}", price_color2)
            stdscr.addstr(idx, start_col + 64, f"{stock_data[3][1]:<9.2f} {stock_data[3][2]}%", change_color2)
            stdscr.addstr(idx, start_col + 84, "|", curses.color_pair(3))
            previous_data[stock_data[0]] = stock_data[1]
            previous_data[stock_data[2]] = stock_data[3]
        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(display_stock_data)
