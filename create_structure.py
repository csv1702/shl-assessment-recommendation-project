import os

PROJECT_NAME = "projet_shl"

structure = {
    "data": [
        "given",
        "raw",
        "processed",
        "embeddings"
    ],
    "scraper": [
        "scrape_shl.py"
    ],
    "pipeline": [
        "data_loader.py",
        "preprocess.py",
        "retriever.py",
        "evaluator.py"
    ],
    "api": [
        "main.py"
    ],
    "frontend": [
        "app.py"
    ],
    "root_files": [
        "requirements.txt",
        ".env",
        "README.md"
    ]
}


def create_project_structure():
    # Create root directory
    os.makedirs(PROJECT_NAME, exist_ok=True)

    # Create folders and files
    for folder, items in structure.items():
        if folder == "root_files":
            for file in items:
                open(os.path.join(PROJECT_NAME, file), "a").close()
        else:
            folder_path = os.path.join(PROJECT_NAME, folder)
            os.makedirs(folder_path, exist_ok=True)

            for item in items:
                item_path = os.path.join(folder_path, item)
                if "." in item:
                    open(item_path, "a").close()
                else:
                    os.makedirs(item_path, exist_ok=True)

    print("✅ Project structure created successfully!")


if __name__ == "__main__":
    create_project_structure()
