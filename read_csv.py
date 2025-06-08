import pandas as pd
import os

data_path = 'datasets/'
file_name_temp = '서울시 부동산 실거래가 정보_{}.csv'


def read_year_data(year):
    file_name = file_name_temp.format(year)
    file_path = data_path + file_name
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='cp949')
        return df


def analyze_missing_data(df):
    print("\n=== 결측치 분석 ===")
    print("\n각 컬럼별 결측치 개수:")
    print(df.isnull().sum())
    print("\n각 컬럼별 결측치 비율:")
    print((df.isnull().sum() / len(df) * 100).round(2))
    print("\n결측치가 있는 행 미리보기:")
    print(df[df.isnull().any(axis=1)].head())


def clean_data(df, delete_columns, decision_columns):
    # 불필요한 컬럼 삭제
    df_cleaned = df.drop(columns=list(delete_columns), errors='ignore')
    
    # 기준 컬럼에 결측치가 있는 행 삭제
    df_cleaned = df_cleaned.dropna(subset=list(decision_columns))
    
    print(f"\n=== 데이터 정제 결과 ===")
    print(f"원본 데이터 행 수: {len(df)}")
    print(f"정제 후 데이터 행 수: {len(df_cleaned)}")
    print(f"삭제된 행 수: {len(df) - len(df_cleaned)}")
    
    return df_cleaned

def preprocess_data_and_save(year):
    df_sel_year = read_year_data(year)

    # 데이터 정제를 위한 기준 칼럼 정의
    decision_column_str = ["지번구분", "토지면적(㎡)", "층", "건물용도","건축년도","건물명", "본번", "부번", "자치구명"]

    # 불필요 칼럼 정의
    delete_column_str = {"취소일", "권리구분", "신고구분", "신고한 개업공인중개사 시군구명"}

    # 데이터 정제 전 결측치 분석
    print("\n=== 정제 전 데이터 분석 ===")
    analyze_missing_data(df_sel_year)

    # 데이터 정제
    df_sel_year_cleaned = clean_data(df_sel_year, delete_column_str, decision_column_str)

    # 정제 후 결측치 분석
    print("\n=== 정제 후 데이터 분석 ===")
    analyze_missing_data(df_sel_year_cleaned)

    # 정제된 데이터를 CSV 파일로 저장
    output_path = str(year) + '.csv'
    df_sel_year_cleaned.to_csv(data_path + output_path, index=False, encoding='cp949')
    print(f"\n정제된 데이터가 {output_path}에 저장되었습니다.")

    return df_sel_year_cleaned

# 2017년부터 2025년까지의 데이터만 처리
""" for year in range(2017, 2026):
    file_name = file_name_temp.format(year)
    file_path = data_path + file_name
    
    if os.path.exists(file_path):
        print(f"\n=== {year}년 데이터 처리 중 ===")
        try:
            df = pd.read_csv(file_path, encoding='cp949')
            print("\n데이터 미리보기:")
            print(df.head())
            print("\n데이터 정보:")
            print(df.info())
        except Exception as e:
            print(f"파일 처리 중 오류 발생: {e}")
    else:
        print(f"\n{year}년 데이터 파일이 존재하지 않습니다.") """

print("===============================================")
print("데이터 정제 시작")
print("===============================================")

# 2017년 데이터 처리
df_2017_cleaned = preprocess_data_and_save(2017)

df_2018_cleaned = preprocess_data_and_save(2018)

df_2019_cleaned = preprocess_data_and_save(2019)

df_2020_cleaned = preprocess_data_and_save(2020)

df_2021_cleaned = preprocess_data_and_save(2021)

df_2022_cleaned = preprocess_data_and_save(2022)

df_2023_cleaned = preprocess_data_and_save(2023)

df_2024_cleaned = preprocess_data_and_save(2024)

df_2025_cleaned = preprocess_data_and_save(2025)

