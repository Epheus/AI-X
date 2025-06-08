import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

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

# 모든 자치구의 평균 거래금액 분석
show_all_gu_avg_price(dfs, years)


