from uuid import uuid4


def gen_copy_button(copy_text):
    button_id = str(uuid4())
    copy_button = f"""
        <div>
            <button style="display: flex; justify-content: center; text-align: center; cursor: pointer; background-color: transparent; color: white; border: 2px solid white; padding: 10px 20px; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer;
        transition: all 0.3s ease;" id="{button_id}" onclick="copyToClipboard(`{copy_text}`)"><svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 -960 960 960" width="18px" fill="#ffffff">
    <path
        d="M360-240q-33 0-56.5-23.5T280-320v-480q0-33 23.5-56.5T360-880h360q33 0 56.5 23.5T800-800v480q0 33-23.5 56.5T720-240H360Zm0-80h360v-480H360v480ZM200-80q-33 0-56.5-23.5T120-160v-560h80v560h440v80H200Zm160-240v-480 480Z" />
</svg></button>
        </div>
        <script>
        const button = document.getElementById("{button_id}");
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text)
               .then(() => {{
                    button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 -960 960 960" width="18px" fill="#ffffff">
    <path
        d="m424-296 282-282-56-56-226 226-114-114-56 56 170 170Zm56 216q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z" />
</svg>`;
                    setTimeout(() => {{
                        button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 -960 960 960" width="18px" fill="#ffffff">
    <path
        d="M360-240q-33 0-56.5-23.5T280-320v-480q0-33 23.5-56.5T360-880h360q33 0 56.5 23.5T800-800v480q0 33-23.5 56.5T720-240H360Zm0-80h360v-480H360v480ZM200-80q-33 0-56.5-23.5T120-160v-560h80v560h440v80H200Zm160-240v-480 480Z" />
</svg>`;
                    }}, 2000); // Reset after 2 seconds
                }})
                .catch((err) => {{
                    console.error("Error copying text: ", err);
                }});
        }}
    </script>
    """
    return copy_button