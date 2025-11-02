# 🔨 Rebuild Twenty CRM with LeadOn Integration

## ⚠️ Important Note

**This is NOT recommended for your hackathon!** Use LeadOn Pro instead (http://localhost:8000).

Only follow these steps if you have 30-60 minutes and want to customize Twenty CRM itself.

---

## 📋 Prerequisites

### 1. Install Node.js 24.5.0
```powershell
# Download from: https://nodejs.org/
# Or use nvm-windows:
nvm install 24.5.0
nvm use 24.5.0
```

### 2. Install Yarn 4.0.2
```powershell
npm install -g yarn
yarn set version 4.0.2
```

### 3. Verify Installations
```powershell
node --version  # Should show v24.5.0
yarn --version  # Should show 4.0.2
docker --version  # Should show Docker version
```

---

## 🔧 Build Steps

### Step 1: Navigate to Twenty CRM Directory
```powershell
cd C:\Users\Gamer\Downloads\LeadOn\CRM\twenty
```

### Step 2: Install Dependencies
```powershell
yarn install
```
**Time:** ~5-10 minutes

### Step 3: Build the Frontend
```powershell
cd packages\twenty-front
yarn build
```
**Time:** ~10-20 minutes

### Step 4: Build the Server
```powershell
cd ..\twenty-server
yarn build
```
**Time:** ~5-10 minutes

### Step 5: Build Docker Image
```powershell
cd ..\..
docker build -t leadon-twenty:custom .
```
**Time:** ~10-20 minutes

### Step 6: Update docker-compose.yml
Edit `CRM\twenty\packages\twenty-docker\docker-compose.yml`:

**Change line 5:**
```yaml
image: twentycrm/twenty:${TAG:-latest}
```

**To:**
```yaml
image: leadon-twenty:custom
```

**Change line 61:**
```yaml
image: twentycrm/twenty:${TAG:-latest}
```

**To:**
```yaml
image: leadon-twenty:custom
```

### Step 7: Restart Docker Containers
```powershell
cd packages\twenty-docker
docker compose down
docker compose up -d
```

### Step 8: Wait for Startup
```powershell
docker compose logs -f server
```
Wait until you see: "Application is running on: http://localhost:3000"

Press Ctrl+C to exit logs

### Step 9: Test the Integration
1. Open http://localhost:4000
2. Go to the People page
3. Click the blue robot button (bottom-right)
4. Type: "Find CTOs at AI companies in San Francisco"
5. Click Send

---

## 🐛 Troubleshooting

### Build Fails
```powershell
# Clear cache and try again
yarn cache clean
rm -rf node_modules
yarn install
```

### Docker Build Fails
```powershell
# Clear Docker cache
docker system prune -a
docker build --no-cache -t leadon-twenty:custom .
```

### Port Already in Use
```powershell
# Stop all containers
docker compose down

# Check what's using port 4000
netstat -ano | findstr :4000

# Kill the process (replace PID with actual process ID)
taskkill /F /PID <PID>
```

### Node Version Issues
```powershell
# Make sure you're using Node 24.5.0
node --version

# If not, switch to it
nvm use 24.5.0
```

---

## ⏱️ Total Time Estimate

- Install prerequisites: 10-15 minutes
- Install dependencies: 5-10 minutes
- Build frontend: 10-20 minutes
- Build server: 5-10 minutes
- Build Docker image: 10-20 minutes
- **Total: 40-75 minutes**

---

## 🎯 Alternative: Use LeadOn Pro Instead

Instead of spending 40-75 minutes rebuilding Twenty CRM, you can:

1. Open **http://localhost:8000** (LeadOn Pro)
2. Start demoing **immediately**
3. Have a **fully customized** interface
4. **No build required**
5. **No risk** of build failures

**LeadOn Pro has everything you need:**
- ✅ AI chatbox
- ✅ Contact search
- ✅ Contact management
- ✅ Campaign creation
- ✅ Export features
- ✅ Modern UI

---

## 💡 Recommendation

**For your hackathon, use LeadOn Pro!**

Only rebuild Twenty CRM if:
- You have 1+ hour of free time
- You're comfortable with Node/Yarn/Docker
- You want to explore Twenty CRM's advanced features
- You're not under time pressure

**Otherwise, LeadOn Pro is the better choice!** 🚀

