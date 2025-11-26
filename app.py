import streamlit as st
import os

# --- 1. Настройка и Конфигурация Страницы ---
st.set_page_config(
    page_title="Калькулятор с Историей",
    layout="centered"
)

# Устанавливаем заголовок приложения
st.title("🚀 Калькулятор с Историей")
st.write("Введите два числа и выберите операцию.")

# --- 2. Инициализация Истории ---
# Если история не существует в состоянии сессии, создаем пустой список
if 'history' not in st.session_state:
    st.session_state['history'] = []

# --- 3. Интерфейс Калькулятора (Центральная Часть) ---

# Создаем колонки: 1 для ввода и 1 для картинки справа
# Соотношение: 2 части для калькулятора, 2 части для картинки
col_input, col_right_image = st.columns([2, 2])

# Интерфейс ввода находится в левой колонке (col_input)
with col_input:
    # 3 колонки для ввода чисел и операции
    c1, c2, c3 = st.columns([1, 1, 1])

    with c1:
        number1 = st.number_input("Первое число:", value=0.0, key="num1")
    with c2:
        operation = st.selectbox("Операция:", ("+", "-", "*", "/"), key="op")
    with c3:
        number2 = st.number_input("Второе число:", value=0.0, key="num2")

    result = None
    symbol = operation

    # Кнопка для вычисления
    if st.button("Вычислить", use_container_width=True):
        try:
            if symbol == "+":
                result = number1 + number2
            elif symbol == "-":
                result = number1 - number2
            elif symbol == "*":
                result = number1 * number2
            elif symbol == "/":
                if number2 != 0:
                    result = number1 / number2
                else:
                    st.error("❌ Ошибка: Деление на ноль!")
                    result = None # Сбрасываем результат

            if result is not None:
                # Форматируем результат для вывода и истории
                if result == int(result):
                    result_str = str(int(result))
                else:
                    result_str = f"{result:.3f}"

                # Создаем запись истории
                entry = f"**{number1} {symbol} {number2}** = **{result_str}**"

                # Добавляем запись в начало списка
                st.session_state['history'].insert(0, entry)

                # Обрезаем историю, чтобы было не более 10 записей
                st.session_state['history'] = st.session_state['history'][:10]

                st.success(f"✅ Результат: **{result_str}**")

        except Exception as e:
            st.error(f"Произошла ошибка: {e}")

# --- 4. Отображение Вашей Гифки (Правая Часть) ---
GIF_FILENAME = "zaza.gif"

if os.path.exists(GIF_FILENAME):
    with col_right_image:
        # st.image поддерживает гифки. use_column_width=True растянет ее по колонке
        st.image(GIF_FILENAME, caption="Просто для поглядывания!", use_column_width=True)
else:
    with col_right_image:
        st.info(f"Загрузите файл **{GIF_FILENAME}** в папку проекта для отображения картинки/гифки справа.")


# --- 5. Отображение Истории (Левая Боковая Панель) ---
# На боковой панели ТОЛЬКО история, без гифок.
st.sidebar.markdown("---")
st.sidebar.header("📜 История Решений (до 10)")
st.sidebar.markdown("---")


if st.session_state['history']:
    # Отображаем историю
    for i, entry in enumerate(st.session_state['history']):
        st.sidebar.markdown(f"**{i + 1}.** {entry}")
else:
    st.sidebar.info("История пуста. Выполните первое вычисление!")