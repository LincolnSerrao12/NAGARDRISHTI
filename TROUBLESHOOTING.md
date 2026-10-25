# 🔧 Troubleshooting Guide

## ✅ **Video Download Not Working - FIXED!**

### What Was Wrong
The video download was broken due to **critical bugs in file handling**:
1. ❌ Wrong file extension being removed (.avi instead of .mp4)
2. ❌ Video path being reconstructed incorrectly
3. ❌ No proper download endpoint
4. ❌ Missing CORS headers

### What's Fixed Now
1. ✅ Correct file extension handling (.mp4)
2. ✅ Proper path reconstruction
3. ✅ Dedicated `/download/<video_id>` endpoint
4. ✅ CORS headers added
5. ✅ Enhanced error handling
6. ✅ Better logging for debugging

---

## 🚀 **How to Run (Fixed Version)**

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Run the Flask app
python app.py

# Step 3: Open in browser
# Go to http://localhost:5000
```

### Expected Console Output
```
============================================================
🚀 Starting Pothole Detection Web Interface
============================================================
📊 Model: runs/detect/train-2/weights/best.pt
🌐 Open http://localhost:5000 in your browser
============================================================
 * Running on http://0.0.0.0:5000
```

---

## 🎯 **Testing the Video Download**

### Step-by-Step Test
1. Open http://localhost:5000 in browser
2. Upload a video file (MP4, MOV, or AVI)
3. Wait for "Processing video frame-by-frame..." message
4. Wait for video to load in the results section
5. **Click the "⬇️ Download Processed Video" button**
6. File should download as `pothole_detection_xxxxx.mp4`

### What to Check in Console
```
[VIDEO] ==========================================
[VIDEO] Input: uploads/xxxxx_video.mp4
[VIDEO] Output: uploads/output_xxxxx.mp4
[VIDEO] Resolution: 1920x1080
[VIDEO] FPS: 30
[VIDEO] Total Frames: 900
[VIDEO] ==========================================
[VIDEO] Starting frame processing...
[VIDEO] Frame 90/900 (10%)  ← Progress indicator
[VIDEO] Frame 180/900 (20%)
...
[VIDEO] ✅ Processed 900 frames, 15 detections found
[VIDEO] Encoding to MP4... (writing 900 frames)
[VIDEO] Encoded 90/900 frames (10%)
[VIDEO] ✅ MP4 encoding completed successfully
[VIDEO] ✅ ==========================================
[VIDEO] Processing Complete!
[VIDEO] File: uploads/output_xxxxx.mp4
[VIDEO] Size: 45.23 MB
[VIDEO] Detections: 15
[VIDEO] ✅ ==========================================
```

---

## 🐛 **Common Issues & Fixes**

### Issue #1: "Error: Failed to fetch"
**Cause:** Flask server not running or not accessible

**Fix:**
```bash
# Make sure Flask is running
python app.py

# Check if port 5000 is available
# Windows: netstat -ano | findstr :5000
# Mac/Linux: lsof -i :5000

# If in use, kill it:
# Windows: taskkill /PID <PID> /F
# Mac/Linux: kill -9 <PID>
```

---

### Issue #2: Model not found
**Cause:** Trained model not in expected location

**Fix:**
```bash
# Check where your model is
dir runs\detect\*\weights\best.pt

# Edit app.py line 26-31 and add your actual path:
model_paths = [
    'YOUR_ACTUAL_PATH/best.pt',
    'runs/detect/train-2/weights/best.pt',
]
```

---

### Issue #3: Video file not found after processing
**Cause:** File path issue or encoding failed

**Check:**
```bash
# List files in uploads folder
dir uploads\

# You should see:
# output_xxxxx.mp4  (processed video)
```

---

### Issue #4: Video takes too long to process
**Cause:** Large video or slow CPU

**Solutions:**
```bash
# Option 1: Use smaller video (under 100MB)
# Option 2: Use lower resolution video
# Option 3: Use GPU acceleration (if GPU available)
```

---

### Issue #5: Browser says "Cannot download"
**Cause:** CORS issue or download endpoint problem

**Fix:**
```python
# Already fixed in updated app.py
# CORS headers automatically added
# Download endpoint: /download/<video_id>
```

---

## 📊 **Folder Management**

### Clean up old videos
```bash
# Show statistics
python cleanup_videos.py stats

# Remove videos older than 24 hours
python cleanup_videos.py clean-old

# Remove videos if folder exceeds 1GB
python cleanup_videos.py clean-size

# Do all cleanup
python cleanup_videos.py clean-all
```

---

## 🔍 **Debug Checklist**

- [ ] Flask server running? (check console output)
- [ ] Port 5000 available? (no other app using it)
- [ ] Model file exists? (check runs/detect folder)
- [ ] Browser opened http://localhost:5000?
- [ ] Can upload image? (test with image first)
- [ ] Can upload video? (then test download)
- [ ] Downloads folder has file? (check your Downloads)
- [ ] File opens in media player? (check file is valid)

---

## 📝 **Console Debugging Tips**

### Enable full error traces
```python
# In app.py, line 280, use:
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Check browser console
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for error messages
4. Screenshot and share if stuck

---

## 🎬 **Test Videos to Use**

Good test videos:
- ✅ Small videos (under 50MB)
- ✅ Common formats (MP4)
- ✅ Resolution: 720p or 1080p
- ✅ FPS: 24-30 fps

Bad test videos:
- ❌ Very large (over 500MB)
- ❌ Rare codecs (ProRes, etc)
- ❌ Very high resolution (8K)

---

## 📞 **Still Having Issues?**

### Provide this info when asking for help:

1. **Console output** (copy all text from console)
2. **Browser console errors** (F12 → Console)
3. **File size** of uploaded video
4. **Video format** (MP4, MOV, AVI)
5. **Which step fails** (upload, process, download)

---

## ✅ **All Bugs Fixed Summary**

| Bug | Severity | Status |
|-----|----------|--------|
| Wrong file extension handling | 🔴 CRITICAL | ✅ FIXED |
| No download endpoint | 🔴 CRITICAL | ✅ FIXED |
| Missing CORS headers | 🟠 HIGH | ✅ FIXED |
| Poor error handling | 🟠 MEDIUM | ✅ FIXED |
| No file verification | 🟠 MEDIUM | ✅ FIXED |
| Inadequate logging | 🟡 LOW | ✅ FIXED |
| Download button issue | 🟡 LOW | ✅ FIXED |
| No cache control | 🟡 LOW | ✅ FIXED |

---

## 🎉 **You're All Set!**

The application should now work perfectly for:
- ✅ Image detection
- ✅ Video processing
- ✅ Video playback
- ✅ Video download
- ✅ Error handling
- ✅ Folder management

Happy detecting! 🚀

---

Generated by: Senior Full Stack Developer  
Date: 2026-09-10
