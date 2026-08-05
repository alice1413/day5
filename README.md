# 서울 행정동별 출동건수 지도

서울 행정동의 출동건수를 흰색(적음)에서 빨간색(많음)으로 표현하는 Streamlit + Plotly Choropleth 지도입니다.

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

브라우저가 열리면 초기 화면은 서울시청을 중심으로 표시됩니다. 지도 위 행정동에 마우스를 올리면 행정동 코드, 이름, 출동건수를 볼 수 있습니다. 상단의 `목*동만 보기` 토글을 켜면 목1동~목5동만 표시됩니다.

## GitHub 및 Streamlit Community Cloud 배포

1. 이 폴더 전체를 새 GitHub 저장소에 올립니다. `data/dong_emergency_count.geojson`도 반드시 함께 올립니다.
2. [Streamlit Community Cloud](https://share.streamlit.io/)에서 GitHub 저장소를 선택합니다.
3. Main file path에 `app.py`를 지정하고 배포합니다.

지도 바탕은 Plotly의 OpenStreetMap 스타일을 사용하므로 별도의 Mapbox 토큰이 필요하지 않습니다.
