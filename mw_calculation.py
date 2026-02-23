# Install required package (run this cell first if Biopython is not installed)
# !pip install biopython

from Bio import SeqIO
from google.colab import files
import pandas as pd

# 1️⃣ Upload the FASTA file
print("Please upload your FASTA file containing protein sequences.")
uploaded = files.upload()
fasta_file = list(uploaded.keys())[0]  # Get the name of the uploaded file

# 2️⃣ Approximate monoisotopic masses of amino acids (in Da)
aa_weights = {
    'A': 89.09, 'R': 174.20, 'N': 132.12, 'D': 133.10,
    'C': 121.15, 'E': 147.13, 'Q': 146.15, 'G': 75.07,
    'H': 155.16, 'I': 131.17, 'L': 131.17, 'K': 146.19,
    'M': 149.21, 'F': 165.19, 'P': 115.13, 'S': 105.09,
    'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15
}

# 3️⃣ Parse sequences and calculate molecular weight
results = []

for record in SeqIO.parse(fasta_file, "fasta"):
    seq = str(record.seq).upper()  # Ensure uppercase for consistency
    # Sum residue masses and subtract water for each peptide bond
    mw = sum(aa_weights.get(residue, 0) for residue in seq) - (len(seq) - 1) * 18.015
    results.append((record.id, len(seq), round(mw, 2)))  # (ID, length, MW)

# 4️⃣ Create DataFrame and display results
df = pd.DataFrame(results, columns=['ID', 'Length', 'MW_Da'])
print("\nCalculated Molecular Weights:")
display(df)  # In Colab, this shows a nice table

# Optional: Show basic statistics
print("\nSummary statistics:")
print(df['MW_Da'].describe())

# 5️⃣ Save to CSV and download
default_filename = "protein_molecular_weights.csv"

output_filename = input(
    f"Enter output filename (example: my_proteins.csv) or press Enter for default '{default_filename}': "
).strip()

if not output_filename:
    output_filename = default_filename

df.to_csv(output_filename, index=False, encoding='utf-8')
print(f"\nFile saved as: '{output_filename}'")

# Trigger download in Colab
files.download(output_filename)