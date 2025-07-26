"""
Script to convert HTML content to f-string format
"""


def generate_html_fstring():
    """Generate HTML content using f-strings"""

    html_content = f"""<style>
.timeline-compute-remort {{
    overflow: auto;
    width: 100%;
}}

.timeline-compute-remort table {{
    border: 1px solid #dededf;
    height: 100%;
    width: 100%;
    table-layout: fixed;
    border-collapse: collapse;
    border-spacing: 1px;
    text-align: left;
}}

.timeline-compute-remort caption {{
    caption-side: top;
    text-align: left;
}}

.timeline-compute-remort th {{
    border: 1px solid #dededf;
    background-color: #eceff1;
    color: #000000;
    padding: 5px;
}}

.timeline-compute-remort td {{
    border: 1px solid #dededf;
    padding: 5px;
}}

.timeline-compute-remort tr:nth-child(even) td {{
    background-color: #ffffff;
    color: #000000;
}}

.timeline-compute-remort tr:nth-child(odd) td {{
    background-color: #ffffff;
    color: #000000;
}}
</style>
<div class="timeline-compute-remort" role="region" tabindex="0">
<table>
    <caption>Table 1</caption>
    <thead>
        <tr>
            <th>Component</th>
            <th>Feature</th>
            <th>Time (s)</th>
            <th>Health</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
    </tbody>
</table>
<div style="margin-top:8px">Made with <a href="https://www.htmltables.io/" target="_blank">HTML Tables</a></div>
</div>"""

    return html_content


def write_line_by_line_fstrings():
    """Write each line as a separate f-string"""

    lines = [
        f"<style>",
        f".timeline-compute-remort {{",
        f"    overflow: auto;",
        f"    width: 100%;",
        f"}}",
        f"",
        f".timeline-compute-remort table {{",
        f"    border: 1px solid #dededf;",
        f"    height: 100%;",
        f"    width: 100%;",
        f"    table-layout: fixed;",
        f"    border-collapse: collapse;",
        f"    border-spacing: 1px;",
        f"    text-align: left;",
        f"}}",
        f"",
        f".timeline-compute-remort caption {{",
        f"    caption-side: top;",
        f"    text-align: left;",
        f"}}",
        f"",
        f".timeline-compute-remort th {{",
        f"    border: 1px solid #dededf;",
        f"    background-color: #eceff1;",
        f"    color: #000000;",
        f"    padding: 5px;",
        f"}}",
        f"",
        f".timeline-compute-remort td {{",
        f"    border: 1px solid #dededf;",
        f"    padding: 5px;",
        f"}}",
        f"",
        f".timeline-compute-remort tr:nth-child(even) td {{",
        f"    background-color: #ffffff;",
        f"    color: #000000;",
        f"}}",
        f"",
        f".timeline-compute-remort tr:nth-child(odd) td {{",
        f"    background-color: #ffffff;",
        f"    color: #000000;",
        f"}}",
        f"</style>",
        f'<div class="timeline-compute-remort" role="region" tabindex="0">',
        f"<table>",
        f"    <caption>Table 1</caption>",
        f"    <thead>",
        f"        <tr>",
        f"            <th>Component</th>",
        f"            <th>Feature</th>",
        f"            <th>Time (s)</th>",
        f"            <th>Health</th>",
        f"        </tr>",
        f"    </thead>",
        f"    <tbody>",
        f"        <tr>",
        f"            <td></td>",
        f"            <td></td>",
        f"            <td></td>",
        f"            <td></td>",
        f"        </tr>",
        f"        <tr>",
        f"            <td></td>",
        f"            <td></td>",
        f"            <td></td>",
        f"            <td></td>",
        f"        </tr>",
        f"        <tr>",
        f"            <td></td>",
        f"            <td></td>",
        f"            <td></td>",
        f"            <td></td>",
        f"        </tr>",
        f"        <tr>",
        f"            <td></td>",
        f"            <td></td>",
        f"            <td></td>",
        f"            <td></td>",
        f"        </tr>",
        f"    </tbody>",
        f"</table>",
        f'<div style="margin-top:8px">Made with <a href="https://www.htmltables.io/" target="_blank">HTML Tables</a></div>',
        f"</div>",
    ]

    return lines


def write_html_with_variables(component="", feature="", time="", health=""):
    """Write HTML with variable placeholders using f-strings"""

    html_content = f"""<style>
.timeline-compute-remort {{
    overflow: auto;
    width: 100%;
}}

.timeline-compute-remort table {{
    border: 1px solid #dededf;
    height: 100%;
    width: 100%;
    table-layout: fixed;
    border-collapse: collapse;
    border-spacing: 1px;
    text-align: left;
}}

.timeline-compute-remort caption {{
    caption-side: top;
    text-align: left;
}}

.timeline-compute-remort th {{
    border: 1px solid #dededf;
    background-color: #eceff1;
    color: #000000;
    padding: 5px;
}}

.timeline-compute-remort td {{
    border: 1px solid #dededf;
    padding: 5px;
}}

.timeline-compute-remort tr:nth-child(even) td {{
    background-color: #ffffff;
    color: #000000;
}}

.timeline-compute-remort tr:nth-child(odd) td {{
    background-color: #ffffff;
    color: #000000;
}}
</style>
<div class="timeline-compute-remort" role="region" tabindex="0">
<table>
    <caption>Table 1</caption>
    <thead>
        <tr>
            <th>Component</th>
            <th>Feature</th>
            <th>Time (s)</th>
            <th>Health</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>{component}</td>
            <td>{feature}</td>
            <td>{time}</td>
            <td>{health}</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
    </tbody>
</table>
<div style="margin-top:8px">Made with <a href="https://www.htmltables.io/" target="_blank">HTML Tables</a></div>
</div>"""

    return html_content


if __name__ == "__main__":
    print("Method 1: Complete HTML as single f-string")
    print("=" * 50)
    html1 = generate_html_fstring()
    print(html1)

    print("\n\nMethod 2: Each line as separate f-string")
    print("=" * 50)
    lines = write_line_by_line_fstrings()
    for line in lines:
        print(f"    {repr(line)},")

    print("\n\nMethod 3: HTML with variable placeholders")
    print("=" * 50)
    html3 = write_html_with_variables("Engine", "Turbo", "2.5", "Good")
    print(html3)

    # Example of how to use the line-by-line approach
    print("\n\nExample: Building HTML line by line")
    print("=" * 50)
    html_lines = write_line_by_line_fstrings()
    complete_html = "\n".join(html_lines)

    # Write to file
    with open("generated_output.html", "w", encoding="utf-8") as f:
        f.write(complete_html)

    print("HTML written to 'generated_output.html'")
