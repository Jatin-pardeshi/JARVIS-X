import os
import shutil

def cleanup():
    print("Initiating Weekly System Cleanup...")
    paths_to_clean = [
        os.path.join(os.environ.get('USERPROFILE', 'C:\\'), 'Temp'),
        os.path.join(os.environ.get('USERPROFILE', 'C:\\'), 'Downloads', 'OSINT')
    ]
    
    for path in paths_to_clean:
        if os.path.exists(path):
            print(f"Cleaning directory: {path}")
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception as e:
                    print(f"Failed to delete {item_path}. Reason: {e}")
        else:
            print(f"Directory not found: {path}")
            
    print("Cleanup sequence complete.")

if __name__ == "__main__":
    cleanup()
