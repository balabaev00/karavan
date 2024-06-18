def get_top_correlations(df_pivot, product_name, n=10, top_products_count=1000, ):
    total_sales = df_pivot.sum()
    # Выбираем топ товаров по суммарным продажам
    top_temp_df_products = total_sales.nlargest(top_products_count).index

    # Создаем матрицу корреляции для топ товаров
    correlation_matrix = df_pivot[top_temp_df_products].corr()
    # Создаем матрицу корреляции для всех товаров
    # correlation_matrix = df_pivot.corr()

    # Проверяем, существует ли продукт в данных
    if product_name not in correlation_matrix.columns:
        raise ValueError(f"Продукт {product_name} не найден в данных")

    # Извлечение корреляций для указанного продукта
    correlations = correlation_matrix[product_name].drop(product_name)

    # Сортировка корреляций по убыванию
    most_correlated_products = correlations.sort_values(ascending=False).head(n)

    return most_correlated_products
