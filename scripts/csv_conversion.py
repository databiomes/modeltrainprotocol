import pandas as pd

from model_train_protocol import Protocol
from model_train_protocol.csv import CSVConversion


def main():
    file_name: str = "databiomes_chat"
    # local_path: str = f"C:\\Users\\Nikita\\Downloads\\{file_name}.csv"
    local_path: str = f"D:\\Nikita\\Documents\\work\\databiomes\\repos\\models\\models\\landing_page_model\\{file_name}.csv"

    if local_path.endswith('.xlsx'):
        csv_data: pd.DataFrame = pd.read_excel(local_path)
    elif local_path.endswith('.csv'):
        csv_data: pd.DataFrame = pd.read_csv(local_path)
    else:
        raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")
    csv_conversion: CSVConversion = CSVConversion(csv_data=csv_data, protocol_name=file_name)
    protocol: Protocol = csv_conversion.to_mtp()
    protocol.save()
    protocol.template()


if __name__ == "__main__":
    main()
