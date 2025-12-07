# z-Image ComfyUI Multi-Style Production System

**Professional ComfyUI workflow leveraging z-Image's Vision-LLM architecture for automated style variations**

Developed by [Jozef Kubica](https://jozefkubica.com) | December 2025

---

## 🎯 Overview

This workflow system demonstrates a paradigm shift in AI image generation: **text-based style injection** through Vision-LLM integration. Unlike traditional approaches requiring model retraining or LoRA adapters, z-Image's language-model foundation enables dynamic style transformation through prompt engineering alone.

### Why It Matters for Production

**Traditional Approach:**
- Different LoRAs for each brand style
- Retraining required for style changes
- Limited flexibility, high technical overhead

**This System:**
- One workflow, infinite style variations
- Text-based style definitions
- Instant brand adaptation
- Zero retraining required

---

## 🚀 Key Features

### Vision-LLM Architecture Advantage

[z-Image (Alibaba)](https://z-image.vip/en/blog/z-image-turbo-vs-flux-comparison) integrates Vision-LLM capabilities, making it exceptionally prompt-responsive. This creates a strategic advantage:

**Prompt Position = Style Control**

Style descriptions placed before `{$@}` receive higher weighting, enabling automated brand consistency without technical overhead.

```
"Black cyberpunk landscape with neon lights, featuring {$@}"
  ↓
{$@} = "confident young woman"
  ↓
Output: Cyberpunk-styled portrait
```

### Multi-Style System

Six pre-configured styles demonstrate range:

1. **Default** - Clean baseline output
2. **Vintage Photo** - Warm retro aesthetics
3. **Cyberpunk Neon** - Futuristic tech aesthetic
4. **Comic Cover** - Illustrated campaign style
5. **Studio Anime** - Japanese animation aesthetic
6. **B&W Darkroom** - High-fashion editorial

**Extensible:** Add new styles by creating text blocks - no coding required.

---

## 📸 Example Output

**Single Prompt, Six Styles:**

*"Depiction of confident young woman applying luxury skincare serum to radiant skin..."*

Results demonstrate complete style transformation while maintaining subject consistency - ideal for multi-brand campaigns.

---

## 🛠️ System Architecture

### Workflow Components

```
┌─────────────────┐
│   User Prompt   │
│     (Node 4)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────┐
│  Style Nodes    │────▶│ Style Switch │
│   (Nodes 5-10)  │     │   (Node 11)  │
└─────────────────┘     └──────┬───────┘
                               │
                               ▼
                        ┌──────────────┐
                        │String Replace│
                        │   {$@} → 

Prompt │
                        └──────┬───────┘
                               │
                               ▼
            ┌──────────────────────────────┐
            │    Generation Pipeline       │
            │  CLIP → Sampler → VAE Decode │
            └──────────────────────────────┘
```

### Technical Stack

- **Model:** z-Image Turbo (bf16) - Alibaba's Vision-LLM image model
- **Text Encoder:** Qwen 3 4B (Lumina2 type)
- **VAE:** ae.safetensors
- **Switch Logic:** rgthree's Any Switch node
- **Automation:** n8n-compatible for workflow orchestration

---

## 🔧 Installation & Setup

### Prerequisites

```bash
# ComfyUI installation with custom nodes:
- ComfyUI Manager
- rgthree-comfy (for Any Switch node)
```

### Model Downloads

Place these in your ComfyUI models folder:

```
ComfyUI/
├── models/
│   ├── unet/
│   │   └── z_image_turbo_bf16.safetensors
│   ├── clip/
│   │   └── qwen_3_4b.safetensors
│   └── vae/
│       └── ae.safetensors
```

**Model Sources:**
- z-Image: [Hugging Face](https://huggingface.co/stabilityai/z-image)
- Qwen CLIP: [Hugging Face](https://huggingface.co/Qwen/Qwen-VL)

### Workflow Installation

1. Download `Z-Image_style+text2img-Simplified.json`
2. Open ComfyUI
3. Drag & drop JSON file into interface
4. Load workflow

---

## 💡 Usage

### Basic Workflow

1. **Enter Prompt** (Node 4)
   - Keep it general for maximum style flexibility
   - Avoid technical photography terms
   - Example: `"Depiction of [subject], [key details], [mood/lighting]"`

2. **Select Style** (Nodes 5-10)
   - Right-click unused styles → `Bypass`
   - Leave one style active
   - Active style node shows green border

3. **Generate**
   - Queue prompt
   - Wait 8-14 seconds (M4 Pro performance)
   - Output appears in SaveImage node

### Prompt Engineering Tips

**❌ Avoid overly technical prompts:**
```
"Professional DSLR photograph shot with Canon EOS R5, 85mm f/1.4..."
```
Technical details override style injection.

**✅ Use general descriptions:**
```
"Depiction of confident woman holding product, soft light, elegant styling"
```
Allows Vision-LLM to interpret through style lens.

---

## 🚀 Batch Processing

Automated generation for multiple prompts using included Python script.

### Quick Start

```bash
# 1. Create prompts file
cd /path/to/workflows
nano prompts.txt

# Add prompts (one per line):
# Luxury product on marble surface, dramatic lighting
# Professional portrait in modern office, natural light
# Urban street scene at sunset, cinematic atmosphere

# 2. Start ComfyUI
# Load workflow in desktop app

# 3. Run batch script
python3 START_BATCH_FIXED.command
```

### Performance

**M4 Pro Benchmarks:**
- Single image: 8-14 seconds
- 10 prompts: ~2-3 minutes
- 50 prompts: ~10-15 minutes
- Overnight batches: 100+ images hands-off

**Script Features:**
- Automatic seed randomization
- Queue management
- Progress tracking
- Error handling

---

## 🎨 Creating Custom Styles

### Method 1: Text-Based (Recommended)

Add new style node:

```
New Style Node (PrimitiveStringMultiline):
"[Your style description] featuring {$@}"

Examples:
"Minimalist Scandinavian design aesthetic featuring {$@}"
"Dramatic film noir atmosphere with chiaroscuro lighting, depicting {$@}"
"Vibrant pop art illustration with bold colors showing {$@}"
```

Connect to Any Switch node input.

### Method 2: Prompt Position Testing

Experiment with style placement:

**Style Before Subject:**
```
"Cinematic movie still featuring {$@}"
→ Strong style influence
```

**Style After Subject:**
```
"{$@} in cinematic movie style"
→ Subject-focused, subtle style
```

**Balanced:**
```
"Cinematic portrait: {$@}, dramatic atmosphere"
→ Balanced influence
```

---

## 📊 Use Cases

### Agency Workflows

**Multi-Brand Campaigns**
- One prompt → Six brand variations
- Instant client presentations
- Rapid A/B testing

**Production Efficiency**
- Eliminate LoRA training overhead
- Instant style switching
- Reproducible brand consistency

**Creative Exploration**
- Rapid style iteration
- Concept development
- Mood board generation

### Specific Applications

1. **E-Commerce Photography**
   - Product + 6 lifestyle aesthetics
   - Same composition, different brand worlds

2. **Editorial Content**
   - Magazine spread variations
   - Style matching to publication identity

3. **Social Media**
   - Platform-specific aesthetics
   - Trend-responsive styling
   - Consistent brand voice

---

## 🔬 Technical Deep Dive

### Vision-LLM Integration

z-Image's architecture processes text through a large language model before image generation. This creates two advantages:

1. **Semantic Understanding**: Style descriptions are interpreted contextually, not just as keywords
2. **Positional Weighting**: Text position influences generation priority

### Prompt Processing Pipeline

```
User Input
    ↓
Style Template: "[STYLE] featuring {$@}"
    ↓
String Replacement: Replace {$@} with user prompt
    ↓
Vision-LLM Processing: Semantic interpretation
    ↓
Image Generation: Style-aware output
```

### Why Position Matters

Traditional models treat all prompt text equally. Vision-LLMs weight text by position:

```
"Dark moody photo of cat"
vs.
"Cat in dark moody setting"
```

First version emphasizes style (photo characteristics).
Second version emphasizes subject (cat characteristics).

---

## 🔮 Roadmap

### In Development

**Resolution Master Node**
- Any aspect ratio output
- Independent of training resolution
- Intelligent upscaling integration

**QwenVL Prompt Optimizer**
- Image-to-prompt generation
- Style extraction from reference images
- Automatic prompt enhancement

**Extended Style Library**
- 20+ pre-configured styles
- Industry-specific templates
- Seasonal/trend-based styles

---

## 📁 Repository Structure

```
z-image-comfyui-workflows/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── workflows/
│   ├── basic/
│   │   ├── z-image-basic.json        # Simple workflow
│   │   └── README.md                  # Basic usage
│   └── advanced/
│       ├── Z-Image_style+text2img-Simplified.json
│       ├── START_BATCH_FIXED.command  # Batch processing
│       └── BATCH_ANLEITUNG.md         # Batch guide (German)
├── docs/
│   ├── SETUP.md                       # Installation guide
│   ├── PROMPT_ENGINEERING.md          # Prompt tips
│   └── TROUBLESHOOTING.md             # Common issues
└── examples/
    ├── default.png
    ├── cyberpunk.png
    ├── vintage.png
    ├── bw.png
    ├── comic.png
    └── anime.png
```

---

## 🤝 Contributing

Contributions welcome! Areas of interest:

- Additional style templates
- Performance optimizations
- Integration with other tools
- Documentation improvements

---

## 📜 License

MIT License - See LICENSE file for details

---

## 👤 Author

**Jozef Kubica**  
AI Creator | Communication Designer | Photographer

- Website: [jozefkubica.com](https://jozefkubica.com)
- YouTube: [@cre.ai.tiv.company](https://www.youtube.com/@cre.ai.tiv.company)
- LinkedIn: [linkedin.com/in/jozefkubica](https://www.linkedin.com/in/jozefkubica)
- Instagram: [@cre.ai.tiv.company](https://www.instagram.com/cre.ai.tiv.company)

---

## 🙏 Acknowledgments

- Alibaba for z-Image model
- Qwen team for Vision-LLM research
- ComfyUI community for extensible architecture
- rgthree for essential custom nodes

---

## 📞 Contact & Support

**Questions? Collaborations?**
- Email: info@jozefkubica.com
- LinkedIn: Professional inquiries welcome

**Found this useful?**
- ⭐ Star the repository
- 🔗 Share with your network
- 📝 Provide feedback via Issues

---

*Last updated: December 2025*

