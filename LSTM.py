import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.font_manager as fm
from sklearn.preprocessing import MinMaxScaler

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
            print(f"{file_path} 없음")
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

# 실행
if __name__ == '__main__':
    df_all = load_data()
    df_clean = preprocess(df_all)
    df_mean = get_mean_prices(df_clean)
    pred_df = predict_2026_lstm(df_mean)

    gu = "강남구"
    plot_gu_predictions(df_mean, pred_df, gu)