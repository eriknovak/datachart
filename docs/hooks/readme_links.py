"""Points the home page's README links at the version being built: the
README pins them to /latest/ for GitHub, but a page inlined into the dev or
an older release site must link within that site."""

# the README's absolute docs prefix; the home page sits at the site root, so
# the remainder is a valid relative link on every mike version
LATEST = 'href="https://eriknovak.github.io/datachart/latest/'


def on_page_content(html, page, config, files):
    if page.file.src_uri != "index.md":
        return html
    return html.replace(LATEST, 'href="')
