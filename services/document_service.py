from typing import Optional
import os

import PyPDF2  # Para PDFs

from docx import Document  # Para DOCX

from ebooklib import epub  # Para EPUB

from reportlab.lib.pagesizes import letter  # Para exportar PDFs
from reportlab.pdfgen import canvas


class DocumentService:
    def import_document(self, file_path: str) -> Optional[str]:
        """Importa texto de um arquivo de documento."""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext == '.pdf':
            return self._import_pdf(file_path)
        elif ext == '.docx':
            return self._import_docx(file_path)
        elif ext == '.epub':
            return self._import_epub(file_path)
        elif ext == '.txt':
            return self._import_txt(file_path)
        else:
            raise ValueError(f"Formato de arquivo não suportado: {ext}")

    def export_document(self, text: str, file_path: str, format: str) -> None:
        """Exporta texto para um arquivo de documento."""
        format = format.lower()
        if format == 'pdf':
            self._export_pdf(text, file_path)
        elif format == 'docx':
            self._export_docx(text, file_path)
        elif format == 'txt':
            self._export_txt(text, file_path)
        else:
            raise ValueError(f"Formato de exportação não suportado: {format}")

    @staticmethod
    def _import_pdf(file_path: str) -> str:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text

    @staticmethod
    def _import_docx(file_path: str) -> str:
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text

    @staticmethod
    def _import_epub(file_path: str) -> str:
        book = epub.read_epub(file_path)
        text = ''
        for item in book.get_items():
            if item.get_type() == epub.ITEM_DOCUMENT:
                content = item.get_content()
                text += content.decode('utf-8')
        return text

    @staticmethod
    def _import_txt(file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def _export_pdf(text: str, file_path: str) -> None:
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        # Configurações do texto
        text_object = c.beginText(50, height - 50)
        text_object.setFont("Helvetica", 12)
        line_height = 14  # Espaço entre linhas

        # Tratando cada linha para evitar estouro de página
        for line in text.split('\n'):
            words = line.split(' ')
            line_buffer = ""

            for word in words:
                # Testa se a linha com a nova palavra excede a largura da página
                if c.stringWidth(line_buffer + word, "Helvetica", 12) < (width - 100):
                    line_buffer += word + " "
                else:
                    text_object.textLine(line_buffer.strip())
                    line_buffer = word + " "

                    # Verifica se a altura atual do texto está muito baixa
                    if text_object.getY() <= 50:
                        c.drawText(text_object)
                        c.showPage()
                        text_object = c.beginText(50, height - 50)
                        text_object.setFont("Helvetica", 12)

            # Adiciona a linha final ao objeto de texto
            if line_buffer:
                text_object.textLine(line_buffer.strip())

                # Verifica novamente se precisa mudar de página
                if text_object.getY() <= 50:
                    c.drawText(text_object)
                    c.showPage()
                    text_object = c.beginText(50, height - 50)
                    text_object.setFont("Helvetica", 12)

        # Desenha o texto restante e salva o PDF
        c.drawText(text_object)
        c.save()

    @staticmethod
    def _export_docx(text: str, file_path: str) -> None:
        doc = Document()
        doc.add_paragraph(text)
        doc.save(file_path)

    @staticmethod
    def _export_txt(text: str, file_path: str) -> None:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)