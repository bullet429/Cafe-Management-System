import pandas as pd

class CafeCsvFile:
    def _init_(self):
        pass

    def authenticate_csv(self):
        user_data = [["worker", "123"], ["owner", "456"]]
        file_path = "Authanticate.csv"
        with open(file_path, mode='w') as file:
            file.write("Username,Password\n")
            for row in user_data:
                file.write(','.join(row) + '\n')
        print("Authentication CSV file created successfully.")

    def menu_csv(self):
        menu_data = {
            "Product Category": ["Tea and Coffee"] * 5 + ["Snacks"] * 5 + ["Burgers and Sandwiches"] * 5,
            "Product ID": [x for x in range(1, 16)],
            "Product Name": ["KADAK CHAI", "BLACK TEA", "GREEN TEA", "BLACK COFFEE", "BLACK COFFEE",
                             "MAGGI", "CHEESE MAGGI", "SALAD WRAPS", "SPICY PANEER WRAPS", "FRENCH FRIES SALTED",
                             "VEG. BURGER", "CHEESE & VEG. BURGER", "GRILLED SANDWICHES", "ITALIAN SANDWICHES", "MEXICAN SANDWICHES"],
            "Selling Price": ["15", "15", "20", "20", "30", "60", "80", "80", "90", "70", "45", "60", "50", "80", "90"],
            "Profit Price": ["5", "5", "6", "4", "8", "15", "20", "18", "30", "25", "10", "15", "18", "20", "25"]}
        
        menu_df = pd.DataFrame(menu_data)
        file_path = "menu_data.csv"
        menu_df.to_csv(file_path, index=False)
        print("Menu CSV file created successfully.")

    def create_csv_file(self, file_path):
        fields = ["Month", "All Profit", "Food Ingredients", "Light Bill", "Worker Salary", "Maintenance", "Rent", "Other Money", "Net Profit"]
        with open(file_path, 'w') as csv_file:
            csv_file.write(','.join(fields) + '\n')

        print(f"Monthly profit CSV file created successfully at {file_path}")


cafe_manager = CafeCsvFile()


cafe_manager.authenticate_csv()
cafe_manager.menu_csv()


csv_file_path = "monthly_expenses.csv"
cafe_manager.create_csv_file(csv_file_path)

print("cuugc b ")