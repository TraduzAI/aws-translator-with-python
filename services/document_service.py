# services/document_service.py

import os
from typing import Optional

# Para PDFs
import PyPDF2

# Para DOCX
from docx import Document

# Para EPUB
from ebooklib import epub

# Para exportar PDFs
from reportlab.lib.pagesizes import letter
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

    def _import_pdf(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text

    def _import_docx(self, file_path: str) -> str:
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text

    def _import_epub(self, file_path: str) -> str:
        book = epub.read_epub(file_path)
        text = ''
        for item in book.get_items():
            if item.get_type() == epub.ITEM_DOCUMENT:
                content = item.get_content()
                text += content.decode('utf-8')
        return text

    def _import_txt(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _export_pdf(self, text: str, file_path: str) -> None:
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        text_object = c.beginText(50, height - 50)
        for line in text.split('\n'):
            text_object.textLine(line)
        c.drawText(text_object)
        c.save()

    def _export_docx(self, text: str, file_path: str) -> None:
        doc = Document()
        doc.add_paragraph(text)
        doc.save(file_path)

    def _export_txt(self, text: str, file_path: str) -> None:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
