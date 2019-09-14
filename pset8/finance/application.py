import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]
    rows = []
    portfolio_total = 0

    # Get amount of cash from users table, make a row: fill 4 fields of dict with "" and make "total": cash
    select_cash_res = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
    cash = float(select_cash_res[0]["cash"])
    portfolio_total += cash

    # Get dict of symbols and shares from portfolio table by SELECT
    symbols_and_shares = db.execute("SELECT symbol, shares FROM portfolio WHERE id = :user_id", user_id=user_id)
    if not symbols_and_shares:
        #rows.append({"symbol": "", "name":"", "shares":None, "price":None, "total": None })
        return render_template("index.html", cash=usd(cash), portfolio_total=usd(portfolio_total))
    else:

        # Make a list of dict to pass it to HTML page
        for i in range(len(symbols_and_shares)):

            # Access individual symbol and shares
            symbol = symbols_and_shares[i]["symbol"]
            shares = int(symbols_and_shares[i]["shares"])

            # Get name and current price from API via lookup()
            lookup_res = lookup(symbols_and_shares[i]["symbol"])
            name = lookup_res["name"]
            price = float(lookup_res["price"])

            # Get total price for each stock
            total = shares * price

            # Advance portfolio_total by total
            portfolio_total += total

            # Put all the information together into one dict
            rows.append({"symbol": symbol, "name": name, "shares": shares, "price": usd(price), "total": usd(total)})

    return render_template("index.html", rows=rows, cash=usd(cash), portfolio_total=usd(portfolio_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        user_id = session["user_id"]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if user provided symbol and shares
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol", 400)
        if not request.form.get("shares"):
            return apology("missing shares", 400)

        # Check if shares input is numeric integer
        if request.form.get("shares").isdecimal():
            return apology("input positive number", 400)
        shares = int(request.form.get("shares"))

        # Look up the symbol in API, ensure that it exists
        if not lookup(symbol):
            return apology("symbol does not exist", 400)
        lookup_res = lookup(symbol)

        # Get current price of 1 share
        price_of_one_share = float(lookup_res["price"])

        # Get current amount of cash
        cur_cash_res = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        if not cur_cash_res:
            return apology("could not access data", 400)
        cur_cash = float(cur_cash_res[0]["cash"])

        # Calculate shares price
        shares_price = shares * price_of_one_share

        # Ensure the user has enough cash to afford the stock
        if cur_cash < shares_price:
            return "can not afford"

        # If user already has shares of this symbol, update porfolio table. Otherwise insert new row into table
        check_portfolio_res = db.execute(
            "SELECT * FROM portfolio WHERE symbol = :symbol AND id = :user_id", symbol=symbol, user_id=user_id)
        if len(check_portfolio_res) != 0:
            db.execute(
                "UPDATE portfolio SET shares = shares + :shares, price = price + :shares_price, date_time = :date_time WHERE symbol = :symbol AND id = :user_id",
                shares=shares, shares_price=shares_price, date_time=timestamp, symbol=symbol, user_id=user_id)
        else:
            db.execute("INSERT INTO portfolio ('id', 'symbol', 'shares', 'price', 'date_time') VALUES (:user_id, :symbol, :shares, :price, :date_time)",
                       user_id=user_id, symbol=symbol, shares=shares, price=shares_price, date_time=timestamp)

        # Change shares_price value to negative 1) to insert action into transactions table and 2) to update amount of cash in users table
        shares_price = -(shares_price)

        # Insert the action with shares to transactions table
        db.execute(
            "INSERT INTO 'transactions' ('id', 'symbol', 'shares', 'price', 'date_time') VALUES (:user_id, :symbol, :shares, :price, :date_time)",
            user_id=user_id, symbol=symbol, shares=shares, price=shares_price, date_time=timestamp)

        # Update amount of cash in users table
        new_cash = cur_cash + shares_price
        db.execute(
            "UPDATE users SET cash = :new_cash WHERE id = :user_id",
            new_cash=new_cash, user_id=user_id)

        # Success for POST
        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    username = request.args.get("username")

    usernames = db.execute("SELECT username FROM users WHERE username = :username", username=username)
    if len(usernames) >= 1:
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    rows = db.execute("SELECT symbol, shares, price, date_time FROM transactions WHERE id = :user_id", user_id=session["user_id"])
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure user's input is provided
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol", 400)

        # Look up the symbol, ensure that it exists
        if not lookup(symbol):
            return apology("symbol does not exist", 400)
        lookup_res = lookup(symbol)

        stock_info = {'name': lookup_res['name'], 'symbol': lookup_res['symbol'], 'price': format(lookup_res['price'], '.2f')}
        return render_template("quote.html", stock_info=stock_info)

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        # Ensure username does not already exist in the .db
        rows_for_username = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if len(rows_for_username) != 0:
            return apology("username already exists. try another one", 400)

        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return apology("must provide password", 400)

        # Ensure passwords are the same in both text fields
        elif password != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Insert new user to table users
        result = db.execute(f"INSERT INTO users (username, hash) VALUES (:name, :hash_pwd)",
                            name=username, hash_pwd=generate_password_hash(password))

        # Check for failure (if couldn't insert to the .db)
        if not result:
            return apology("error. please try to register again", 400)

        # Query database for username to get new user's id and automatically log this user in
        rows_for_id = db.execute("SELECT * FROM users WHERE username = :username",
                                 username=username)

        # Remember which user has logged in
        session["user_id"] = rows_for_id[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        user_id = session["user_id"]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if user provided symbol and shares
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol", 400)
        if not request.form.get("shares"):
            return apology("missing shares", 400)

        # Check if shares input is numeric integer
        if request.form.get("shares").isdecimal() == False:
            return apology("input positive number", 400)
        shares = int(request.form.get("shares"))

        # Look up the symbol in API, ensure that it exists
        if not lookup(symbol):
            return apology("symbol does not exist", 400)
        lookup_res = lookup(symbol)

        # Get current price of 1 share
        price_of_one_share = float(lookup_res["price"])

        # Get current amount of cash
        cur_cash_res = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        if not cur_cash_res:
            return apology("could not access data", 400)
        cur_cash = float(cur_cash_res[0]["cash"])

        # Calculate price of shares
        shares_price = shares * price_of_one_share

        # Ensure the user has this amount of shares
        shares_amount_res = db.execute(
            "SELECT shares FROM portfolio WHERE symbol = :symbol AND id = :user_id", symbol=symbol, user_id=user_id)
        # If user does not have enough shares to sell
        if int(shares_amount_res[0]["shares"]) < shares:
            return apology(f"Can't sell. You only have {shares_amount_res[0]['shares']} shares", 400)

        # If users sells all the shares of 1 stock, remove the row from portfolio table. Otherwise update portfolio table
        if int(shares_amount_res[0]["shares"]) == shares:
            db.execute("DELETE FROM portfolio WHERE symbol = :symbol AND id = :user_id", symbol=symbol, user_id=user_id)

        elif int(shares_amount_res[0]["shares"]) > shares:
            db.execute(
                "UPDATE portfolio SET shares = shares - :shares, price = price + :shares_price, date_time = :date_time WHERE symbol = :symbol AND id = :user_id",
                shares=shares, shares_price=shares_price, date_time=timestamp, symbol=symbol, user_id=user_id)

        # Insert the action with shares to transactions table
        db.execute(
            "INSERT INTO 'transactions' ('id', 'symbol', 'shares', 'price', 'date_time') VALUES (:user_id, :symbol, :shares, :price, :date_time)",
            user_id=user_id, symbol=symbol, shares=shares, price=shares_price, date_time=timestamp)

        # Update amount of cash in users table
        new_cash = cur_cash + shares_price
        db.execute(
            "UPDATE users SET cash = :new_cash WHERE id = :user_id",
            new_cash=new_cash, user_id=user_id)

        # Success for POST
        flash("Sold!")
        return redirect("/")

    else:
        symbols_res = db.execute("SELECT symbol FROM portfolio WHERE id = :user_id", user_id=session["user_id"])
        return render_template("sell.html", symbols=symbols_res)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
