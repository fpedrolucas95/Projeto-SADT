from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
import os
from sistema.modulo_leitor_arquivo_PDF.leitor_pdf import analisar_pdf

app = Flask(__name__)
socketio = SocketIO(app)

# Configurações
temp_folder = "./temp/"
os.makedirs(temp_folder, exist_ok=True)

@app.route('/')
def carregar_arquivo():
   return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def carregar_arquivos():
   if request.method == 'POST':
      pdf_files = request.files.getlist("pdf")
      total_guias = 0
      todas_guias = []

      for pdf in pdf_files:
         nome_arquivo_pdf = secure_filename(pdf.filename)
         pdf.save(os.path.join(temp_folder, nome_arquivo_pdf))
         
         # Análise do PDF
         def emit_progress(percentage):
             socketio.emit('progress', {'percentage': percentage})

         guias_sadt_pages = analisar_pdf(os.path.join(temp_folder, nome_arquivo_pdf), emit_progress)
         todas_guias.append(guias_sadt_pages)
         total_guias += len(guias_sadt_pages)

      # Mensagem com as páginas identificadas
      if total_guias > 0:
         if len(pdf_files) > 1:
            mensagem = "Encontrei {} guias nos arquivos selecionados.".format(total_guias)
         else:
            mensagem = "Encontrei {} guias no arquivo selecionado.".format(total_guias)
      else:
         if len(pdf_files) > 1:
            mensagem = "Não foram encontradas guias nos arquivos selecionados."
         else:
            mensagem = "Não foram encontradas guias no arquivo selecionado."

      return render_template('upload.html', message=mensagem, guias=todas_guias)

@socketio.on('connect')
def handle_connect():
    print('Conectado')

@socketio.on('disconnect')
def handle_disconnect():
    print('Desconectado')

# A indicação do ChatGPT não funcionou, e o Github Actions ficou apenas no Run por horas. Talvez não funcione no actions devido a necessidade de processamento. Voltando ao código original:
if __name__ == '__main__': 
   socketio.run(app, debug=True)
