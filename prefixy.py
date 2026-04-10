
import os
import subprocess
import re
import sys
app=[]
prefix=[]
proton=[]


def parse_file_to_array(file_path, filter_func=None, normalize_whitespace=True):
    """
    Reads a file and returns a list of cleaned + filtered lines.

    - Removes \r
    - Strips leading/trailing whitespace
    - Normalizes internal whitespace if enabled

    :param file_path: Path to file
    :param filter_func: Optional function(line) -> bool
    :param normalize_whitespace: If True, cleans weird whitespace
    :return: List of processed lines
    """

    def clean_line(line: str) -> str:
        # Remove carriage returns
        line = line.replace("\r", "")

        # Normalize unicode whitespace to normal spaces
        line = re.sub(r"\s+", " ", line)

        return line.strip()

    results = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = clean_line(line)

            # skip empty lines after cleanup
            if not line:
                continue

            # apply optional filter
            if filter_func is None or filter_func(line):
                results.append(line)

    return results

def clean_path(raw_path):
    cleaned = raw_path.strip('"').strip("'")
    return cleaned

def launch_with_proton(proton_path, prefix_path, exe_path):
    """
    Launches a Windows executable using a specific Proton version and prefix.
    """
    # Expand and get absolute paths to prevent "file not found" errors
    proton_bin = os.path.abspath(os.path.expanduser(clean_path(proton_path)))
    prefix_dir = os.path.abspath(os.path.expanduser(clean_path(prefix_path)))
    game_exe = os.path.abspath(os.path.expanduser(clean_path(exe_path)))

    # Identify the Steam installation path (needed for some Proton versions)
    # Usually the parent directory of the steamapps folder
    steam_apps_dir = os.path.dirname(os.path.dirname(prefix_dir))
    steam_path = os.path.dirname(steam_apps_dir)

    # Set up the environment variables Proton requires
    env = os.environ.copy()
    env["STEAM_COMPAT_DATA_PATH"] = prefix_dir
    env["STEAM_COMPAT_CLIENT_INSTALL_PATH"] = steam_path
    
    # Optional: Enable logging for troubleshooting
    # env["PROTON_LOG"] = "1"
    # Command structure: /path/to/proton run /path/to/game.exe
    cmd = [proton_bin, "run", game_exe]

    print(f"--- Launching Game ---")
    print(f"Proton: {proton_bin}")
    print(f"Prefix: {prefix_dir}")
    print(f"Target: {game_exe}")

    try:
        # Run the command and wait for it to finish
        subprocess.run(cmd, env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Game exited with code {e.returncode}")
    except FileNotFoundError:
        print("Error: One of the paths provided does not exist.")

if __name__ == "__main__":
    # --- CONFIGURATION ---
    # 1. Path to the actual 'proton' python script in your Steam files
    choice = int(sys.argv[1])
    

    PROTON_PATHS = parse_file_to_array("proton.txt") 

    # 2. Path where the game's prefix (pfx) will be stored or is already located
    PREFIX_PATHS =  parse_file_to_array("compat.txt")
    
    # 3. Path to the Windows .exe file
    GAME_EXE_PATHS = parse_file_to_array("app.txt")

    launch_with_proton(PROTON_PATHS[choice], PREFIX_PATHS[choice], GAME_EXE_PATHS[choice])

