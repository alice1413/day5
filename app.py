"""서울 행정동별 출동건수 Choropleth 지도."""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="서울 행정동 출동건수", page_icon="🚒", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "dong_emergency_count.geojson"
CITY_HALL = {"lat": 37.5665, "lon": 126.9780}


@st.cache_data
def load_geojson(path: str) -> dict:
    """GeoJSON을 한 번만 읽어 화면 갱신 시에도 빠르게 표시한다."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def make_dataframe(geojson: dict) -> pd.DataFrame:
    """Plotly 색상 및 호버에 필요한 속성만 표 형태로 만든다."""
    return pd.DataFrame(
        [
            {
                "행정동 코드": feature["properties"]["ADM_CD"],
                "행정동명": feature["properties"]["ADM_NM"],
                "출동건수": feature["properties"]["emergency_count"],
            }
            for feature in geojson["features"]
        ]
    )


def build_map(data: pd.DataFrame, geojson: dict):
    fig = px.choropleth_mapbox(
        data,
        geojson=geojson,
        locations="행정동 코드",
        featureidkey="properties.ADM_CD",
        color="출동건수",
        color_continuous_scale=[[0, "#ffffff"], [1, "#e31a1c"]],
        range_color=(data["출동건수"].min(), data["출동건수"].max()),
        mapbox_style="open-street-map",
        center=CITY_HALL,
        zoom=10.2,
        opacity=0.72,
        hover_name="행정동명",
        hover_data={"행정동 코드": True, "행정동명": False, "출동건수": ":,"},
        labels={"출동건수": "출동건수", "행정동 코드": "행정동 코드"},
    )
    fig.update_traces(
        marker_line_color="#555555",
        marker_line_width=0.45,
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "행정동 코드: %{customdata[0]}<br>"
            "출동건수: %{z:,}건<extra></extra>"
        ),
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar={"title": "출동건수", "ticksuffix": "건"},
    )
    return fig


st.title("서울 행정동별 출동건수")
st.caption("색이 진한 빨간색일수록 출동건수가 많습니다.")

geojson = load_geojson(str(DATA_PATH))
df = make_dataframe(geojson)

only_mok_dong = st.toggle("목*동만 보기", value=False)
if only_mok_dong:
    df = df[df["행정동명"].str.match(r"^목.*동$", na=False)]
    st.caption(f"목*동 {len(df)}개 행정동을 표시 중입니다.")

st.plotly_chart(build_map(df, geojson), use_container_width=True, config={"scrollZoom": True})
