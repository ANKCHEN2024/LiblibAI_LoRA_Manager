# -*- coding: utf-8 -*-
import os
import json
import hashlib
import traceback
from datetime import datetime
from safetensors import safe_open
from comfy.sd import load_lora_for_models

class MetadataParser:
    @staticmethod
    def generate_file_fingerprint(file_path):
        file_size = os.path.getsize(file_path)
        modify_time = os.path.getmtime(file_path)
        return f"{file_size}-{modify_time}"

    @staticmethod
    def parse_display_name(raw_name):
        replacements = {
            'v1': '版本1', 'v2': '版本2',
            'portrait': '肖像', 'landscape': '风景'
        }
        return ''.join([replacements.get(part, part) for part in raw_name.split('_')])

class ModelManager:
    def __init__(self):
        self.model_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "lora_models"))
        self.cache_file = os.path.join(self.model_dir, ".model_cache.json")
        self.model_cache = self.load_cache()
        os.makedirs(self.model_dir, exist_ok=True)

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_cache(self):
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.model_cache, f, ensure_ascii=False, indent=2)

    def scan_models(self, force_update=False):
        updated = False
        current_cache = {}

        for root, _, files in os.walk(self.model_dir):
            for filename in files:
                if not filename.lower().endswith(('.safetensors', '.pt')):
                    continue
                
                filepath = os.path.join(root, filename)
                fingerprint = MetadataParser.generate_file_fingerprint(filepath)
                
                if not force_update and filepath in self.model_cache:
                    if self.model_cache[filepath]['fingerprint'] == fingerprint:
                        current_cache[filepath] = self.model_cache[filepath]
                        continue
                
                metadata = self.parse_metadata(filepath)
                display_name = metadata.get('display_name') or MetadataParser.parse_display_name(
                    os.path.splitext(filename)[0])
                
                current_cache[filepath] = {
                    "fingerprint": fingerprint,
                    "display_name": display_name,
                    "internal_name": os.path.splitext(filename)[0],
                    "tags": metadata.get('tags', []),
                    "description": metadata.get('description', ""),
                    "add_time": datetime.now().isoformat()
                }
                updated = True

        if updated:
            self.model_cache = current_cache
            self.save_cache()

        return sorted(current_cache.values(), 
                     key=lambda x: x["add_time"], 
                     reverse=True)

    def parse_metadata(self, filepath):
        try:
            if filepath.endswith('.safetensors'):
                with safe_open(filepath, framework='pt') as f:
                    metadata = json.loads(f.metadata().get('ssmd', '{}'))
                    return {
                        "display_name": metadata.get("display_name"),
                        "tags": metadata.get("tags", []),
                        "description": metadata.get("description", "")
                    }
            return {}
        except Exception as e:
            print(f"[Metadata Error] {filepath}: {str(e)}")
            return {}

class LoRALoader:
    @classmethod
    def INPUT_TYPES(cls):
        manager = ModelManager()
        return {
            "required": {
                "base_model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_model": ("STRING", {
                    "default": "None",
                    "dynamicPrompts": False,
                    "choices": ["None"] + [m["internal_name"] for m in manager.scan_models()]
                }),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1})
            }
        }

    CATEGORY = "LiblibAI/LoRA Management"
    RETURN_TYPES = ("MODEL", "CLIP")
    RETURN_NAMES = ("MODEL_OUT", "CLIP_OUT")
    FUNCTION = "load_lora"

    def load_lora(self, base_model, clip, lora_model="None", strength=1.0):
        if lora_model == "None" or strength == 0:
            return (base_model, clip)
        
        manager = ModelManager()
        model_list = manager.scan_models()
        target_model = next((m for m in model_list if m["internal_name"] == lora_model), None)

        if not target_model:
            raise ValueError(f"Model '{lora_model}' not found\n"
                            f"1. Check file existence in lora_models\n"
                            f"2. Verify file extension (.safetensors/.pt)")

        print(f"🔧 [LiblibAI] Loading LoRA: {target_model['display_name']} (strength:{strength})")
        try:
            new_model, new_clip = load_lora_for_models(
                base_model, clip, 
                target_model["filepath"], 
                strength, strength
            )
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"Load failed: {str(e)}\n"
                              f"Possible reasons:\n"
                              f"1. Corrupted model file\n"
                              f"2. Incompatible with base model")

        return (new_model, new_clip)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return hashlib.sha256(json.dumps(kwargs).encode()).hexdigest()
