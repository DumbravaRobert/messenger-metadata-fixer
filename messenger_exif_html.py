import os
import argparse
from bs4 import BeautifulSoup
import exiftool
from datetime import datetime
import csv

ROOT_PATH = r"<your_path_here>"
SUBFOLDERS = ["inbox", "e2ee_cutover", "archived_threads", "filtered_threads", "message_requests"]

stats = {
    "processed": 0,
    "missing": 0,
    "errors": 0,
    "skipped_nonmedia": 0,
    "skipped_external": 0,
    "skipped_outside": 0,
    "skipped_no_ts": 0
}

report_rows = []


def parse_timestamp(ts_text: str):
    months = {
        "ian.": "Jan", "feb.": "Feb", "mar.": "Mar", "apr.": "Apr",
        "mai": "May", "iun.": "Jun", "iul.": "Jul", "aug.": "Aug",
        "sept.": "Sep", "oct.": "Oct", "nov.": "Nov", "dec.": "Dec"
    }
    parts = ts_text.split(" ", 1)
    if parts[0] in months:
        ts_text = months[parts[0]] + " " + parts[1]

    try:
        dt = datetime.strptime(ts_text, "%b %d, %Y %I:%M:%S %p")
        return dt.strftime("%Y:%m:%d %H:%M:%S")
    except Exception:
        return None


def process_root(root, et, debug):
    for conv in os.listdir(root):
        conv_path = os.path.join(root, conv)
        if not os.path.isdir(conv_path):
            continue

        print(f"\n[INFO] Conversation: {conv}")

        for file in os.listdir(conv_path):
            if file.startswith("message_") and file.endswith(".html"):
                html_path = os.path.join(conv_path, file)
                print(f"[INFO]   Processing HTML: {html_path}")

                with open(html_path, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")

                for section in soup.find_all("section", class_="_a6-g"):
                    footer = section.find("footer")
                    ts_div = footer.find("div", class_="_a72d") if footer else None
                    ts_text = ts_div.get_text(strip=True) if ts_div else None
                    ts_parsed = parse_timestamp(ts_text) if ts_text else None

                    if ts_text and ts_parsed and debug:
                        print(f"    [DEBUG] {ts_text} -> {ts_parsed}")

                    links = section.find_all("a", href=True)
                    if not links:
                        continue

                    for link in links:
                        rel_path = link["href"]

                        # skip external links
                        if rel_path.startswith("http://") or rel_path.startswith("https://"):
                            stats["skipped_external"] += 1
                            continue

                        rel_path = rel_path.replace("/", os.sep)

                        if "messages" + os.sep in rel_path:
                            rel_path = rel_path.split("messages" + os.sep, 1)[-1]

                        file_path = os.path.join(ROOT_PATH, rel_path)

                        if not (os.sep + "photos" + os.sep in file_path.lower() or os.sep + "videos" + os.sep in file_path.lower()):
                            stats["skipped_nonmedia"] += 1
                            report_rows.append([file_path, "SKIPPED", "non-media"])
                            continue

                        if not os.path.exists(file_path):
                            print(f"    [WARN] Missing file: {file_path}")
                            stats["missing"] += 1
                            report_rows.append([file_path, "MISSING", "file not found"])
                            continue

                        if not ts_parsed:
                            stats["skipped_no_ts"] += 1
                            report_rows.append([file_path, "SKIPPED", "no timestamp"])
                            continue

                        try:
                            et.execute(
                                f"-EXIF:DateTimeOriginal={ts_parsed}",
                                f"-EXIF:CreateDate={ts_parsed}",
                                f"-EXIF:ModifyDate={ts_parsed}",
                                f"-XMP:DateCreated={ts_parsed}",
                                f"-XMP:CreateDate={ts_parsed}",
                                f"-XMP:ModifyDate={ts_parsed}",
                                f"-IPTC:DateCreated={ts_parsed}",
                                f"-QuickTime:CreateDate={ts_parsed}",
                                f"-QuickTime:ModifyDate={ts_parsed}",
                                f"-FileCreateDate={ts_parsed}",
                                f"-FileModifyDate={ts_parsed}",
                                "-overwrite_original",
                                file_path
                            )
                            print(f"    [OK] Wrote date to {file_path}")
                            stats["processed"] += 1
                        except Exception as e:
                            print(f"    [ERROR] Could not write {file_path}: {e}")
                            stats["errors"] += 1


def main(debug: bool):
    with exiftool.ExifTool() as et:
        for folder in SUBFOLDERS:
            root = os.path.join(ROOT_PATH, folder)
            if not os.path.exists(root):
                continue
            print(f"\n[INFO] Processing root folder: {root}")
            process_root(root, et, debug)

    # write report next to the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(script_dir, "report.csv")
    with open(report_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["file", "status", "reason"])
        writer.writerows(report_rows)

    print("\n===== SUMMARY =====")
    print(f"Processed:        {stats['processed']}")
    print(f"Missing files:    {stats['missing']}")
    print(f"Errors:           {stats['errors']}")
    print(f"Skipped non-media:{stats['skipped_nonmedia']}")
    print(f"Skipped external: {stats['skipped_external']}")
    print(f"Skipped outside:  {stats['skipped_outside']}")
    print(f"Skipped no TS:    {stats['skipped_no_ts']}")
    print(f"\n[INFO] Report written to: {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug logs")
    args = parser.parse_args()
    main(args.debug)
