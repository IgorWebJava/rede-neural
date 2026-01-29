import os

def generate_doc_summary():
    print("📝 Gerando Sumário de Documentação Técnica...")
    
    summary_content = "# 📚 Sumário de Documentação Técnica (Auto-Generated)\n\n"
    summary_content += "Este arquivo lista todos os recursos técnicos disponíveis na SKILL para consulta rápida do agente.\n\n"
    
    # Mapear referências
    summary_content += "## 📖 Referências Arquiteturais\n"
    if os.path.isdir("references"):
        for file in sorted(os.listdir("references")):
            if file.endswith(".md"):
                title = file.replace(".md", "").replace("_", " ").title()
                summary_content += f"- **{title}**: `references/{file}`\n"
    
    # Mapear templates
    summary_content += "\n## 🛠️ Templates de Código (Kernels)\n"
    if os.path.isdir("templates"):
        for file in sorted(os.listdir("templates")):
            if file.endswith(".py"):
                summary_content += f"- **Kernel**: `templates/{file}`\n"
            elif file.endswith(".md"):
                summary_content += f"- **Template**: `templates/{file}`\n"
            elif file.endswith(".yaml"):
                summary_content += f"- **Config**: `templates/{file}`\n"

    with open("references/TECHNICAL_SUMMARY.md", "w") as f:
        f.write(summary_content)
    
    print("✅ TECHNICAL_SUMMARY.md gerado em references/.")

if __name__ == "__main__":
    generate_doc_summary()
