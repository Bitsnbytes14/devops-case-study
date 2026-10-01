"""Extract the CA II PDF diagram assets supplied by the student."""
from pathlib import Path
from pypdf import PdfReader

SOURCE = Path(r"C:\Users\Ineff\Downloads\RoomFit DevOps Case Study (CA II).pdf")
OUT = Path(__file__).parents[1] / "docs" / "diagrams" / "ca-ii-reference"
OUT.mkdir(parents=True, exist_ok=True)

for page_number in (3, 4, 6, 8, 11, 12, 21):
    page = PdfReader(SOURCE).pages[page_number - 1]
    for index, image in enumerate(page.images, start=1):
        (OUT / f"page-{page_number}-{index}.{image.name.split('.')[-1]}").write_bytes(image.data)
