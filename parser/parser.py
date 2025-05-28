# parser.py
import sys, os, csv, re, requests, json
from requests.adapters import HTTPAdapter, Retry

# All helper functions here (smart_capitalize, normalize_code, etc.)
# Same as your original code...

def main(csv_path):
    results = []
    if not os.path.exists(csv_path):
        return json.dumps({"error": "File does not exist."})

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)

        for index, row in enumerate(reader, start=1):
            if len(row) < 11:
                continue

            cleaned = [normalize_code(field.replace('"', '').replace('  ', ' ')) for field in row]
            first, last, model = cleaned[0], cleaned[1], cleaned[10]
            street1, street2 = cleaned[2], cleaned[3]
            city, state, country = cleaned[4], cleaned[5], cleaned[7]
            email, phone = cleaned[8], cleaned[9]
            comments = cleaned[11]

            folder_name = f"{index:03d}_{safe_filename(capitalize_title(first, last, model))}"
            os.makedirs(folder_name, exist_ok=True)

            address_block = format_address(street1, street2, city, state, country)
            content = f"""Address:\n{address_block}\n\nEmail: {email}\n\nTelephone: {phone}\n\nStory:\n{comments}"""

            txt_filename = os.path.join(folder_name, f"{safe_filename(capitalize_title(first, last, model))}.txt")
            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write(content)

            log = [f"Created folder: {folder_name}", f"Created file: {txt_filename}"]

            file_fields = [f for f in cleaned if any(f.lower().endswith(ext) for ext in file_exts)]
            for i, url in enumerate(file_fields, start=1):
                ext = os.path.splitext(url)[-1]
                save_name = f"{safe_filename(capitalize_title(first, last, model))} {i}{ext}"
                save_path = os.path.join(folder_name, save_name)
                download_file(url, save_path, lambda m: log.append(m))

            results.append(log)

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main(sys.argv[1])
