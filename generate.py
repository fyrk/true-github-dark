import re

import requests

r = requests.get("https://github.com")
css_url = re.search(r"https://github\.githubassets\.com/assets/frameworks-\w+\.css", r.text).group(0)
print("CSS URL:", css_url)
r = requests.get(css_url)
css = r.text

with open("github-style.css", "w") as f:
    f.write(css)


def change_colors(colors, to_new_color):
    changed_colors = []
    for color_property in colors.split(";"):
        name, value = color_property.split(":")
        if match := re.search(r"#([0-9A-F]{6})", value, re.IGNORECASE):
            color = match.group(1)
            r, g, b = (int(color[i:i + 2], 16) for i in range(0, 6, 2))
            mean = (r + g + b) / 3
            if max(r, g, b) - min(r, g, b) < 30 and min(r, g, b) != max(r, g, b):
                new_value = to_new_color(r, g, b, mean)
                changed_colors.append((name, new_value))
                print(f"      change {name+':':40} {value} to {new_value} {(r, g, b, round(mean, 1))}")
            else:
                print(f"don't change {name+':':40} {value} {(r, g, b, round(mean, 1))}")

    color_properties = ""
    for name, value in changed_colors:
        color_properties += name + ":" + value + "; "
    return color_properties


def create_userstyle(filename, style_name, description, changed_colors_and_wrappers):
    with open(filename, "w") as f:
        f.write(f"""/* ==UserStyle==
@name        {style_name}
@description {description}
@namespace   FlorianRaediker
@version     1.1.0
@author      Florian Rädiker
@homepageURL https://github.com/FlorianRaediker/true-github-dark
@license     MIT
@updateURL   https://florianraediker.github.io/true-github-dark/{filename}
==/UserStyle== */
""")
        f.write("""@-moz-document regexp("^https?://((education|graphql|guides|raw|resources|status|developer|support|vscode-auth)\\.)?github\\.com/((?!(sponsors)).)*$"), domain("githubusercontent.com"), domain("www.githubstatus.com") { /* domains from https://github.com/StylishThemes/GitHub-Dark */\n""")
        for comment, color_properties, wrappers in changed_colors_and_wrappers:
            if comment:
                f.write("/* " + comment + " */\n")
            for start, end in wrappers:
                f.write(start)
                f.write(color_properties)
                f.write(end)
            f.write("\n")
        f.write("}\n")


dark_colors = re.search(r"\[data-color-mode=dark]\[data-dark-theme=dark],\[data-color-mode=light]\[data-light-theme=dark]{(.*?)}", css).group(1)
dark_dimmed_colors = re.search(r"\[data-color-mode=dark]\[data-dark-theme=dark_dimmed],\[data-color-mode=light]\[data-light-theme=dark_dimmed]{(.*?)}", css).group(1)

print("\n\n================\nCHANGE DARK COLORS")
changed_dark_colors = change_colors(dark_colors,
                                    lambda r,g,b,m: "#" + f"{round(m):02X}"*3)
print("\n\n================\nCHANGE DIMMED COLORS")
changed_dark_dimmed_colors = change_colors(dark_dimmed_colors,
                                           lambda r,g,b,m: "#" + f"{round(m):02X}"*3)

print("\n\n================\nDARKEN DARK COLORS")
darker_dark_colors = change_colors(dark_colors,
                                   lambda r,g,b,m: "#" + f"{round(m*0.65 if m < 20 else (m*0.75 if m < 64 else m)):02X}"*3)

dark_wrappers = [
    ("[data-color-mode=dark][data-dark-theme=dark], [data-color-mode=light][data-light-theme=dark] {\n    ", "\n}\n"),
    ("@media (prefers-color-scheme: light) { [data-color-mode=auto][data-light-theme=dark] {\n    ", "\n}}\n"),
    ("@media (prefers-color-scheme: dark) { [data-color-mode=auto][data-dark-theme=dark] {\n    ", "\n}}\n")
]
dimmed_wrappers = [
    ("[data-color-mode=dark][data-dark-theme=dark_dimmed], [data-color-mode=light][data-light-theme=dark_dimmed] {\n    ", "\n}\n"),
    ("@media (prefers-color-scheme: light) { [data-color-mode=auto][data-light-theme=dark_dimmed] {\n    ", "\n}}\n"),
    ("@media (prefers-color-scheme: dark) { [data-color-mode=auto][data-dark-theme=dark_dimmed] {\n    ", "\n}}\n")
]

create_userstyle("true-github-dark.user.css",
                 "True GitHub Dark",
                 "Change bluish dark colors on GitHub to truly dark",
                 [
                     ("Dark colors", changed_dark_colors, dark_wrappers),
                     ("Dimmed colors", changed_dark_dimmed_colors, dimmed_wrappers)
                 ])

create_userstyle("true-github-dark-darker.user.css",
                 "True GitHub Dark - Darker",
                 "Change bluish dark colors on GitHub to truly, even darker colors",
                 [
                     ("", darker_dark_colors, dark_wrappers)
                 ])
