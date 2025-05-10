import os
import requests
import hashlib
os.system("clear" if os.name == "posix" else "cls")

REPO_URL = "https://raw.githubusercontent.com/tausifzaman/AdminDirectoryFinder/refs/heads/main/"
GITHUB_DIR = "https://github.com/tausifzaman/AdminDirectoryFinder"

FILES = [
    "main.py",
    "directory.txt",
    "README.md",
    "LICENSE",
    "update.py"
]

LOGO = r"""
                              / |/ | .-~/
                          T\ Y  I  |/  /  _
         /T               | \I  |  I  Y.-~/
        I l   /I       T\ |  |  l  |  T  /
     T\ |  \ Y l  /T   | \I  l   \ `  l Y
 __  | \l   \l  \I l __l  l   \   `  _. |
 \ ~-l  `\   `\  \  \ ~\  \   `. .-~   |
  \   ~-. "-.  `  \  ^._ ^. "-.  /  \   |
.--~-._  ~-  `  _  ~-_.-"-." ._ /._ ." ./
 >--.  ~-.   ._  ~>-"    "\   7   7   ]
^.___~"--._    ~-{  .-~ .  `\ Y . /    |
<__ ~"-.  ~       /_/   \   \I  Y   : |
  ^-.__           ~(_/   \   >._:   | l______
      ^--.,___.-~"  /_/   !  `-.~"--l_ /     ~"-.
             (_/ .  ~(   /'     "~"--,Y   -=b-. _)
              (_/ .  \  :           / l      c"~o \
               \ /    `.    .     .^   \_.-~"~--.  )
                (_/ .   `  /     /       !       )/
                 / / _.   '.   .':      /        '
                 ~(_/ .   /    _  `  .-<_ 
                   /_/ . ' .-~" `.  / \  \          ,z=.
                   ~( /   '  :   | K   "-.~-.______//
                     "-,.    l   I/ \_    __{--->._(==.
                      //(     \  <    ~"~"     //
                     /' /\     \  \     ,v=.  ((
                   .^. / /\     "  }__ //===-  `
                  / / ' '  "-.,__ {---(==-
                .^ '       :  T  ~"   ll        instagram : @_tausif_zaman
               / .  .  . : | :!        \            github.com/tausifzaman
              (_/  /   | | j-"          ~^
                ~-<_(_.^-~"
"""

def sha256_file(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def sha256_url(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return hashlib.sha256(r.content).hexdigest(), r.content
    except:
        return None, None
    return None, None

def main():
    print("\033[93m" + LOGO + "\033[0m")  # Yellow color

    updated_files = []

    for file in FILES:
        local_hash = sha256_file(file)
        remote_hash, _ = sha256_url(REPO_URL + file)

        if remote_hash is None:
            print(f"[-] Could not fetch remote hash for {file}")
            continue

        if local_hash != remote_hash:
            status = "Added" if local_hash is None else "Updated"
            updated_files.append((file, status))

    if not updated_files:
        print("[✓] All files are up to date.")
        return

    print("\n[!] Updates available for the following files:")
    for file, status in updated_files:
        print(f" - {file} [{status}]")

    choice = input("\n[?] Do you want to update these files? (y/n): ").strip().lower()
    if choice != "y":
        print("[-] Update cancelled by user.")
        return

    for file, _ in updated_files:
        try:
            res = requests.get(REPO_URL + file)
            if res.status_code == 200:
                with open(file, "wb") as f:
                    f.write(res.content)
                print(f"[+] {file} updated successfully.")
            else:
                print(f"[-] Failed to download {file}")
        except Exception as e:
            print(f"[-] Error updating {file}: {e}")

    print("\n[✓] All selected files updated successfully.")

if __name__ == "__main__":
    main()
