from app.utils.similarity import calculate_similarity
from app.models.comparison import Comparison
from app.services.usage_service import check_daily_limit

def compare_texts(texto_1: str, texto_2: str, user, db):
    check_daily_limit(user, db)
    resultado = calculate_similarity(texto_1, texto_2)
    comp = Comparison(user_id=user.id, texto_1=texto_1, texto_2=texto_2, resultado=resultado)
    db.add(comp)
    db.commit()
    return resultado
