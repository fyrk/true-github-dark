import re

import jinja2
import requests


def change_colors(colors, to_new_color, include_all=False):
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
                if include_all:
                    changed_colors.append((name, value))
        elif include_all:
            changed_colors.append((name, value))

    color_properties = ""
    for name, value in changed_colors:
        color_properties += name + ":" + value + ";"
    return color_properties


sites = {}


for name, url, css_pattern, light_pattern, dark_pattern, dimmed_pattern in (
        ("github", "https://github.com", r"https://github\.githubassets\.com/assets/frameworks-\w+\.css",
         r"\[data-light-theme=light]{(.*?)}",
         r"\[data-dark-theme=dark]{(.*?)}",
         r"\[data-dark-theme=dark_dimmed]{(.*?)}"),

        ("github-support", "https://support.github.com", r"https://support-assets\.github\.com/assets/frameworks-\w+\.css",
         r'\[data-light-theme="light"]{(.*?)}',
         r'\[data-dark-theme="dark"]{(.*?)}',
         r'\[data-dark-theme="dark_dimmed"]{(.*?)}'),

        ("github-docs", None, "https://docs.github.com/dist/index.css",
         r"\[data-dark-theme=light]{(.*?)}",
         r"\[data-dark-theme=dark]{(.*?)}",
         r"\[data-dark-theme=dark_dimmed]{(.*?)}"),

        ("github-resources", None, "https://resources.github.com/assets/css/index.css",
         r'\[data-light-theme="light"]{(.*?)}',
         r'\[data-dark-theme="dark"]{(.*?)}',
         r'\[data-dark-theme="dark_dimmed"]{(.*?)}'),

):
    print("\n\n\n########################\n#", name.upper())
    if url is not None:
        r = requests.get(url)
        css_url = re.search(css_pattern, r.text).group(0)
    else:
        css_url = css_pattern
    css = requests.get(css_url).text

    with open("run/" + name + ".css", "w") as f:
        f.write(css)

    themes = sites[name] = {
        "light": re.search(light_pattern, css).group(1),
        "dark": re.search(dark_pattern, css).group(1),
        "dark_dimmed": re.search(dimmed_pattern, css).group(1)
    }
    make_truly_dark = lambda r,g,b,m: "#" + f"{round(m):02X}"*3
    make_truly_darker = lambda r,g,b,m: "#" + f"{round(m*0.65 if m < 20 else (m*0.75 if m < 64 else m)):02X}"*3
    themes["truly_dark"] = change_colors(themes["dark"], make_truly_dark)
    themes["truly_dark_dimmed"] = change_colors(themes["dark_dimmed"], make_truly_dark)
    themes["truly_darker"] = change_colors(themes["dark"], make_truly_darker)

    for theme in ("light", "dark", "dark_dimmed"):
        themes[theme + "!i"] = themes[theme].replace(";", "!important;")
    themes["truly_dark!i"] = change_colors(themes["dark"], make_truly_dark, True)
    themes["truly_dark_dimmed!i"] = change_colors(themes["dark_dimmed"], make_truly_dark, True)
    themes["truly_darker!i"] = change_colors(themes["dark"], make_truly_darker, True)


with open("base.user.css.jinja2", "r") as t, open("true-github-dark.user.css", "w") as f:
    template = jinja2.Template(t.read())
    f.write(template.render(
        account_styled_sites=(
            (r'regexp("^https?://((vscode-auth|gist)\.)?github\.com/((?!(sponsors)).)*$")', sites["github"]),
            ('domain("support.github.com")', sites["github-support"])
        ),
        fixed_styled_sites=(
            ('domain("docs.github.com")', "docs", sites["github-docs"]),
            ('domain("resources.github.com")', "resources", sites["github-resources"])
        )
    ))
