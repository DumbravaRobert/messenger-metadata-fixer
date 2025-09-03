# Facebook Metadata Fixer

This repository hosts tools for fixing metadata in Facebook exports.  

When exporting your data from Facebook, the media files from **Messenger** will not have the correct date. Instead, they are assigned the date of the export.  

⚠️ **Important:** This tool only works if you have exported your data in **HTML format**.  
If you exported your data as JSON, please use [facebookmessenger-exif](https://github.com/Yard1/facebookmessenger-exif).

This tool will fix the metadata of your photos so they reflect the **original sending date**.

---

## Usage

### 1. Set up `messenger_exif_html.py`

Inside `messenger_exif_html.py`, update the `ROOT_PATH` to point to your **messages directory** (e.g., `\facebook\your_facebook_activity\messages`):

```python
ROOT_PATH = r"<your path goes here>"
```

By default, the script processes the following subfolders:

```python
SUBFOLDERS = ["inbox", "e2ee_cutover", "archived_threads", "filtered_threads", "message_requests"]
```

If you need to include other directories, simply add them to the list.

---

### 2. Configure `move-media.ps1`

The `move-media.ps1` script moves all photos and videos from Messenger into a single directory, making them easier to view.  
Edit the following variables inside the script:

```powershell
$MessagesRoot    = "<facebook_export_path>"     # path to your 'messages' directory
$Destination = "<move_destination_path>"    # where all media will be moved
```

---

### 3. Notes and Warnings

- Both scripts **modify the original files**:  
  - `messenger_exif_html.py` updates metadata.  
  - `move-media.ps1` moves files.  

👉 Always keep a backup of your exported data before running the scripts!

---

## Step-by-step Instructions

1. Request and download a copy of your Facebook data (**HTML format**).  
2. Download `messenger_exif_html.py` and `move-media.ps1` from this repo.  
3. Download [ExifTool](https://exiftool.org/) and place it in the same directory as the scripts.  
4. Run `messenger_exif_html.py`.  
5. Run `move-media.ps1`.  

---

## License

[MIT](./LICENSE)
