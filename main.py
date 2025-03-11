import requests
import os
import threading
from queue import Queue
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from time import sleep
os.system("clear" if os.name == "posix" else "cls")

console = Console()

logo = """
     _       _ ____  _      _____ _           _
    / \   __| |  _ \(_)_ __|  ___(_)_ __   __| | ___ _ __
   / _ \ / _` | | | | | '__| |_  | | '_ \ / _` |/ _ \ '__|
  / ___ \ (_| | |_| | | |  |  _| | | | | | (_| |  __/ |
 /_/   \_\__,_|____/|_|_|  |_|   |_|_| |_|\__,_|\___|_| V.1.0
         Advanced Multi-URL Admin Directory Finder
"""

console.print(Panel.fit(logo, style="bold cyan", title="[bold yellow]Tausif's Tool"))

while True:
    user_input = console.input("[bold cyan]Enter URLs (comma-separated for multiple domain) : [/]").strip()

    if not user_input:
        console.print("[red]Error: Please enter at least one valid URL.[/]")
        continue

    urls = [url.strip().rstrip("/") for url in user_input.split(",") if url.strip()]

    urls = [("http://" + url) if not url.startswith("http") else url for url in urls]

    if urls:
        break

dir_file = "directory.txt"
if not os.path.exists(dir_file):
    console.print("[bold red]Error: directory.txt not found![/]")
    exit()

with open(dir_file, "r") as f:
    directories = [line.strip().lstrip("/") for line in f.readlines() if line.strip()]

total_dirs = len(directories)
console.print(f"\n[bold green]Total Directories to Scan:[/] {total_dirs} per URL\n")

num_threads = 10  
queue = Queue()

with Progress(
    TextColumn("[bold yellow]{task.percentage:>3.0f}%[/]"),
    BarColumn(),
    TextColumn("[cyan]{task.completed}/{task.total} Scanned[/]"),
    console=console
) as progress:

    task = progress.add_task("Scanning", total=total_dirs * len(urls))

    def scan_directory():
        while not queue.empty():
            target_url, directory = queue.get()
            full_url = f"{target_url}/{directory}" 

            try:
                response = requests.get(full_url, timeout=5, allow_redirects=False)
                status_code = response.status_code

                if status_code in [301, 302]:
                    console.print(f"[bold green][{status_code}][/] {full_url}")
                elif status_code == 200:
                    console.print(f"[bold white][{status_code}][/] {full_url}")
                elif status_code != 404:
                    console.print(f"[bold red][{status_code}][/] {full_url}")

            except requests.exceptions.RequestException:
                console.print(f"[bold red][ERROR][/] Failed to connect: {full_url}")

            progress.update(task, advance=1)
            sleep(0.1) 
            queue.task_done()

    for url in urls:
        for directory in directories:
            queue.put((url, directory))

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=scan_directory)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

console.print("\n[bold green]Scanning Complete![/]")
