# blog
github pages source (virtualenv with pelican + custom theme + md) for `fernandezcuesta.github.io`.

Use `git clone --recursive` to clone submodules.

# TODO:

- Standardise pelican theme (pelican variables, refactor, CSS cleanup)
- Fix theme (left column) when more >1 post for the same day are rendered
- Automatically minify CSS
- Fix duplicate tag detection
- Replace custom codehilite patch with [pelican plugin](https://github.com/getpelican/pelican-plugins):
[better_codeblock_line_numbering](https://github.com/getpelican/pelican-plugins/tree/master/better_codeblock_line_numbering)
