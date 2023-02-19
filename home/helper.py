def verify_excel(filename):
    extension = filename.split(".")[-1]
    return True if extension=="xlsx" else False