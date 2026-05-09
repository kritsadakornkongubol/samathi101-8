import pandas as pd

# Sample data as a DataFrame (replace with pd.read_excel("input1.xlsx") for your file)
# For demonstration, I'm using a simplified version of your data
# data = pd.DataFrame({
#     "Timestamp": ["2024-11-03 15:57:49.406", "2024-11-03 20:22:37.362"],
#     "เลือกกลุ่มของนักศึกษา": ["กลุ่ม G3", "กลุ่ม G2"],
#     "เลือกชื่อนักศึกษา": ["338 ภัสสรรัชต์ กฤษณะโลม", ""],
#     "เลือกชื่อนักศึกษา.1": ["", "217 ภัคจิรา ชัยเพชรโยธิน"],
#     "เลือกประเภทการบันทึกผล": ["บันทึกผลการเรียน", ""],
#     "เลือกประเภทการบันทึกผล.1": ["", "บันทึกผลการเรียน"],
#     "บันทึกผล [ฟังบรรยายพระอาจารย์หลวงพ่อ]": ["ทำแล้ว", ""],
#     "บันทึกผล [ฟังทบทวนบรรยาย]": ["ทำแล้ว", ""],
#     "บันทึกผล [เดินจงกรม 30 นาที]": ["ทำแล้ว", "ทำแล้ว"],
#     "บันทึกผล [เดินจงกรม 30 นาที].1": ["", ""],
#     "บันทึกผล [นั่งสมาธิ 30 นาที]": ["ทำแล้ว", "ทำแล้ว"],
#     "บันทึกผล [นั่งสมาธิ 30 นาที].1": ["", ""]
# })

data = pd.read_excel("test1.xlsx")

# Function to extract base name (remove suffixes like ".1", ".2", etc.)
def get_base_name(col_name):
    return col_name.split(".")[0] if "." in col_name else col_name

# Identify unique base column names
base_names = set(get_base_name(col) for col in data.columns)

# Dictionary to store merged columns
merged_data = {}

# Process each base name dynamically
for base_name in base_names:
    # Find all columns that match this base name (including suffixed ones)
    related_cols = [col for col in data.columns if get_base_name(col) == base_name]
    
    if len(related_cols) > 1:  # If there are multiple columns to merge
        # Merge by taking the first non-empty value across rows
        merged_data[base_name] = data[related_cols].bfill(axis=1).iloc[:, 0].fillna("")
    else:
        # If no duplicates, just copy the column as-is
        merged_data[base_name] = data[related_cols[0]]

# Create a new DataFrame with merged columns
merged_df = pd.DataFrame(merged_data)

# Reorder columns to match the original logical order (optional)
column_order = [
    "Timestamp", "เลือกกลุ่มของนักศึกษา", "เลือกชื่อนักศึกษา", "เลือกประเภทการบันทึกผล",
    "บันทึกผล [ฟังบรรยายพระอาจารย์หลวงพ่อ]", "บันทึกผล [ฟังทบทวนบรรยาย]",
    "บันทึกผล [เดินจงกรม 30 นาที]", "บันทึกผล [นั่งสมาธิ 30 นาที]"
]
merged_df = merged_df[column_order]

# Write to a new Excel file
merged_df.to_excel("output.xlsx", sheet_name="MergedData", index=False)

print("Merged data has been written to 'output.xlsx'. Here’s a preview:")
print(merged_df.head())