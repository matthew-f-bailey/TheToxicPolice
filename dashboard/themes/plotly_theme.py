import plotly.graph_objects as go
import plotly.io as pio

from settings import COLORS

BG_COLOR = "rgb(30,30,30)"

pio.templates["custom"] = go.layout.Template(
    {
        "data": {
            "bar": [
                {
                    "error_x": {"color": "#f2f5fa"},
                    "error_y": {"color": "#f2f5fa"},
                    "marker": {
                        "line": {"color": BG_COLOR, "width": 0.5},
                        "pattern": {"fillmode": "overlay", "size": 10, "solidity": 0.2},
                    },
                    "type": "bar",
                }
            ],
            "barpolar": [
                {
                    "marker": {
                        "line": {"color": BG_COLOR, "width": 0.5},
                        "pattern": {"fillmode": "overlay", "size": 10, "solidity": 0.2},
                    },
                    "type": "barpolar",
                }
            ],
            "carpet": [
                {
                    "aaxis": {
                        "endlinecolor": "#A2B1C6",
                        "gridcolor": "#506784",
                        "linecolor": "#506784",
                        "minorgridcolor": "#506784",
                        "startlinecolor": "#A2B1C6",
                    },
                    "baxis": {
                        "endlinecolor": "#A2B1C6",
                        "gridcolor": "#506784",
                        "linecolor": "#506784",
                        "minorgridcolor": "#506784",
                        "startlinecolor": "#A2B1C6",
                    },
                    "type": "carpet",
                }
            ],
            "choropleth": [
                {"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}
            ],
            "contour": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "contour",
                }
            ],
            "contourcarpet": [
                {"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}
            ],
            "heatmap": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "heatmap",
                }
            ],
            "heatmapgl": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "heatmapgl",
                }
            ],
            "histogram": [
                {
                    "marker": {
                        "pattern": {"fillmode": "overlay", "size": 10, "solidity": 0.2}
                    },
                    "type": "histogram",
                }
            ],
            "histogram2d": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "histogram2d",
                }
            ],
            "histogram2dcontour": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "histogram2dcontour",
                }
            ],
            "mesh3d": [
                {"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}
            ],
            "parcoords": [
                {
                    "line": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "parcoords",
                }
            ],
            "pie": [{"automargin": True, "type": "pie"}],
            "scatter": [{"marker": {"line": {"color": "#283442"}}, "type": "scatter"}],
            "scatter3d": [
                {
                    "line": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scatter3d",
                }
            ],
            "scattercarpet": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scattercarpet",
                }
            ],
            "scattergeo": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scattergeo",
                }
            ],
            "scattergl": [
                {"marker": {"line": {"color": "#283442"}}, "type": "scattergl"}
            ],
            "scattermapbox": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scattermapbox",
                }
            ],
            "scatterpolar": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scatterpolar",
                }
            ],
            "scatterpolargl": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scatterpolargl",
                }
            ],
            "scatterternary": [
                {
                    "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                    "type": "scatterternary",
                }
            ],
            "surface": [
                {
                    "colorbar": {"outlinewidth": 0, "ticks": ""},
                    "colorscale": [
                        [0.0, "#0d0887"],
                        [0.1111111111111111, "#46039f"],
                        [0.2222222222222222, "#7201a8"],
                        [0.3333333333333333, "#9c179e"],
                        [0.4444444444444444, "#bd3786"],
                        [0.5555555555555556, "#d8576b"],
                        [0.6666666666666666, "#ed7953"],
                        [0.7777777777777778, "#fb9f3a"],
                        [0.8888888888888888, "#fdca26"],
                        [1.0, "#f0f921"],
                    ],
                    "type": "surface",
                }
            ],
            "table": [
                {
                    "cells": {
                        "fill": {"color": "#506784"},
                        "line": {"color": BG_COLOR},
                    },
                    "header": {
                        "fill": {"color": "#2a3f5f"},
                        "line": {"color": BG_COLOR},
                    },
                    "type": "table",
                }
            ],
        },
        "layout": {
            "annotationdefaults": {
                "arrowcolor": "#f2f5fa",
                "arrowhead": 0,
                "arrowwidth": 1,
            },
            "autotypenumbers": "strict",
            "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
            "colorscale": {
                "diverging": [
                    [0, "#8e0152"],
                    [0.1, "#c51b7d"],
                    [0.2, "#de77ae"],
                    [0.3, "#f1b6da"],
                    [0.4, "#fde0ef"],
                    [0.5, "#f7f7f7"],
                    [0.6, "#e6f5d0"],
                    [0.7, "#b8e186"],
                    [0.8, "#7fbc41"],
                    [0.9, "#4d9221"],
                    [1, "#276419"],
                ],
                "sequential": [
                    [0.0, "#0d0887"],
                    [0.1111111111111111, "#46039f"],
                    [0.2222222222222222, "#7201a8"],
                    [0.3333333333333333, "#9c179e"],
                    [0.4444444444444444, "#bd3786"],
                    [0.5555555555555556, "#d8576b"],
                    [0.6666666666666666, "#ed7953"],
                    [0.7777777777777778, "#fb9f3a"],
                    [0.8888888888888888, "#fdca26"],
                    [1.0, "#f0f921"],
                ],
                "sequentialminus": [
                    [0.0, "#0d0887"],
                    [0.1111111111111111, "#46039f"],
                    [0.2222222222222222, "#7201a8"],
                    [0.3333333333333333, "#9c179e"],
                    [0.4444444444444444, "#bd3786"],
                    [0.5555555555555556, "#d8576b"],
                    [0.6666666666666666, "#ed7953"],
                    [0.7777777777777778, "#fb9f3a"],
                    [0.8888888888888888, "#fdca26"],
                    [1.0, "#f0f921"],
                ],
            },
            "colorway": [  # 636efa, #EF553B, #00cc96, #ab63fa, #FFA15A, #19d3f3,
                # FF6692, #B6E880, #FF97FF, #FECB52
            ],
            "font": {"color": "#f2f5fa"},
            "geo": {
                "bgcolor": BG_COLOR,
                "lakecolor": BG_COLOR,
                "landcolor": BG_COLOR,
                "showlakes": True,
                "showland": True,
                "subunitcolor": "#506784",
            },
            "hoverlabel": {"align": "left"},
            "hovermode": "closest",
            "mapbox": {"style": "dark"},
            "paper_bgcolor": BG_COLOR,
            "plot_bgcolor": BG_COLOR,
            "polar": {
                "angularaxis": {
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "ticks": "",
                },
                "bgcolor": BG_COLOR,
                "radialaxis": {
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "ticks": "",
                },
            },
            "scene": {
                "xaxis": {
                    "backgroundcolor": BG_COLOR,
                    "gridcolor": "#506784",
                    "gridwidth": 2,
                    "linecolor": "#506784",
                    "showbackground": True,
                    "ticks": "",
                    "zerolinecolor": "#C8D4E3",
                },
                "yaxis": {
                    "backgroundcolor": BG_COLOR,
                    "gridcolor": "#506784",
                    "gridwidth": 2,
                    "linecolor": "#506784",
                    "showbackground": True,
                    "ticks": "",
                    "zerolinecolor": "#C8D4E3",
                },
                "zaxis": {
                    "backgroundcolor": BG_COLOR,
                    "gridcolor": "#506784",
                    "gridwidth": 2,
                    "linecolor": "#506784",
                    "showbackground": True,
                    "ticks": "",
                    "zerolinecolor": "#C8D4E3",
                },
            },
            "shapedefaults": {"line": {"color": "#f2f5fa"}},
            "sliderdefaults": {
                "bgcolor": "#C8D4E3",
                "bordercolor": BG_COLOR,
                "borderwidth": 1,
                "tickwidth": 0,
            },
            "ternary": {
                "aaxis": {"gridcolor": "#506784", "linecolor": "#506784", "ticks": ""},
                "baxis": {"gridcolor": "#506784", "linecolor": "#506784", "ticks": ""},
                "bgcolor": BG_COLOR,
                "caxis": {"gridcolor": "#506784", "linecolor": "#506784", "ticks": ""},
            },
            "title": {"x": 0.05},
            "updatemenudefaults": {"bgcolor": "#506784", "borderwidth": 0},
            "xaxis": {
                "automargin": True,
                "gridcolor": "#283442",
                "linecolor": "#506784",
                "ticks": "",
                "title": {"standoff": 15},
                "zerolinecolor": "#283442",
                "zerolinewidth": 2,
            },
            "yaxis": {
                "automargin": True,
                "gridcolor": "#283442",
                "linecolor": "#506784",
                "ticks": "",
                "title": {"standoff": 15},
                "zerolinecolor": "#283442",
                "zerolinewidth": 2,
            },
        },
    }
)
