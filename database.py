import sqlite3


# =========================================================
# CREATE DATABASE
# =========================================================

def create_database():

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    # =====================================================
    # USERS TABLE
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # =====================================================
    # BIO DATA TABLE
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS biodata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            dob TEXT,
            gender TEXT,
            education TEXT,
            occupation TEXT,
            salary REAL,
            address TEXT,
            financial_goal TEXT
        )
    """)

    # =====================================================
    # MONTHLY SALARY TABLE
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monthly_salary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            salary REAL NOT NULL,
            UNIQUE(username, year, month)
        )
    """)

    # =====================================================
    # EXPENSES TABLE
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)

    # =====================================================
    # SAVINGS TABLE
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS savings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            date TEXT,
            savings_type TEXT,
            amount REAL,
            description TEXT
        )
    """)

    connection.commit()
    connection.close()


# =========================================================
# USER FUNCTIONS
# =========================================================

def create_user(username, password):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username, password)
            VALUES (?, ?)
            """,
            (username, password)
        )

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        connection.close()


def check_login(username, password):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    connection.close()

    return user is not None


# =========================================================
# BIO DATA FUNCTIONS
# =========================================================

def save_biodata(
    username,
    full_name,
    email,
    phone,
    dob,
    gender,
    education,
    occupation,
    salary,
    address,
    financial_goal
):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO biodata
        (
            username,
            full_name,
            email,
            phone,
            dob,
            gender,
            education,
            occupation,
            salary,
            address,
            financial_goal
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        full_name,
        email,
        phone,
        str(dob),
        gender,
        education,
        occupation,
        salary,
        address,
        financial_goal
    ))

    connection.commit()
    connection.close()


def get_biodata(username):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM biodata
        WHERE username = ?
        """,
        (username,)
    )

    data = cursor.fetchone()

    connection.close()

    return data


# =========================================================
# MONTHLY SALARY FUNCTIONS
# =========================================================

def save_monthly_salary(
    username,
    year,
    month,
    salary
):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO monthly_salary
        (
            username,
            year,
            month,
            salary
        )
        VALUES (?, ?, ?, ?)
    """, (
        username,
        year,
        month,
        salary
    ))

    connection.commit()
    connection.close()


def get_monthly_salary(
    username,
    year,
    month
):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT salary
        FROM monthly_salary
        WHERE username = ?
        AND year = ?
        AND month = ?
        """,
        (
            username,
            year,
            month
        )
    )

    result = cursor.fetchone()

    connection.close()

    if result:

        return float(result[0])

    return None


# =========================================================
# EXPENSE FUNCTIONS
# =========================================================

def add_expense(
    username,
    expense_date,
    category,
    amount,
    description
):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (
            username,
            date,
            category,
            amount,
            description
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        str(expense_date),
        category,
        amount,
        description
    ))

    connection.commit()
    connection.close()


def get_expenses(username):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            date,
            category,
            amount,
            description
        FROM expenses
        WHERE username = ?
        ORDER BY date DESC
    """, (username,))

    expenses = cursor.fetchall()

    connection.close()

    return expenses


# =========================================================
# SAVING FUNCTIONS
# =========================================================

def add_saving(
    username,
    saving_date,
    saving_type,
    amount,
    description
):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO savings
        (
            username,
            date,
            savings_type,
            amount,
            description
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        str(saving_date),
        saving_type,
        amount,
        description
    ))

    connection.commit()
    connection.close()


def get_savings(username):

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            date,
            savings_type,
            amount,
            description
        FROM savings
        WHERE username = ?
        ORDER BY date DESC
    """, (username,))

    savings = cursor.fetchall()

    connection.close()

    return savings