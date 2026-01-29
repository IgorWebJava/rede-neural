import os
import sys
import re

def check_skill_compliance():
    print("🔍 Iniciando Linter de Conformidade da SKILL...")
    errors = []
    warnings = []
    
    # 1. Verificar SKILL.md
    if not os.path.exists("SKILL.md"):
        errors.append("❌ SKILL.md não encontrado na raiz.")
    else:
        with open("SKILL.md", "r") as f:
            content = f.read()
            # Verificar Frontmatter
            if not content.startswith("---"):
                errors.append("❌ SKILL.md deve começar com frontmatter YAML (---).")
            
            # Verificar campos proibidos no frontmatter
            forbidden_fields = ["category", "tags", "version", "author", "compatibility", "license"]
            frontmatter = content.split("---")[1] if "---" in content else ""
            for field in forbidden_fields:
                if f"{field}:" in frontmatter:
                    warnings.append(f"⚠️ Campo não padrão '{field}' encontrado no frontmatter.")
            
            # Verificar tamanho
            lines = content.splitlines()
            if len(lines) > 500:
                warnings.append(f"⚠️ SKILL.md muito longo ({len(lines)} linhas). Considere mover detalhes para references/.")

    # 2. Verificar Estrutura de Pastas
    required_dirs = ["references", "templates", "scripts"]
    for d in required_dirs:
        if not os.path.isdir(d):
            errors.append(f"❌ Diretório obrigatório '{d}/' não encontrado.")

    # 3. Verificar Arquivos Proibidos
    forbidden_files = ["README.md", "CHANGELOG.md", "LICENSE.txt"]
    for f in forbidden_files:
        if os.path.exists(f):
            warnings.append(f"⚠️ Arquivo não recomendado '{f}' encontrado na raiz da SKILL.")

    # 4. Verificar Progressive Disclosure
    if os.path.isdir("references"):
        ref_files = os.listdir("references")
        if len(ref_files) < 3:
            warnings.append("⚠️ Poucos arquivos em references/. Use mais Progressive Disclosure.")

    # Resultado
    print("\n--- Relatório de Validação ---")
    for e in errors: print(e)
    for w in warnings: print(w)
    
    if not errors:
        print("\n✅ SKILL aprovada com sucesso (com possíveis avisos).")
        return True
    else:
        print("\n❌ SKILL reprovada. Corrija os erros acima.")
        return False

if __name__ == "__main__":
    success = check_skill_compliance()
    sys.exit(0 if success else 1)
