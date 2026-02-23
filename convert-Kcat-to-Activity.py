import pandas as pd
from google.colab import files

# 1️⃣ Upload the input CSV file
uploaded = files.upload()
csv_file = list(uploaded.keys())[0]  # Get the filename of the uploaded file

# 2️⃣ Try reading the file with different encodings to handle common issues
encodings = ['utf-8', 'latin1', 'cp1252']
df = None

for enc in encodings:
    try:
        df = pd.read_csv(csv_file, encoding=enc)
        print(f"File successfully read with encoding: {enc} ✅")
        break
    except Exception as e:
        print(f"Reading with {enc} failed ❌ ({str(e)})")

if df is None:
    raise ValueError("Could not read the CSV file with any of the tried encodings.")

# Show the available columns for verification
print("\nAvailable columns in the DataFrame:")
print(df.columns.tolist())

# 3️⃣ Calculate specific activity (μmol TPA / min / mg enzyme)
# Formula: activity = (kcat in s⁻¹ × 60) / MW in g/mol (Da)
df["activity (μmol/min·mg)"] = df["kcat [s^(-1)]"] * 60 / df["MW_Da"]

# Optional: Preview the first few rows of the result
print("\nFirst 5 rows after adding activity column:")
print(df.head())

# 4️⃣ Save the updated DataFrame and download it
output_file = "calculated_activity.csv"
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"\nOutput file saved as: {output_file}")

files.download(output_file)