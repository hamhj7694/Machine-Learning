# TMDB 사이트의 영화정보를 기반으로 영화 추천서비스 제작하기

# streamlit 으로 웹앱 제작
# 0.모듈 설치
# 1) pip install streamlit
# 2) pip install tmdbv3api <-- tmdb 영화정보를 쉽게 가져오도록 구현한 모듈 (이걸 안쓰면 open api 수업에 소개했던 방법으로 정보를 가져와야 함)

# 1.모듈 사용을 위해 import
import pickle
import os
import streamlit as st
from tmdbv3api import Movie, TMDb

# 실행 환경에 잘못된 전역 프록시가 설정되어 있어도 TMDB에는 직접 연결합니다.
for _proxy_env in ('NO_PROXY', 'no_proxy'):
    _hosts = [host.strip() for host in os.environ.get(_proxy_env, '').split(',') if host.strip()]
    for _host in ('api.themoviedb.org', 'image.tmdb.org'):
        if _host not in _hosts:
            _hosts.append(_host)
    os.environ[_proxy_env] = ','.join(_hosts)

# 2. TMBD 영화정보를 쉽게가져오기 위한 객체 생성
movie= Movie()
tmdb= TMDb()

# 3. tmdb 의 open api 키를 발급받아 사용
tmdb.api_key= '4704d6d917590acc0fdea33c3505baa7'

# 4. 피클로 저장했던 영화 데이터와 유사도표 가져오기
movies= pickle.load( open('./movies.pickle', 'rb') ) # -- pandas dataframe
cosine_sim= pickle.load( open('./cosine_sim.pickle', 'rb') )  #-- matrix (줄거리 기반)
cosine_sim2= pickle.load( open('./cosine_sim2.pickle', 'rb') )  #-- matrix (영화정보 기반)

#-----------------
# 5. 화면 구성하기
#1) 
st.set_page_config(layout='wide')
#2)
st.title('AIflex')

#3) 영화제목들을 리스트로...사용자가 목록중에 선택할 수 있도록 하기 위해.
movie_list= movies['title'].values

# 영화 데이터 한국어 기준으로...
tmdb.language= 'ko-KR'

#4) 영화제목을 선택할 수 있도록.. 선택박스로 만들고 옵션으로 영화제목리스트를 지정
title= st.selectbox('Choose a movie you like', movie_list)

#7) get_recommendations 만들기
#영화 제목 전달 받아 -> 유사도 점수 상위 10개 영화 추출하고, TMDB에서 포스터 찾아 return
def get_recommendations(title):
    # 전달 받은 영화제목의 인덱스값 얻어오기
    idx= movies[ movies['title']==title ].index[0] #인덱스 달라하면 리스트로 줌

    # 유사도 행렬표 받기(감독, 장르, 키워드 기반)
    sim_scores= enumerate( cosine_sim2[idx] )

    # 유사도 점수 순으로 내림차순
    sim_scores= sorted(sim_scores, key= lambda x:x[1], reverse=True) # (0 인덱스, 1점수)
    
    # 본인 영화는 제외
    sim_scores= sim_scores[1:11] # 1~10

    # 추천된 영화 목록 10개의 인덱스 정보 추출
    movie_indics= [ score[0] for score in sim_scores ] # top10 영화의 인덱스번호들 받아오기

    # 인덱스 정보를 이용하여 영화들의 제목, 이미지 추출
    images= []
    titles= []
    for i in movie_indics:
        #해당 영화의 고유식별번호 id
        id= movies['id'].iloc[i]

        # TMDB 의 여러 정보를 주는 open api 요청 작업을 아주 쉽게 해주는 모듈 Movie 객체 이용
        details= movie.details(id) #영화식별번호를 주고, 해당 영화의 정보를 받아오기

        # 포스터 이미지 받기
        image_path= details['poster_path']
        # 포스터 없는 경우도 있음
        if image_path:
            image_path= 'https://image.tmdb.org/t/p/w500' + image_path
        else:
            image_path= './logo.png' # 포스터 없을 때 보여주기

        images.append(image_path)
        titles.append(details['title'])

    return images, titles

#5) [추천]버튼을 클릭하면 선택한 영화제목과 유사한 영화정보들을 유사도기반으로 추천
if st.button('추천'):
    #6) 추천 버튼 누르면 유사도표와 비교하여 상위 10개 영화제목과 이미지 추출 -- 시간 소요될듯
    with st.spinner('추천 영화를 탐색중입니다...'):
        #영화 이미지, 영화 제목들을 리턴받는 기능함수 만들어서 호출
        images, titles= get_recommendations(title)

        #8) 위 함수 실행 결과 [추천 영화 top 10]의 이미지와 제목 화면에 표시
        idx=0
        for i in range(0,2): # 총 2줄
            cols= st.columns(5) # 5칸씩
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1


#-----------------------------

# streamlit 웹앱의 실행은 run 버튼이 아니라. 터미널에서 streamlit run 파일명
