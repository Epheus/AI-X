import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.linear_model import LinearRegression

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows 기준
font_prop = fm.FontProperties(fname=font_path).get_name()
plt.rc("font", family=font_prop)



data_path = 'datasets/'
file_name_temp = '서울시 부동산 실거래가 정보_{}.csv'


# 연도별 파일 읽기
def load_data():
    combined = pd.DataFrame()

    for year in range(2017, 2026):
        file_name = file_name_temp.format(year)
        file_path = data_path + file_name

        if os.path.exists(file_path):
            df = pd.read_csv(file_path, encoding='cp949')
            df["연도"] = year
            combined = pd.concat([combined, df], ignore_index=True)
        else:
            print(f"{file} 없음")
    return combined


# 전처리
def preprocess(df):
    # 필요한 컬럼만 유지
    keep_cols = ["자치구명", "건물용도", "계약일", "물건금액(만원)", "연도"]
    df = df[keep_cols].dropna()
    df = df.rename(columns={"자치구명": "자치구", "물건금액(만원)": "금액"})
    df = df[df["금액"] > 0]
    return df


# 연도별 평균금액 계산
def get_mean_prices(df):
    grouped = df.groupby(["자치구", "건물용도", "연도"])["금액"].mean().reset_index()
    return grouped


# 2026년 예측
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


# 시각화
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


# 실행
if __name__ == '__main__':
    df_all = load_data()
    df_clean = preprocess(df_all)
    df_mean = get_mean_prices(df_clean)
    pred_df = predict_2026(df_mean)

    # 원하는 자치구 설정
    gu = "강남구"  # 예: 강남구, 마포구 등
    plot_gu_predictions(df_mean, pred_df, gu)