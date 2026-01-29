import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modalities.code.processor import CodeProcessor, LogicValidator
import numpy as np

def test_code_logic():
    print("🧪 Testando Núcleo de Código e Raciocínio Lógico...")
    
    # 1. Setup do Processador de Código
    # Vocab: 50 tokens, Emb: 16, Hidden: 32
    cp = CodeProcessor(50, 16, 32)
    
    # Simular tokens de código: [IF, VAR, ASSIGN, VALUE]
    code_tokens = [10, 2, 5, 20]
    
    # Forward Pass
    logic_vector = cp(code_tokens)
    
    # Verificação de Dimensões
    assert logic_vector.data.shape == (1, 16), f"Shape lógico incorreto: {logic_vector.data.shape}"
    print("✅ Processamento de Tokens de Código Validado!")
    
    # 2. Testar Validador de Lógica (Sintaxe)
    valid_code = "x = 10\nif x > 5: print(x)"
    invalid_code = "if x > 5 print(x)" # Erro de sintaxe (falta :)
    
    assert LogicValidator.verify_syntax(valid_code) == True
    assert LogicValidator.verify_syntax(invalid_code) == False
    print("✅ Validador de Sintaxe Lógica Validado!")

if __name__ == "__main__":
    try:
        test_code_logic()
    except Exception as e:
        print(f"❌ Falha no Teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
