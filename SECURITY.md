# 安全性指南 (Security Guide)

## 🔒 概述

本專案包含敏感的 API 金鑰和憑證，請務必遵循以下安全準則。

---

## ✅ 安全檢查

執行安全檢查腳本：
```powershell
.\安全檢查.ps1
```

此腳本會檢查：
- ✓ `.env` 是否在 `.gitignore` 中
- ✓ `.env` 是否被 Git 追蹤
- ✓ Git 歷史中是否有 `.env`
- ✓ 其他敏感檔案
- ✓ DEBUG 模式設定
- ✓ Git 暫存區狀態

---

## 🛡️ 受保護的檔案

以下檔案已被 `.gitignore` 保護，**永遠不會**被提交：

```
.env
.env.local
.env.*.local
.env.production
.env.development
*.key
*.pem
*.crt
secrets/
credentials/
```

---

## 🔑 API 金鑰管理

### 1. 環境變數設定

**開發環境：**
```bash
# .env (本地開發)
LINE_CHANNEL_ACCESS_TOKEN=your_dev_token
LINE_CHANNEL_SECRET=your_dev_secret
GROQ_API_KEY=your_dev_groq_key
DEBUG=True
```

**生產環境：**
```bash
# .env.production (生產環境)
LINE_CHANNEL_ACCESS_TOKEN=your_prod_token
LINE_CHANNEL_SECRET=your_prod_secret
GROQ_API_KEY=your_prod_groq_key
DEBUG=False
```

### 2. 金鑰分離原則

- ❌ **不要**在開發和生產環境使用相同的 API 金鑰
- ✅ **要**為每個環境建立獨立的金鑰
- ✅ **要**定期輪替金鑰（建議每 90 天）

### 3. 如何取得 API 金鑰

**LINE Bot：**
1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 建立 Messaging API Channel
3. 複製 Channel Access Token 和 Channel Secret

**Groq API：**
1. 前往 [Groq Console](https://console.groq.com/)
2. 註冊帳號（免費）
3. 建立 API Key

---

## ⚠️ 如果不小心提交了 .env

### 立即行動：

#### 1. 從 Git 移除（如果還沒 push）
```bash
git rm --cached .env
git commit -m "Remove .env from tracking"
```

#### 2. 從 Git 歷史清除（如果已經 push）

**選項 A：使用 git filter-branch**
```bash
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  --prune-empty --tag-name-filter cat -- --all

git push origin --force --all
```

**選項 B：使用 BFG Repo-Cleaner（推薦）**
```bash
# 安裝 BFG
# https://rtyley.github.io/bfg-repo-cleaner/

bfg --delete-files .env
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push origin --force --all
```

#### 3. 更換所有 API 金鑰

**重要：** 即使從 Git 移除，歷史記錄可能已被看到，請立即：
- 🔄 在 LINE Developers Console 重新發行 Token
- 🔄 在 Groq Console 刪除舊 Key 並建立新的
- 🔄 更新 `.env` 檔案

---

## 🚀 部署安全

### Docker 部署

使用 Docker secrets 或環境變數：

```yaml
# docker-compose.yml
services:
  app:
    environment:
      - LINE_CHANNEL_ACCESS_TOKEN=${LINE_CHANNEL_ACCESS_TOKEN}
      - LINE_CHANNEL_SECRET=${LINE_CHANNEL_SECRET}
      - GROQ_API_KEY=${GROQ_API_KEY}
      - DEBUG=False
```

執行時傳入環境變數：
```bash
export LINE_CHANNEL_ACCESS_TOKEN=your_token
export LINE_CHANNEL_SECRET=your_secret
export GROQ_API_KEY=your_key
docker-compose up -d
```

### 雲端部署（Render / Heroku / Railway）

1. 在平台的環境變數設定中加入：
   - `LINE_CHANNEL_ACCESS_TOKEN`
   - `LINE_CHANNEL_SECRET`
   - `GROQ_API_KEY`
   - `DEBUG=False`

2. **不要**在 `render.yaml` 或 `app.json` 中寫死金鑰值

---

## 🔍 安全最佳實踐

### ✅ 要做的事

1. **使用環境變數**
   ```python
   # ✅ 正確
   api_key = os.getenv('GROQ_API_KEY')
   ```

2. **定期檢查**
   ```bash
   # 每週執行
   .\安全檢查.ps1
   ```

3. **使用 .env.example**
   ```bash
   # .env.example（可以提交）
   LINE_CHANNEL_ACCESS_TOKEN=your_line_token_here
   GROQ_API_KEY=your_groq_key_here
   ```

4. **設定 Git hooks**
   ```bash
   # .git/hooks/pre-commit
   if git diff --cached --name-only | grep -q "^.env$"; then
       echo "Error: Attempting to commit .env file!"
       exit 1
   fi
   ```

### ❌ 不要做的事

1. **不要硬編碼**
   ```python
   # ❌ 錯誤
   api_key = "gsk_abc123def456"
   ```

2. **不要分享螢幕截圖**
   - 不要在截圖中包含 `.env` 內容
   - 不要分享包含 API 金鑰的終端輸出

3. **不要在公開場合**
   - 不要在 GitHub Issues 貼上完整錯誤訊息（可能包含金鑰）
   - 不要在 Discord/Slack 分享 `.env` 內容

---

## 🔐 進階：密鑰管理服務

### Azure Key Vault

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://your-vault.vault.azure.net/", 
                     credential=credential)

api_key = client.get_secret("GROQ-API-KEY").value
```

### AWS Secrets Manager

```python
import boto3

client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='prod/groq/api-key')
api_key = response['SecretString']
```

---

## 📞 發現安全問題？

如果發現安全漏洞，請：
1. **不要**在公開的 GitHub Issues 回報
2. 直接聯繫專案維護者
3. 提供詳細的漏洞描述

---

## 📋 安全檢查清單

部署前確認：

- [ ] `.env` 已加入 `.gitignore`
- [ ] `.env` 未被 Git 追蹤
- [ ] 執行 `.\安全檢查.ps1` 通過
- [ ] 生產環境設定 `DEBUG=False`
- [ ] 使用不同的開發/生產金鑰
- [ ] 已設定金鑰輪替提醒
- [ ] 測試端點已移除或保護
- [ ] 日誌不會記錄敏感資訊

---

## 🔗 相關資源

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [12-Factor App](https://12factor.net/)
- [LINE Bot Security Best Practices](https://developers.line.biz/en/docs/messaging-api/development-guidelines/)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)

---

**最後更新：** 2025/11/09  
**維護者：** 請定期檢查並更新此文件
