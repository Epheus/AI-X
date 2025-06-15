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
- 심규호 | kyuho.shim@lge.com
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
자치구 별 부동산 거래금액 분포(Boxplot)
<img src="https://github.com/Epheus/AI-X/blob/main/visualize/Figure_1_2017.jpg" width="600"/>
<br>
<br>
연도별 자치구 별 평균 부동산 거래금액 분포(Barplot)
<img src="https://github.com/Epheus/AI-X/blob/main/visualize/Figure_2_2017.jpg" width="600"/>
연도별 부동산 물건금액(만원)과 각 Feature간 상관관계
<img src="https://github.com/Epheus/AI-X/blob/main/visualize/Figure_3_2017.jpg" width="600"/>
- 토지면적과 건물 면적은 전체적으로는 정비례의 경향이 나타나지만, 특정 부동산 유형에서는 이 관계가 다르게 나타남
 1) 아파트 : 건물면적↑↑, 토지면적↓↓, 건물면적 중심의 가격 결정 특징을 가짐
 2) 오피스텔 : 건물면적↑↑, 토지면적↓, 소형 주거/ 상업지, 건물 중심
 3) 단독/ 다가구 : 건물면적↑, 토지면적↑↑, 토지중심의 자산/ 건물면적 영향이 적음

### 예(강남구) 연도별 평균 금액의 변화 
앞에서 진행한 read_csv.py로 정제된 데이터를 만들고 
final_pt.py를 실행시킬 때 아래와 같이 예로 강남구를 선택해서 진행하면 아래와 같은 연도별 강남구의 평균 건물 각격의 변화를 출력할 수 있다.

![Image](https://github.com/user-attachments/assets/ccc34c2c-8934-4189-b5eb-b50747638300)

데이터 분석을 위해 전체 구에대해 년도별 평균 금액 가격을 나타내보면 아래와 같이 특정 기간(코로나 기간)을 제외하고 증가 추세에 있음을 알 수 있다. 
그러나 자세히 보면 구마다의 특성은 같지 않음을 알 수 있으며, 2025년도에 들어서 안정세로 접어드는 구도 있음을 알 수 있다. 
![Image](https://github.com/user-attachments/assets/688a2b23-d18c-4d00-a337-47085360ef15)


### 참고사항
### 상관도 분석을 통한 특정 구의 집값 예측
내년 집값을 예측할 때 모델을 통한 예측을 할 수도 있지만 상관도 분석을 이용하면 상관성이 높은 구가 올랐다면 내가 고민하는 구의 집값이 오를지 안오를지를 예측할 수 있다. 
예를 들어 양천구의 년도 구간별 상관성을 보면 다음과 같다. 
![Image](https://github.com/user-attachments/assets/415ecb7f-9153-446d-b6c9-aee1c5744603)

목표가 되는 양천구 26년도 집값에 가장 상관성이 높은 곳은 송파구다. 
따라서 송파구가 26년도에 올라갔다면 양천구도 오를 가능성이 높다고 예측할 수 있다. 특정 구 1개로 불안하다면 그도안 높은 상관도를 보였던 다른 구인 도봉구와 은평구를 참조할 수도 있다. 

이러한 방식을 활용하기위한 각 구별 전체 상관도는 다음과 같다. 


## III. Methodology
### 적용 모델 : 
1. 선형회귀 모델
건물용도별로 연도(2017~2025)를 독립변수로, 금액 평균을 종속변수로 회귀 분석
최소 3년 이상 데이터가 있을 경우만 적용
scikit-learn의 LinearRegression 사용

2. LSTM 모델
시계열 모델 기반으로 과거 3년 평균 금액 데이터를 학습하여 다음 해 예측
MinMaxScaler를 활용하여 정규화 후 모델 학습 및 예측
Tensorflow Keras 기반 LSTM 구성
과거 3년 데이터를 시퀀스로 구성하여 1년 후를 예측하는 구조

## IV. Evaluation & Analysis
### 데이터 학습 및 예측 : 

강남구 – 건물용도별 평균 거래금액 추이 및 2026년 예측
아래는 강남구의 다가구주택과 아파트에 대한 예측 결과 그래프입니다.
(각 자치구별 예상 그래프는 Liner Regression 및 LSTM python 파일에서 해당 자치구로 변경하면 결과 확인 가능합니다.)

1. 선형회귀모델 결과 그래프
![선형회귀모델 결과_강남구](https://github.com/user-attachments/assets/3f8cd6e7-92ff-4380-80ea-7d3180edc9ea)

2. LSTM을 통한 결과 그래프
![LSTMfinal결과](https://github.com/user-attachments/assets/e44c3171-ef9f-46fa-922a-87f26d03bae0)

두 모델 모두 지속적인 상승 추세를 보이며, 2026년에도 가격 상승이 예상됨
강남구는 아파트뿐 아니라 다가구주택의 실거래가도 상승세를 보이고 있음
단순 선형회귀와 LSTM의 결과가 유사하여 데이터의 일관성과 모델의 신뢰성 확보
향후 수요 집중 및 개발 영향으로 해당 지역의 부동산 상승 가능성 큼

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
심규호 - 데이터를 바탕으로 2026년 강남구 집값 예측 - 선형회귀모델, LSTM 모델 두가지 분석 결과 도출 


## VI. Conclusion: Discussion
### Conclusion
서울시 전체 자치구 대상으로 LSTM 분석해보니, 개인 노트북으로 불가하여 (시행착오를 반복해야하는데, 한번의 py 파일 실행으로 향후 업데이트가 안됨), 대표적인 강남구로 건축유형별로 2026년 집값 예측함.
향후 Colab등 클라우드 기반 서비스를 이용하여 각 자치구 별 전체 분석도 가능할 것으로 보임. 이번 프로젝트에서는 대표적인 강남구에 대한 결과를 업로드 하였음.

또한 부동산 거래 평균 가격으로 미래 가치를 예측하였기 때문에, 행정구역 변화, 정부 정책, 금리 등 외부 요인을 반영하지 못함
연 단위 평균이기 때문에 계절성/월간 추이는 미반영됨

향후에 정책/금융 변수 포함한 멀티모달 예측 모델 및 Transformer 기반 시계열 예측 모델 도입 검토가 되면 더욱 더 정확한 값을 예측할 수 있을 것 같고,
자치구 간 연관관계 분석 및 클러스터링 가능성 탐색하면 더 발전된 모델로 변모 가능 예상됨

### Discussion
<br>
<br>


## VII. Credits
Dataset searching, Dataset preprocessing, Data visualization, Methodology introduction
Code implementation, Model training and evaluation, Video recording, Write up Github



