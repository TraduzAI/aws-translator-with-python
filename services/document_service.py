# services/document_service.py

"""
Document Service Module
=======================

Este módulo fornece serviços para importar e exportar textos a partir e para
diferentes formatos de documentos. Suporta os seguintes formatos:

- **Importação**:
    - PDF (`.pdf`)
    - DOCX (`.docx`)
    - EPUB (`.epub`)
    - TXT (`.txt`)
- **Exportação**:
    - PDF (`.pdf`)
    - DOCX (`.docx`)
    - TXT (`.txt`)

Classes:
    DocumentService: Classe responsável pela importação e exportação de documentos.

Dependências:
    - PyPDF2: Biblioteca para manipulação de arquivos PDF.
    - python-docx: Biblioteca para manipulação de arquivos DOCX.
    - EbookLib: Biblioteca para manipulação de arquivos EPUB.
    - reportlab: Biblioteca para geração de PDFs.
    - typing: Biblioteca padrão para anotações de tipos.

Exemplo de Uso:
    >>> from services.document_service import DocumentService
    >>> doc_service = DocumentService()

    # Importar um documento
    >>> texto = doc_service.import_document('exemplo.pdf')

    # Exportar um documento
    >>> doc_service.export_document(texto, 'saida.docx', 'docx')
"""

from typing import Optional
import os

import PyPDF2  # Para PDFs
from docx import Document  # Para DOCX
from ebooklib import epub  # Para EPUB

from reportlab.lib.pagesizes import letter  # Para exportar PDFs
from reportlab.pdfgen import canvas


class DocumentService:
    """
    Serviço para importar e exportar textos a partir e para diferentes formatos de documentos.

    Esta classe fornece métodos para importar textos de arquivos PDF, DOCX, EPUB e TXT, bem
    como exportar textos para arquivos PDF, DOCX e TXT. Utiliza diversas bibliotecas para
    manipulação de diferentes formatos de arquivos.

    Métodos:
        import_document(file_path: str) ⇾ Optional[str]:
            Importa texto de um arquivo de documento.

        export_document(text: str, file_path: str, format: str) ⇾ None:
            Exporta texto para um arquivo de documento.
    """

    def import_document(self, file_path: str) -> Optional[str]:
        """
        Importa texto de um arquivo de documento.

        Este metodo determina o tipo de arquivo com base na extensão e utiliza o metodo
        apropriado para extrair o texto.

        Parâmetros:
            file_path (str): Caminho para o arquivo de documento a ser importado.

        Retorna:
            Optional[str]: O texto extraído do documento ou `None` se não for possível extrair.

        Exceções:
            - ValueError: Se o formato do arquivo não for suportado.
            - Exception: Se ocorrer um erro durante a importação do documento.

        Exemplos de Uso:
            >>> doc_service = DocumentService()
            >>> texto = doc_service.import_document('documento.pdf')
            >>> print(texto)
            "Este é o conteúdo extraído do PDF."
        """
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
        """
        Exporta texto para um arquivo de documento.

        Este metodo determina o formato de exportação com base no parâmetro `format`
        e utiliza o metodo apropriado para salvar o texto no formato desejado.

        Parâmetros:
            text (str): O texto a ser exportado.
            file_path (str): Caminho onde o arquivo exportado será salvo.
            format (str): Formato de exportação desejado (`'pdf'`, `'docx'`, `'txt'`).

        Retorna:
            None

        Exceções:
            - ValueError: Se o formato de exportação não for suportado.
            - Exception: Se ocorrer um erro durante a exportação do documento.

        Exemplos de Uso:
            >>> doc_service = DocumentService()
            >>> texto = "Este é o texto que será exportado."
            >>> doc_service.export_document(texto, 'saida.docx', 'docx')
        """
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
        """
        Importa texto de um arquivo PDF.

        Utiliza a biblioteca PyPDF2 para extrair o texto de cada página do PDF.

        Parâmetros:
            file_path (str): Caminho para o arquivo PDF a ser importado.

        Retorna:
            str: O texto extraído do PDF.

        Exceções:
            - FileNotFoundError: Se o arquivo PDF não for encontrado.
            - Exception: Se ocorrer um erro durante a leitura do PDF.
        """
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ''
                for page in reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text + '\n'
                return text.strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {file_path}")
        except Exception as e:
            raise Exception(f"Erro ao importar PDF: {str(e)}")

    @staticmethod
    def _import_docx(file_path: str) -> str:
        """
        Importa texto de um arquivo DOCX.

        Utiliza a biblioteca python-docx para extrair o texto de cada parágrafo do DOCX.

        Parâmetros:
            file_path (str): Caminho para o arquivo DOCX a ser importado.

        Retorna:
            str: O texto extraído do DOCX.

        Exceções:
            - FileNotFoundError: Se o arquivo DOCX não for encontrado.
            - Exception: Se ocorrer um erro durante a leitura do DOCX.
        """
        try:
            doc = Document(file_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
            return text.strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo DOCX não encontrado: {file_path}")
        except Exception as e:
            raise Exception(f"Erro ao importar DOCX: {str(e)}")

    @staticmethod
    def _import_epub(file_path: str) -> str:
        """
        Importa texto de um arquivo EPUB.

        Utiliza a biblioteca EbookLib para extrair o conteúdo textual dos documentos do EPUB.

        Parâmetros:
            file_path (str): Caminho para o arquivo EPUB a ser importado.

        Retorna:
            str: O texto extraído do EPUB.

        Exceções:
            - FileNotFoundError: Se o arquivo EPUB não for encontrado.
            - Exception: Se ocorrer um erro durante a leitura do EPUB.
        """
        try:
            book = epub.read_epub(file_path)
            text = ''
            for item in book.get_items():
                if item.get_type() == epub.ITEM_DOCUMENT:
                    content = item.get_content()
                    text += content.decode('utf-8') + '\n'
            return text.strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo EPUB não encontrado: {file_path}")
        except Exception as e:
            raise Exception(f"Erro ao importar EPUB: {str(e)}")

    @staticmethod
    def _import_txt(file_path: str) -> str:
        """
        Importa texto de um arquivo TXT.

        Abre o arquivo de texto e lê todos o seu conteúdo.

        Parâmetros:
            file_path (str): Caminho para o arquivo TXT a ser importado.

        Retorna:
            str: O texto extraído do TXT.

        Exceções:
            - FileNotFoundError: Se o arquivo TXT não for encontrado.
            - Exception: Se ocorrer um erro durante a leitura do TXT.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo TXT não encontrado: {file_path}")
        except Exception as e:
            raise Exception(f"Erro ao importar TXT: {str(e)}")

    @staticmethod
    def _export_pdf(text: str, file_path: str) -> None:
        """
        Exporta texto para um arquivo PDF.

        Utiliza a biblioteca ReportLab para gerar um PDF a partir do texto fornecido,
        cuidando da formatação e quebra de linhas conforme necessário.

        Parâmetros:
            text (str): O texto a ser exportado para o PDF.
            file_path (str): Caminho onde o arquivo PDF será salvo.

        Retorna:
            None

        Exceções:
            - Exception: Se ocorrer um erro durante a criação do PDF.
        """
        try:
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
        except Exception as e:
            raise Exception(f"Erro ao exportar PDF: {str(e)}")

    @staticmethod
    def _export_docx(text: str, file_path: str) -> None:
        """
        Exporta texto para um arquivo DOCX.

        Utiliza a biblioteca python-docx para criar um documento DOCX com o texto fornecido.

        Parâmetros:
            text (str): O texto a ser exportado para o DOCX.
            file_path (str): Caminho onde o arquivo DOCX será salvo.

        Retorna:
            None

        Exceções:
            - Exception: Se ocorrer um erro durante a criação do DOCX.
        """
        try:
            doc = Document()
            doc.add_paragraph(text)
            doc.save(file_path)
        except Exception as e:
            raise Exception(f"Erro ao exportar DOCX: {str(e)}")

    @staticmethod
    def _export_txt(text: str, file_path: str) -> None:
        """
        Exporta texto para um arquivo TXT.

        Abre (ou cria) o arquivo de texto e escreve todos os conteúdos fornecidos.

        Parâmetros:
            text (str): O texto a ser exportado para o TXT.
            file_path (str): Caminho onde o arquivo TXT será salvo.

        Retorna:
            None

        Exceções:
            - Exception: Se ocorrer um erro durante a escrita no TXT.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            raise Exception(f"Erro ao exportar TXT: {str(e)}")
