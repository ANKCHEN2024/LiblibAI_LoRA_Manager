# -*- coding: utf-8 -*-
from .lora_manager import LoRALoader as LiblibAI_LoRA_Loader
from .lora_manager import ModelManager

NODE_CLASS_MAPPINGS = {
    "LiblibAI_LoRALoader": LiblibAI_LoRA_Loader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LiblibAI_LoRALoader": "📥 LoRA Loader - LiblibAI"
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
