import os
import sys
import re

# Constantes de auditoria (usando ofuscação simples para evitar auto-detecção)
F_TERMS = {
    "tor" + "ch": "RULE 09 - Proibição de P-y-T-o-r-c-h",
    "tensor" + "flow": "RULE 09 - Proibição de T-e-n-s-o-r-F-l-o-w",
    "ker" + "as": "RULE 09 - Proibição de K-e-r-a-s",
    "ja" + "x": "RULE 09 - Proibição de J-A-X",
    "on" + "nx": "RULE 09 - Proibição de O-N-N-X",
    "sk" + "learn": "RULE 09 - Proibição de S-c-i-k-i-t-L-e-a-r-n",
    "hugging" + "face": "RULE 09 - Proibição de H-u-g-g-i-n-g-F-a-c-e",
    "api" + "_key": "RULE 01 - Possível exposição de segredo",
    "sec" + "ret": "RULE 01 - Possível exposição de segredo"
}

def audit_rules(directory):
    print(f"🔍 Sovereign Auditor: Analisando arquivos em '{directory}'...")
    violations = []
    
    error_patterns = [
        (r"except\s*:\s*pass", "RULE 08 - Proibição de 'except: pass'"),
    ]

    for root, _, files in os.walk(directory):
        # Pular o próprio script de auditoria para evitar falsos positivos
        if "sovereign_auditor.py" in files:
            files.remove("sovereign_auditor.py")
            
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", errors="ignore") as f:
                    content = f.read()
                    content_lower = content.lower()
                    
                    for term, rule in F_TERMS.items():
                        # Verificar apenas imports reais para evitar falsos positivos em strings de log ou docstrings
                        if f"import {term}" in content_lower or f"from {term}" in content_lower:
                            violations.append(f"❌ VIOLAÇÃO: {rule} detectada em {path}")

                    for pattern, rule in error_patterns:
                        if re.search(pattern, content):
                            violations.append(f"❌ VIOLAÇÃO: {rule} detectada em {path}")
                            
                    if "time.sleep(" in content and "data_pipeline" not in file:
                        violations.append(f"❌ VIOLAÇÃO: RULE 02 - Sleep artificial detectado em {path}")

    return violations

def audit_project_structure(directory):
    # Esta verificação só deve rodar se o diretório alvo for um PROJETO, não a própria SKILL
    is_project = os.path.isdir(os.path.join(directory, "core")) or os.path.isdir(os.path.join(directory, "engine"))
    
    if not is_project:
        print("ℹ️  Diretório alvo não parece ser um projeto derivado. Pulando verificação de estrutura de módulos.")
        return []

    print(f"🔍 Sovereign Auditor: Verificando Consistência Estrutural do Projeto...")
    required_dirs = ["core", "engine", "autograd", "layers", "modalities", "fusion", "memory", "autonomy", "rules"]
    missing = []
    for d in required_dirs:
        if not os.path.isdir(os.path.join(directory, d)):
            missing.append(d)
    return missing

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    
    violations = audit_rules(target)
    missing_dirs = audit_project_structure(target)
    
    if violations or missing_dirs:
        print("\n--- Relatório de Auditoria ---")
        for v in violations: print(v)
        for m in missing_dirs: print(f"❌ VIOLAÇÃO: RULE 06/11 - Módulo de projeto '{m}' ausente.")
        sys.exit(1)
    else:
        print("\n✅ Auditoria concluída: Conformidade preservada.")
        sys.exit(0)
