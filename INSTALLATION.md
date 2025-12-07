# Installation & Setup Guide

## 📋 Prerequisites

- **ComfyUI** installed and running
- **z-Image model** installed in ComfyUI
- **Python 3.7+** with `requests` library
- **Workflow file** downloaded from this repository

---

## 🚀 Quick Start

### 1. Download Repository

**Option A: Download ZIP**
1. Click green "Code" button → "Download ZIP"
2. Extract to your preferred location

**Option B: Git Clone**
```bash
git clone https://github.com/creaitivcompany/z-image-comfyui-workflow.git
cd z-image-comfyui-workflow
```

---

### 2. Install z-Image Model

If you haven't already:

1. **Download z-Image Turbo model:**
   - Visit [z-Image website](https://z-image.vip/)
   - Download the model file (typically `z-image-turbo-bf16.safetensors`)

2. **Place in ComfyUI:**
   ```
   ComfyUI/models/unet/z-image-turbo-bf16.safetensors
   ```

3. **Download required CLIP:**
   - Model: Qwen 3 4B (Lumina2 type)
   - Path: `ComfyUI/models/text_encoders/`

4. **Download VAE:**
   - Required: `ae.safetensors`
   - Path: `ComfyUI/models/vae/`

---

### 3. Import Workflow into ComfyUI

1. Open ComfyUI in your browser (usually http://127.0.0.1:8188)
2. Click "Load" button
3. Navigate to: `workflows/Z-Image_style+text2img-Simplified.json`
4. Click "Open"

✅ Workflow should now be loaded in ComfyUI!

---

### 4. Setup Batch Processing (Optional)

#### Create prompts file

1. Copy example file:
   ```bash
   cp prompts_EXAMPLE.txt prompts.txt
   ```

2. Edit `prompts.txt` with your own prompts (one per line)

#### Configure script

Edit `batch_FINAL.py` if needed:

```python
# Line 30-38: Configuration section
COMFYUI_URL = "http://127.0.0.1:8188"  # Change if using different port
WORKFLOW_FILE = "Z-Image_style+text2img-Simplified.json"
PROMPTS_FILE = "prompts.txt"
ACTIVE_STYLE_NODE_ID = 5  # Change for different styles
```

**Style Options:**
- `5` = Default (no style)
- `6` = Vintage Photo
- `7` = Cyberpunk Neon
- `8` = Comic Cover
- `9` = Studio Anime
- `10` = B&W Darkroom

#### Install Python dependencies

```bash
pip install requests
```

---

## 🎬 Usage

### Manual Workflow (ComfyUI Interface)

1. **Load workflow** in ComfyUI
2. **Enter your prompt** in Node 4 ("User Prompt")
3. **Select style** using Node 11 ("Any Switch")
   - Index 0 = Default
   - Index 1 = Vintage
   - Index 2 = Cyberpunk
   - etc.
4. **Click "Queue Prompt"**

### Batch Processing (Automated)

#### macOS:
```bash
cd /path/to/z-image-comfyui-workflow
./START_BATCH_FIXED.command
```

#### Windows/Linux:
```bash
cd /path/to/z-image-comfyui-workflow
python3 batch_FINAL.py
```

**What happens:**
1. Script loads workflow
2. Reads prompts from `prompts.txt`
3. Shows preview of prompts
4. Asks for confirmation
5. Queues all prompts to ComfyUI
6. ComfyUI processes them sequentially

**Output location:**
- ComfyUI default: `ComfyUI/output/`

---

## 🔧 Troubleshooting

### "ComfyUI not reachable"

**Check:**
1. Is ComfyUI running? Open http://127.0.0.1:8188 in browser
2. Using custom port? Update `COMFYUI_URL` in `batch_FINAL.py`

**Fix:**
```bash
# Start ComfyUI if not running
cd /path/to/ComfyUI
python main.py
```

---

### "Workflow file not found"

**Check:**
1. Are you in the correct directory?
   ```bash
   pwd  # Should show z-image-comfyui-workflow directory
   ```
2. Is workflow file present?
   ```bash
   ls workflows/
   ```

**Fix:**
- Place script in same directory as workflow file, OR
- Update `WORKFLOW_FILE` path in script

---

### "Prompts file not found"

**Create prompts.txt:**
```bash
cat > prompts.txt << EOF
Depiction of confident young woman applying luxury skincare serum
Depiction of athletic person doing yoga at sunrise
EOF
```

Or copy example:
```bash
cp prompts_EXAMPLE.txt prompts.txt
```

---

### Models not loading in ComfyUI

**Check model paths:**
```
ComfyUI/
├── models/
│   ├── unet/
│   │   └── z-image-turbo-bf16.safetensors
│   ├── text_encoders/
│   │   └── qwen_3_4b.safetensors
│   └── vae/
│       └── ae.safetensors
```

**Refresh ComfyUI:**
- Click "Refresh" button in node selector
- Restart ComfyUI server

---

### Wrong style applied

**In manual workflow:**
- Check Node 11 ("Any Switch") index setting
- Index matches style order (0=first, 1=second, etc.)

**In batch script:**
- Check `ACTIVE_STYLE_NODE_ID` in `batch_FINAL.py`
- Node ID matches style node in workflow

---

### Slow generation

**Normal speeds:**
- M4 Pro: 8-14 seconds per image
- M1 Pro: 15-25 seconds per image
- NVIDIA RTX 4090: 5-10 seconds per image

**Speed tips:**
1. Reduce steps in KSampler (default: 8)
2. Use bf16 model version (faster than fp32)
3. Close other GPU-intensive applications

---

## 📁 File Structure Reference

```
z-image-comfyui-workflow/
├── README.md                           # Main documentation
├── INSTALLATION.md                     # This file
├── LICENSE                             # MIT License
│
├── workflows/
│   └── Z-Image_style+text2img-Simplified.json  # Main workflow
│
├── scripts/
│   ├── START_BATCH_FIXED.command      # macOS launcher
│   └── batch_FINAL.py                  # Batch processor
│
├── docs/
│   └── BATCH_ANLEITUNG.md             # Batch processing guide (German)
│
├── examples/
│   ├── z-image-default.png
│   ├── z-image-cyberpunk.png
│   └── ... (other style examples)
│
├── prompts_EXAMPLE.txt                 # Example prompts
└── prompts.txt                         # Your prompts (create this)
```

---

## 🎓 Next Steps

1. **Experiment with styles:** Try different `ACTIVE_STYLE_NODE_ID` values
2. **Create custom styles:** Edit style nodes directly in workflow
3. **Optimize settings:** Adjust steps, CFG, resolution for your needs
4. **Share results:** Tag @cre.ai.tiv.company on Instagram!

---

## 💬 Support

**Issues?** 
- Open an issue on GitHub
- Check existing issues first

**Questions?**
- See main README.md for detailed workflow documentation
- Check [ComfyUI Discord](https://discord.gg/comfyui) for general ComfyUI help

---

## 📚 Additional Resources

- **z-Image Documentation:** https://z-image.vip/
- **ComfyUI Wiki:** https://github.com/comfyanonymous/ComfyUI
- **Author's Portfolio:** https://jozefkubica.com
- **AI Video Content:** https://www.youtube.com/@cre.ai.tiv.company

---

**Happy generating!** 🎨
