# Theme Explorer

Pick a theme and see how it draws every chart, or pick a chart and see it under every theme. The [Theme Gallery](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/theme-gallery/index.md) shows each theme's palette and six signature charts; this page covers the chart types the gallery leaves out, with values, dense marks and value scales, where the themes differ most. Every image is rendered by datachart when the site is built.

The sample data and the builder of each chart are defined in a hidden cell. The next cell renders each chart under each theme with `config.set_theme(...)`, then hands the pictures to a small page with the selectors.

```
def render(build, theme):
    """One chart under one theme, as a WebP data URI."""
    config.set_theme(theme)
    fig = build()
    buffer = io.BytesIO()
    fig.savefig(buffer, format="webp", dpi=100, pil_kwargs={"quality": 82})
    plt.close(fig)
    return "data:image/webp;base64," + base64.b64encode(buffer.getvalue()).decode()


images = {
    theme: {name: render(build, theme) for name, build in CHARTS.items()}
    for theme in THEMES
}
config.reset_config()
```

Applying a theme replaces the whole global configuration, so the last line of the build cell resets it. See the [themes how-to](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/themes/index.md) for customizing themes attribute by attribute.
