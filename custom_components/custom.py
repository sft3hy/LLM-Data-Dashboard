from uuid import uuid4

with open("data/resources/content_copy.svg", "r") as copy:
    copy_svg = copy.read()

with open("data/resources/check_circle.svg", "r") as check:
    check_svg = check.read()

def gen_copy_button(copy_text):
    button_id = str(uuid4())
    copy_button = f"""
        <div>
            <button style="display: flex; justify-content: center; text-align: center; cursor: pointer; background-color: transparent; color: white; border: 2px solid white; padding: 10px 20px; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer;
        transition: all 0.3s ease;" id="{button_id}" onclick="copyToClipboard(`{copy_text}`)">{copy_svg}</button>
        </div>
        <script>
        const button = document.getElementById("{button_id}");
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text)
               .then(() => {{
                    button.innerHTML = `{check_svg}`;
                    setTimeout(() => {{
                        button.innerHTML = `{copy_svg}`;
                    }}, 2000); // Reset after 2 seconds
                }})
                .catch((err) => {{
                    console.error("Error copying text: ", err);
                }});
        }}
    </script>
    """
    return copy_button