from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
import os
from sistema.modulo_leitor_arquivo_PDF.leitor_pdf import analisar_pdf

app = Flask(__name__)
socketio = SocketIO(app)

# Configurações
temp_folder = "/tmp/"
os.makedirs(temp_folder, exist_ok=True)

@app.route('/')
def carregar_arquivo():
   return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def carregar_arquivos():
   if request.method == 'POST':
      pdf_files = request.files.getlist("pdf")
      total_guias = 0

      for pdf in pdf_files:
         nome_arquivo_pdf = secure_filename(pdf.filename)
         pdf.save(os.path.join(temp_folder, nome_arquivo_pdf))
         
         # Análise do PDF
         def emit_progress(percentage):
             socketio.emit('progress', {'percentage': percentage})

         guias_sadt_pages = analisar_pdf(os.path.join(temp_folder, nome_arquivo_pdf), emit_progress)
         total_guias += len(guias_sadt_pages)

      # Mensagem com as páginas identificadas
      if len(pdf_files) > 1:
         mensagem = "Encontrei {} guias nos arquivos selecionados.".format(total_guias)
      else:
         mensagem = "Encontrei {} guias no arquivo selecionado.".format(total_guias)

      return render_template('upload.html', message=mensagem)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
   socketio.run(app, debug=True)