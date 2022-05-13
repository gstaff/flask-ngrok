import atexit
import json
import os
import platform
import shutil
import subprocess
import tempfile
import time
import zipfile
import requests
import httplib2

from pathlib import Path
from threading import Timer
from bs4 import BeautifulSoup, SoupStrainer


def _run_ngrok(autotoken):
    ngrok_path = str(Path(tempfile.gettempdir(), "ngrok"))
    _download_ngrok(ngrok_path)
    system = platform.system()
    if system == "Darwin":
        command = "ngrok"
    elif system == "Windows":
        command = "ngrok.exe"
    elif system == "Linux":
        command = "ngrok"
    else:
        raise Exception(f"{system} is not supported")
    executable = str(Path(ngrok_path, command))
    os.chmod(executable, 777)

    ngrok = subprocess.Popen([executable, 'authtoken', autotoken])
    atexit.register(ngrok.terminate)
    time.sleep(1)
    ngrok = subprocess.Popen([executable, 'http', '5000'])
    atexit.register(ngrok.terminate)
    localhost_url = "http://localhost:4040/api/tunnels"  # Url with tunnel details
    time.sleep(1)
    tunnel_url = requests.get(localhost_url).text  # Get the tunnel information
    j = json.loads(tunnel_url)

    tunnel_url = j['tunnels'][0]['public_url']  # Do the parsing of the get
    tunnel_url = tunnel_url.replace("https", "http")
    return tunnel_url


def _download_ngrok(ngrok_path):
    if Path(ngrok_path).exists():
        return
    system = platform.system()
    http = httplib2.Http()
    status, response = http.request('https://ngrok.com/download')

    # Find the right link according to the system and download the files from it
    if system in ['Darwin', 'Windows', 'Linux']:
        for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
            if link.has_attr('href') and f'stable-{system.lower()}' in link['href']:
                url = link['href']
    else:
        raise Exception(f"{system} is not supported")

    download_path = _download_file(url)
    with zipfile.ZipFile(download_path, "r") as zip_ref:
        zip_ref.extractall(ngrok_path)


def _download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    download_path = str(Path(tempfile.gettempdir(), local_filename))
    with open(download_path, 'wb') as f:
        print('Please wait for the download to be finished (can take a few minutes), This files are required for ngrok link to be generated')
        shutil.copyfileobj(r.raw, f)
    return download_path


def start_ngrok(*autotoken):
    ngrok_address = _run_ngrok(''.join(autotoken))
    print(f" * Running on {ngrok_address}")
    print(f" * Traffic stats available on http://127.0.0.1:4040")


def run_with_ngrok(app, autotoken):
    """
    The provided Flask app will be securely exposed to the public internet via ngrok when run,
    and the its ngrok address will be printed to stdout
    :param app: a Flask application object
    :return: None
    """
    old_run = app.run

    def new_run():
        thread = Timer(1, start_ngrok, args=autotoken)
        thread.setDaemon(True)
        thread.start()
        old_run()
    app.run = new_run
