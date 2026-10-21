# AIflex | Content-based Recommendation Engine

### 영화의 속성과 유사도를 기반으로 추천하는 콘텐츠 기반 영화 추천 웹서비스

> **선택한 영화와 비슷한 영화 10편을 추천하는 개인 프로젝트**입니다. 영화 정보를 바탕으로 사전에 계산한 유사도 행렬을 조회하고, 결과를 TMDB API의 한국어 제목·포스터와 연결해 Streamlit 화면으로 제공합니다.

**개인 프로젝트 · Content-based Recommendation · Similarity Ranking · Streamlit**

### 🌐 [AIflex 배포 서비스 체험하기](https://machine-learning-movies.streamlit.app/) · [상세 Notion 포트폴리오](https://app.notion.com/p/400c753ff28a81b89284e7bbb2b9cc49)

**[💻 웹앱 소스코드](./영화%20추천%20웹%20대쉬보드/webapp.py)** · **[📦 실행 환경](./영화%20추천%20웹%20대쉬보드/requirements.txt)**

---

## 01. 프로젝트 요약

**문제:** 사용자의 평점·구매 기록이 충분하지 않아도, 한 편의 영화를 기준으로 콘텐츠 자체의 특징이 비슷한 영화를 추천할 수 있을까?

**접근:** 영화 정보를 비교 가능한 특징으로 표현하고, 아이템 간 **Cosine Similarity**를 계산해 가장 가까운 영화를 순위화하는 콘텐츠 기반 추천(Content-based Filtering) 방식을 사용했습니다.

**구현 결과:** 추천용 데이터와 유사도 행렬을 불러오는 Python 로직을 Streamlit·TMDB API와 연결해 **영화 선택 → Top 10 추천 → 한국어 제목·포스터 표시**까지 동작하는 웹앱으로 구성했습니다.

| 구분 | 구현 범위 |
|---|---|
| 추천 방식 | 영화 1편 기준 **Item-to-Item** 유사 영화 추천 |
| 추천 결과 | 자기 영화 항목을 제외하는 상위 **10개** 결과 추출 |
| 유사도 데이터 | 사전 계산된 영화정보 기반 `cosine_sim2.pickle` 사용 |
| 사용자 인터페이스 | Streamlit 선택창·추천 버튼·로딩 표시, **5열 × 2행** 결과 |
| 정보 보강 | TMDB API로 **한국어 영화 제목·포스터** 조회 |

## 02. 추천 알고리즘·데이터 흐름

노션 포트폴리오에서 정의한 추천 패턴은 다음과 같습니다.

```text
영화 속성 / Metadata
        ↓
Feature 설계·Vectorization
        ↓
Cosine Similarity 계산
        ↓
Similarity Matrix 저장
        ↓
영화 선택 → 유사도 행 조회 → 내림차순 Ranking
        ↓
자기 항목을 제외한 Top 10 인덱스
        ↓
TMDB API로 제목·포스터 조회
        ↓
Streamlit 추천 결과 출력
```

> **구현 구분:** 현재 공개 저장소에서는 **사전 계산된 Pickle 데이터·유사도 행렬을 불러오는 웹앱**을 확인할 수 있습니다. 앞단의 Feature 추출·벡터화·유사도 행렬 생성은 [Colab 원본 코드](https://colab.research.google.com/drive/1_dM5sWCGHncKf2EzDhgZ79ZbMIGfYe-4)에서 확인할 수 있으며, 이 공개 저장소에는 배포용 Runtime과 사전 생성 아티팩트를 둡니다.

### 실제 웹앱의 추천 흐름

1. `movies['title']`로 선택 목록을 만들고, 선택한 제목의 영화 인덱스를 찾습니다.
2. `cosine_sim2[idx]`의 후보 유사도 점수를 내림차순으로 정렬합니다.
3. 정렬 결과의 `[1:11]`을 추출하여 추천 후보 10개를 얻습니다.
4. 영화의 `id`를 이용해 TMDB 상세 정보를 조회하고 제목·포스터를 구성합니다.
5. 추천 결과를 Streamlit의 **5 × 2 그리드**에 표시합니다.

현재 코드는 선택한 영화 자신이 정렬 결과 첫 번째에 있다는 전제에서 `[1:11]`로 제외합니다. 동점 등의 경우를 견고하게 처리하려면 선택 영화 인덱스를 **명시적으로 필터링**하는 개선이 필요합니다.

## 03. 데이터 아티팩트와 적용 모델

| 파일 | 역할 | 현재 웹앱 사용 |
|---|---|---|
| `movies.pickle` | 영화 제목·ID 등을 담은 DataFrame | 사용 |
| `cosine_sim.pickle` | 줄거리 기반 유사도 행렬 | 로드하지만 추천에는 사용하지 않음 |
| `cosine_sim2.pickle` | 영화정보 기반 유사도 행렬 | **실제 추천 순위 계산에 사용** |

세 파일은 **Git LFS**로 관리합니다. GitHub 파일 화면에 표시되는 짧은 텍스트는 실데이터가 아닌 LFS 포인터이며, 로컬 실행 시 실제 아티팩트를 내려받아야 합니다.

이 방식은 새 입력마다 모델을 학습하는 것이 아니라 **사전 계산된 유사도 행렬에서 추천 순위를 조회하는 구조**입니다. LLM이나 딥러닝 생성 모델이 추천 결과를 생성하는 방식은 아닙니다.

## 04. 웹 애플리케이션

```text
사용자: 영화 선택 및 '추천' 클릭
          ↓
Streamlit → get_recommendations(title)
          ↓
영화 ID · cosine_sim2 → 상위 10개 추천
          ↓
TMDB API (ko-KR)
          ↓
한국어 제목 · 포스터 이미지
          ↓
Streamlit UI (5개씩 2줄)
```

- **입력:** `st.selectbox`, `st.button`
- **처리 중 표시:** `st.spinner`
- **외부 정보:** TMDB의 영화 상세 정보·포스터 경로 이용
- **예외 표시:** 포스터가 없을 때 `logo.png` 사용
- **배포:** Streamlit Community Cloud 서비스 URL을 통한 체험 링크 제공

## 05. 기술 스택 및 역할

| 구분 | 기술·내용 |
|---|---|
| Recommendation | Content-based Filtering · Cosine Similarity · Top-N Ranking |
| 데이터 처리·저장 | Python · Pandas DataFrame · Pickle · Git LFS |
| Web UI | Streamlit |
| 외부 API | TMDB · `tmdbv3api` |
| 개발 의존성 | `scikit-learn` (requirements에 포함, 현재 웹앱은 사전 계산 행렬을 사용) |
| 역할 | 개인 프로젝트: 영화 추천 서비스 구성·추천 로직 연결·웹앱 구현 및 배포 |

**프로젝트 핵심:** 추천 알고리즘의 결과를 웹에서 실제로 사용할 수 있도록 **데이터 아티팩트 로딩 → 유사도 Ranking → 외부 API → 사용자 화면**까지 연결한 경험입니다.

## 06. 로컬 실행

Python 환경, TMDB API 키, Git LFS 아티팩트가 필요합니다.

```bash
git clone https://github.com/hamhj7694/Machine-Learning.git
cd Machine-Learning

git lfs install
git lfs pull

pip install -r requirements.txt
streamlit run app.py
```

TMDB API 키는 환경변수 `TMDB_API_KEY` 또는 Streamlit Secrets에 설정합니다. 코드에 키를 직접 기록하지 않습니다.

- Streamlit Secrets: `.streamlit/secrets.toml`에 `TMDB_API_KEY` 설정
- 공개 저장소에 API 키 파일·환경변수 파일을 업로드하지 않도록 주의
- Git LFS 아티팩트가 내려받아지지 않거나 TMDB 요청이 실패하면 추천 결과 표시가 정상 동작하지 않을 수 있음

## 07. 구현 범위·평가 기준·개선 방향

**현재 코드로 확인되는 구현:** 영화 선택, 사전 계산된 유사도 행렬 기반 Top 10 조회, TMDB 한국어 제목·포스터 연동, Streamlit 화면 표시.

**모델링 코드 근거:** 추천 피처 구성과 유사도 행렬 계산은 [Google Colab 원본 노트북](https://colab.research.google.com/drive/1_dM5sWCGHncKf2EzDhgZ79ZbMIGfYe-4)에서 확인할 수 있습니다. 배포 저장소에서는 생성된 아티팩트를 불러와 사용합니다.\n\n**추가 검증이 필요한 부분:** 추천 모델링의 재현 가능한 아티팩트 생성·버전 관리, 추천 품질 평가(예: 사용자 선호도·정답 데이터 기반 지표), 새로운 데이터에 대한 재학습·아티팩트 재생성 절차. **추천 정확도나 정량적인 성능 개선 수치는 별도로 측정하지 않았으므로 기재하지 않았습니다.**

**확장 가능한 방향:** 동일한 Feature 설계 → 유사도 → Ranking → Top-N 구조를 음료·메뉴·상품·선물 등 다른 콘텐츠로 전환할 수 있습니다. 다만 **현재 실제 구현·배포된 도메인은 영화 추천**이며, 다른 도메인의 추천 서비스가 이미 완성되었다는 의미는 아닙니다.

---

### 관련 링크

- **[🌐 AIflex 배포 서비스](https://machine-learning-movies.streamlit.app/)**
- **[📖 Notion 상세 포트폴리오](https://app.notion.com/p/400c753ff28a81b89284e7bbb2b9cc49)**
- **[💻 Streamlit 웹앱 구현](./영화%20추천%20웹%20대쉬보드/webapp.py)**

*TMDB API는 영화 제목·포스터 등 정보 제공에 활용되며, 유사도 기반 추천 순위는 프로젝트의 추천 아티팩트로 계산합니다.*
