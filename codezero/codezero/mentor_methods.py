try:
    from .models import *
except Exception:
    from models import *





def get_list():
    table = Mentor.select()
    lista = [("MENTOR NAME", "School Location")]
    for item in table:
        lista.append((item.name, item.school.name))
    return lista