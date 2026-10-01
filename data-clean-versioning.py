import pandas as pd
import boto3
from datetime import date

# ==============================
# 1. Load raw CSV
# ==============================
raw_path = "Mlops_house_predication_raw_data.csv"

df = pd.read_csv(raw_path)

print("=========== Before Cleaning ============")
print(df.isnull().sum())
print(f"Shape Before : {df.shape}")

# ==============================
# 2. Clean data
# ==============================
df_clean = df.dropna()

print("\n=========== After Cleaning ============")
print(df_clean.isnull().sum())
print(f"Shape After : {df_clean.shape}")

# ==============================
# 3. Save cleaned CSV locally
# ==============================
clean_path = "Mlops_house_predication_clean_v1.csv"

df_clean.to_csv(clean_path, index=False)

print(f"\nCleaned file saved locally: {clean_path}")

# ==============================
# 4. Connect to S3
# ==============================
s3 = boto3.client("s3")

BUCKET = "mlops-house-prediction"

def upload_processed_data(local_path):

    key = f"processed/{date.today()}/Mlops_house_predication_clean_v1.csv"

    s3.upload_file(
        local_path,
        BUCKET,
        key
    )

    print(f"\nUploaded successfully!")
    print(f"s3://{BUCKET}/{key}")

    return key


# ==============================
# 5. Upload to S3
# ==============================
upload_processed_data(clean_path)