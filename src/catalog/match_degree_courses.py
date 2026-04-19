import csv
import sys
from pathlib import Path


def normalize_title(title):
    return " ".join(title.lower().replace("&", "and").split())


def load_course_inventory(file_path):
    inventory = {}

    with file_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            subj = row.get("SUBJ", "").strip()
            numb = row.get("NUMB", "").strip()
            title = row.get("TITLE", "").strip()

            if not subj or not numb:
                continue

            inventory[(subj, numb)] = title

    return inventory


def load_degree_plan(file_path):
    degree_courses = []

    with file_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            year = row.get("YEAR", "").strip()
            term = row.get("TERM", "").strip()
            subj = row.get("SUBJ", "").strip()
            numb = row.get("NUMB", "").strip()
            title = row.get("TITLE", "").strip()

            if not subj or not numb:
                continue

            degree_courses.append(
                {
                    "YEAR": year,
                    "TERM": term,
                    "SUBJ": subj,
                    "NUMB": numb,
                    "TITLE": title,
                }
            )

    return degree_courses


def compare_degree_to_inventory(degree_courses, inventory):
    results = []

    for course in degree_courses:
        key = (course["SUBJ"], course["NUMB"])

        if key not in inventory:
            results.append(
                {
                    "YEAR": course["YEAR"],
                    "TERM": course["TERM"],
                    "SUBJ": course["SUBJ"],
                    "NUMB": course["NUMB"],
                    "DEGREE_TITLE": course["TITLE"],
                    "INVENTORY_TITLE": "",
                    "STATUS": "NOT_FOUND",
                }
            )
            continue

        inventory_title = inventory[key]
        degree_title_norm = normalize_title(course["TITLE"])
        inventory_title_norm = normalize_title(inventory_title)

        if degree_title_norm == inventory_title_norm:
            status = "MATCHED_EXACT"
        else:
            status = "MATCHED_TITLE_DIFF"

        results.append(
            {
                "YEAR": course["YEAR"],
                "TERM": course["TERM"],
                "SUBJ": course["SUBJ"],
                "NUMB": course["NUMB"],
                "DEGREE_TITLE": course["TITLE"],
                "INVENTORY_TITLE": inventory_title,
                "STATUS": status,
            }
        )

    return results


def write_match_report(file_path, results):
    with file_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "YEAR",
                "TERM",
                "SUBJ",
                "NUMB",
                "DEGREE_TITLE",
                "INVENTORY_TITLE",
                "STATUS",
            ]
        )

        for row in results:
            writer.writerow(
                [
                    row["YEAR"],
                    row["TERM"],
                    row["SUBJ"],
                    row["NUMB"],
                    row["DEGREE_TITLE"],
                    row["INVENTORY_TITLE"],
                    row["STATUS"],
                ]
            )


def print_summary(results, degree_name):
    exact = sum(1 for row in results if row["STATUS"] == "MATCHED_EXACT")
    title_diff = sum(1 for row in results if row["STATUS"] == "MATCHED_TITLE_DIFF")
    not_found = sum(1 for row in results if row["STATUS"] == "NOT_FOUND")

    print(degree_name)
    print(f"Matched exact: {exact}")
    print(f"Matched with title difference: {title_diff}")
    print(f"Not found: {not_found}")
    print()

    for row in results:
        print(
            f'{row["SUBJ"]} {row["NUMB"]} | {row["STATUS"]} | '
            f'Degree: {row["DEGREE_TITLE"]} | '
            f'Inventory: {row["INVENTORY_TITLE"]}'
        )


def main():
    if len(sys.argv) < 2:
        print("Usage: python .\\src\\catalog\\match_degree_courses.py <degree_file_name>")
        print("Example: python .\\src\\catalog\\match_degree_courses.py computer_science_bs.csv")
        sys.exit(1)

    repo_root = Path(__file__).resolve().parents[2]

    inventory_file = repo_root / "data" / "processed" / "course_inventory.csv"
    degree_file_name = sys.argv[1]
    degree_file = repo_root / "data" / "degree_plans" / "matched" / degree_file_name

    if not degree_file.exists():
        print(f"Degree file not found: {degree_file}")
        sys.exit(1)

    output_name = degree_file.stem + "_match_report.csv"
    output_file = repo_root / "data" / "degree_plans" / "matched" / output_name

    inventory = load_course_inventory(inventory_file)
    degree_courses = load_degree_plan(degree_file)
    results = compare_degree_to_inventory(degree_courses, inventory)

    write_match_report(output_file, results)
    print_summary(results, degree_file_name)

    print()
    print(f"Match report written to: {output_file}")


if __name__ == "__main__":
    main()