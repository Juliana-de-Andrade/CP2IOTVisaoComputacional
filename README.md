# Sistema de Segurança Infantil - Detecção de Crianças em Áreas de Risco

## Sobre o Projeto
Sistema de visão computacional para detecção e monitoramento de crianças em ambientes domésticos, com geração de alertas em tempo real quando crianças são detectadas em áreas potencialmente perigosas.

## Ferramentas Utilizadas

1. ROBOFLOW
- Função: Treinamento de modelo customizado para classificação criança/adulto
- Dataset personalizado com bounding boxes
- Augmentation de dados
- Exportação para formato YOLOv8

2. HUGGING FACE
- Função: Modelos State-of-the-Art para comparação
- Modelos modernos de detecção de objetos
- Arquiteturas transformer-based
- Comparação de performance

## Dataset
- Fonte: Kids and Adults Detection - Kaggle
- Total: 300+ imagens anotadas
- Classes: child, adult
- Split: 70% treino, 20% validação, 10% teste

## Sistema de Cores
- VERDE: Criança
- AZUL: Adulto  
- VERDE ESCURO (Borda): Detecção Roboflow
- AZUL ESCURO (Borda): Detecção Hugging Face
- VERMELHO: Alerta (criança em zona de risco)

## Configurações
ZONAS_DE_RISCO:
- Cozinha: [700, 500, 950, 650]
- Escada: [50, 350, 300, 650]
- Janela: [750, 50, 950, 200]

TREINAMENTO YOLOv8:
- epochs: 50
- batch: 8
- imgsz: 640
- patience: 10

## Resultados Comparativos
ROBOFLOW:
- Precisão Criança: 94%
- Precisão Adulto: 96%
- Vantagem: Alta customização

HUGGING FACE:
- Precisão Criança: 91% 
- Precisão Adulto: 93%
- Vantagem: Modelos modernos

## Como Executar
pip install numpy==1.24.3 opencv-python ultralytics roboflow

python sistema_seguranca_final.py

Controles:
- Q: Sair do sistema
- R: Reset da demonstração

## Demonstração
O sistema mostra:
- Crianças (verde) se movendo para zonas de risco
- Adultos (azul) circulando normalmente
- Alertas vermelhos quando crianças entram em áreas perigosas
- Comparação lado a lado: Roboflow vs Hugging Face

## Como Executar
Pré-requisitos
pip install opencv-python numpy ultralytics roboflow

Execução
python sistema_seguranca_final.py

## Link do Vídeo com Demonstração:
https://drive.google.com/drive/folders/1ajD_dWVe2zxkATMMsFfToXGkrUYl4kfz?usp=sharing

## Link do Dataset no Kaggle:
https://www.kaggle.com/datasets/kaushigihanml/kids-and-adults-detection?resource=download

## Equipe:
Juliana de Andrade Sousa RM: 558834
Victor Hugo Carvalho Pereira RM: 558550
