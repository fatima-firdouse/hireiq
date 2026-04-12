# frontend/components/charts.py

import plotly.graph_objects as go
import plotly.express as px


def match_score_gauge(score: int) -> go.Figure:
    if score < 40:
        color = "#FF4B4B"
    elif score < 70:
        color = "#FFA500"
    else:
        color = "#00CC44"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Match Score", "font": {"size": 20}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 40],   "color": "#FFE5E5"},
                {"range": [40, 70],  "color": "#FFF3E0"},
                {"range": [70, 100], "color": "#E5FFE5"},
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 0.75,
                "value": score
            }
        }
    ))
    fig.update_layout(
        height=300,
        margin=dict(t=50, b=20, l=30, r=30)
    )
    return fig


def skills_gap_chart(matched: list, missing: list) -> go.Figure:
    all_skills = matched + missing
    colors = ["#00CC44"] * len(matched) + ["#FF4B4B"] * len(missing)
    values = [1] * len(all_skills)

    fig = go.Figure(go.Bar(
        x=values,
        y=all_skills,
        orientation="h",
        marker_color=colors,
        text=(
            ["✅ Matched"] * len(matched) +
            ["❌ Missing"] * len(missing)
        ),
        textposition="inside",
        insidetextanchor="middle"
    ))

    fig.update_layout(
        title="Skills Analysis",
        xaxis={"showticklabels": False, "showgrid": False},
        yaxis={"autorange": "reversed"},
        height=max(300, len(all_skills) * 35),
        margin=dict(t=50, b=20, l=150, r=30),
        showlegend=False
    )
    return fig


def bias_breakdown_chart(bias_instances: list) -> go.Figure:
    if not bias_instances:
        return None

    from collections import Counter
    type_counts = Counter(b["bias_type"] for b in bias_instances)

    fig = px.pie(
        names=list(type_counts.keys()),
        values=list(type_counts.values()),
        title="Bias Types Found",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(height=300, margin=dict(t=50, b=20))
    return fig


def quality_score_bar(score: int) -> go.Figure:
    color = (
        "#FF4B4B" if score < 40
        else "#FFA500" if score < 70
        else "#00CC44"
    )

    fig = go.Figure(go.Bar(
        x=[score],
        y=["JD Quality"],
        orientation="h",
        marker_color=color,
        text=[f"{score}/100"],
        textposition="inside"
    ))

    fig.update_layout(
        xaxis={"range": [0, 100]},
        height=120,
        margin=dict(t=20, b=20, l=10, r=10),
        showlegend=False
    )
    return fig


def requirement_inflation_chart(score: int) -> go.Figure:
    """
    Horizontal bar showing requirement calibration score.
    100 = perfectly calibrated, 0 = massively inflated.
    """
    color = (
        "#FF4B4B" if score < 40
        else "#FFA500" if score < 70
        else "#00CC44"
    )

    fig = go.Figure(go.Bar(
        x=[score],
        y=["Requirements"],
        orientation="h",
        marker_color=color,
        text=[f"{score}/100"],
        textposition="inside"
    ))

    fig.update_layout(
        title="Requirement Calibration Score",
        xaxis={"range": [0, 100]},
        height=120,
        margin=dict(t=40, b=20, l=10, r=10),
        showlegend=False
    )
    return fig