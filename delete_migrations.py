#! /usr/bin/python
import shutil
import os


def delete_migrations():
    print("Starting to Delete...")
    cwd = os.getcwd()
    folders = os.listdir()
    for folder in folders:
        folder_path = os.path.join(cwd, folder)
        if os.path.isdir(folder_path) and folder not in ['venv', '.git']:
            dirs = os.listdir(folder_path)
            for dir in dirs:
                if dir in ["migrations", "__pycache__"]:
                    path = os.path.join(folder_path, dir)
                    shutil.rmtree(path)
                    print(f"{path} deleted successfully")
    if "db.sqlite3" in folders:
        os.remove(os.path.join(cwd, "db.sqlite3"))
    print("Migrations and db.sqlite3 deleted Successfully.")


if __name__ == "__main__":
    delete_migrations()
