import os
import time
import numpy as np

class SovereignDashboard:
    """
    Dashboard de Auditoria Neural via Terminal (RULE 14).
    Visualização em tempo real da saúde e performance do sistema.
    """
    def __init__(self):
        self.start_time = time.time()
        self.history = {"loss": [], "grad_norm": [], "lr": []}

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_bar(self, value, max_val=1.0, width=20):
        percent = min(value / max_val, 1.0)
        filled = int(width * percent)
        return "[" + "=" * filled + " " * (width - filled) + "]"

    def update(self, step, loss, grad_norm, lr, status="HEALTHY"):
        self.history["loss"].append(loss)
        self.history["grad_norm"].append(grad_norm)
        self.history["lr"].append(lr)
        
        self.clear()
        elapsed = time.time() - self.start_time
        
        print("=" * 50)
        print(f" 🧠 SOVEREIGN NEURAL DASHBOARD V4 - Step {step}")
        print(f" Status: {status} | Uptime: {elapsed:.2f}s")
        print("=" * 50)
        
        # Loss Visualization
        avg_loss = np.mean(self.history["loss"][-10:]) if self.history["loss"] else 0
        print(f" Loss:      {loss:.6f} (Avg: {avg_loss:.6f})")
        print(f" Progress:  {self.draw_bar(1.0/max(1, loss), 2.0)}")
        
        # Gradient Health
        print(f" Grad Norm: {grad_norm:.6f}")
        grad_status = "OK" if grad_norm < 10.0 else "⚠️ HIGH"
        print(f" Stability: {self.draw_bar(grad_norm, 20.0)} {grad_status}")
        
        # Learning Rate
        print(f" Learn Rate: {lr:.6f}")
        
        print("-" * 50)
        print(" [S]ave Weights | [Q]uit | [A]udit System")
        print("=" * 50)

if __name__ == "__main__":
    # Teste do Dashboard
    db = SovereignDashboard()
    for i in range(10):
        db.update(i, 0.5 - i*0.04, 2.5 + i*0.5, 0.01)
        time.sleep(0.5)
