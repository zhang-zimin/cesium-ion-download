import urllib.request
import json
import os
import gzip
import io
import sys

def load_env_file():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Load .env file
load_env_file()

# Configuration
asset_id = int(os.getenv('CESIUM_ASSET_ID', '3443919'))

# Get token from environment variables
ion_token = os.getenv('CESIUM_ION_TOKEN')

if not ion_token or ion_token == 'your_cesium_ion_token_here':
    print("Error: No valid Cesium Ion token found")
    print("Please follow these steps:")
    print("1. Edit the .env file")
    print("2. Replace 'your_cesium_ion_token_here' with your actual token")
    print("3. Or set the CESIUM_ION_TOKEN environment variable")
    print("\nHow to get a token:")
    print("- Visit https://cesium.com/ion/")
    print("- Log into your account")
    print("- Go to 'Access Tokens' page")
    print("- Create a new token or copy existing token")
    sys.exit(1)

print(f"Using Asset ID: {asset_id}")
print(f"Token (first 10 chars): {ion_token[:10]}...")

base_url = f"https://assets.ion.cesium.com/{asset_id}/"

headers = {
    "Authorization": f"Bearer {ion_token}",
    "User-Agent": "Mozilla/5.0"
}

def download_tileset():
    try:
        req = urllib.request.Request(base_url + "tileset.json", headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read()
        if response.info().get('Content-Encoding') == 'gzip':
            data = gzip.decompress(data)
        return json.loads(data.decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"URL: {e.url}")
        if e.code == 401:
            print("Authentication failed! Please check if your Cesium Ion token is valid.")
            print("Possible reasons:")
            print("1. Token has expired")
            print("2. Token is invalid or malformed")
            print("3. No permission to access this resource")
        elif e.code == 403:
            print("Permission denied! Your token doesn't have access to this resource.")
        elif e.code == 404:
            print("Resource not found! Please check if the asset_id is correct.")
        raise
    except Exception as e:
        print(f"Download failed: {e}")
        raise

def download_files(node, path=""):
    if "content" in node and "uri" in node["content"]:
        file_url = base_url + node["content"]["uri"]
        local_path = os.path.join("downloads", path, node["content"]["uri"])
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        if not os.path.exists(local_path):
            try:
                req = urllib.request.Request(file_url, headers=headers)
                with urllib.request.urlopen(req) as res:
                    data = res.read()
                    if res.info().get('Content-Encoding') == 'gzip':
                        data = gzip.decompress(data)
                    with open(local_path, 'wb') as f:
                        f.write(data)
                print(f"Downloaded: {file_url}")
            except urllib.error.HTTPError as e:
                print(f"HTTP Error {e.code} downloading {file_url}: {e.reason}")
            except Exception as e:
                print(f"Failed to download {file_url}: {e}")

    if "children" in node:
        for child in node["children"]:
            download_files(child, path)

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    tileset = download_tileset()
    download_files(tileset["root"])