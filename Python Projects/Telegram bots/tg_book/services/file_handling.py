BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    ch = ',.!:;?'
    ssize = size
    if len(text) <= size+start:
        ssize = len(text)-start
    else:
        for i in range(size+start-1, start, -1):
            if text[i] in ch and text[i+1] not in ch:
                return [text[start: start + ssize], ssize]
            ssize -= 1
    return [text[start: start + ssize], ssize]


def prepare_book(path: str) -> None:
    with open(path, 'r') as file:
        lines = file.readlines()
        pages_count = 1
        text = ''
        size = 0
        for line in lines:
            text += line
        for _ in range(len(text)//PAGE_SIZE+1):
            t = _get_part_text(text, size, PAGE_SIZE)[0]
            t = t.strip().lstrip()
            size += _get_part_text(text, size, PAGE_SIZE)[1]
            book[pages_count] = t
            pages_count += 1


prepare_book(BOOK_PATH)