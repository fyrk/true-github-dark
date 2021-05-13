[![Install directly with Stylus](https://img.shields.io/badge/Install%20directly%20with-Stylus-00adad.svg)](https://github.com/FlorianRaediker/true-github-dark/raw/main/true-github-dark.user.css)

# True GitHub Dark
[Stylus](https://add0n.com/stylus.html) theme that changes GitHub's bluish dark colors to truly dark. Works with both dark and dimmed themes.

In the style's settings, themes for [GitHub Docs](https://docs.github.com) and [GitHub Resources](https://resources.github.com) can also be changed. Additionally, GitHub's theme can be changed even if you're not logged in.

## Installation
 1. Install Stylus Browser Extension ([Firefox](https://addons.mozilla.org/en-US/firefox/addon/styl-us/), [Chromium-based](https://chrome.google.com/webstore/detail/stylus/clngdbkpkpeebahjckkjfobafhncgmne), [Opera](https://addons.opera.com/extensions/details/stylus/)).
 2. Install [true-github-dark.user.css](https://github.com/FlorianRaediker/true-github-dark/raw/main/true-github-dark.user.css).

### How it works
[`generate.py`](generate.py) downloads the current CSS files from GitHub, GitHub Docs, and GitHub Resources, then extracts the color variables and applies different filters to the dark and dimmed colors (filter for "Truly Dark/Dimmed" changes RGB values to their mean if they are too different, thus creating a greyscale color; filter for "Truly Darker" additionally makes colors darker if the mean value is below a certain threshold).
The UserCSS is then generated using Jinja2.

### Thanks
Thanks to the [GitHub-Dark](https://github.com/StylishThemes/GitHub-Dark) theme, which I used until GitHub had its own dark theme.
