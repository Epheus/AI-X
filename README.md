# AI-X
# 서울시 부동산 실거래가 정보를 활용한 26년도 집값 예측
<br>

발표 동영상 링크
https://
<br>
<br>

## 목차
1. [Members](#members)
2. [Proposal](#i-proposal)
3. [Datasets](#ii-datasets)
4. [Methodology](#iii-methodology)
5. [Evaluation & Analysis](#iv-evaluation--analysis)
6. [Related Work](#v-related-work)
7. [Conclusion](#vi-conclusion-discussion)
8. [Credits](#vii-credits)
<br>
<br>


## Members
- 최가형 | kahyung.choi@lge.com
- 유준석 | alex.you@lge.com
- 심규호 | yuho.shim@lge.com
<br>
<br>


## I. Proposal
### Motivation
서울시는 인구 밀도, 교통, 교육, 정책 등 다양한 요인이 복합적으로 작용하는 부동산 시장을 갖고 있으며, 가격 변동성과 수요 예측의 불확실성이 큰 지역입니다. 
특히 최근 몇 년간의 급격한 가격 상승과 정부 정책 변화는 시민들의 주거 안정성과 관련된 불안 요인을 가중시키고 있습니다.
정확한 집값 예측은 개인의 내 집 마련 의사결정뿐 아니라, 정부의 정책 수립, 부동산 세제 조정, 공급 계획 수립 등 공공 행정 전반에도 중대한 영향을 미칩니다.
행정적・경제적 의사결정의 핵심 도구로서, 신뢰할 수 있는 공공데이터 기반의 집값 예측 모델의 필요성은 점점 증대되고 있습니다.
<br>
<br>


### Goal
- 본 프로젝트는 서울시의 부동산 실거래가 공공데이터(출처 : 서울 열린데이터 광장)를 기반으로, 특정 지역의 주택 가격 상승/ 하강을 예측하는 모델을 구축하는 것을 목표로 합니다.
- 이를 위해 거래 시점, 위치, 면적, 층수, 건물 노후도, 건물정보 등 공공데이터의 다양한 요소 특성을 반영하고, 관련 변수의 상관성을 분석하는 것으로 향후 집 값의 변화를 예측 해보려고 합니다.
- 궁극적으로는 서울시 부동산 시장의 동태를 정량적으로 파악하고, 미래를 예측 가능한 형태로 제시하는 것이 본 과제의 핵심 목적입니다.
<br>


### 서울시 집 값에 대하여...
서울시 집값은 서울 지역 내 부동산, 주로 아파트의 매매 가격을 의미합니다. 
특히 서울시의 아파트 가격은 시장의 주요 지표 중 하나이며, 그 추이를 통해 부동산 시장의 건강 상태를 파악할 수 있습니다. 
서울시 집값은 다양한 요인에 의해 영향을 받으며, 최근에는 정부 정책, 금리 변동, 경제 상황, 그리고 신축 아파트 공급량 등이 주요 변수로 작용하고 있습니다.

- 최근 추이 :
최근 서울시 아파트 가격은 2021년 이후 2022년과 2023년 연속 하락했지만, 2024년 3월부터 꾸준히 상승세를 보이고 있습니다. 

- 평균 가격 :
2025년 1월 기준 서울 아파트 평균 가격은 13억 8천 289만원으로, 이전 최고점을 넘어섰습니다. 

- 상위권 아파트 :
서울 상위 20% 아파트의 평균 매매가격은 30억 942만원으로, 처음 30억원을 돌파했습니다. 

- 정부 정책 :
정부의 부동산 관련 정책은 집값에 영향을 미치며, 규제 완화, 금리 조정, 공급 확대 등의 정책이 서울시 집값에 영향을 미칩니다. 

- 금리 변동 :
금리 인하 또는 인상은 대출 금리를 영향을 미치며, 이는 수요를 변화시켜 서울시 집값에 영향을 미칠 수 있습니다. 

- 참고 : 서울시 집값은 다양한 요인에 의해 복잡하게 영향을 받으며, 단일 요인만으로는 전체적인 시장 상황을 파악하기 어렵습니다. 따라서 서울시 집값 관련 자료를 다각도로 분석하고, 부동산 시장 전문가의 의견도 참고하는 것이 좋습니다.
[출처 : Google AI Searching - https://www.google.com/search?q=%EC%84%9C%EC%9A%B8%EC%8B%9C+%EC%A7%91%EA%B0%92+%EC%9D%B4%EB%9E%80&sca_esv=cf6290cf059c5086&sxsrf=AE3TifMjDumFLPRwJ4Dvg7rLZmNJW1x3VQ%3A1748947104481&source=hp&ei=oNA-aK-qG5bf2roP15KrwQ8&iflsig=AOw8s4IAAAAAaD7esIXsHFmAba93I_9YST1FVAGIpc6v&ved=0ahUKEwiv-pDXh9WNAxWWr1YBHVfJKvgQ4dUDCCs&uact=5&oq=%EC%84%9C%EC%9A%B8%EC%8B%9C+%EC%A7%91%EA%B0%92+%EC%9D%B4%EB%9E%80&gs_lp=Egdnd3Mtd2l6IhfshJzsmrjsi5wg7KeR6rCSIOydtOuegDIFECEYoAEyBRAhGKABMgUQIRigAUi8GFAAWMwXcAN4AJABA5gBjwGgAaYTqgEEMC4yMLgBA8gBAPgBAZgCDKAC3gjCAgQQABgDwgILEC4YgAQYsQMYgwHCAgsQABiABBixAxiDAcICBBAuGAPCAgUQABiABMICCBAAGIAEGLEDwgIFEC4YgATCAggQLhiABBixA8ICCxAuGIAEGNEDGMcBwgIOEC4YgAQYsQMYxwEYrwHCAgsQLhiABBjHARivAcICChAuGAMYxwEYrwHCAggQABiABBiiBMICBRAAGO8FwgIEEAAYHsICBhAAGAgYHpgDAJIHAzMuOaAHrZsBsgcDMC45uAfUCMIHBzIuOS4wLjHIBxw&sclient=gws-wiz]
<br>
<br>


## II. Datasets
### Datasets
* 데이터셋 링크
```
서울 열린데이터 광장 : [https://data.seoul.go.kr]
서울 열린데이터 광장 공공데이터 : https://data.seoul.go.kr/dataList/datasetList.do
서울시 부동산 실거래가 정보 : 2017년도 부터 2025년도 정보 활용 (코로나 이전 시기 데이터 포함)
```
<img src="https://github.com/user-attachments/assets/7031e130-3354-4560-a141-fc5af3470f2d" width="600"/>
<br>
<br>


#### 1. 환경 설정
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
.\venv\Scripts\activate  # Windows

# 필요한 패키지 설치
pip install pandas
pip install matplotlib
pip install seaborn
```

#### 2. 데이터 준비
- `datasets` 디렉토리에 CSV 파일을 위치시킵니다.
- 파일명 형식: `서울시 부동산 실거래가 정보_YYYY.csv`

#### 3. 스크립트 실행
```bash
python read_csv.py
```
#### 4. 실행 결과 예시 (아래와 같이 결측치가 없는지를 확인한다.)
스크립트 실행 후 다음과 같은 결과를 확인할 수 있습니다:

```
=== 정제 후 데이터 분석 ===

=== 결측치 분석 ===

각 컬럼별 결측치 개수:
접수연도        0
자치구코드       0
자치구명        0
법정동코드       0
법정동명        0
지번구분        0
지번구분명       0
본번          0
부번          0
건물명         0
계약일         0
물건금액(만원)    0
건물면적(㎡)     0
토지면적(㎡)     0
층           0
건축년도        0
건물용도        0

각 컬럼별 결측치 비율:
접수연도        0.0
자치구코드       0.0
자치구명        0.0
법정동코드       0.0
법정동명        0.0
지번구분        0.0
지번구분명       0.0
본번          0.0
부번          0.0
건물명         0.0
계약일         0.0
물건금액(만원)    0.0
건물면적(㎡)     0.0
토지면적(㎡)     0.0
층           0.0
건축년도        0.0
건물용도        0.0
```

#### 5. 최종결과
read_csv.py가 실행되면 datasets 밑에는 년도.csv 파일이 생성되고 해당 파일은 결측치가 없는 정제된 데이터이다. 
따라서 해당 파일로 부동산 예측을 진행하면 된다. 


#### 참고사항: 데이터 정제 기준되는 칼럼과 불필요한 칼럼을 설정할 수 있다. 
- 기준 컬럼: 지번구분, 토지면적(㎡), 층, 건물용도, 건축년도, 본번, 부번, 자치구명
- 제거되는 컬럼: 취소일, 권리구분, 신고구분, 신고한 개업공인중개사 시군구명

#### 주의사항
- CSV 파일은 cp949 인코딩을 사용합니다 (한글 지원)
- 데이터 파일은 반드시 `datasets` 디렉토리에 위치해야 합니다
<br>
<br>


### 데이터 시각화
```
![2017년 서울시 자치구별 부동산 거래 건수](https://private-user-images.githubusercontent.com/59636924/449779945-100e70b6-9814-4e2d-9344-b9f060b4c7ff.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDg3OTAxNDUsIm5iZiI6MTc0ODc4OTg0NSwicGF0aCI6Ii81OTYzNjkyNC80NDk3Nzk5NDUtMTAwZTcwYjYtOTgxNC00ZTJkLTkzNDQtYjlmMDYwYjRjN2ZmLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA2MDElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwNjAxVDE0NTcyNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWY1YjZiZDkzOTkwYjMzMjQ5NjlkOWExZGFkNTY0MTlkNjE0ZjYxNGZlNzYxOWI3MDhjYTM3MjA1ZDhiZWZhNjYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.ED7h67ZLy-4V3QtUbBDzhHiL3KqI3t2htnAxog1mLbc)
```
<img src="https://github.com/user-attachments/assets/5a980472-e621-46fc-8dae-cdcd24759cc5" width="600"/>
<br>
<br>

### 예(강남구) 연도별 평균 금액의 변화 
앞에서 진행한 read_csv.py로 정제된 데이터를 만들고 
final_pt.py를 실행시킬 때 아래와 같이 예로 강남구를 선택해서 진행하면 아래와 같은 연도별 강남구의 평균 건물 각격의 변화를 출력할 수 있다.

![Image](https://github.com/user-attachments/assets/ccc34c2c-8934-4189-b5eb-b50747638300)

데이터 분석을 위해 전체 구에대해 년도별 평균 금액 가격을 나타내보면 아래와 같이 특정 기간(코로나 기간)을 제외하고 증가 추세에 있음을 알 수 있다. 
그러나 자세히 보면 국 구마다의 특성은 같지 않음을 알 수 있으며, 2025년도에 들어서 안정세로 접어드는 구도 있음을 알 수 있다. 
![Image](https://github.com/user-attachments/assets/688a2b23-d18c-4d00-a337-47085360ef15)


## III. Methodology
### 적용 모델 : 
<br>
[description]
<br>
<br>


## IV. Evaluation & Analysis
### 데이터 학습 및 검증 : 
``` python

```
<br>

### 모델 사용한 예측 수행 : 
``` python

```
<br>
<br>


## V. Related Work 
<br>
* Reference A
  - https://
<br>
<br>  
* Reference A
  - https://
<br>
<br>


## VI. Conclusion: Discussion
### Conclusion
<br>


### Discussion
<br>
<br>


## VII. Credits
Dataset searching, Dataset preprocessing, Data visualization, Methodology introduction
Code implementation, Model training and evaluation, Video recording, Write up Github



