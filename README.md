# True GitHub Dark
[Stylus](https://add0n.com/stylus.html) theme that changes GitHub's bluish dark theme colors to truly dark. 

## Installation
 1. Install Stylus Browser Extension ([Firefox](https://addons.mozilla.org/en-US/firefox/addon/styl-us/), [Chromium-based](https://chrome.google.com/webstore/detail/stylus/clngdbkpkpeebahjckkjfobafhncgmne), [Opera](https://addons.opera.com/extensions/details/stylus/)).
 2. There are two styles available:
     * [true-github-dark.user.css](https://florianraediker.github.io/true-github-dark/true-github-dark.user.css)
       changes bluish colors from the dark and dimmed themes to truly dark
       (change the theme at https://github.com/settings/appearance).
     * [true-github-darker.user.css](https://florianraediker.github.io/true-github-dark/true-github-darker.user.css)
       changes colors from the dark theme to truly, even darker colors.

### How it works
[`generate.py`](generate.py) downloads the current CSS file from GitHub, extracts the colors for dark and dimmed themes
and applies different filters to them
(filter for true-github-dark.user.css changes rgb values to their mean if they are too different, thus creating a
 greyscale color;
 filter for true-github-darker.user.css additionally makes colors darker if the mean value is below a certain threshold).
The generated style is then saved to the appropriate file.

### Thanks
Thanks to the [GitHub-Dark](https://github.com/StylishThemes/GitHub-Dark) theme, which I used until GitHub had its own
dark theme.
