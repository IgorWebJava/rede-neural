import numpy as np
import multiprocessing as mp
import time
from numba import jit

# ----------------------------------------------------------------------
# 1. DataWorker (Processo Produtor)
# ----------------------------------------------------------------------

@jit(nopython=True, cache=True)
def _process_data_kernel(data_chunk):
    """
    Kernel de pré-processamento otimizado com Numba.
    Simula uma operação complexa de pré-processamento (ex: normalização, aumento).
    """
    # Exemplo: Normalização simples e aplicação de uma função não-linear
    data_chunk = data_chunk / 255.0
    data_chunk = np.maximum(0.0, data_chunk) # Simula ReLU para introduzir não-linearidade
    return data_chunk

def data_worker_process(data_queue, stop_event, config, data_source):
    """
    Processo worker que carrega, pré-processa e coloca batches na fila.
    """
    # RULE 02: Performance Não-Bloqueante
    # RULE 08: Tratamento Explícito de Erros
    
    while not stop_event.is_set():
        try:
            # 1. Carregamento de Dados (Simulação de I/O)
            # Em um projeto real, aqui ocorreria o carregamento de arquivos (opencv, soundfile, etc.)
            batch_size = config['training']['batch_size']
            raw_batch = np.random.randint(0, 256, size=(batch_size, 224, 224, 3), dtype=np.uint8)
            
            # 2. Pré-processamento Otimizado
            processed_batch = _process_data_kernel(raw_batch.astype(np.float32))
            
            # 3. Colocar na Fila (Prefetching)
            # block=True com timeout para evitar deadlock e respeitar RULE 02
            data_queue.put(processed_batch, block=True, timeout=1.0)
            
        except Exception as e:
            # RULE 08: Mensagens claras e contexto do erro
            print(f"[ERROR] DataWorker Failure: {str(e)}")
            stop_event.set()
            break

# ----------------------------------------------------------------------
# 2. SovereignDataLoader (Gerenciador de Pipeline)
# ----------------------------------------------------------------------

class SovereignDataLoader:
    """
    Gerenciador do pipeline de dados Multi-Worker conforme RULE 02.
    """
    def __init__(self, config, data_source):
        self.config = config
        self.data_source = data_source
        self.num_workers = config['runtime'].get('num_workers', 1)
        self.prefetch_factor = config['runtime'].get('prefetch_factor', 1)
        
        # A fila deve ter um tamanho máximo para evitar estouro de memória
        max_queue_size = self.num_workers * self.prefetch_factor
        self.data_queue = mp.Queue(maxsize=max_queue_size)
        self.stop_event = mp.Event()
        self.workers = []

    def start_workers(self):
        """Inicia os processos workers."""
        for i in range(self.num_workers):
            worker = mp.Process(
                target=data_worker_process,
                args=(self.data_queue, self.stop_event, self.config, self.data_source),
                name=f"DataWorker-{i}"
            )
            self.workers.append(worker)
            worker.start()

    def get_batch(self):
        """Retorna um batch pré-processado da fila (RULE 02)."""
        try:
            return self.data_queue.get(block=True, timeout=5.0)
        except Exception:
            raise RuntimeError("Data pipeline timeout: Fila de dados vazia por mais de 5s.")

    def stop_workers(self):
        """Sinaliza para os workers pararem e espera por eles."""
        self.stop_event.set()
        for worker in self.workers:
            worker.join(timeout=2)
            if worker.is_alive():
                worker.terminate()
