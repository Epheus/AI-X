import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from scipy import stats

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우의 경우
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

def show_avg_price(dfs, gu, years):
    # 강남구의 년도별 평균 물건 금액을 구하고 그래프로 표시
    print("\n===  {} 년도별 평균 거래금액 분석 ===".format(gu))

    # 각 연도별 강남구 데이터 필터링 및 평균 거래금액 계산
    gangnam_prices = []

    for year, df in zip(years, dfs):
        gangnam_mean = df[df['자치구명'] == gu]['물건금액(만원)'].mean() / 10000
        gangnam_prices.append(gangnam_mean)
        print(f"{year}년 {gu} 평균 거래금액: {gangnam_mean:.2f}억원")

    # 그래프 그리기
    plt.figure(figsize=(12, 6))
    plt.plot(years, gangnam_prices, marker='o')
    plt.title('{} avg price per year'.format(gu))
    plt.xlabel('year')
    plt.ylabel('avg price [억 원]')
    plt.grid(True)
    plt.xticks(years)
    plt.show()

def show_all_gu_avg_price(dfs, years):
    # 모든 자치구의 년도별 평균 물건 금액을 구하고 그래프로 표시
    print("\n=== 모든 자치구 년도별 평균 거래금액 분석 ===")
    
    # 그래프 그리기
    plt.figure(figsize=(15, 8))
    
    # 각 자치구별로 평균 거래금액 계산 및 그래프 그리기
    for gu in sorted(common_gu):
        gu_prices = []
        for year, df in zip(years, dfs):
            gu_mean = df[df['자치구명'] == gu]['물건금액(만원)'].mean() / 10000
            gu_prices.append(gu_mean)
            print(f"{year}년 {gu} 평균 거래금액: {gu_mean:.2f}억원")
        
        plt.plot(years, gu_prices, marker='o', label=gu)
    
    plt.title('서울시 자치구별 연도별 평균 거래금액 추이')
    plt.xlabel('연도')
    plt.ylabel('평균 거래금액 [억 원]')
    plt.grid(True)
    plt.xticks(years)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def analyze_price_changes_and_correlation(dfs, years, start_year=2017, end_year=2019):
    """
    2017-2019년 구별 평균 가격 증감과 상관성을 분석하는 함수
    """
    print(f"\n=== {start_year}-{end_year}년 구별 평균 가격 증감 및 상관성 분석 ===")
    
    # 분석할 연도 범위의 데이터프레임 선택
    target_dfs = [df for df, year in zip(dfs, years) if start_year <= year <= end_year]
    target_years = [year for year in years if start_year <= year <= end_year]
    
    # 각 구별 평균 가격 계산
    gu_prices = {}
    for gu in sorted(common_gu):
        prices = []
        for df in target_dfs:
            mean_price = df[df['자치구명'] == gu]['물건금액(만원)'].mean() / 10000
            prices.append(mean_price)
        gu_prices[gu] = prices
    
    # 증감률 계산
    price_changes = {}
    for gu, prices in gu_prices.items():
        start_price = prices[0]
        end_price = prices[-1]
        change_rate = ((end_price - start_price) / start_price) * 100
        price_changes[gu] = change_rate
    
    # 증감률 기준으로 정렬
    sorted_changes = sorted(price_changes.items(), key=lambda x: x[1], reverse=True)
    
    print("\n=== 구별 평균 가격 증감률 (%) ===")
    for gu, change in sorted_changes:
        print(f"{gu}: {change:.2f}%")
    
    # 상관성 분석
    print("\n=== 구별 상관성 분석 ===")
    correlation_matrix = np.zeros((len(common_gu), len(common_gu)))
    
    for i, gu1 in enumerate(sorted(common_gu)):
        for j, gu2 in enumerate(sorted(common_gu)):
            if i != j:
                correlation, p_value = stats.pearsonr(gu_prices[gu1], gu_prices[gu2])
                correlation_matrix[i, j] = correlation
    
    # 상관성이 높은 구 쌍 찾기
    high_correlation_pairs = []
    for i, gu1 in enumerate(sorted(common_gu)):
        for j, gu2 in enumerate(sorted(common_gu)):
            if i < j:  # 중복 방지
                correlation = correlation_matrix[i, j]
                if abs(correlation) > 0.7:  # 상관계수 0.7 이상인 경우만 표시
                    high_correlation_pairs.append((gu1, gu2, correlation))
    
    # 상관성이 높은 구 쌍 출력
    print("\n=== 상관성이 높은 구 쌍 (상관계수 > 0.7) ===")
    for gu1, gu2, corr in sorted(high_correlation_pairs, key=lambda x: abs(x[2]), reverse=True):
        print(f"{gu1} - {gu2}: {corr:.3f}")
    
    # 시각화
    plt.figure(figsize=(15, 8))
    for gu in sorted(common_gu):
        plt.plot(target_years, gu_prices[gu], marker='o', label=gu)
    
    plt.title(f'{start_year}-{end_year}년 구별 평균 거래금액 추이')
    plt.xlabel('연도')
    plt.ylabel('평균 거래금액 [억 원]')
    plt.grid(True)
    plt.xticks(target_years)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    return correlation_matrix

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

def visualize_correlation_chain_with_connections(correlation_matrices, start_gu, matrix_info):
    """
    특정 구로부터 시작하는 상관관계 체인을 시각화하는 함수
    
    Parameters:
    correlation_matrices: [2022-2025, 2019-2022, 2017-2019] 순서의 상관관계 행렬 리스트
    start_gu (str): 시작할 구 이름
    matrix_info: 각 행렬의 기간 정보
    """
    # 각 기간별 최고 상관관계 구 찾기
    correlations = []
    highest_corr_gus = []
    
    for matrix in correlation_matrices:
        highest_gu, corr = find_highest_correlation_gu(matrix, start_gu)
        highest_corr_gus.append(highest_gu)
        correlations.append(corr)
    
    # 고유한 구 목록 찾기
    unique_gus = list(set(highest_corr_gus))
    
    # 시각화
    plt.figure(figsize=(15, 8))
    
    # 동그라미와 선 그리기
    circle_radius = 0.4
    spacing = 3
    vertical_spacing = 2
    
    # 시작 구 그리기
    circle = plt.Circle((0, 0), circle_radius, fill=False, color='black')
    plt.gca().add_patch(circle)
    plt.text(0, 0, start_gu, ha='center', va='center')
    
    # 각 기간별 최고 상관관계 구 그리기
    for i, (highest_gu, corr, period) in enumerate(zip(highest_corr_gus, correlations, matrix_info)):
        x_pos = spacing + i * spacing * 2
        plt.gca().add_patch(plt.Circle((x_pos, 0), circle_radius, fill=False, color='black'))
        plt.text(x_pos, 0, f"{period}\n{highest_gu}\n({corr:.3f})", ha='center', va='center')
        plt.plot([circle_radius, x_pos - circle_radius], [0, 0], 'k-')

        # ★ 여기서 other_gus를 미리 만듭니다
        other_gus = [gu for gu in unique_gus if gu != highest_gu]
        for j, other_gu in enumerate(other_gus):
            y_pos = -(j + 1) * vertical_spacing
            plt.gca().add_patch(plt.Circle((x_pos, y_pos), circle_radius, fill=False, color='red'))
            cor_value = find_correlation_between_gu(correlation_matrices[i], highest_gu, other_gu)
            plt.text(x_pos, y_pos, f"{other_gu}\n({cor_value:.3f})", ha='center', va='center')
            plt.plot([x_pos, x_pos], [0, y_pos], 'r--')
    
    # 그래프 설정
    plt.axis('equal')
    plt.axis('off')
    plt.title(f'{start_gu}의 기간별 최고 상관관계 구 체인')
    plt.tight_layout()
    plt.show()

# datasets 폴더에서 숫자.csv 파일만 찾기
data_path = './datasets/'
df_2017 = pd.read_csv(data_path + '2017.csv', encoding='cp949', low_memory=False)
df_2018 = pd.read_csv(data_path + '2018.csv', encoding='cp949', low_memory=False)
df_2019 = pd.read_csv(data_path + '2019.csv', encoding='cp949', low_memory=False)
df_2020 = pd.read_csv(data_path + '2020.csv', encoding='cp949', low_memory=False)
df_2021 = pd.read_csv(data_path + '2021.csv', encoding='cp949', low_memory=False)
df_2022 = pd.read_csv(data_path + '2022.csv', encoding='cp949', low_memory=False)
df_2023 = pd.read_csv(data_path + '2023.csv', encoding='cp949', low_memory=False)
df_2024 = pd.read_csv(data_path + '2024.csv', encoding='cp949', low_memory=False)
df_2025 = pd.read_csv(data_path + '2025.csv', encoding='cp949', low_memory=False)


print("자치구명 추출 시작")

# 각 연도별 데이터프레임에서 자치구명 추출
gu_2017 = set(df_2017['자치구명'].unique())
gu_2018 = set(df_2018['자치구명'].unique())
gu_2019 = set(df_2019['자치구명'].unique())
gu_2020 = set(df_2020['자치구명'].unique())
gu_2021 = set(df_2021['자치구명'].unique())
gu_2022 = set(df_2022['자치구명'].unique())
gu_2023 = set(df_2023['자치구명'].unique())
gu_2024 = set(df_2024['자치구명'].unique())
gu_2025 = set(df_2025['자치구명'].unique())

# 모든 자치구명 집합
all_gu = gu_2017 | gu_2018 | gu_2019 | gu_2020 | gu_2021 | gu_2022 | gu_2023 | gu_2024 | gu_2025

# 모든 연도에 공통적으로 있는 자치구명
common_gu = gu_2017 & gu_2018 & gu_2019 & gu_2020 & gu_2021 & gu_2022 & gu_2023 & gu_2024 & gu_2025

print("\n=== 모든 연도에 공통적으로 있는 자치구명 ===")
for gu in sorted(common_gu):
    print(gu)

# 각 연도별로 없는 자치구명 확인
years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
gu_sets = [gu_2017, gu_2018, gu_2019, gu_2020, gu_2021, gu_2022, gu_2023, gu_2024, gu_2025]

print("\n=== 각 연도별 누락된 자치구명 ===")
for year, gu_set in zip(years, gu_sets):
    missing_gu = all_gu - gu_set
    if missing_gu:
        print(f"\n{year}년 누락된 자치구명:")
        for gu in sorted(missing_gu):
            print(f"- {gu}")
    else:
        print(f"{year}년 누락 자치구 없음")


# 강남구의 년도별 평균 물건 금액을 구하고 그래프로 표시
print("\n=== 강남구 년도별 평균 거래금액 분석 ===")

# 각 연도별 강남구 데이터 필터링 및 평균 거래금액 계산
dfs = [df_2017, df_2018, df_2019, df_2020, df_2021, df_2022, df_2023, df_2024, df_2025]

show_avg_price(dfs, '강남구', years)

show_avg_price(dfs, '양천구', years)

# 강남구와 양천구의 평균 거래금액 분석
print("\n=== 강남구와 양천구 년도별 평균 거래금액 분석 ===")
dfs = [df_2017, df_2018, df_2019, df_2020, df_2021, df_2022, df_2023, df_2024, df_2025]

# 모든 자치구의 평균 거래금액 분석
show_all_gu_avg_price(dfs, years)

# 기존 코드 마지막에 추가
correlation_matrix_2017_2019 = analyze_price_changes_and_correlation(dfs, years, 2017, 2019)
correlation_matrix_2019_2022 = analyze_price_changes_and_correlation(dfs, years, 2019, 2022)
correlation_matrix_2022_2025 = analyze_price_changes_and_correlation(dfs, years, 2022, 2025)

# 예시: 강남구에 대한 분석
highest_corr_gu, corr_value = find_highest_correlation_gu(correlation_matrix_2017_2019, '강남구')
print(f"\n강남구의 최고 상관관계 구: {highest_corr_gu}")
print(f"상관계수: {corr_value:.3f}")

# 예시: 강남구와 송파구 간의 상관관계 분석
corr_value = find_correlation_between_gu(correlation_matrix_2017_2019, '강남구', '송파구')
print(f"\n강남구와 송파구 간의 상관관계:")
print(f"상관계수: {corr_value:.3f}")

# 기존 코드 마지막에 추가
# 예시: 강남구에 대한 상관관계 체인 시각화 (연결 포함)
correlation_matrices = [correlation_matrix_2022_2025, correlation_matrix_2019_2022, correlation_matrix_2017_2019]
matrix_info = ['2022-2025', '2019-2022', '2017-2019']
visualize_correlation_chain_with_connections(correlation_matrices, '양천구', matrix_info)

# 기존 코드 마지막에 추가
# 모든 구에 대한 상관관계 체인 시각화
visualize_all_gu_correlations(correlation_matrices, matrix_info)








