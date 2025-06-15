import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import platform


data_path = 'datasets/'
file_name_temp = '{}.csv'
save_dir = './visualize'
os.makedirs(save_dir, exist_ok=True)


# 시스템 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False


# 연도별 데이터 불러오기
def read_year_data_cleaned(year):
    file_name = file_name_temp.format(year)
    file_path = os.path.join(data_path, file_name)

    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='cp949', low_memory=False)
        return df
    else:
        print(f"[경고] {file_path} 없음")
        return None


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
    #plt.show()
    plt.savefig(os.path.join(save_dir, f'Figure_3_{year}.jpg'))
    plt.close()




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
    #plt.show()
    plt.savefig(os.path.join(save_dir, f'Figure_1_{year}.jpg'))
    plt.close()

    # 2) Barplot 시각화 : 25개 자치구 별 평균 부동산 거래금액 분포
    sns.barplot(x='자치구명', y='물건금액(만원)', data=df_cleaned,
                estimator='mean',
                order=df_cleaned.groupby('자치구명')['물건금액(만원)'].mean().sort_values(ascending=False).index)
    plt.title(f'{year}년 자치구 별 평균 부동산 거래금액 분포', fontsize=12)
    plt.xticks(rotation=90)
    formatter = FuncFormatter(lambda x, _: f'{int(x / 1000)}k')
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.tight_layout()
    #plt.show()
    plt.savefig(os.path.join(save_dir, f'Figure_2_{year}.jpg'))
    plt.close()






# 전체 연도 루프 실행
for year in range(2017, 2026):
    print(f'\n🔎 {year}년 데이터 시각화 시작')
    df = read_year_data_cleaned(year)
    if df is not None:
        visualize_gu_prices(df, year)
        visualize_correlation(df, year)




