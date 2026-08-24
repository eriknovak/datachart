"""Strips nbconvert scaffolding the llmstxt autoclean does not cover: cell
prompts, clipboard widgets and their duplicated code text, paragraph anchors,
and cell outputs — llms-full.txt keeps prose and code only."""

# prose and code only (ADR 0016): outputs and widget scaffolding go
_REMOVE_CLASSES = (
    "jp-InputPrompt",
    "jp-OutputPrompt",
    "zeroclipboard-container",
    "clipboard-copy-txt",
    "anchor-link",
    "jp-Cell-outputWrapper",
)


def preprocess(soup, output):
    for class_ in _REMOVE_CLASSES:
        for element in soup.find_all(class_=class_):
            element.decompose()
