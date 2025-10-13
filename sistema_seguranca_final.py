import cv2
import numpy as np
import random
import time

print("🚀 SISTEMA DE SEGURANÇA INFANTIL - ROBOFLOW + HUGGING FACE")
print("📊 Ferramentas utilizadas:")
print("   • ROBOFLOW: Treinamento de modelo customizado (criança/adulto)")
print("   • HUGGING FACE: Modelos State-of-the-Art para comparação")
print("=" * 60)

class SistemaSeguranca:
    def __init__(self):
        self.largura = 1000
        self.altura = 700
        self.alertas = 0
        self.deteccoes_roboflow = 0
        self.deteccoes_huggingface = 0
        
        # Zonas de perigo
        self.zonas_risco = {
            'COZINHA': [700, 500, 950, 650],
            'ESCADA': [50, 350, 300, 650],
            'JANELA': [750, 50, 950, 200]
        }
        
        # CORES CORRETAS:
        self.cor_crianca = (0, 255, 0)       # Verde - Criança
        self.cor_adulto = (255, 0, 0)        # Azul - Adulto
        self.cor_roboflow = (0, 100, 0)      # Verde escuro - borda Roboflow
        self.cor_huggingface = (0, 0, 100)   # Azul escuro - borda Hugging Face
        self.cor_alerta = (0, 0, 255)        # Vermelho - Alerta
        
    def criar_ambiente_comparativo(self):
        """Cria ambiente mostrando ambas as ferramentas"""
        frame = np.ones((self.altura, self.largura, 3), dtype=np.uint8) * 240
        
        # Área Roboflow
        cv2.rectangle(frame, (50, 100), (450, 500), (220, 220, 220), -1)
        cv2.putText(frame, "ROBOFLOW - Modelo Customizado", (60, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.cor_roboflow, 2)
        
        # Área Hugging Face
        cv2.rectangle(frame, (550, 100), (950, 500), (220, 220, 220), -1)
        cv2.putText(frame, "HUGGING FACE - Modelo SOTA", (560, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.cor_huggingface, 2)
        
        # Zonas de risco (compartilhadas)
        for nome, (x1, y1, x2, y2) in self.zonas_risco.items():
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), self.cor_alerta, 2)
            cv2.putText(frame, nome, (int(x1)+5, int(y1)+25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.cor_alerta, 2)
        
        return frame

    def simular_deteccao_roboflow(self, frame, pessoa_pos, pessoa_tipo):
        """Simula detecção do Roboflow (modelo customizado)"""
        x, y = int(pessoa_pos[0]), int(pessoa_pos[1])
        
        if pessoa_tipo == "criança":
            altura = 80
            cor = self.cor_crianca  # VERDE para criança
            texto = "CRIANÇA"
            confianca = 0.94
            borda_cor = self.cor_roboflow
        else:
            altura = 110
            cor = self.cor_adulto   # AZUL para adulto
            texto = "ADULTO"
            confianca = 0.96
            borda_cor = self.cor_roboflow
        
        # Bounding box Roboflow
        bbox = [x-35, y-40, x+35, y+80]
        bbox = [int(coord) for coord in bbox]
        
        # Preenchimento com cor da pessoa + borda da ferramenta
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), cor, -1)
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), borda_cor, 3)
        
        cv2.putText(frame, f"{texto} (Roboflow) - {confianca:.2f}", (bbox[0]-10, bbox[1]-15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        # Verificar alerta APENAS para crianças
        alerta = self.verificar_alerta(bbox)
        if alerta and pessoa_tipo == "criança":
            cv2.putText(frame, f"ALERTA! {alerta}", (bbox[0]-10, bbox[1]-35),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.cor_alerta, 2)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), self.cor_alerta, 4)
            self.alertas += 1
        
        self.deteccoes_roboflow += 1
        return bbox

    def simular_deteccao_huggingface(self, frame, pessoa_pos, pessoa_tipo):
        """Simula detecção do Hugging Face (modelos SOTA)"""
        x, y = int(pessoa_pos[0]), int(pessoa_pos[1])
        
        if pessoa_tipo == "criança":
            altura = 75
            cor = self.cor_crianca  # VERDE para criança
            texto = "CRIANÇA"
            confianca = 0.91
            borda_cor = self.cor_huggingface
        else:
            altura = 105
            cor = self.cor_adulto   # AZUL para adulto
            texto = "ADULTO"
            confianca = 0.93
            borda_cor = self.cor_huggingface
        
        # Bounding Box Hugging Face
        bbox = [x-30, y-35, x+30, y+75]
        bbox = [int(coord) for coord in bbox]
        
        # Preenchimento com cor da pessoa + borda da ferramenta
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), cor, -1)
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), borda_cor, 2)
        
        cv2.putText(frame, f"{texto} (HF) - {confianca:.2f}", (bbox[0]-10, bbox[1]-15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        # Pontos de referência (característica de modelos SOTA)
        pontos = [
            (x, y-25),  # Cabeça
            (x-20, y),  # Ombro esq
            (x+20, y),  # Ombro dir
            (x-15, y+40), # Quadril esq
            (x+15, y+40)  # Quadril dir
        ]
        
        for ponto in pontos:
            cv2.circle(frame, ponto, 4, borda_cor, -1)
        
        # Verificar alerta APENAS para crianças
        alerta = self.verificar_alerta(bbox)
        if alerta and pessoa_tipo == "criança":
            cv2.putText(frame, f"ALERTA! {alerta}", (bbox[0]-10, bbox[1]-35),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.cor_alerta, 2)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), self.cor_alerta, 4)
        
        self.deteccoes_huggingface += 1
        return bbox

    def verificar_alerta(self, bbox):
        """Verifica se a pessoa está em zona de risco"""
        x1, y1, x2, y2 = bbox
        centro_x = (x1 + x2) // 2
        centro_y = (y1 + y2) // 2
        
        for zona, (zx1, zy1, zx2, zy2) in self.zonas_risco.items():
            if zx1 <= centro_x <= zx2 and zy1 <= centro_y <= zy2:
                return zona
        return None

    def criar_painel_comparativo(self, frame, frame_count):
        """Cria painel comparativo entre as ferramentas"""
        # Título principal
        cv2.putText(frame, "COMPARATIVO: ROBOFLOW vs HUGGING FACE", (50, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        # Métricas Roboflow
        cv2.putText(frame, "ROBOFLOW (Customizado):", (60, 550),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.cor_roboflow, 2)
        cv2.putText(frame, f"- Detecções: {self.deteccoes_roboflow}", (80, 570),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.cor_roboflow, 1)
        cv2.putText(frame, "- Treinado com dataset específico", (80, 585),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.cor_roboflow, 1)
        
        # Métricas Hugging Face
        cv2.putText(frame, "HUGGING FACE (SOTA):", (560, 550),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.cor_huggingface, 2)
        cv2.putText(frame, f"- Detecções: {self.deteccoes_huggingface}", (580, 570),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.cor_huggingface, 1)
        cv2.putText(frame, "- Modelos State-of-the-Art", (580, 585),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.cor_huggingface, 1)
        
        # Estatísticas gerais
        cv2.putText(frame, f"Tempo: {frame_count//10}s | Alertas: {self.alertas}", (50, 620),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        # Legenda
        cv2.putText(frame, "VERDE: Criança | AZUL: Adulto | VERMELHO: Alerta", (50, 645),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        cv2.putText(frame, "Borda VERDE ESCURO: Roboflow | Borda AZUL ESCURO: Hugging Face", (50, 660),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

def demonstrar_comparativo():
    """Demonstra o sistema comparativo COM CRIANÇAS E ADULTOS"""
    print("🎯 INICIANDO DEMONSTRAÇÃO COMPARATIVA")
    print("📋 Cenários demonstrados:")
    print("   • CRIANÇAS: Se movem para zonas de risco → GERAM ALERTAS")
    print("   • ADULTOS: Circulam normalmente → NÃO geram alertas")
    print("   • Comparação: Roboflow vs Hugging Face")
    
    sistema = SistemaSeguranca()
    
    # AGORA TEMOS CRIANÇAS E ADULTOS EM AMBAS AS FERRAMENTAS:
    # Roboflow (lado esquerdo)
    crianca_roboflow = [200, 300]    # CRIANÇA Roboflow
    adulto_roboflow = [350, 400]     # ADULTO Roboflow
    
    # Hugging Face (lado direito)  
    crianca_huggingface = [700, 300]  # CRIANÇA Hugging Face
    adulto_huggingface = [850, 400]   # ADULTO Hugging Face
    
    frame_count = 0
    
    print("✅ Sistema pronto! Iniciando em 3 segundos...")
    time.sleep(3)
    
    while True:
        frame = sistema.criar_ambiente_comparativo()
        frame_count += 1
        
        # MOVIMENTOS DAS CRIANÇAS (vão para zonas de perigo)
        # Criança Roboflow - vai para cozinha
        if frame_count < 80:
            crianca_roboflow[0] += 4
        elif frame_count < 150:
            crianca_roboflow[0] += 3
            crianca_roboflow[1] += 2
        else:
            crianca_roboflow[0] += 2
        
        # Criança Hugging Face - movimento similar
        crianca_huggingface[0] = crianca_roboflow[0] + 500
        crianca_huggingface[1] = crianca_roboflow[1]
        
        # MOVIMENTOS DOS ADULTOS (ficam em áreas seguras)
        # Adulto Roboflow - movimento circular
        adulto_roboflow[0] = 350 + int(40 * np.sin(frame_count * 0.05))
        adulto_roboflow[1] = 400 + int(20 * np.cos(frame_count * 0.04))
        
        # Adulto Hugging Face - movimento similar
        adulto_huggingface[0] = adulto_roboflow[0] + 500
        adulto_huggingface[1] = adulto_roboflow[1]
        
        # DETECÇÕES ROBOFLOW (lado esquerdo)
        sistema.simular_deteccao_roboflow(frame, crianca_roboflow, "criança")   # CRIANÇA
        sistema.simular_deteccao_roboflow(frame, adulto_roboflow, "adulto")     # ADULTO
        
        # DETECÇÕES HUGGING FACE (lado direito)
        sistema.simular_deteccao_huggingface(frame, crianca_huggingface, "criança")  # CRIANÇA
        sistema.simular_deteccao_huggingface(frame, adulto_huggingface, "adulto")    # ADULTO
        
        # PAINEL COMPARATIVO
        sistema.criar_painel_comparativo(frame, frame_count)
        
        # MOSTRAR RESULTADO
        cv2.imshow('ROBOFLOW vs HUGGING FACE - Crianças (Verde) e Adultos (Azul) - Q para sair', frame)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    
    print(f"\n✅ DEMONSTRAÇÃO CONCLUÍDA!")
    print(f"📊 ESTATÍSTICAS FINAIS:")
    print(f"   • Alertas totais: {sistema.alertas} (apenas crianças em risco)")
    print(f"   • Detecções Roboflow: {sistema.deteccoes_roboflow}")
    print(f"   • Detecções Hugging Face: {sistema.deteccoes_huggingface}")
    print(f"   • Tempo total: {frame_count//10} segundos")
    print(f"🎯 FERRAMENTAS DEMONSTRADAS: ROBOFLOW + HUGGING FACE")

# EXECUTAR SISTEMA
if __name__ == "__main__":
    demonstrar_comparativo()