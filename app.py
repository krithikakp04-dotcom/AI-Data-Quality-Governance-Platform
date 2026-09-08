from data_ingestion import ingest_data

df = ingest_data("dataset.csv")

print("\nDataset Preview:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)