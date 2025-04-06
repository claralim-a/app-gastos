

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


color_scheme = ['#0378A6','#07F2F2','#21405F','#E5E9EF',
                        '#ED7F05','#FFAD1F','#A15500','#E6572C','#FF6047'] 

color_scheme_plus = ['#0378A6','#07F2F2','#21405F','#E5E9EF',
                        '#ED7F05','#FFAD1F','#A15500','#E6572C','#FF6047', 
                        '#0326A6', '#19E0AC', '#E45F52', '#AD0223', '#3E697A',
                        '#036969', '#646669', '#56A5F5'] 