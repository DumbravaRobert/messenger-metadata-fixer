# Facebook Metadata Fixer

This repository hosts tools for fixing metadata in Facebook exports.  

When exporting your data from Facebook, the media files from **Messenger** will not have the correct date. Instead, they are assigned the date of the export.  

⚠️ **Important:** This tool only works if you have exported your data in **HTML format**.  
If you exported your data as JSON, please use [facebookmessenger-exif](https://github.com/Yard1/facebookmessenger-exif).

This tool will fix the metadata of your photos so they reflect the **original sending date**.

**Important: ONLY IMAGES AND VIDEOS WILL BE PROCCESSED AND CORRECTED BY THE SCRIPT. OTHER FILES WILL BE IGNORED(AUDIO FILES, ZIP FILES, DOCS, etc)**

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
2. Extract your data  
3. Download `messenger_exif_html.py` and `move-media.ps1` from this repo.  
4. Download [ExifTool](https://exiftool.org/) and place it in the same directory as the scripts.  
5. Run `messenger_exif_html.py`.  ( if needed, can be started with --debug for more info). 
6. Run `move-media.ps1`.  


## Summary fields explained
At the end of the execution, you will see a short summary of what has happened:

- Processed - The number of media files (photos and videos) where the script successfully updated the metadata date fields using the timestamp extracted from the HTML messages.
- Missing files - The number of media files referenced in the HTML that could not be found on disk (e.g., deleted, moved, or not included in the export).
- Errors - The number of files where the script found the media file, but ExifTool failed to update the metadata (for example, due to a corrupted file).
- Skipped non-media - Files that were referenced but were not actual photos or videos (e.g., stickers, GIFs, thumbnails, or other attachments).
- Skipped external - Links pointing outside the export, usually HTTP or HTTPS URLs (such as links to websites, shared files, or chats). These are ignored.
- Skipped outside - Files that were part of the export but not inside the messages/ folders (for example, Facebook posts, reactions, or stickers used elsewhere).
- Skipped no TS - Media files that did not have any timestamp in the corresponding HTML, so the script could not determine when they were originally sent.

**A CSV file will be generated with all the skipped files and the reason why.**

---

## License

[MIT](./LICENSE)
