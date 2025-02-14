from config import connect_to_db
from datetime import datetime
import psycopg2

# Function to add an expense
def add_expense(amount, category, description):
    try:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO expenses (amount, category, description, date) VALUES (%s, %s, %s, %s)",
                       (amount, category, description, date))
        
        conn.commit()
        print("✅ Expense added successfully!")
    
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
    
    finally:
        conn.close()

# Function to view all expenses
def view_expenses():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        expenses = cursor.fetchall()

        print("\n📌 All Expenses:")
        if expenses:
            for expense in expenses:
                print(expense)  # Format: (id, amount, category, description, date)
        else:
            print("ℹ️ No expenses found.")

    except psycopg2.Error as e:
        print(f"❌ Error retrieving expenses: {e}")
    
    finally:
        conn.close()

# Function to show category-wise expense summary
def category_wise_expense():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC")
        summary = cursor.fetchall()

        print("\n📌 Category-wise Expense Summary:")
        if summary:
            for category, total in summary:
                print(f"📂 {category}: ₹{total}")
        else:
            print("ℹ️ No expenses found.")

    except psycopg2.Error as e:
        print(f"❌ Error retrieving category summary: {e}")
    
    finally:
        conn.close()

# Function to show monthly expense summary
def monthly_expense_summary():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("SELECT DATE_TRUNC('month', date) AS month, SUM(amount) FROM expenses GROUP BY month ORDER BY month DESC")
        summary = cursor.fetchall()

        print("\n📌 Monthly Expense Summary:")
        if summary:
            for month, total in summary:
                print(f"📅 {month.strftime('%B %Y')}: ₹{total}")
        else:
            print("ℹ️ No expenses found.")

    except psycopg2.Error as e:
        print(f"❌ Error retrieving monthly summary: {e}")
    
    finally:
        conn.close()

# Function to delete a specific expense
def delete_expense(expense_id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM expenses WHERE id = %s RETURNING id", (expense_id,))
        deleted_id = cursor.fetchone()

        if deleted_id:
            conn.commit()
            print(f"✅ Expense with ID {expense_id} deleted successfully!")
        else:
            print("⚠️ Expense not found!")

    except psycopg2.Error as e:
        print(f"❌ Error deleting expense: {e}")
    
    finally:
        conn.close()

# Function to delete all expenses (reset table)
def delete_all_expenses():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("TRUNCATE TABLE expenses RESTART IDENTITY;")
        conn.commit()

        print("✅ All expenses deleted! Table reset.")

    except psycopg2.Error as e:
        print(f"❌ Error resetting table: {e}")
    
    finally:
        conn.close()

# Function to create expenses table (Run once)
def create_table():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
                category VARCHAR(50) NOT NULL,
                description TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        print("✅ Table created successfully!")

    except psycopg2.Error as e:
        print(f"❌ Error creating table: {e}")
    
    finally:
        conn.close()

# Function to handle invalid input
def get_valid_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("⚠️ Please enter a positive number.")
            else:
                return value
        except ValueError:
            print("⚠️ Invalid input! Please enter a valid number.")

# Main menu
def main():
    create_table()  # Ensure table exists before using the app
    
    while True:
        print("\n=== Expense Tracker ===")
        print("1️⃣ Add Expense")
        print("2️⃣ View Expenses")
        print("3️⃣ View Category-wise Expense Summary")
        print("4️⃣ View Monthly Expense Summary")
        print("5️⃣ Delete an Expense (by ID)")
        print("6️⃣ Delete All Expenses")
        print("7️⃣ Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            amount = get_valid_number("Enter amount: ₹")
            category = input("Enter category (Food, Transport, Education, Entertainment, Dress, Trip): ")
            description = input("Enter description: ")
            add_expense(amount, category, description)

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            category_wise_expense()

        elif choice == "4":
            monthly_expense_summary()

        elif choice == "5":
            view_expenses()  # Show existing expenses
            try:
                expense_id = int(input("Enter the ID of the expense to delete: "))
                delete_expense(expense_id)
            except ValueError:
                print("⚠️ Invalid ID! Please enter a valid number.")

        elif choice == "6":
            confirm = input("⚠️ Are you sure? This will delete ALL expenses (y/n): ")
            if confirm.lower() == "y":
                delete_all_expenses()

        elif choice == "7":
            print("👋 Exiting... Have a great day!")
            break

        else:
            print("⚠️ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
