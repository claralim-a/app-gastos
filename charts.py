def fn_update_layout(fig, 
                     width:int=1000,
                     height:int=800,
                     title_text:str=None, 
                     title_font_size:int=20,
                     xaxis_title:str=None, 
                     yaxis_title:str=None,
                     xaxis_tickfont_size:int=16,
                     yaxis_tickfont_size:int=16,
                     annotations_text:str=None):
    if title_text is not None:
        fig.update_layout(
            title=dict(
                text=title_text,
                font=dict(size=title_font_size)
            )
        )

    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        xaxis=dict(tickfont=dict(size=xaxis_tickfont_size)),
        yaxis=dict(tickfont=dict(size=yaxis_tickfont_size))
    )
    
    fig.update_layout(
        legend=dict(orientation="h", y=1.02, yanchor="bottom", xanchor="right", x=1, title=None, font=dict(size=16))
    )
    
    fig.update_layout(width=width, height=height)

    if annotations_text is not None:
        fig.update_layout(
            annotations=[
                dict(
                    xref='paper', yref='paper',
                    x=0, y=-0.1,
                    xanchor='left', yanchor='top',
                    text=annotations_text,
                    showarrow=False,
                    font=dict(size=12)
                )
            ]
        )
    
    return fig  # Adicionando retorno da figura modificada

