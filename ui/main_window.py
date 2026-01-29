import customtkinter as ctk
import sys
import os
import numpy as np

# Adicionar raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chat.hybrid_ai import HybridAIChat
from ui.training_view import TrainingView
from autonomy.resource_manager import SovereignResourceManager

class SovereignApp(ctk.CTk):
    """
    Interface Desktop Moderna Soberana (V11).
    Versão Consolidada: Chat Híbrido + Treinamento Visual.
    """
    def __init__(self):
        super().__init__()

        self.title("Neural Multimodal Sovereign V11 - Platform")
        self.geometry("1100x700")
        ctk.set_appearance_mode("dark")

        # Gerenciador de Recursos
        self.resource_manager = SovereignResourceManager()

        # Configuração de Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Sidebar (Navegação)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column: 0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="SOVEREIGN V11", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column: 0, padx=20, pady=(20, 10))

        self.chat_button = ctk.CTkButton(self.sidebar_frame, text="💬 Chat Híbrido", command=self.show_chat)
        self.chat_button.grid(row=1, column: 0, padx=20, pady=10)

        self.train_button = ctk.CTkButton(self.sidebar_frame, text="🏋️ Treinamento", command=self.show_training)
        self.train_button.grid(row=2, column: 0, padx=20, pady=10)

        self.gov_button = ctk.CTkButton(self.sidebar_frame, text="🌐 Governança", command=self.show_gov)
        self.gov_button.grid(row=3, column: 0, padx=20, pady=10)

        # 2. Main Content Area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column: 1, sticky="nsew", padx=20, pady=20)
        
        # Inicializar Chat AI (Mock params)
        mock_params = {
            'vision_w': np.random.randn(784, 32), 'vision_b': np.zeros((1, 32)),
            'text_w': np.random.randn(32, 32), 'text_b': np.zeros((1, 32)),
            'classifier_w': np.random.randn(64, 1), 'classifier_b': np.zeros((1, 1))
        }
        self.chat_engine = HybridAIChat(mock_params)

        # Mostrar Chat por padrão
        self.show_chat()

    def show_chat(self):
        self._clear_main_frame()
        
        chat_label = ctk.CTkLabel(self.main_frame, text="💬 Chat AI Híbrido", font=ctk.CTkFont(size=24, weight="bold"))
        chat_label.pack(pady=10)

        self.chat_display = ctk.CTkTextbox(self.main_frame, width=800, height=400)
        self.chat_display.pack(padx=20, pady=10, fill="both", expand=True)

        self.input_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Digite sua mensagem multimodal...")
        self.input_entry.pack(padx=20, pady=10, fill="x")
        self.input_entry.bind("<Return>", self.send_message)

        self.send_btn = ctk.CTkButton(self.main_frame, text="Enviar", command=self.send_message)
        self.send_btn.pack(pady=10)

    def send_message(self, event=None):
        text = self.input_entry.get()
        if text:
            self.chat_display.insert("end", f"👤 Você: {text}\n")
            self.input_entry.delete(0, "end")
            
            # Processar via Chat Engine
            response, explanation = self.chat_engine.process_message(text)
            
            self.chat_display.insert("end", f"🤖 Sovereign: {response}\n")
            self.chat_display.insert("end", f"💡 XAI: {explanation['reasoning']}\n\n")
            self.chat_display.see("end")

    def show_training(self):
        self._clear_main_frame()
        self.training_view = TrainingView(self.main_frame, self.resource_manager)
        self.training_view.pack(fill="both", expand=True)

    def show_gov(self):
        self._clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="🌐 Governança de Enxame", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=20)
        
        info = ctk.CTkLabel(self.main_frame, text="Reputação e Consenso Bizantino Ativos.")
        info.pack()

    def _clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = SovereignApp()
    print("🖥️ Plataforma Desktop V11 inicializada com sucesso.")
    # app.mainloop()
