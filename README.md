**Sistema de Previsão de Vida Útil de Peças**

Este projeto tem como objetivo prever a vida útil de peças mecânicas, como parafusos, correias e ventosas, com base em dados de uso fornecidos pelos usuários. A aplicação utiliza técnicas de aprendizado de máquina para estimar quantos dias cada peça deve durar, considerando o tempo diário de uso e descanso. Os dados são armazenados em arquivos CSV e alimentam modelos preditivos treinados com algoritmos de regressão (Random Forest).


*  **Funcionalidades**

   * Registro de novas peças com informações sobre tempo de uso e descanso diário.

   * Cálculo automático da intensidade de uso (leve, moderado ou intenso).

   * Previsão da vida útil da peça (em dias), com base nos dados fornecidos.


*  **Interface de chat que exibe:**

   * Intensidade de uso

   * Status da peça

   * Data da troca

   * Vida útil restante estimada

   * Janela recomendada para substituição da peça

   * Registro de peças que apresentaram falha, com data da troca e data da quebra, permitindo aprimorar o modelo com dados reais.

   * Atualização automática dos arquivos CSV e reprocessamento dos modelos por meio da interface (em desenvolvimento).


*  **Tecnologias Utilizadas**
  
   * Python

   * Pandas e Scikit-learn

   * HTML, CSS e JavaScript (frontend)

   * Machine Learning com RandomForestRegressor

   * Persistência de dados em arquivos CSV
