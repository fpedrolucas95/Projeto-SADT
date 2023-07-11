<h1>Projeto de Análise de Documentos PDF</h1>
<p align="left">
    <a href="https://www.python.org" target="_blank"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="python"/></a>
    <a href="https://flask.palletsprojects.com/" target="_blank"> <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="flask"/></a>
    <a href="https://pytorch.org/" target="_blank"> <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="pytorch"/></a>
    <a href="https://getbootstrap.com/" target="_blank"> <img src="https://img.shields.io/badge/Bootstrap-000000?style=for-the-badge&logo=Bootstrap&logoColor=white" alt="Bootstrap"/></a>
</p>

<p>Esse projeto permite a análise de documentos PDF buscando por guias SADT, utilizando um modelo de rede neural.</p>

<h2>Funcionalidades</h2>
<h3>Upload de Documentos PDF</h3>
<p><b>Interface de usuário para upload de documentos PDF:</b> A aplicação fornece uma interface de usuário onde os usuários podem selecionar vários arquivos PDF para upload. Uma vez que os arquivos são selecionados, eles são salvos temporariamente em uma pasta especificada.</p>
<h3>Análise de Documentos PDF</h3>
<p><b>Análise de documentos PDF para identificação de guias SADT utilizando um modelo de rede neural:</b> Cada arquivo PDF carregado é então analisado página por página. As páginas são convertidas em imagens, que são então alimentadas em um modelo de rede neural ResNet50 treinado para identificar guias SADT. Cada página identificada como uma guia SADT é registrada. O número total de guias SADT encontradas em todos os arquivos é então calculado.</p>
<h3>Feedback em Tempo Real</h3>
<p><b>Progresso da análise em tempo real utilizando Socket.IO:</b> À medida que cada arquivo PDF é analisado, o progresso é emitido para a interface do usuário através de Socket.IO. Isso permite que os usuários vejam o progresso da análise em tempo real na forma de uma barra de progresso.</p>

<h2>Próximos Passos</h2>
<p>As futuras melhorias deste projeto incluem a inspeção visual de cada guia SADT para identificação de inconformidades utilizando inteligência artificial, a extração de dados dos campos de cada guia SADT reconhecida, a comparação dos dados extraídos com um XML correspondente.</p>

<h2>Tecnologias Utilizadas</h2>
<p>Este projeto utiliza Python como a linguagem de programação principal. Flask é usado para fornecer a interface de usuário e gerenciar o upload de arquivos. PyTorch é usado para o modelo de aprendizado de máquina, que é um ResNet50 que foi treinado para identificar guias SADT em imagens de páginas de PDF. O projeto também usa o Flask-SocketIO para fornecer feedback em tempo real na interface do usuário sobre o progresso da análise dos documentos PDF.</p>

<h2>Funcionalidades</h2>
<ul>
    <li>[x] Interface de usuário para upload de documentos PDF.</li>
    <li>[x] Análise de documentos PDF para identificação de guias SADT utilizando um modelo de rede neural.</li>
    <li>[x] Progresso da análise em tempo real utilizando Socket.IO.</li>
    <li>[ ] Inspeção visual de cada guia SADT para identificação de inconformidades e identificação dos campos com dados, também utilizando inteligência artificial.</li>
    <li>[ ] Extração de dados dos campos de cada guia SADT reconhecida utilizando a biblioteca PyTesseract.</li>
    <li>[ ] Comparação dos dados extraídos com um XML correspondente.</li>
    <li>[ ] Empacotamento da aplicação como um Docker para ser executada no Google Cloud ou na Azure (ambas tem ferramentas de processamento de imagem e de reconhecimento de caracteres incríveis).</li>
</ul>

<h2>Como Executar</h2>
<p>Para rodar esse projeto em sua máquina local, siga os passos abaixo:</p>
Primeiro, clone o repositório para o seu ambiente local usando o comando Git. Se você não tiver o Git instalado, pode simplesmente baixar o código como um arquivo zip e extrair.

```
git clone https://github.com/fpedrolucas95/Projeto-SADT/
```

Entre no diretório do projeto:
```
cd Projeto-SADT
```
Agora, é preciso instalar as dependências necessárias para executar o projeto. Elas estão listadas no arquivo requirements.txt. Vamos usar o pip, um gerenciador de pacotes Python, para fazer isso. Se você não tiver o Python instalado, terá que instalá-lo primeiro.
```
pip install -r requirements.txt
```
Depois de instalar as dependências, você pode iniciar o servidor Flask. Isso pode ser feito executando o arquivo app.py.
```
python app.py
```
Uma vez que o servidor esteja funcionando, você poderá acessar a aplicação em seu navegador web pelo endereço http://localhost:5000 ou http://127.0.0.1:5000 a menos que especificado de outra forma na saída do comando acima.
<p>Lembre-se de que você precisa ter o Python instalado em sua máquina, além do pip (gerenciador de pacotes Python), e um terminal para digitar os comandos.</p>


<h2>📄 Licença</h2>
<p>Este projeto está sob a licença GNU General Public License v3.0. Qualquer pessoa é bem-vinda para contribuir com correções de erros ou novas funcionalidades. Se você deseja contribuir, basta criar um pull request com suas alterações.</p>

<h2>Desenvolvedor</h2>

<p>Nome: Pedro Lucas França</p>
<p>Email: fpedrolucas95@gmail.com</p>
<a href="https://www.francadev.com.br" target=_blank>Visite meu site</a>
