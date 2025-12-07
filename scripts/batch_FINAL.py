#!/usr/bin/env python3
"""
Z-Image Batch Processing Script
================================

Batch generates images using z-Image ComfyUI workflow with multiple prompts.
Supports style switching and automated seed randomization.

Setup:
1. Place this script in your ComfyUI root directory
2. Create 'prompts.txt' with one prompt per line
3. Ensure workflow file is in the same directory
4. Start ComfyUI server
5. Run: python3 batch_FINAL.py

Configuration:
- Edit WORKFLOW_FILE to match your workflow filename
- Edit ACTIVE_STYLE_NODE_ID to switch styles (see Style Options below)
- Edit COMFYUI_URL if using non-default port

Style Options (ACTIVE_STYLE_NODE_ID):
- 5  = Default (no style)
- 6  = Vintage Photo
- 7  = Cyberpunk Neon
- 8  = Comic Cover
- 9  = Studio Anime
- 10 = B&W Darkroom
"""

import json
import requests
import time
import copy
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# ComfyUI Server URL (default: http://127.0.0.1:8188)
COMFYUI_URL = "http://127.0.0.1:8188"

# Workflow file (relative to this script)
WORKFLOW_FILE = "Z-Image_style+text2img-Simplified.json"

# Prompts file (one prompt per line)
PROMPTS_FILE = "prompts.txt"

# Active style node ID (see Style Options in docstring above)
ACTIVE_STYLE_NODE_ID = 5

# Node types to skip during conversion
SKIP_NODES = ['Note', 'Reroute']

# ============================================================================
# FUNCTIONS
# ============================================================================

def get_active_style_text(workflow, style_node_id):
    """Extract style text from the active style node"""
    for node in workflow['nodes']:
        if node['id'] == style_node_id:
            return node.get('widgets_values', ['{$@}'])[0]
    return '{$@}'  # Fallback: no style

def convert_workflow_to_api_format(workflow, prompt_text, style_text):
    """
    Convert workflow to ComfyUI API format.
    Injects prompt_text and style_text into the workflow.
    """
    
    # Collect nodes to bypass
    bypass_node_ids = set()
    for node in workflow['nodes']:
        if node['type'] in SKIP_NODES or ('mode' in node and node['mode'] == 4):
            bypass_node_ids.add(str(node['id']))
    
    api_workflow = {}
    
    for node in workflow['nodes']:
        node_id = str(node['id'])
        node_type = node['type']
        
        if node_id in bypass_node_ids:
            continue
        
        # Skip PrimitiveNodes and Any Switch (we set style directly)
        if node_type in ['PrimitiveNode', 'PrimitiveString', 'PrimitiveStringMultiline', 'Any Switch (rgthree)']:
            continue
            
        api_workflow[node_id] = {
            "class_type": node_type,
            "inputs": {}
        }
        
        # Handle widget values
        if 'widgets_values' in node and node['widgets_values']:
            
            if node_type == 'UNETLoader':
                api_workflow[node_id]['inputs']['unet_name'] = node['widgets_values'][0]
                if len(node['widgets_values']) > 1:
                    api_workflow[node_id]['inputs']['weight_dtype'] = node['widgets_values'][1]
                else:
                    api_workflow[node_id]['inputs']['weight_dtype'] = 'default'
                    
            elif node_type == 'CLIPLoader':
                api_workflow[node_id]['inputs']['clip_name'] = node['widgets_values'][0]
                if len(node['widgets_values']) > 1:
                    api_workflow[node_id]['inputs']['type'] = node['widgets_values'][1]
                if len(node['widgets_values']) > 2:
                    api_workflow[node_id]['inputs']['device'] = node['widgets_values'][2]
                    
            elif node_type == 'VAELoader':
                api_workflow[node_id]['inputs']['vae_name'] = node['widgets_values'][0]
                
            elif node_type == 'CLIPTextEncode':
                api_workflow[node_id]['inputs']['text'] = node['widgets_values'][0]
                
            elif node_type == 'StringReplace':
                # CRITICAL: Set all three values directly!
                wv = node['widgets_values']
                api_workflow[node_id]['inputs']['string'] = style_text      # ← Style text
                api_workflow[node_id]['inputs']['find'] = wv[1] if len(wv) > 1 else '{$@}'
                api_workflow[node_id]['inputs']['replace'] = prompt_text    # ← User prompt
                
            elif node_type == 'KSamplerAdvanced':
                wv = node['widgets_values']
                api_workflow[node_id]['inputs'] = {
                    'add_noise': wv[0] if len(wv) > 0 else 'enable',
                    'noise_seed': wv[1] if len(wv) > 1 else 1,
                    'control_after_generate': wv[2] if len(wv) > 2 else 'randomize',
                    'steps': wv[3] if len(wv) > 3 else 8,
                    'cfg': wv[4] if len(wv) > 4 else 1,
                    'sampler_name': wv[5] if len(wv) > 5 else 'euler',
                    'scheduler': wv[6] if len(wv) > 6 else 'simple',
                    'start_at_step': wv[7] if len(wv) > 7 else 0,
                    'end_at_step': wv[8] if len(wv) > 8 else 10000,
                    'return_with_leftover_noise': wv[9] if len(wv) > 9 else 'disable'
                }
                
            elif node_type == 'EmptyLatentImage':
                wv = node['widgets_values']
                api_workflow[node_id]['inputs'] = {
                    'width': wv[0] if len(wv) > 0 else 944,
                    'height': wv[1] if len(wv) > 1 else 1408,
                    'batch_size': wv[2] if len(wv) > 2 else 1
                }
                
            elif node_type == 'SaveImage':
                api_workflow[node_id]['inputs']['filename_prefix'] = node['widgets_values'][0]
        
        # Handle connections (skip to PrimitiveNodes and Any Switch)
        if 'inputs' in node:
            for inp in node['inputs']:
                if 'link' in inp and inp['link'] is not None:
                    for link in workflow['links']:
                        if link[0] == inp['link']:
                            source_node = str(link[1])
                            source_output = link[2]
                            
                            source_node_obj = next((n for n in workflow['nodes'] if n['id'] == int(source_node)), None)
                            
                            if source_node_obj:
                                source_type = source_node_obj['type']
                                
                                # Skip PrimitiveNodes, Any Switch AND bypass nodes
                                if source_type in ['PrimitiveNode', 'PrimitiveString', 'PrimitiveStringMultiline', 'Any Switch (rgthree)']:
                                    continue
                                    
                                if source_node in bypass_node_ids:
                                    continue
                                
                                api_workflow[node_id]['inputs'][inp['name']] = [source_node, source_output]
                            break
    
    return api_workflow

def queue_prompt(api_workflow):
    """Queue a prompt to ComfyUI server"""
    try:
        response = requests.post(
            f"{COMFYUI_URL}/prompt",
            json={"prompt": api_workflow, "client_id": "batch_processor"}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"      ✗ Error: {e}")
        if hasattr(e, 'response'):
            print(f"      Response: {e.response.text[:300]}")
        return None

def main():
    """Main batch processing function"""
    print("=" * 70)
    print("🚀 Z-IMAGE BATCH PROCESSOR")
    print("=" * 70)
    print()
    
    # Check ComfyUI connection
    try:
        requests.get(COMFYUI_URL, timeout=2)
        print(f"✅ ComfyUI running at {COMFYUI_URL}")
    except:
        print(f"✗ ComfyUI not reachable at {COMFYUI_URL}")
        print(f"  Make sure ComfyUI is running!")
        return
    
    # Check workflow file
    workflow_path = Path(WORKFLOW_FILE)
    if not workflow_path.exists():
        print(f"✗ Workflow file not found: {WORKFLOW_FILE}")
        print(f"  Current directory: {Path.cwd()}")
        return
    
    print(f"✅ Workflow: {WORKFLOW_FILE}")
    
    with open(workflow_path, 'r') as f:
        workflow_template = json.load(f)
    
    # Get style text
    style_text = get_active_style_text(workflow_template, ACTIVE_STYLE_NODE_ID)
    print(f"✅ Style: Node {ACTIVE_STYLE_NODE_ID}")
    print(f"   → {style_text[:70]}...")
    
    # Check prompts file
    prompts_path = Path(PROMPTS_FILE)
    if not prompts_path.exists():
        print(f"✗ Prompts file not found: {PROMPTS_FILE}")
        print(f"  Create a file with one prompt per line.")
        return
    
    print(f"✅ Prompts: {PROMPTS_FILE}")
    
    with open(prompts_path, 'r', encoding='utf-8') as f:
        prompts = [line.strip() for line in f if line.strip()]
    
    if not prompts:
        print(f"✗ No prompts found in {PROMPTS_FILE}")
        return
    
    print(f"✅ {len(prompts)} prompts loaded\n")
    
    # Preview prompts
    print("📋 PROMPTS:")
    print("-" * 70)
    for i, p in enumerate(prompts[:5], 1):
        print(f"   {i}. {p[:65]}...")
    if len(prompts) > 5:
        print(f"   ... +{len(prompts)-5} more")
    print("-" * 70)
    print()
    
    # Confirm
    resp = input(f"➡️  Generate {len(prompts)} images? (y/n): ")
    if resp.lower() not in ['y', 'yes', 'j', 'ja']:
        print("✗ Cancelled")
        return
    
    print()
    print("🎨 BATCH PROCESSING")
    print("=" * 70)
    print()
    
    success = 0
    
    for i, prompt in enumerate(prompts, 1):
        workflow = copy.deepcopy(workflow_template)
        
        # Update seed in KSamplerAdvanced (Node 17)
        for node in workflow['nodes']:
            if node['id'] == 17 and node['type'] == 'KSamplerAdvanced':
                new_seed = int(time.time() * 1000) + i
                if len(node['widgets_values']) > 1:
                    node['widgets_values'][1] = new_seed
        
        print(f"[{i}/{len(prompts)}] {prompt[:60]}...")
        
        # Convert with prompt AND style
        api_wf = convert_workflow_to_api_format(workflow, prompt, style_text)
        
        result = queue_prompt(api_wf)
        
        if result and 'prompt_id' in result:
            print(f"   ✅ Queued! (ID: {result['prompt_id']})")
            success += 1
        
        print()
        
        # Delay between requests (except last one)
        if i < len(prompts):
            time.sleep(2)
    
    print("=" * 70)
    print(f"✅ Successfully queued: {success}/{len(prompts)}")
    print("=" * 70)
    print()
    print("💡 TIP: Check ComfyUI interface to monitor generation progress")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n✗ Cancelled by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
