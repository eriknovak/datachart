"""Build guard: every nav guide/reference page must appear in the llmstxt
sections config, so new pages cannot silently drop out of llms.txt."""

from fnmatch import fnmatch

from mkdocs.exceptions import PluginError

# only guide and reference pages belong in llms.txt (ADR 0016)
GUARDED_PREFIXES = ("how-to-guides/", "references/")


def _nav_paths(items):
    for item in items:
        if isinstance(item, str):
            yield item
        elif isinstance(item, dict):
            for value in item.values():
                if isinstance(value, str):
                    yield value
                else:
                    yield from _nav_paths(value)


def _section_patterns(sections):
    for entries in sections.values():
        for entry in entries:
            if isinstance(entry, dict):
                yield from entry.keys()
            else:
                yield entry


def on_config(config):
    patterns = list(_section_patterns(config.plugins["llmstxt"].config["sections"]))
    missing = [
        path
        for path in _nav_paths(config.nav or [])
        if path.startswith(GUARDED_PREFIXES)
        and not any(fnmatch(path, pattern) for pattern in patterns)
    ]
    if missing:
        raise PluginError(
            "Pages in nav but missing from the llmstxt sections config "
            f"(add each with a description): {', '.join(missing)}"
        )
    return config
