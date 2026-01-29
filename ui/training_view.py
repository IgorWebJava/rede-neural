import customtkinter as ctk
import time
import threading
import random

class TrainingView(ctk.CTkFrame):
    """
    Página de Treinamento Visual Soberana (V11).
    Integra métricas de hardware e progresso neural em Python nativo.
    """
    def __init__(self, master, resource_manager, **kwargs):
        super().__init__(master, **kwargs)
        self.resource_manager = resource_manager
        self.is_training = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 1. Header
        self.header = ctk.CTkLabel(self, text="🏋️ Centro de Treinamento Soberano", font=ctk.CTkFont(size=22, weight="bold"))
        self.header.grid(row=0, column: 0, columnspan=2, pady=20)

        # 2. Métricas de Hardware (Esquerda)
        self.hw_frame = ctk.CTkFrame(self)
        self.hw_frame.grid(row=1, column: 0, padx=20, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.hw_frame, text="📊 Monitor de Recursos", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        self.cpu_label = ctk.CTkLabel(self.hw_frame, text="CPU: 0%")
        self.cpu_label.pack()
        
        self.mem_label = ctk.CTkLabel(self.hw_frame, text="Memória: 0%")
        self.mem_label.pack()
        
        self.temp_label = ctk.CTkLabel(self.hw_frame, text="Temperatura: 0°C")
        self.temp_label.pack()

        # 3. Métricas Neurais (Direita)
        self.neural_frame = ctk.CTkFrame(self)
        self.neural_frame.grid(row=1, column: 1, padx=20, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.neural_frame, text="🧠 Performance Neural", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        self.loss_label = ctk.CTkLabel(self.neural_frame, text="Loss: --")
        self.loss_label.pack()
        
        self.acc_label = ctk.CTkLabel(self.neural_frame, text="Acurácia: --")
        self.acc_label.pack()

        # 4. Controles
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=2, column: 0, columnspan=2, pady=20)
        
        self.start_btn = ctk.CTkButton(self.control_frame, text="Iniciar Treino", fg_color="green", command=self.toggle_training)
        self.start_btn.pack(side="left", padx=10)
        
        self.stop_btn = ctk.CTkButton(self.control_frame, text="Parar", fg_color="red", command=self.stop_training)
        self.stop_btn.pack(side="left", padx=10)

        # Iniciar monitor de hardware
        self.update_hw_stats()

    def toggle_training(self):
        if not self.is_training:
            self.is_training = True
            self.start_btn.configure(text="Pausar", fg_color="orange")
            threading.Thread(target=self.simulate_training, daemon=True).start()
        else:
            self.is_training = False
            self.start_btn.configure(text="Continuar", fg_color="green")

    def stop_training(self):
        self.is_training = False
        self.start_btn.configure(text="Iniciar Treino", fg_color="green")
        self.loss_label.configure(text="Loss: --")
        self.acc_label.configure(text="Acurácia: --")

    def simulate_training(self):
        epoch = 0
        while self.is_training:
            epoch += 1
            loss = max(0.1, 1.0 / (epoch * 0.5 + 1) + random.uniform(-0.05, 0.05))
            acc = min(0.99, 0.5 + (epoch * 0.02) + random.uniform(-0.01, 0.01))
            
            self.loss_label.configure(text=f"Loss: {loss:.4f}")
            self.acc_label.configure(text=f"Acurácia: {acc*100:.2f}%")
            time.sleep(1)

    def update_hw_stats(self):
        load = self.resource_manager.get_system_load()
        self.cpu_label.configure(text=f"CPU: {load['cpu']:.1f}%")
        self.mem_label.configure(text=f"Memória: {load['mem']:.1f}%")
        self.temp_label.configure(text=f"Temperatura: {load['temp']:.1f}°C")
        self.after(2000, self.update_hw_stats)
