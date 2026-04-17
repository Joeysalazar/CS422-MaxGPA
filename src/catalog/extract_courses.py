import csv
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parents[2]
    input_file = repo_root / "data" / "raw" / "pub_rec_master_w2016-f2025.csv"
    output_file = repo_root / "data" / "processed" / "course_inventory.csv"

    unique_courses = {}
    rows_read = 0

    with input_file.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            rows_read += 1

            subj = row.get("SUBJ", "").strip()
            numb = row.get("NUMB", "").strip()
            title = row.get("TITLE", "").strip()

            if not subj or not numb:
                continue

            key = (subj, numb)

            if key not in unique_courses:
                unique_courses[key] = title

    with output_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["SUBJ", "NUMB", "TITLE"])

        for subj, numb in sorted(unique_courses.keys()):
            writer.writerow([subj, numb, unique_courses[(subj, numb)]])

    print(f"Read {rows_read} rows")
    print(f"Wrote {len(unique_courses)} unique courses to {output_file}")


if __name__ == "__main__":
    main()