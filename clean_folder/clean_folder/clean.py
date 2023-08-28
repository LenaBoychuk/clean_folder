from pathlib import Path
import re
import sys
import shutil


CYRILLIC_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i",
               "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
               "u", "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")
TRANS = {}

image_files = list()
document_files = list()
music_files = list()
video_files = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {
    "JPEG": image_files,
    "JPG": image_files,
    "PNG": image_files,
    "SVG": image_files,
    "AVI": video_files,
    "MP4": video_files,
    "MOV": video_files,
    "MKV": video_files,
    "MP3": music_files,
    "OGG": music_files,
    "WAV": music_files,
    "AMR": music_files,
    "DOC": document_files,
    "DOCX": document_files,
    "TXT": document_files,
    "PDF": document_files,
    "PPTX": document_files,
    "XLSX": document_files,
    "ZIP": archives,
    "GZTAR": archives,
    "TAR": archives,
}


for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
        
def normalize(name):
    name_extension = name.split('.')
    extension = name_extension[-1]
    name = ".".join(name_extension[:-1:])
    new_name = name.translate(TRANS)
    new_name = re.sub('\W - .', '_', new_name)
    return f"{new_name}.{extension}"


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("PICTURES", "VIDEO", "DOCUMENTS", "MUSIC", "OTHERS", "ARCHIVES"):
                folders.append(item)
                scan(item)
            continue
        extension = get_extensions(item.name)
        new_name = folder/item.name

        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)


def handle_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
        
    new_name = normalize(path.name)
    new_name = re.sub(r"(.zip|.gztar|.tar)", '', new_name)
   
    archive_folder = root_folder / dist / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), root_folder / dist / new_name)
    except shutil.ReadError or FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()

def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass
            
def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass

def main():
    path = sys.argv[1]
    print(f"Start in {path}")
    folder_path = Path(path)

    scan(folder_path)
    
    
    for file in image_files:
        handle_file(file, folder_path, "IMAGES")

    for file in document_files:
        handle_file(file, folder_path, "DOCUMENTS")

    for file in music_files:
        handle_file(file, folder_path, "MUSIC")

    for file in video_files:
        handle_file(file, folder_path, "VIDEO")

    for file in others:
        handle_file(file, folder_path, "OTHERS")

    for file in archives:
        handle_archive(file, folder_path, "ARCHIVES")

    get_folder_objects(folder_path)

if __name__ == '__main__':
    main()
    

