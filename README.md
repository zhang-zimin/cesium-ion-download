# Cesium Ion 3D Tiles 下载器

这个工具可以帮助您从 Cesium Ion 下载 3D Tiles 数据集。

## 快速开始

### 1. 配置 Token

**方法1：使用 .env 文件 (推荐)**
1. 复制 `.env.example` 文件并重命名为 `.env`
2. 编辑 `.env` 文件，将 `your_cesium_ion_token_here` 替换为您的真实 token

**方法2：设置环境变量**
在 PowerShell 中运行：
```powershell
$env:CESIUM_ION_TOKEN="YOUR_TOKEN_HERE"
```

### 2. 获取 Cesium Ion Token
1. 访问 https://cesium.com/ion/
2. 登录您的账户
3. 转到 "Access Tokens" 页面
4. 创建新的 token 或复制现有的 token

### 3. 运行程序
```powershell
python main.py
```

## 配置选项

- `CESIUM_ION_TOKEN`: 您的 Cesium Ion 访问令牌 (必需)
- `CESIUM_ASSET_ID`: 要下载的资源 ID (可选，默认: 3443919)

## 注意事项
- Token 通常以 "eyJ" 开头
- 确保您有权访问指定的 asset ID
- 如果是私有 asset，确保 token 有足够的权限
- `.env` 文件已被添加到 `.gitignore`，不会被提交到版本控制
