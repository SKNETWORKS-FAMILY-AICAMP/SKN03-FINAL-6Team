from langchain_community.document_loaders import PDFPlumberLoader
from langchain_core.documents import Document
import pdfplumber
import json

def LoadPDF(file_path:str):
    loader = PDFPlumberLoader(file_path)
    docs = loader.load()
    return docs

def LoadPDF2(file_path: str):
    docs = []
    # PDFPlumber를 사용하여 파일을 로드합니다.
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            # 페이지 크기 확인
            width, height = page.width, page.height

            # 2개의 영역(열)으로 나누기
            left_bbox = (0, 0, width / 2, height)   # 왼쪽 열
            right_bbox = (width / 2, 0, width, height)  # 오른쪽 열

            # 왼쪽 열 텍스트 추출
            left_text = page.within_bbox(left_bbox).extract_text() or ""
            
            # 오른쪽 열 텍스트 추출
            right_text = page.within_bbox(right_bbox).extract_text() or ""

            # 텍스트 병합
            page_text = left_text + "\n" + right_text

            # 문서를 Langchain 형식으로 변환하여 추가
            if page_text.strip():
                docs.append(Document(
                    page_content=page_text,
                    metadata={
                        'source': file_path,
                        'file_path': file_path,
                        'page': page.page_number,
                        'total_pages': len(pdf.pages),
                        'CreationDate': pdf.metadata.get('CreationDate', None),
                        'ModDate': pdf.metadata.get('ModDate', None)
                    }
                ))

    return docs


def loadPDF3(file_path: str):

    with open("../data/data.json", "r", encoding="utf-8") as f:
        state = json.load(f)

        docs = []
        # PDFPlumber를 사용하여 파일을 로드합니다.
        for page_num in state['page_numbers']:
            # 문서를 Langchain 형식으로 변환하여 추가
            page_text = state['texts'][str(page_num)]
            if page_text.strip():
                docs.append(Document(
                    page_content=page_text,
                    metadata={
                        'source': state['filepath'],
                        'page': page_num,
                        'total_pages': len(state['page_metadata']),                     }
                    ))
    return docs