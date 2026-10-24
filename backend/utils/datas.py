def para_texto_iso(valor):
    """
    Datas vindas de consultas SQL: o SQLite devolve texto ('AAAA-MM-DD HH:MM:SS.ffffff')
    e o MySQL devolve datetime. Padroniza para 'AAAA-MM-DDTHH:MM:SS'.
    """
    if valor is None:
        return None
    if hasattr(valor, "isoformat"):
        return valor.isoformat(timespec="seconds")
    return str(valor)[:19].replace(" ", "T")
