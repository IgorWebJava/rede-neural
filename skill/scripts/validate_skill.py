#!/usr/bin/env python3
"""
Script de validação para a skill Neural Multimodal Sovereign.
Verifica conformidade com a nova estrutura e padrões da comunidade.
"""

import os
import sys
import yaml
from pathlib import Path

def validate_skill(skill_path):
    """Valida a estrutura e conteúdo da skill."""
    errors = []
    warnings = []
    
    # Verifica existência do SKILL.md
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md não encontrado")
        return errors, warnings
    
    # Verifica frontmatter
    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()
        if not content.startswith('---'):
            errors.append("Frontmatter YAML ausente no SKILL.md")
        else:
            # Extrai e valida frontmatter
            try:
                parts = content.split('---')
                if len(parts) < 3:
                    errors.append("Formato de frontmatter inválido no SKILL.md")
                else:
                    frontmatter = parts[1]
                    metadata = yaml.safe_load(frontmatter)
                    
                    required_fields = ['name', 'description', 'category', 'version']
                    for field in required_fields:
                        if field not in metadata:
                            errors.append(f"Campo obrigatório '{field}' ausente no frontmatter")
                    
                    recommended_fields = ['tags', 'author', 'compatibility', 'license']
                    for field in recommended_fields:
                        if field not in metadata:
                            warnings.append(f"Campo recomendado '{field}' ausente no frontmatter")
            except Exception as e:
                errors.append(f"Erro ao processar frontmatter: {e}")
    
    # Verifica estrutura de diretórios
    required_dirs = ['architecture', 'prompts', 'templates', 'examples', 'scripts']
    for dir_name in required_dirs:
        if not (skill_path / dir_name).exists():
            errors.append(f"Diretório obrigatório '{dir_name}' não encontrado")
    
    # Verifica README.md
    if not (skill_path / "README.md").exists():
        errors.append("README.md não encontrado")
    
    # Verifica CHANGELOG.md
    if not (skill_path / "CHANGELOG.md").exists():
        warnings.append("CHANGELOG.md não encontrado (recomendado para versionamento)")
        
    # Verifica se existem arquivos .txt (não recomendados)
    txt_files = list(skill_path.glob("**/*.txt"))
    if txt_files:
        warnings.append(f"Encontrados {len(txt_files)} arquivos .txt. Recomenda-se usar apenas .md")
    
    return errors, warnings

if __name__ == "__main__":
    # O script está em scripts/, então o path da skill é o pai
    skill_path = Path(__file__).parent.parent
    errors, warnings = validate_skill(skill_path)
    
    print(f"\n--- Validação da Skill: {skill_path.name} ---\n")
    
    if errors:
        print("❌ ERROS ENCONTRADOS:")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("\n⚠️  AVISOS:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors:
        print("\n✅ Estrutura básica da skill validada com sucesso!")
    
    sys.exit(1 if errors else 0)
