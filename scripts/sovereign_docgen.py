import os
import inspect
import sys

# Adicionar raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class SovereignDocGen:
    """
    Motor de Auto-Documentação Dinâmica (RULE 14).
    V10: Analisa a estrutura do projeto e gera um sumário técnico atualizado.
    """
    def __init__(self, root_dir="."):
        self.root_dir = root_dir

    def generate_summary(self):
        summary = "# 📚 Sumário Técnico Evolutivo (V10)\n\n"
        summary += "Gerado automaticamente pelo Sovereign DocGen.\n\n"
        
        for root, dirs, files in os.walk(self.root_dir):
            # Ignorar diretórios ocultos e __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            level = root.replace(self.root_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            folder = os.path.basename(root)
            
            if folder:
                summary += f"{indent}- **📁 {folder}/**\n"
            
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                if f.endswith('.py'):
                    summary += f"{sub_indent}- 📄 {f}\n"
        
        return summary

    def save_doc(self, output_path="./docs/AUTO_GENERATED_SUMMARY.md"):
        content = self.generate_summary()
        with open(output_path, 'w') as f:
            f.write(content)
        print(f"✅ Documentação gerada em {output_path}")

if __name__ == "__main__":
    docgen = SovereignDocGen()
    docgen.save_doc()
