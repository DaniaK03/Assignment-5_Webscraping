import pandas as pd

def clean_data():
    file_name = "ebay_tech_deals.csv"
    cleaned_file = "cleaned_ebay_deals.csv"
    
    try:
        df = pd.read_csv(file_name, dtype=str)
    except FileNotFoundError:
        print("Raw data file not found.")
        return
 
    def clean_price(value):
        if isinstance(value, str):
            value = value.replace("US $", "").replace("$", "").replace(",", "").strip()
            return float(value) if value.replace(".", "").isdigit() else None
        return None

    df['price'] = df['price'].apply(clean_price)
    df['original_price'] = df['original_price'].apply(clean_price)

    df['original_price'].fillna(df['price'], inplace=True)

    df["discount_percentage"] = ((df["original_price"] - df["price"]) / df["original_price"]) * 100
    df["discount_percentage"] = df["discount_percentage"].round(2)  


    df["discount_percentage"].fillna(0, inplace=True)


    df['shipping'] = df['shipping'].str.strip()
    df['shipping'].replace(["", "N/A"], "Shipping info unavailable", inplace=True)

    
    df.to_csv(cleaned_file, index=False)
    print("Cleaned data saved to", cleaned_file)

if __name__ == "__main__":
    clean_data()
