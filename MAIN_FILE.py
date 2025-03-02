#IMPORT THR REQUIRED LIBREARIES
from datetime import datetime
import pandas as pd
import os


#THESE CSV FILE PATHS UPLOADED FROM THE PC  
order_csv_file = "F:/CAFE_PROJECT/CAFE_PROJECT/CAFE_November_2023.csv"
MENU_CSV_PATH = "F:/CAFE_PROJECT/CAFE_PROJECT/menu_data.csv"
monthly_expenses_csv = "F:/CAFE_PROJECT/CAFE_PROJECT/monthly_expenses.csv"
aun_csv_file_path = "F:/CAFE_PROJECT/CAFE_PROJECT/Authanticate.csv" 


# FUNCTION FOR VALID USERNAME
def is_valid_username(name):
    if name.isalpha() or name.isspace():
        return name


# FUNCTION FOR VALID MOBILE NUMBER
def is_valid_mobile_number(mobile_number):
    starts = ("6", "7", "8", "9")
    final_mob = mobile_number.isdigit() and len(mobile_number) == 10 and mobile_number.startswith(starts)
    return final_mob


# FUNCTION FOR CREATING CSV FILE NAME BASED ON MONTH & YEAR
def csv_file_name():
    current_datetime = datetime.now()
    month_year = current_datetime.strftime("%B_%Y")
    return f"CAFE_{month_year}.csv"


#COLUMN NAMES
column_names = ["Order Date", "Order Time", "Order ID", "Customer Name", "Mobile No.", "Item Names", "Item Price","GST", "Final Price", "Payment Mode"]


#GENERATE THE CSV FILE NAMES
csv_file = csv_file_name()


# CHECK IF CSV FILE IS CREATED IN THE PC
def check_file_exists(csv_file):
    return os.path.exists(csv_file)


# CREATE A CSV FILE IF NOT CREATED IN THE PC
def create_csv_file(csv_file, column_names):
    if not check_file_exists(csv_file):
        with open(csv_file, 'w') as f:
            f.write(','.join(column_names))


# MAKE A DATAFRMAE FROM THE CSV FILE
def load_orders(csv_file):
    return pd.read_csv(csv_file)


# EXPORT THE DATAFRAME INTO THE CSV FILE
def save_orders(dataframe, csv_file):
    dataframe.to_csv(csv_file, index=False)
    
# MAKE A MENU DATAFRAME BY USING FUNCTION FROM THE CSV FILE
menu_df = load_orders(MENU_CSV_PATH)

# FUNCTION TO ADD A NEW ORDER ALSO ADD IN CSV FILE
def add_order():
    
    csv_file = csv_file_name()
    #IF CSV FILE IS NOT CREATED THEN CREATED BY THIS FUNCTION
    create_csv_file(csv_file, column_names)
    
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%d-%m-%Y")
    current_time = current_datetime.strftime("%H:%M:%S")
    only_date = current_datetime.strftime("%d")

    orders_df = load_orders(csv_file)
    orders_today = orders_df[orders_df["Order Date"] == current_date]

    # GENERATE THE ORDER ID
    if orders_today.empty:
        order_id = f"{only_date}_1"
    else:
        latest_order_id = orders_today["Order ID"].tolist()[-1]
        order_id_set = latest_order_id.split("_")
        order_id = f"{order_id_set[0]}_{int(order_id_set[1]) + 1}"

    while True:
        user_name = input("TYPE CUSTOMER NAME: ")
        if is_valid_username(user_name):
            break
        else:
            print("Invalid user name. Please try again.")

    while True:
        mob_no = input("TYPE CUSTOMER MOBILE NO.: ")
        if is_valid_mobile_number(mob_no):
            break
        else:
            print("Invalid mobile number. Please try again.")

    print("Menu:")
    print(menu_df[["Product ID", "Product Name", "Selling Price"]])

    order_items_no = input("TYPE CUSTOMER ORDER ITEM NO.: ")
    order_item_list = [int(item) for item in order_items_no.split(" ")]

    selected_menu = menu_df[menu_df['Product ID'].isin(order_item_list)][["Product ID", "Product Name", "Selling Price"]]
    item_dict = {}
    for item in order_item_list:
        item_dict[item] = "-".join(selected_menu[selected_menu['Product ID'] == item]['Product Name'].tolist())
    item_list =[ "-".join([item_dict[item] for item in order_item_list])]
    unique_item_prices = selected_menu.groupby('Product ID')['Selling Price'].first()
    item_price_list = [int(unique_item_prices.loc[item]) for item in order_item_list]
    item_price = sum(item_price_list)
    gst_price = item_price * 0.075
    final_price = item_price + gst_price

    while True:
        payment_mode = int(input("PAYMENT 1.ONLINE & 2.OFFLINE: "))
        if payment_mode in [1, 2]:
            break
        else:
            print("Choose Valid Option : ")

    if payment_mode == 1:
        payment_result = "ONLINE"
    else:
        payment_result = "OFFLINE"

    new_order_df = pd.DataFrame({
        "Order Date": [current_date],
        "Order Time": [current_time],
        "Order ID": [order_id],
        "Customer Name": [user_name],
        "Mobile No.": [mob_no],
        "Item Names": [item_list],
        "Item Price": [item_price],
        "GST": [gst_price],
        "Final Price": [final_price], 
        "Payment Mode": [payment_result],
    })

    orders_df = pd.concat([orders_df, new_order_df], ignore_index=True)
    save_orders(orders_df, csv_file)

    print(f"Order added successfully to {csv_file}.")


# FUNCTION FOR VIEWING ORDERS
def view_orders():
    csv_file = csv_file_name()

    with open(csv_file, mode='r') as csvfile:
        lines = csvfile.readlines()

        if len(lines) <= 1:
            print("No orders found.")
            
        header = lines[0].strip().split(',')
        
        orders = [line.strip().split(',') for line in lines[1:]]

        print("All Orders:")
        for order in orders:
            display_order(order, header)
            print("----------------------")

def display_order(order, header):
    print("\nOrder Details:")
    for key, value in zip(header, order):
        print(f"{key}: {value}")
        

# FUNCTION FOR UPDATE THE ORDER AND ALSO UPDATE THE CSV FILE
def update_order():

    csv_file_path = csv_file_name()     #HERE ORDER CSV FILE

    selected_columns = ['Order ID', 'Customer Name', 'Final Price']
    df = pd.read_csv(csv_file_path, usecols=selected_columns)
    print(df)

    order_id_to_update = input("Enter the Order ID to update: ")

    if not check_file_exists(csv_file):
        print("CSV file does not exist. No orders to update.")

    orders_df = load_orders(csv_file)

    if order_id_to_update in orders_df['Order ID'].values.tolist():
        order_index = orders_df[orders_df['Order ID'] == order_id_to_update].index[0]
        print("\nExisting Order Details:")
        display_order(orders_df.loc[order_index], orders_df.columns)

        while True:
            print("\n1. Update Customer Name\n2. Update Mobile Number\n3. Add/Update Items\n4. Change Payment Mode\n5. Exit")
            choice = input("Choose an option (1/2/3/4/5): ")

            if choice == "1":
                new_name = input("Enter the new customer name: ")
                if is_valid_username(new_name):
                    orders_df.at[order_index, "Customer Name"] = new_name
                    print("Customer name updated successfully.")
                else:
                    print("Invalid user name. Customer name not updated.")
            elif choice == "2":
                new_mobile = input("Enter the new mobile number: ")
                if is_valid_mobile_number(new_mobile):
                    orders_df.at[order_index, "Mobile No."] = new_mobile
                    print("Mobile number updated successfully.")
                else:
                    print("Invalid mobile number. Mobile number not updated.")
            elif choice == "3":
                print("Menu:")
                print(menu_df[["Product ID", "Product Name", "Selling Price"]])

                while True:
                    order_items_no = input("Enter the product IDs separated by space: ")
                    order_item_list = [int(item) for item in order_items_no.split()]

                    selected_menu = menu_df[menu_df['Product ID'].isin(order_item_list)][["Product ID", "Product Name", "Selling Price"]]
                    item_dict = {}
                    for item in order_item_list:
                        item_dict[item] = "-".join(selected_menu[selected_menu['Product ID'] == item]['Product Name'].tolist())
                    item_list =[ "-".join([item_dict[item] for item in order_item_list])]
                    unique_item_prices = selected_menu.groupby('Product ID')['Selling Price'].first()
                    item_price_list = [int(unique_item_prices.loc[item]) for item in order_item_list]
                    item_price = sum(item_price_list)
                    gst_price = item_price * 0.075
                    final_price = item_price + gst_price

                    orders_df.at[order_index, "Item Names"] = item_list
                    orders_df.at[order_index, "Item Price"] = item_price
                    orders_df.at[order_index, "GST"] = gst_price
                    orders_df.at[order_index, "Final Price"] = final_price

                    print("Product(s) added/updated in the order.")
                    break
                
            elif choice == "4":
                while True:
                    new_payment_mode = input("Enter the new payment mode (1.ONLINE / 2.OFFLINE): ")
                    if new_payment_mode in ["1", "2"]:
                        if new_payment_mode == "1":
                            payment_mode = "ONLINE" 
                        else:
                            payment_mode = "OFFLINE"
                        orders_df.at[order_index, "Payment Mode"] = payment_mode
                        break

                print("Payment mode updated in the order.")
            elif choice == "5":
                print("Exiting the order update process.")
                break
            else:
                print("Invalid choice. Please enter a valid choice.")
                continue

        save_orders(orders_df, csv_file)

    else:
        print(f"Order ID {order_id_to_update} not found in the orders.")
        
        

#MAKE DELETE FUNCTION 
def delete_order():

    csv_file = csv_file_name()

    selected_columns = ['Order ID', 'Customer Name', 'Final Price']
    df = pd.read_csv(csv_file, usecols=selected_columns)
    print(df)

    order_id_to_delete = input("Enter the Order ID to delete (15_1) : ")

    if not check_file_exists(csv_file):
        print("CSV file does not exist. No orders to delete.")
        return

    orders_df = load_orders(csv_file)

    if order_id_to_delete in orders_df['Order ID'].values.tolist():
        order_index = orders_df[orders_df['Order ID'] == order_id_to_delete].index[0]

        print("\nOrder to Delete:")
        display_order(orders_df.loc[order_index], orders_df.columns)
        
        confirmation = input("Do you want to delete this order? (y/n): ")
        
        if confirmation.lower() == "y" or confirmation.upper() == "Y":
            orders_df = orders_df.drop(order_index)
            save_orders(orders_df, csv_file)

            print(f"\nOrder with Order ID {order_id_to_delete} deleted successfully.")
        else:
            print(f"\nDeletion canceled. Order with Order ID {order_id_to_delete} not deleted.")
    else:
        print(f"Order ID {order_id_to_delete} not found in the orders.")

    


#CHANGE THE PASSWORD FUNCTION
def change_password():
    
    #HERE AUNTHTICATE CSV FILE PATH
    with open(aun_csv_file_path, mode='r') as file:
        lines = file.readlines()

    username = input("Enter the username: ")

    for i, line in enumerate(lines[1:]):  
        user_data = line.strip().split(',')
        if user_data[0] == username:
            new_password = input("Enter the new password: ")
            user_data[1] = new_password
            lines[i + 1] = ','.join(user_data) + '\n'


            with open(aun_csv_file_path, mode='w') as file:
                file.writelines(lines)

            print(f"Password for user '{username}' changed successfully.")

    print(f"User '{username}' not found in the CSV file.")



#ADD OR UPDATE OR DELETE PRODUCT MENU ITEMS

def read_menu_csv():
    if os.path.exists(MENU_CSV_PATH):
        with open(MENU_CSV_PATH, 'r') as file:
            header = next(file)
            menu_data = [line.strip().split(',') for line in file]
        return menu_data
    else:
        print("No CSV file found. Creating a new one...")


def write_menu_csv(menu_data):
    with open(MENU_CSV_PATH, 'w') as file:
        file.write("Product Category,Product ID,Product Name,Selling Price,Profit Price\n")
        for row in menu_data:
            file.write(','.join(row) + '\n')


def add_or_update_product():
    menu_data = read_menu_csv()
    
    print("\n1. Add Product")
    print("2. Update Product")
    print("3. Delete Product")
    print("4. Exit")

    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        add_product(menu_data)
    elif choice == "2":
        update_product(menu_data)
    elif choice == "3":
        delete_product_by_id()
    elif choice == "4":
        print("\nExiting...")
    else:
        print("Invalid choice. Please enter a valid option.")


def add_product(menu_data):
    product_category = input("Enter Product Category: ")
    product_name = input("Enter Product Name: ")
    selling_price = float(input("Enter Selling Price: "))
    profit_price = float(input("Enter Profit Price: "))

    new_product_id = str(int(len(menu_data)) + 1)
    new_row = [product_category, new_product_id, product_name, str(selling_price), str(profit_price)]

    menu_data.append(new_row)
    write_menu_csv(menu_data)
    print(f"\nProduct added successfully with Product ID: {new_product_id}")


def read_ID_name_menu_csv():
    if os.path.exists(MENU_CSV_PATH):
        with open(MENU_CSV_PATH, 'r') as file:
            lines = file.readlines()
        header = lines[0].strip().split(',')
        menu_data = [line.strip().split(',') for line in lines[1:]]
        #product_id_and_name = []
        #for row in menu_data:
            #product_id_and_name.append((row[1], row[2]))
        product_id_and_name = [(row[1], row[2]) for row in menu_data]
        print("Product ID\tProduct Name")
        for product in product_id_and_name:
            print(f"{product[0]}\t\t{product[1]}")
    else:
        print("No CSV file found. Creating a new one...")
    
    
def update_product(menu_data):
    read_ID_name_menu_csv()
    product_id_to_update = input("Enter Product ID to update: ")
    
    product_found = False
    for row in menu_data:
        if row[1] == product_id_to_update:
            product_found = True
            print(f"\nCurrent details for Product ID {product_id_to_update}:")
            print(','.join(row))

            product_category = input("Enter new product category (press Enter to keep the current value): ")
            product_name = input("Enter new product name (press Enter to keep the current value): ")
            selling_price = input("Enter new selling price (press Enter to keep the current value): ")
            profit_price = input("Enter new profit price (press Enter to keep the current value): ")

            if product_category:
                row[0] = product_category
            if product_name:
                row[2] = product_name
            if selling_price:
                row[3] = selling_price
            if profit_price:
                row[4] = profit_price
            break

    if not product_found:
        print(f"\nProduct ID {product_id_to_update} not found in the menu.")

    write_menu_csv(menu_data)

    if product_found:
        print(f"\nProduct updated successfully with Product ID {product_id_to_update}.")


#MAKE A DELETE MENU FUNCTION
def del_read_menu_csv():
    if os.path.exists(MENU_CSV_PATH):
        with open(MENU_CSV_PATH, 'r') as file:
            lines = file.readlines()
        header, menu_data = lines[0].strip().split(','), [line.strip().split(',') for line in lines[1:]]
        return header, menu_data
    else:
        print("No CSV file found. Creating a new one...")
        return None

def del_write_menu_csv(header, menu_data):
    with open(MENU_CSV_PATH, 'w') as file:
        file.write(','.join(header) + '\n')
        file.writelines([','.join(row) + '\n' for row in menu_data])

def delete_product_by_id():
    header, menu_data = del_read_menu_csv()

    if menu_data is not None:
        print("Product ID\tProduct Name")
        for row in menu_data:
            print(f"{row[1]}\t\t{row[2]}")

        product_id_to_delete = input("Enter the Product ID to delete: ")
        found = any(row[1] == product_id_to_delete for row in menu_data)

        if found:
            confirm_delete = input("Do you want to delete this product? (y/n): ").lower()
            if confirm_delete == 'y':
                menu_data = [row for row in menu_data if row[1] != product_id_to_delete]
                print(f"Product with ID {product_id_to_delete} deleted successfully.")
            else:
                print("Deletion canceled.")
        else:
            print(f"No product found with ID {product_id_to_delete}.")

        del_write_menu_csv(header, menu_data)



#MAKE A FUNCTION FOR VISULIZATION

#FOR PATICULAR DAY
def day():
    order_csv_file_path = "F:/CAFE_PROJECT/CAFE_PROJECT/CAFE_November_2023.csv"     #HERE ORDER CSV FILE

    selected_day = input("Enter the desired day (e.g., '14'): ")
    with open(order_csv_file_path, 'r') as file:
        lines = file.readlines()
        header = lines[0].strip().split(',')
        day_index = header.index('Order Date')
        item_names_index = header.index('Item Names')
        all_product_names = []
        for line in lines[1:]:
            values = line.strip().split(',')
            day = values[day_index].split('-')[0]
            item_names = values[item_names_index].replace("[", "").replace("]", "").replace("'", "").split('-')
            if day == selected_day:
                all_product_names.extend(item_names)
    product_counts = {}

    for product in all_product_names:
        if product in product_counts:
            product_counts[product] += 1
        else:
            product_counts[product] = 1

    menu_dict = read_menu_csv_vis()
    result_df_list = []

    for product, count in product_counts.items():
        if product in menu_dict:
            profit_price = menu_dict[product]
            total_profit = count * profit_price
            result_df_list.append({'Product': product, 'Count': count, 'Total Profit': total_profit})
        else:
            print(f"{product}: Profit information not available in the menu")

    result_df = pd.concat([pd.DataFrame([item]) for item in result_df_list], ignore_index=True)

    print(result_df)

#READ MENU CSV FILE FUNCTION
def read_menu_csv_vis():

    menu_csv_file = "F:/CAFE_PROJECT/CAFE_PROJECT/menu_data.csv"      #HERE MENU CSV FILE

    product_info = {}

    with open(menu_csv_file, 'r') as file:
        lines = file.readlines()
        headers = lines[0].strip().split(',')
        product_name_index = headers.index('Product Name')
        profit_price_index = headers.index('Profit Price')


        for line in lines[1:]:
            # Split the line by commas
            values = line.strip().split(',')
            product_name = values[product_name_index]
            profit_price = float(values[profit_price_index]) 
            product_info[product_name] = profit_price

    return product_info


#FOR A PARTICULAR MONTH
def month():
    order_csv_file_path = "F:/CAFE_PROJECT/CAFE_PROJECT/CAFE_November_2023.csv"    #HERE ORDER CSV FILE

    with open(order_csv_file_path, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()
        header = lines[0].strip().split(',')
        item_names_index = header.index('Item Names')

        all_product_names = []

        for line in lines[1:]:
            values = line.strip().split(',')
            item_names = values[item_names_index].replace("[", "").replace("]", "").replace("'", "").split('-')
            all_product_names.extend(item_names)

    product_counts = {}

    for product in all_product_names:
        if product in product_counts:
            product_counts[product] += 1
        else:
            product_counts[product] = 1

    menu_dict = read_menu_csv_vis()

    result_df_list = []

    for product, count in product_counts.items():
        if product in menu_dict:
            profit_price = menu_dict[product]
            total_profit = count * profit_price
            result_df_list.append({'Product': product, 'Count': count, 'Total Profit': total_profit})
        else:
            print(f"{product}: Profit information not available in the menu")

    result_df = pd.concat([pd.DataFrame([item]) for item in result_df_list], ignore_index=True)

    print(result_df)


#MANAGE THE VISUALIZATION FUNCTION
def main_visualization():
    while True:
        print("1. Day\n2. Month\n3. Exit")
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            day()
        elif choice == '2':
            month()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")



#FUNCTION FOR CHECK PROFITS
#FOR PATICULAR DAY
def day():
    order_csv_file_path = "F:/CAFE_PROJECT/CAFE_PROJECT/CAFE_November_2023.csv"     #HERE ORDER CSV FILE

    selected_day = input("Enter the desired day (e.g., '14'): ")
    with open(order_csv_file_path, 'r') as file:
        lines = file.readlines()
        header = lines[0].strip().split(',')
        day_index = header.index('Order Date')
        item_names_index = header.index('Item Names')
        all_product_names = []
        for line in lines[1:]:
            values = line.strip().split(',')
            day = values[day_index].split('-')[0]
            item_names = values[item_names_index].replace("[", "").replace("]", "").replace("'", "").split('-')
            if day == selected_day:
                all_product_names.extend(item_names)
    product_counts = {}

    for product in all_product_names:
        if product in product_counts:
            product_counts[product] += 1
        else:
            product_counts[product] = 1

    menu_dict = read_menu_csv_vis()
    result_df_list = []

    for product, count in product_counts.items():
        if product in menu_dict:
            profit_price = menu_dict[product]
            total_profit = count * profit_price
            result_df_list.append({'Product': product, 'Count': count, 'Total Profit': total_profit})
        else:
            print(f"{product}: Profit information not available in the menu")

    result_df = pd.concat([pd.DataFrame([item]) for item in result_df_list], ignore_index=True)

    print(result_df)

#READ MENU CSV FILE FUNCTION
def read_menu_csv_vis():

    menu_csv_file = "F:/CAFE_PROJECT/CAFE_PROJECT/menu_data.csv"      #HERE MENU CSV FILE

    product_info = {}

    with open(menu_csv_file, 'r') as file:
        lines = file.readlines()
        headers = lines[0].strip().split(',')
        product_name_index = headers.index('Product Name')
        profit_price_index = headers.index('Profit Price')


        for line in lines[1:]:
            # Split the line by commas
            values = line.strip().split(',')
            product_name = values[product_name_index]
            profit_price = float(values[profit_price_index]) 
            product_info[product_name] = profit_price

    return product_info


#FOR A PARTICULAR MONTH
def month():
    order_csv_file_path = "F:/CAFE_PROJECT/CAFE_PROJECT/CAFE_November_2023.csv"    #HERE ORDER CSV FILE

    with open(order_csv_file_path, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()
        header = lines[0].strip().split(',')
        item_names_index = header.index('Item Names')

        all_product_names = []

        for line in lines[1:]:
            values = line.strip().split(',')
            item_names = values[item_names_index].replace("[", "").replace("]", "").replace("'", "").split('-')
            all_product_names.extend(item_names)

    product_counts = {}

    for product in all_product_names:
        if product in product_counts:
            product_counts[product] += 1
        else:
            product_counts[product] = 1

    menu_dict = read_menu_csv_vis()

    result_df_list = []

    for product, count in product_counts.items():
        if product in menu_dict:
            profit_price = menu_dict[product]
            total_profit = count * profit_price
            result_df_list.append({'Product': product, 'Count': count, 'Total Profit': total_profit})
        else:
            print(f"{product}: Profit information not available in the menu")

    result_df = pd.concat([pd.DataFrame([item]) for item in result_df_list], ignore_index=True)

    print(result_df)


#MANAGE THE VISUALIZATION FUNCTION
def main_visualization():
    while True:
        print("1. Day\n2. Month\n3. Exit")
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            day()
        elif choice == '2':
            month()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")



#FUNCTION FOR CHECK PROFITS
def month_sum(csv_file_path):
    df = pd.read_csv(csv_file_path)
    item_names = df['Item Names'].str.replace("[", "").str.replace("]", "").str.replace("'", "", regex=False).str.split('-')
    
    all_product_names = [product for item in item_names for product in item]

    menu_dict = read_menu_csv_vis()

    total_profit_sum = 0

    for product in all_product_names:
        if product in menu_dict:
            profit_price = menu_dict[product]
            total_profit_sum += profit_price

    return total_profit_sum



def add_month_to_expenses(month_csv_path):
    # Check if the month already exists in the expenses CSV
    df_expenses = pd.read_csv("F:/CAFE_PROJECT/CAFE_PROJECT/monthly_expenses.csv")      #HERE MONTHLY_EXPENSE FILE

    # Get the month name from the CSV file path
    month_name = pd.to_datetime(month_csv_path, format="F:/CAFE_PROJECT/CAFE_PROJECT/CAFE_%B_%Y.csv").strftime('%B')

    if month_name in df_expenses["Month"].values:
        print(f"{month_name} data already exists in monthly_expenses.csv. Skipping...")
        return

    # Get user input for expenses
    food_ingredients = float(input("Enter food ingredients cost: "))
    worker_salary = float(input("Enter worker salary cost: "))
    light_bill = float(input("Enter light bill cost: "))
    maintenance = float(input("Enter maintenance cost: "))
    rent = float(input("Enter rent cost: "))
    other_money = float(input("Enter other expenses: "))

    # Calculate total profit for the month
    total_profit = month_sum(month_csv_path)

    # Calculate net profit
    net_profit = total_profit - (food_ingredients + worker_salary + light_bill + maintenance + rent + other_money)

    # Create a DataFrame with the values
    df = pd.DataFrame({
        "Month": [month_name],
        "All Profit": [total_profit],
        "Food Ingredients": [food_ingredients],
        "Light Bill": [light_bill],
        "Worker Salary": [worker_salary],
        "Maintenance": [maintenance],
        "Rent": [rent],
        "Other Money": [other_money],
        "Net Profit": [net_profit]
    })

    # Append the DataFrame to the CSV file
    df.to_csv("monthly_expenses.csv", mode='a', header=False, index=False)
    print("Values added successfully to monthly_expenses.csv")


def update_monthly_expenses(month_expenses_path):
    # Read the existing data from the CSV file
    df_expenses = pd.read_csv(month_expenses_path)

    # Get user input for the month to update
    update_month = input("Enter the month to update: ")

    # Check if the specified month exists in the DataFrame
    if update_month not in df_expenses["Month"].values:
        print(f"{update_month} data does not exist in {month_expenses_path}.")
        return

    # Display the current values for the specified month
    current_row = df_expenses[df_expenses["Month"] == update_month]
    print("Current values:")
    print(current_row)

    # Fetch 'All Profit' from the month_sum function
    all_profit_value = month_sum(f"CAFE_{update_month}_2023.csv")

    # Update values for individual columns excluding 'All Profit' and 'Net Profit'
    columns_to_update = df_expenses.columns[2:-1]  # Exclude the 'Month', 'All Profit', and 'Net Profit' columns

    # Take new values as input for each column
    new_values = [float(input(f"Enter new value for {column}: ")) for column in columns_to_update]

    # Update the values in the DataFrame
    df_expenses.loc[df_expenses["Month"] == update_month, columns_to_update] = new_values

    # Update 'All Profit' value
    df_expenses.loc[df_expenses["Month"] == update_month, 'All Profit'] = all_profit_value

    # Calculate 'Net Profit' after updating values
    new_sum = df_expenses.loc[df_expenses["Month"] == update_month, columns_to_update].sum(axis=1).values[0]
    df_expenses.loc[df_expenses["Month"] == update_month, 'Net Profit'] = all_profit_value - new_sum

    # Write the updated data back to the CSV file
    df_expenses.to_csv(month_expenses_path, index=False)

    print(f"\n{update_month} data updated successfully in {month_expenses_path}")


def display_monthly_expenses(month_expenses_path):
    try:
        df_expenses = pd.read_csv(month_expenses_path)
        print("\nMonthly Expenses:")
        print(df_expenses)
    except FileNotFoundError:
        print(f"{month_expenses_path} not found. No data to display.")


def check_profits():
    while True:
        print("\n1. Add Month to Expenses\n2. Update Monthly Expenses\n3. Display Monthly Expenses\n4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            # Example usage:
            month_csv_path = "F:/CAFE_PROJECT/CAFE_PROJECT/CAFE_November_2023.csv"      #HERE CAFE NOVEMBER FILE
            CAFE_November_2023_csv_path = "F:/CAFE_PROJECT/CAFE_PROJECT/CAFE_November_2023.csv"     #HERE CAFE NOVEMBER FILE
            add_month_to_expenses(CAFE_November_2023_csv_path)
        elif choice == '2':
            monthly_expenses_csv_path = "F:/CAFE_PROJECT/CAFE_PROJECT/monthly_expenses.csv"
            update_monthly_expenses(monthly_expenses_csv_path)
        elif choice == '3':
            monthly_expenses_csv_path = "F:/CAFE_PROJECT/CAFE_PROJECT/monthly_expenses.csv" 
            display_monthly_expenses(monthly_expenses_csv_path)
        elif choice == '4':
            print("Exit")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

# FUNCTION FOR DISPLAYING THE MAIN MENU FOR WORKERS
def display_worker_menu():
    while True:
        print("\nMenu Options:")
        print("1. Add Order")
        print("2. View Orders")
        print("3. Update Orders")
        print("4. Delete Orders")
        print("5. Exit")
        
        user_menu = input("SELECT OPTION FROM MENU: ")

        if user_menu == "1":
            add_order()
        elif user_menu == "2":
            view_orders()
        elif user_menu == "3":
            update_order()
        elif user_menu == "4":
            delete_order()
        elif user_menu == "5":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please select a valid option.")
 

            
 # FUNCTION FOR DISPLAYING THE OWNER MENU
def display_owner_menu():
    while True:
        print("\nOwner Menu:")
        print("1. Change Password")
        print("2. Change/Update/Delete Product")
        print("3. Display Analysis")
        print("4. Check Profits")
        print("5. Exit")
        owner_menu_choice = int(input("SELECT OPTION FROM OWNER MENU: "))
    
        if owner_menu_choice == 1:
            change_password()
        elif owner_menu_choice == 2:
            add_or_update_product()
        elif owner_menu_choice == 3:
            main_visualization()
        elif owner_menu_choice == 4:
            check_profits()
        elif owner_menu_choice == 5:
            print("Exiting...")
            break
        else:
            print("Invalid option. Please select a valid option.")
            
            

#AUNTHATICATE THE USER
def authenticate_user(csv_file_path):

    while True:
        entered_username = input("Enter your username: ")
        entered_password = input("Enter your password: ")

        with open(csv_file_path, mode='r') as file:
            lines = file.readlines()

        for line in lines[1:]:
            user_data = line.strip().split(',')
            if user_data[0] == entered_username and user_data[1] == entered_password:
                return entered_username

        print("Invalid credentials. Try again.")

    return None


def display_menu(username):
    if username == "worker":
        display_worker_menu()
    elif username == "owner":
       display_owner_menu()
    else:
        print("Invalid username.")


authenticated_username = authenticate_user(aun_csv_file_path)

if authenticated_username:
    display_menu(authenticated_username)
else:
    print("Authentication failed. Invalid username or password.")
    

            





