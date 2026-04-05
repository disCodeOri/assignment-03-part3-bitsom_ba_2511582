# Part 3: Product Explorer & Error-Resilient Logger
# Fetches product data from DummyJSON API, saves to files, and handles errors properly.

import requests
import sys
import io
from datetime import datetime

# Fixing rupee/special character display on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Logging errors with timestamp to error_log.txt (used across all tasks)
def log_error(source, error_type, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ERROR in {source}: {error_type} — {message}\n"
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"  (Logged to error_log.txt)")


# Task 1: File Read & Write Basics
print("=" * 60)
print("TASK 1 — File Read & Write Basics")
print("=" * 60)

notes = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes."
]

# Writing the five given lines using write mode
with open("python_notes.txt", "w", encoding="utf-8") as f:
    for line in notes:
        f.write(line + "\n")
print("File written successfully.")

# Appending two of my own lines
with open("python_notes.txt", "a", encoding="utf-8") as f:
    f.write("Topic 6: Functions help in reusing code and keeping things modular.\n")
    f.write("Topic 7: File handling is essential for reading and saving data.\n")
print("Lines appended.")

# Reading the file back and printing each line numbered
print("\n--- Reading python_notes.txt ---")
with open("python_notes.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    print(f"{i}. {line.strip()}")

print(f"\nTotal number of lines: {len(lines)}")

# Asking user for a keyword and searching case-insensitively
keyword = input("\nEnter a keyword to search in notes: ").strip()
matches = [line.strip() for line in lines if keyword.lower() in line.lower()]

if matches:
    print(f"Lines containing '{keyword}':")
    for m in matches:
        print(f"  - {m}")
else:
    print(f"No lines found containing '{keyword}'.")


# Task 2: API Integration
print("\n" + "=" * 60)
print("TASK 2 — API Integration")
print("=" * 60)

# Step 1 — Fetching 20 products
print("\n--- Step 1: Fetch and Display Products ---")
products = []
try:
    response = requests.get("https://dummyjson.com/products?limit=20", timeout=10)
    if response.status_code == 200:
        data = response.json()
        products = data["products"]

        # Printing as a formatted table
        print(f"{'ID':<4}| {'Title':<31}| {'Category':<14}| {'Price':<9}| {'Rating'}")
        print("-" * 4 + "|" + "-" * 31 + "|" + "-" * 14 + "|" + "-" * 9 + "|" + "-" * 7)
        for p in products:
            print(f"{p['id']:<4}| {p['title']:<30}| {p['category']:<13}| ${p['price']:<8}| {p['rating']}")
    else:
        print(f"Unexpected status code: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
    log_error("fetch_products", "ConnectionError", "No connection could be made")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
    log_error("fetch_products", "Timeout", "Request timed out")
except Exception as e:
    print(f"An error occurred: {e}")
    log_error("fetch_products", type(e).__name__, str(e))

# Step 2 — Keeping only those with rating >= 4.5, sorting by price descending
print("\n--- Step 2: Filter (rating >= 4.5) & Sort by Price ---")
if products:
    filtered = [p for p in products if p["rating"] >= 4.5]
    filtered.sort(key=lambda x: x["price"], reverse=True)

    if filtered:
        print(f"{'ID':<4}| {'Title':<31}| {'Price':<9}| {'Rating'}")
        print("-" * 4 + "|" + "-" * 31 + "|" + "-" * 9 + "|" + "-" * 7)
        for p in filtered:
            print(f"{p['id']:<4}| {p['title']:<30}| ${p['price']:<8}| {p['rating']}")
    else:
        print("No products found with rating >= 4.5.")
else:
    print("Skipped — no products were fetched.")

# Step 3 — Fetching all laptops from the laptops category
print("\n--- Step 3: Search by Category (Laptops) ---")
try:
    response = requests.get("https://dummyjson.com/products/category/laptops", timeout=10)
    if response.status_code == 200:
        laptops = response.json()["products"]
        for laptop in laptops:
            print(f"  {laptop['title']} — ${laptop['price']}")
    else:
        print(f"Unexpected status code: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
    log_error("search_laptops", "ConnectionError", "No connection could be made")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
    log_error("search_laptops", "Timeout", "Request timed out")
except Exception as e:
    print(f"An error occurred: {e}")
    log_error("search_laptops", type(e).__name__, str(e))

# Step 4 — Sending a POST request to simulate adding a product
print("\n--- Step 4: POST Request (Simulated) ---")
new_product = {
    "title": "My Custom Product",
    "price": 999,
    "category": "electronics",
    "description": "A product I created via API"
}

try:
    response = requests.post("https://dummyjson.com/products/add", json=new_product, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
    log_error("add_product", "ConnectionError", "No connection could be made")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
    log_error("add_product", "Timeout", "Request timed out")
except Exception as e:
    print(f"An error occurred: {e}")
    log_error("add_product", type(e).__name__, str(e))


# Task 3: Exception Handling
print("\n" + "=" * 60)
print("TASK 3 — Exception Handling")
print("=" * 60)

# Part A — safe_divide catches division by zero and wrong types
print("\n--- Part A: Guarded Calculator ---")

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print(f"safe_divide(10, 2) = {safe_divide(10, 2)}")
print(f"safe_divide(10, 0) = {safe_divide(10, 0)}")
print(f'safe_divide("ten", 2) = {safe_divide("ten", 2)}')

# Part B — Reading file with proper error handling and finally block
print("\n--- Part B: Guarded File Reader ---")

def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"Successfully read '{filename}' ({len(content)} characters).")
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    finally:
        print("File operation attempt complete.")

print("\nTesting with 'python_notes.txt':")
read_file_safe("python_notes.txt")

print("\nTesting with 'ghost_file.txt':")
read_file_safe("ghost_file.txt")

# Part C — Already done in Task 2, all API calls have try-except
print("\n--- Part C: Robust API Calls ---")
print("All API calls in Task 2 are wrapped with try-except handling for")
print("ConnectionError, Timeout, and general exceptions.")

# Part D — Asking user for product IDs until they type quit
print("\n--- Part D: Product Lookup Loop ---")
while True:
    user_input = input("Enter a product ID to look up (1–100), or 'quit' to exit: ").strip()

    if user_input.lower() == "quit":
        print("Exiting product lookup.")
        break

    # Making sure input is actually a number
    try:
        product_id = int(user_input)
    except ValueError:
        print("Warning: Please enter a valid integer.")
        continue

    if product_id < 1 or product_id > 100:
        print("Warning: ID must be between 1 and 100.")
        continue

    # Fetching the product by ID
    try:
        response = requests.get(f"https://dummyjson.com/products/{product_id}", timeout=10)
        if response.status_code == 200:
            product = response.json()
            print(f"  Product: {product['title']} — ${product['price']}")
        elif response.status_code == 404:
            print("Product not found.")
            log_error("lookup_product", "HTTPError", f"404 Not Found for product ID {product_id}")
        else:
            print(f"Unexpected status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("lookup_product", "ConnectionError", "No connection could be made")
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("lookup_product", "Timeout", "Request timed out")
    except Exception as e:
        print(f"An error occurred: {e}")
        log_error("lookup_product", type(e).__name__, str(e))


# Task 4: Logging to File
print("\n" + "=" * 60)
print("TASK 4 — Logging to File")
print("=" * 60)

# Triggering a ConnectionError on purpose using a fake URL
print("\n--- Triggering ConnectionError (fake URL) ---")
try:
    requests.get("https://thisurldoesnotexist12345.com/api", timeout=5)
except requests.exceptions.ConnectionError as e:
    print("Connection failed. Please check your internet.")
    log_error("fetch_products", "ConnectionError", "No connection could be made")
except requests.exceptions.Timeout:
    print("Request timed out.")
    log_error("fetch_products", "Timeout", "Request timed out")
except Exception as e:
    print(f"Error: {e}")
    log_error("fetch_products", type(e).__name__, str(e))

# Triggering a 404 by requesting product ID 999 which doesn't exist
print("\n--- Triggering 404 Error (product ID 999) ---")
try:
    response = requests.get("https://dummyjson.com/products/999", timeout=10)
    if response.status_code == 404:
        print("Product not found (404).")
        log_error("lookup_product", "HTTPError", "404 Not Found for product ID 999")
    else:
        print(f"Status: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
    log_error("lookup_product", "ConnectionError", "No connection could be made")
except Exception as e:
    print(f"Error: {e}")
    log_error("lookup_product", type(e).__name__, str(e))

# Printing everything that got logged
print("\n--- Contents of error_log.txt ---")
with open("error_log.txt", "r", encoding="utf-8") as f:
    print(f.read())

print("=" * 60)
print("All tasks complete!")
print("=" * 60)
