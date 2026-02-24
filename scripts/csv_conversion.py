import pandas as pd  # add to pyproject

from model_train_protocol import Protocol
from model_train_protocol._internal.csv.conversion import CSVConversion


def main():

    local_path: str = f"C:\\Users\\Nikita\\Downloads\\ruby(4).csv"
    # local_path: str = "D:\\Nikita\\Documents\\work\\databiomes\\repos\\models\\landing_page_model\\landing_page_model_csv.csv"

    if local_path.endswith('.xlsx'):
        csv_data: pd.DataFrame = pd.read_excel(local_path)
    elif local_path.endswith('.csv'):
        csv_data: pd.DataFrame = pd.read_csv(local_path)
    else:
        raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")
    csv_conversion: CSVConversion = CSVConversion(csv_data=csv_data)
    protocol: Protocol = csv_conversion.to_mtp()
    protocol.save()
    protocol.template()

if __name__ == "__main__":
    main()