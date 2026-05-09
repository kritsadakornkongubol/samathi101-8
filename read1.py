import pandas as pd

# Define file paths
input_file = r"E:\projectcode\python\samathi101\test1.xlsx"
output_file = r"E:\projectcode\python\samathi101\test2.xlsx"

# Read the Excel file
df = pd.read_excel(input_file, sheet_name="Sheet1")

# Find all columns that match the given names
student_columns = [col for col in df.columns if "เลือกชื่อนักศึกษา" in col]
category_columns = [col for col in df.columns if "เลือกประเภทการบันทึกผล" in col]

# Merge all matching columns, ignoring blank values
df["เลือกชื่อนักศึกษา (รวม)"] = df[student_columns].astype(str).replace("nan", "").agg(lambda x: " ".join(x[x != ""]), axis=1)
df["เลือกประเภทการบันทึกผล (รวม)"] = df[category_columns].astype(str).replace("nan", "").agg(lambda x: " ".join(x[x != ""]), axis=1)

# Drop the original columns
df.drop(columns=student_columns + category_columns, inplace=True)

# Ensure Timestamp column exists and convert it to datetime
if "Timestamp" in df.columns:
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    # Create the "วันที่เรียน" column based on conditions
    def calculate_study_date(row):
        if pd.isna(row["Timestamp"]):
            return None  # Return None if Timestamp is missing

        date_part = row["Timestamp"].date()

        if row["เลือกประเภทการบันทึกผล (รวม)"] in ["บันทึกผลการเรียน", "บันทึกผลเรียนเสริม"]:
            return date_part if row["Timestamp"].hour >= 18 else date_part - pd.Timedelta(days=1)
        elif row["เลือกประเภทการบันทึกผล (รวม)"] == "การบ้าน":
            return date_part
        else:
            return None  # If none of the conditions match

    df["วันที่เรียน"] = df.apply(calculate_study_date, axis=1)

# Remove duplicate rows based on the key
def filter_rows(group):
    if any(group["เลือกประเภทการบันทึกผล (รวม)"].isin(["บันทึกผลการเรียน", "บันทึกผลเรียนเสริม"])):
        return group.nlargest(1, "Timestamp")  # Keep only the latest Timestamp
    elif any(group["เลือกประเภทการบันทึกผล (รวม)"].isin(["การบ้าน"])):
        return group.nlargest(2, "Timestamp")  # Keep the latest 2 rows
    return group  # If no condition matches, keep all rows

# Apply the filtering function to the dataframe
df_filtered = (
    df.groupby(["เลือกชื่อนักศึกษา (รวม)", "วันที่เรียน"], group_keys=False)
    .apply(filter_rows, include_groups=False)
    .reset_index(drop=True)  # Reset index to avoid multi-index issues
)

# Add the "เลือกชื่อนักศึกษา (รวม)" and "วันที่เรียน" columns to the existing columns in df_filtered
df_filtered["เลือกชื่อนักศึกษา (รวม)"] = df["เลือกชื่อนักศึกษา (รวม)"]
df_filtered["วันที่เรียน"] = df["วันที่เรียน"]

# print(df_filtered)
# Write to a new sheet in a new Excel file
with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    df_filtered.to_excel(writer, sheet_name="Sheet2", index=False)

print("Data processing complete. Output saved to test2.xlsx")
