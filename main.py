import urllib.request
import json
import os
import gzip
import io
import sys

def load_env_file():
    """从 .env 文件加载环境变量"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# 加载 .env 文件
load_env_file()

# 配置信息
asset_id = int(os.getenv('CESIUM_ASSET_ID', '3443919'))

# 从环境变量获取 token
ion_token = os.getenv('CESIUM_ION_TOKEN')

if not ion_token or ion_token == 'your_cesium_ion_token_here':
    print("错误：未找到有效的 Cesium Ion token")
    print("请按以下步骤设置：")
    print("1. 编辑 .env 文件")
    print("2. 将 'your_cesium_ion_token_here' 替换为您的真实 token")
    print("3. 或者设置环境变量 CESIUM_ION_TOKEN")
    print("\n如何获取 token：")
    print("- 访问 https://cesium.com/ion/")
    print("- 登录您的账户")
    print("- 转到 'Access Tokens' 页面")
    print("- 创建新 token 或复制现有 token")
    sys.exit(1)

print(f"使用 Asset ID: {asset_id}")
print(f"Token (前10个字符): {ion_token[:10]}...")

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
            print("认证失败！请检查您的 Cesium Ion token 是否有效。")
            print("可能的原因：")
            print("1. Token 已过期")
            print("2. Token 无效或格式错误")
            print("3. 没有访问此资源的权限")
        elif e.code == 403:
            print("权限被拒绝！您的 token 没有访问此资源的权限。")
        elif e.code == 404:
            print("资源未找到！请检查 asset_id 是否正确。")
        raise
    except Exception as e:
        print(f"下载失败: {e}")
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