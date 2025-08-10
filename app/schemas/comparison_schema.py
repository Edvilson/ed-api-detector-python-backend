from pydantic import BaseModel

class CompareRequest(BaseModel):
    texto_1: str
    texto_2: str

class CompareResponse(BaseModel):
    similaridade: float
    classificacao: str
    resumo: str
