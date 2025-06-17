# AI-X
# 서울시 부동산 실거래가 정보를 활용한 26년도 집값 예측
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
```bash
df_2017_cleaned = preprocess_data_and_save(2017)
df_2018_cleaned = preprocess_data_and_save(2018)
df_2019_cleaned = preprocess_data_and_save(2019)
df_2020_cleaned = preprocess_data_and_save(2020)
df_2021_cleaned = preprocess_data_and_save(2021)
df_2022_cleaned = preprocess_data_and_save(2022)
df_2023_cleaned = preprocess_data_and_save(2023)
df_2024_cleaned = preprocess_data_and_save(2024)
df_2025_cleaned = preprocess_data_and_save(2025)
```

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
- 전처리된 csv 파일들을 `datasets` 디렉토리에 위치시킵니다.
- 파일명 형식: `YYYY.csv` (정제된 데이터)
- visualize.py에서 데이터 시각화를 통하여 결과 값과 각 Feature들간의 경향성 및 상관관계를 확인

```bash
def visualize_gu_prices(df_cleaned, year):
    if '자치구명' not in df_cleaned.columns or '물건금액(만원)' not in df_cleaned.columns:
        print(f"[경고] {year}년 데이터에 필수 컬럼 없음")
        return

    ordered_gu = df_cleaned.groupby('자치구명')['물건금액(만원)'].mean().sort_values(ascending=False).index



    # 1) Boxplot 시각화 : 25개 자치구 별 집 값 가격의 분포
    ordered_gu = df_cleaned.groupby('자치구명')['물건금액(만원)'].mean().sort_values(ascending=False).index

    plt.figure(figsize=(14, 6))
    sns.boxplot(x='자치구명', y='물건금액(만원)', data=df_cleaned, order=ordered_gu)
    plt.title(f'{year}년 자치구 별 부동산 거래금액 분포', fontsize=12)
    plt.xticks(rotation=90)
    formatter = FuncFormatter(lambda x, _: f'{int(x / 1000)}k')
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f'Figure_1_{year}.jpg'))
    plt.close()
```
자치구 별 부동산 거래금액 분포(Boxplot)
<br>
![image](https://github.com/user-attachments/assets/7483187c-67ea-48c5-b46b-17ddf0835b5d)
<br>
<br>
연도별 자치구 별 평균 부동산 거래금액 분포(Barplot)
<br>
```bash
    # 2) Barplot 시각화 : 25개 자치구 별 평균 부동산 거래금액 분포
    sns.barplot(x='자치구명', y='물건금액(만원)', data=df_cleaned,
                estimator='mean',
                order=df_cleaned.groupby('자치구명')['물건금액(만원)'].mean().sort_values(ascending=False).index)
    plt.title(f'{year}년 자치구 별 평균 부동산 거래금액 분포', fontsize=12)
    plt.xticks(rotation=90)
    formatter = FuncFormatter(lambda x, _: f'{int(x / 1000)}k')
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f'Figure_2_{year}.jpg'))
    plt.close()
```
![image](https://github.com/user-attachments/assets/0f2b78e6-231a-4619-9dd9-b4ffa8d9c4f9)
<br>
<br>
연도별 부동산 물건금액(만원)과 각 Feature간 상관관계(Heatmap)
<br>
- 거래 금액(만원)과 각 Feature들의 상관관계 확인을 위해 수치형 컬럼과 문자형 컬럼을 결합하여 Heatmap 시각화(One-hot Encoding)
```bash
def visualize_correlation(df_cleaned, year):
    # 문자형 컬럼 중 고유값 100개 이하인 것만 추출
    non_numeric_cols = df_cleaned.select_dtypes(include='object').columns
    target_cat_cols = [col for col in non_numeric_cols if df_cleaned[col].nunique() <= 100]

    # One-hot encoding
    df_dummies = pd.get_dummies(df_cleaned[target_cat_cols], drop_first=False)

    # 수치형 feature 추출
    numeric_cols = df_cleaned.select_dtypes(include=['int64', 'float64']).drop(columns=['물건금액(만원)'], errors='ignore')

    # 결합 후 상관계수 계산
    df_corr_input = pd.concat([df_cleaned[['물건금액(만원)']], numeric_cols, df_dummies], axis=1)
    corr = df_corr_input.corr()['물건금액(만원)'].drop('물건금액(만원)').sort_values(ascending=False)

    # 3) Heatmap 시각화 : [물건금액] 컬럼에 대한 전체 feature들의 상관관계 히트맵
    # 상위 40개 히트맵 시각화
    plt.figure(figsize=(6, 10))
    sns.heatmap(corr.head(40).to_frame(), annot=True, cmap='coolwarm', fmt='.3f')
    plt.title(f'{year}년 물건금액(만원)과 Feature 상관관계 (Top 40)')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f'Figure_3_{year}.jpg'))
    plt.close()
```
<br>
![image](https://github.com/user-attachments/assets/dcce63ab-5ba4-4321-b194-7a90754db63a)
<br>
- 토지면적과 건물 면적은 전체적으로는 정비례의 경향이 나타나지만, 특정 부동산 유형에서는 이 관계가 다르게 나타남
 1) 아파트 : 건물면적↑↑, 토지면적↓↓, 건물면적 중심의 가격 결정 특징을 가짐
 2) 오피스텔 : 건물면적↑↑, 토지면적↓, 소형 주거/ 상업지, 건물 중심
 3) 단독/ 다가구 : 건물면적↑, 토지면적↑↑, 토지중심의 자산/ 건물면적 영향이 적음
<br>
<br>

### 참고사항
### 상관도 분석을 통한 특정 구의 집값 예측
내년 집값을 예측할 때 모델을 통한 예측을 할 수도 있지만 다른 구의 데이터를 활용하여 예측할 수도 있다고 생각된다. 
이를 위해 몇가지 데이터의 특징살펴보면, 
우선, 강남구와 양천구의 연도별 평균 금액의 변화 그래프에서 데이터의 특징은 코로나 기간(2019-2022) 이전과 이후로 나타나고 있는 것을 알 수 있다. 

#### 예(강남구, 양천구) 연도별 평균 금액의 변화 
- 전처리된 csv 파일들을 `datasets` 디렉토리에 위치시킵니다.
- 파일명 형식: `YYYY.csv` (정제된 데이터)
- final_pt.py를 실행시킬 때 아래와 같이 예로 강남구, 양천구를 선택해서 진행하면 아래와 같은 연도별 강남구의 평균 건물 각격의 변화를 출력할 수 있다.


![Image](https://github.com/user-attachments/assets/ccc34c2c-8934-4189-b5eb-b50747638300)
![image](https://github.com/user-attachments/assets/25ef2f8f-996e-4c8f-afb7-5d106a757dea)
<br>

또한, 데이터 분석을 위해 전체 구에대해 년도별 평균 금액 가격을 나타내보면 모든 구가 동일 추세이지 않고 유사한 추세가 있는 구의 그룹이 있음을 알 수 있다. 

![Image](https://github.com/user-attachments/assets/688a2b23-d18c-4d00-a337-47085360ef15)
<br>
<br>

따라서 특정 구의 오름세는 상관도가 높은 구의 그룹으로 나눌 수 있다고 판단되며, 이를 활용하면 내가 고민하는 구가 오를지 안오를지를 가장 상관성이 높았던 구의 추세를 통해 예측할 수 있게 된다.
예를 들어 양천구의 년도 구간별 상관성을 보면 다음과 같다. 검은색 첫 열은 각 년도 구간별로 선택된 구의 최고 상관도를 나타냈던 구이고
그 밑줄은 최고 상관도로 선택되었던 구가 해당 년도에 어떤 상관도 값을 가졌었는지 나타낸 것이다. 


```bash
def find_highest_correlation_gu(correlation_matrix, gu_name):
    """
    특정 구에 대한 최고 상관관계를 찾는 함수
    
    Parameters:
    correlation_matrix: 상관관계 행렬
    gu_name (str): 분석할 구 이름
    """
    # 구 이름 리스트 생성
    gu_list = sorted(common_gu)
    
    # 해당 구의 인덱스 찾기
    gu_idx = gu_list.index(gu_name)
    
    # 해당 구의 상관관계 값들 추출
    correlations = correlation_matrix[gu_idx].copy()
    
    # 자기 자신과의 상관관계는 제외 (1.0)
    correlations[gu_idx] = 0
    
    # 최고 상관관계 값과 인덱스 찾기
    max_corr_idx = np.argmax(np.abs(correlations))
    max_corr = correlations[max_corr_idx]
    
    return gu_list[max_corr_idx], max_corr

def find_correlation_between_gu(correlation_matrix, gu1_name, gu2_name):
    """
    두 구 간의 상관관계를 찾는 함수
    
    Parameters:
    correlation_matrix: 상관관계 행렬
    gu1_name (str): 첫 번째 구 이름
    gu2_name (str): 두 번째 구 이름
    """
    # 구 이름 리스트 생성
    gu_list = sorted(common_gu)
    
    # 각 구의 인덱스 찾기
    gu1_idx = gu_list.index(gu1_name)
    gu2_idx = gu_list.index(gu2_name)
    
    # 두 구 간의 상관관계 값 찾기
    correlation = correlation_matrix[gu1_idx][gu2_idx]
    
    return correlation
```
![Image](https://github.com/user-attachments/assets/415ecb7f-9153-446d-b6c9-aee1c5744603)
<br>

목표가 되는 양천구 26년도 집값에 가장 상관성이 높은 곳은 송파구다. 
따라서 송파구가 26년도에 올라갔다면 양천구도 오를 가능성이 높다고 예측할 수 있는 것이다. 또한 특정 구 1개로 불안하다면 그동안 높은 상관도를 보였던 다른 구인 도봉구와 은평구를 참조할 수도 있다. 

이러한 방식을 활용하기위한 각 구별 전체 상관도는 다음과 같다. 
<br>
```bash
def visualize_all_gu_correlations(correlation_matrices, matrix_info):
    """
    모든 구의 상관관계 체인을 2열로 나열하여 표시하는 함수
    
    Parameters:
    correlation_matrices: [2022-2025, 2019-2022, 2017-2019] 순서의 상관관계 행렬 리스트
    matrix_info: 각 행렬의 기간 정보
    """
    # 구 목록 가져오기
    gu_list = sorted(common_gu)
    
    # 행과 열 계산
    n_gus = len(gu_list)
    n_cols = 2
    n_rows = (n_gus + 1) // 2  # 올림 나눗셈
    
    # 전체 그래프 크기 설정
    plt.figure(figsize=(20, 5 * n_rows))
    
    # 각 구에 대한 상관관계 체인 그리기
    for idx, gu in enumerate(gu_list):
        # 서브플롯 위치 계산
        row = idx // n_cols
        col = idx % n_cols
        ax = plt.subplot(n_rows, n_cols, idx + 1)
        
        # 각 기간별 최고 상관관계 구 찾기
        correlations = []
        highest_corr_gus = []
        
        for matrix in correlation_matrices:
            highest_gu, corr = find_highest_correlation_gu(matrix, gu)
            highest_corr_gus.append(highest_gu)
            correlations.append(corr)
        
        # 동그라미와 선 그리기
        circle_radius = 0.4
        spacing = 3
        
        for i in range(4):  # 4개의 동그라미 (시작 구 + 3개 기간)
            # 동그라미 그리기
            circle = plt.Circle((i * spacing, 0), circle_radius, fill=False, color='black')
            ax.add_patch(circle)
            
            # 구 이름과 상관계수 표시
            if i == 0:
                text = gu
            else:
                text = f"{matrix_info[i-1]}\n{highest_corr_gus[i-1]}\n({correlations[i-1]:.3f})"
            
            ax.text(i * spacing, 0, text, ha='center', va='center', fontsize=8)
            
            # 선 그리기 (마지막 동그라미 전까지만)
            if i < 3:
                ax.plot([i * spacing + circle_radius, (i+1) * spacing - circle_radius], 
                       [0, 0], 'k-')
        
        # 서브플롯 설정
        ax.set_xlim(-1, 12)  # x축 범위 설정
        ax.set_ylim(-1, 1)   # y축 범위 설정
        ax.axis('off')
        ax.set_title(f'{gu}의 상관관계 체인', fontsize=10)
    
    plt.tight_layout()
    plt.show()
```
![Image](https://github.com/user-attachments/assets/b14f4b64-8f53-4a0e-95d6-36ba7578c396)
<br>
<br>

위의 그림을 통해 사용자는 자신이 관심있는 구의 26년 오름세를 예측하기 위해 상관도가 높은 구의 오름세 변화를 보면서 자신의 판단에 도움을 얻을 수 있다. 

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
```bash
def predict_2026(grouped):
    result = []
    gu_list = grouped["자치구"].unique()

    for gu in gu_list:
        gu_df = grouped[grouped["자치구"] == gu]

        for usage in gu_df["건물용도"].unique():
            data = gu_df[gu_df["건물용도"] == usage]

            if len(data) >= 3:
                X = data["연도"].values.reshape(-1, 1)
                y = data["금액"].values
                model = LinearRegression()
                model.fit(X, y)

                pred_2026 = model.predict([[2026]])[0]
                result.append({"자치구": gu, "건물용도": usage, "2026예측금액": round(pred_2026, 2)})

    return pd.DataFrame(result)


def plot_gu_predictions(grouped, pred_df, target_gu):
    plt.figure(figsize=(10, 6))

    gu_data = grouped[grouped["자치구"] == target_gu]
    pred_data = pred_df[pred_df["자치구"] == target_gu]

    # 건물용도별 선 색상을 고정하기 위해 컬러맵 생성
    usage_list = gu_data["건물용도"].unique()
    colors = plt.cm.get_cmap('tab10', len(usage_list))
    color_dict = {usage: colors(i) for i, usage in enumerate(usage_list)}

    for usage in usage_list:
        usage_data = gu_data[gu_data["건물용도"] == usage]
        color = color_dict[usage]

        # 실거래 데이터 선 그래프
        plt.plot(usage_data["연도"], usage_data["금액"], marker="o", label=f"{usage} (실거래)", color=color)

        # 2026년 예측값 가져오기
        pred_val = pred_data[pred_data["건물용도"] == usage]["2026예측금액"]
        if not pred_val.empty:
            y_pred = pred_val.values[0]

            # 2025년 실제 데이터의 마지막 값과 2026년 예측값 연결 (점선)
            last_year = usage_data["연도"].max()
            last_val = usage_data[usage_data["연도"] == last_year]["금액"].values[0]
            plt.plot([last_year, 2026], [last_val, y_pred], linestyle="--", color=color)

            # 2026년 예측값 점 찍기 (실거래 선 색과 동일)
            plt.scatter(2026, y_pred, color=color, edgecolor='black', zorder=5, s=80, label=f"{usage} (예측)")

    plt.title(f"{target_gu} - 건물용도별 2026년 평균 집값 예측")
    plt.xlabel("연도")
    plt.ylabel("평균 금액 (만원)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
```

![선형회귀모델 결과_강남구](https://github.com/user-attachments/assets/3f8cd6e7-92ff-4380-80ea-7d3180edc9ea)

2. LSTM을 통한 결과 그래프
```bash
# LSTM 모델
def train_lstm_model(X_train, y_train):
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(X_train.shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=100, verbose=0)
    return model

# 시퀀스 생성 함수
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

# 예측 (정규화 포함)
def predict_2026_lstm(grouped):
    result = []
    gu_list = grouped["자치구"].unique()
    for gu in gu_list:
        gu_df = grouped[grouped["자치구"] == gu]
        for usage in gu_df["건물용도"].unique():
            data = gu_df[gu_df["건물용도"] == usage].sort_values("연도")
            prices = data["금액"].values.reshape(-1, 1)

            if len(prices) >= 4:
                scaler = MinMaxScaler()
                scaled_prices = scaler.fit_transform(prices).flatten()

                X, y = create_sequences(scaled_prices, seq_length=3)
                X = X.reshape((X.shape[0], X.shape[1], 1))

                model = train_lstm_model(X, y)

                last_seq = scaled_prices[-3:].reshape((1, 3, 1))
                pred_scaled = model.predict(last_seq, verbose=0)[0][0]

                pred_2026 = scaler.inverse_transform([[pred_scaled]])[0][0]

                result.append({"자치구": gu, "건물용도": usage, "2026예측금액": round(pred_2026, 2)})
    return pd.DataFrame(result)

# 시각화
def plot_gu_predictions(grouped, pred_df, target_gu):
    plt.figure(figsize=(10, 6))
    gu_data = grouped[grouped["자치구"] == target_gu]
    pred_data = pred_df[pred_df["자치구"] == target_gu]

    usage_list = gu_data["건물용도"].unique()
    colors = plt.cm.get_cmap('tab10', len(usage_list))
    color_dict = {usage: colors(i) for i, usage in enumerate(usage_list)}

    for usage in usage_list:
        usage_data = gu_data[gu_data["건물용도"] == usage]
        color = color_dict[usage]

        plt.plot(usage_data["연도"], usage_data["금액"], marker="o", label=f"{usage} (실거래)", color=color)

        pred_val = pred_data[pred_data["건물용도"] == usage]["2026예측금액"]
        if not pred_val.empty:
            y_pred = pred_val.values[0]
            last_year = usage_data["연도"].max()
            last_val = usage_data[usage_data["연도"] == last_year]["금액"].values[0]
            plt.plot([last_year, 2026], [last_val, y_pred], linestyle="--", color=color)
            plt.scatter(2026, y_pred, color=color, edgecolor='black', zorder=5, s=80, label=f"{usage} (예측)")

    plt.title(f"{target_gu} - 건물용도별 2026년 평균 집값 예측 (LSTM)")
    plt.xlabel("연도")
    plt.ylabel("평균 금액 (만원)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
```

![LSTMfinal결과](https://github.com/user-attachments/assets/e44c3171-ef9f-46fa-922a-87f26d03bae0)

두 모델 모두 지속적인 상승 추세를 보이며, 2026년에도 가격 상승이 예상됨
강남구는 아파트뿐 아니라 다가구주택의 실거래가도 상승세를 보이고 있음
단순 선형회귀와 LSTM의 결과가 유사하여 데이터의 일관성과 모델의 신뢰성 확보
향후 수요 집중 및 개발 영향으로 해당 지역의 부동산 상승 가능성 큼

## V. Related Work 
<br>
* Reference 선형회귀모델
<br>
  https://ko.wikipedia.org/wiki/%EC%84%A0%ED%98%95_%ED%9A%8C%EA%B7%80

<br>  
* Reference LSTM 모델
<br>
  https://en.wikipedia.org/wiki/Long_short-term_memory
<br>
<br>



## VI. Conclusion: Discussion
### Conclusion & Discussion
서울시 전체 자치구 대상으로 LSTM 분석해보니, 개인 노트북으로 불가하여 (시행착오를 반복해야하는데, 한번의 py 파일 실행으로 향후 업데이트가 안됨), 대표적인 강남구로 건축유형별로 2026년 집값 예측함.
향후 Colab등 클라우드 기반 서비스를 이용하여 각 자치구 별 전체 분석도 가능할 것으로 보임. 이번 프로젝트에서는 대표적인 강남구에 대한 결과를 업로드 하였음.

또한 부동산 거래 평균 가격으로 미래 가치를 예측하였기 때문에, 행정구역 변화, 정부 정책, 금리 등 외부 요인을 반영하지 못함
연 단위 평균이기 때문에 계절성/월간 추이는 미반영됨

향후에 정책/금융 변수 포함한 멀티모달 예측 모델 및 Transformer 기반 시계열 예측 모델 도입 검토가 되면 더욱 더 정확한 값을 예측할 수 있을 것 같고,
자치구 간 연관관계 분석 및 클러스터링 가능성 탐색하면 더 발전된 모델로 변모 가능 예상됨



## VII. Credits

- 최가형 | Dataset preprocessing, Data visualization, Code implementation, Write up Github
- 유준석 | Dataset searching, Data visualization, Code implementation, Write up Github
- 심규호 | Methodology introduction, Model training and evaluation, Write up Github





