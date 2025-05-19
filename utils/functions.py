
def gera_markdown(title, value, use_color=False):
    # Formata valor
    formatted_value = f"{value:.2f} €"

    # Define a cor com base no valor, se use_color for True
    color_style = ""
    if use_color:
        color = "green" if value > 0 else "red" if value < 0 else "black"
        color_style = f"color: {color};"

    # Markdown com cor condicional aplicada diretamente no <h3>
    return f"""
        <style>
            .larger-font {{
                font-size: 30px;
            }}
        </style>
        <br><br>
        {title} (€)<br>
        <h3 style="margin-top: -20px; {color_style}" class="larger-font">{formatted_value}</h3>
    """


 