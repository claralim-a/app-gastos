

def gera_markdown(title, value):
    # Formata valor
    formatted_value = f"{value:.2f} €"

    # Mkd
    return f"""
        <style>
            .larger-font {{
                font-size: 30px;  
            }}
        </style>
        <br><br>
        {title} (€)<br>
        <h3 style="margin-top: -20px;" class="larger-font">{formatted_value}</h3>
    """

color_scheme = ['#0378A6','#07F2F2','#21405F','#E5E9EF',
                        '#ED7F05','#FFAD1F','#A15500','#E6572C','#FF6047'] 

color_scheme_plus = ['#0378A6','#07F2F2','#21405F','#E5E9EF',
                        '#ED7F05','#FFAD1F','#A15500','#E6572C','#FF6047', 
                        '#0326A6', '#19E0AC', '#E45F52', '#AD0223', '#3E697A',
                        '#036969', '#646669', '#56A5F5'] 