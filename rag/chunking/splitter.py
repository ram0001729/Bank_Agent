class RecursiveTextSplitter:
    def __init__(self, chunk_size: int = 300, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str):
        chunks = []
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        current_chunk = ""

        for line in lines:
            if len(current_chunk) + len(line) + 1 <= self.chunk_size:
                current_chunk += (" " if current_chunk else "") + line
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line

        if current_chunk:
            chunks.append(current_chunk)

        return chunks
