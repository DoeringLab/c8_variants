import sys
import pandas as pd

valid_chr_names = [
    'CP022321.1','CP022322.1','CP022323.1','CP022324.1','CP022325.1',
    'CP022326.1','CP022327.1','CP022328.1','CP022329.1','CP022330.1',
    'CP022331.1','CP022332.1','CP022333.1','CP022334.1','CP022335.1'
]

seqlengths = [
    2291500, 1621676, 1574972, 1084805, 1814975, 1422463, 1399209,
    1398693, 1186813, 1059962, 1562107, 774060, 756017, 942472, 24923
]

seqname_to_seqlength = dict(zip(valid_chr_names, seqlengths))

def validate_bed(file_path):
    try:
        # Load the BED file
        bed = pd.read_csv(file_path, sep='\t', header=None, comment='#')

        # Check for minimum required columns (chrom, start, end, ., 0, .)
        if bed.shape[1] != 6:
            raise ValueError("BED6 file must have exactly 6 columns")

        # Check if start and end columns are integers
        if not pd.api.types.is_integer_dtype(bed[1]) or not pd.api.types.is_integer_dtype(bed[2]):
            raise ValueError("Start and end columns must be integers")

        # Check if start < end
        if not (bed[1] < bed[2]).all():
            raise ValueError("Start positions must be less than the end positions")

        # Check if chromosome names are valid
        if not bed[0].isin(valid_chr_names).all():
            raise ValueError("Invalid chromosome names found in the BED file")

        # Check if start values are >= 0 and <= corresponding seqlengths
        for idx, row in bed.iterrows():
            chrom = row[0]
            start = row[1]
            end = row[2]
            if start < 0 or start > seqname_to_seqlength[chrom]:
                raise ValueError(f"Start position out of bounds for chromosome {chrom} at row {idx + 1}")
            if end < 0 or end > seqname_to_seqlength[chrom]:
                raise ValueError(f"End position out of bounds for chromosome {chrom} at row {idx + 1}")

        # Check that columns 3, 4, and 5 have the values ".", "0", and "." respectively
        if not (bed[3] == '.').all():
            raise ValueError("Column 3 must have the value '.'")
        if not (bed[4] == 0).all():
            raise ValueError("Column 4 must have the value '0'")
        if not (bed[5] == '.').all():
            raise ValueError("Column 5 must have the value '.'")

        print("BED file is valid.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_bed.py <path_to_bed_file>")
        sys.exit(1)

    bed_file_path = sys.argv[1]
    validate_bed(bed_file_path)

