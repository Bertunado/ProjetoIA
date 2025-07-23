Sistema de Previsão de Vida Útil de Peças

Este projeto tem como objetivo prever a vida útil de peças mecânicas, como parafusos, correias e ventosas, com base em dados de uso fornecidos pelos usuários. A aplicação utiliza técnicas de aprendizado de máquina para estimar quantos dias cada peça deve durar, considerando o tempo diário de uso e descanso. Os dados são armazenados em arquivos CSV e alimentam modelos preditivos treinados com algoritmos de regressão (Random Forest).
Funcionalidades
Registro de novas peças com informações sobre tempo de uso e descanso diário.


Cálculo automático da intensidade de uso (leve, moderado ou intenso).


Previsão da vida útil da peça (em dias), com base nos dados fornecidos.


Interface de chat que exibe:


Intensidade de uso


Status da peça


Data da troca


Vida útil restante estimada


Janela recomendada para substituição da peça


Registro de peças que apresentaram falha, com data da troca e data da quebra, permitindo aprimorar o modelo com dados reais.


Atualização automática dos arquivos CSV e reprocessamento dos modelos por meio da interface (em desenvolvimento).


Classificação da Intensidade de Uso
Leve: até 8 horas de uso por dia (vida útil estimada: aproximadamente 2 anos)


Moderado: de 8 a 15 horas por dia (vida útil estimada: aproximadamente 1 ano)


Intenso: mais de 15 horas por dia (vida útil estimada: aproximadamente 6 meses)


Tecnologias Utilizadas
Python


Pandas e Scikit-learn


HTML, CSS e JavaScript (frontend)


Machine Learning com RandomForestRegressor


Persistência de dados em arquivos CSV


Estrutura de Arquivos:

dados_parafuso.csv, dados_correia.csv, dados_ventosa.csv: Arquivos que armazenam os dados de uso registrados para cada tipo de peça.


train_all.py: Script responsável por treinar os modelos com base nos dados disponíveis.


model_parafuso.pkl, model_correia.pkl, model_ventosa.pkl: Modelos treinados, salvos em disco para reutilização.


interface.html: Interface principal para entrada de dados e visualização das previsões.


script.js: Responsável pela lógica de envio de dados ao backend e exibição dos resultados no frontend.
