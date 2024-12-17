from langchain_community.document_loaders import PDFPlumberLoader
from langchain_core.documents import Document
import pdfplumber
from pdfplumber import open as open_pdf
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTFigure
import math

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTFigure
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import math
import os

def pdf_load(file_path, x_tolerance=100):
    # x: x좌표 값 (정렬 대상인 x값)
    # x_tolerance : 허용 오차 범위 (오차 허용 정돌르 조정하는 값)

    def x_group_key(x):
        return min(
            [group for group in range(0, 1000, x_tolerance) if math.isclose(x, group, abs_tol=x_tolerance)],
            default=x
        )

    # 파일명 추출
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # 메타데이터 추출
    metadata = {"car_model": file_name}
    with open(file_path, 'rb') as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        if document.info:
            metadata.update({
                key: value.decode('utf-8', errors='ignore') if isinstance(value, bytes) else value
                for key, value in document.info[0].items()
            })

    contents = []
    for page, page_layout in enumerate(extract_pages(file_path)):

        sorted_objs = sorted(
            (obj for obj in page_layout._objs),
            key=lambda obj: (x_group_key(obj.bbox[0]), -obj.bbox[3])
        )

        text_combine = ""
        imgs = []
        texts = []
        for element in sorted_objs:
            if isinstance(element, LTTextBoxHorizontal):
                text_combine += element.get_text()
                text = {
                    "bbox": element.bbox,
                    "width": element.width,
                    "height": element.height,
                    "x0": element.x0,
                    "x1": element.x1,
                    "y0": element.y0,
                    "y1": element.y1,
                }
                texts.append(text)
            elif isinstance(element, LTFigure):
                img = {
                    "bbox": element.bbox,
                    "matrix": element.matrix,
                    "width": element.width,
                    "height": element.height,
                    "x0": element.x0,
                    "x1": element.x1,
                    "y0": element.y0,
                    "y1": element.y1,
                }
                imgs.append(img)

        content = {
            "page": page,
            "text_combine": text_combine,
            "texts": texts,
            "img": imgs,
        }
        contents.append(content)

    # 메타데이터와 콘텐츠 반환
    return {"metadata": metadata, "contents": contents}










