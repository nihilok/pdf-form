def load_pdf(filename):
    if not str(filename).endswith('.pdf'):
        raise ValueError("file must be pdf file with ext '.pdf'")
    with open(filename) as f:
        f.read()

def write_pdf(filename):
    pass
