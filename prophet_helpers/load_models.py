from enums.product_name_enum import ProductName
from prophet.serialize import model_from_json

MODELS_PATH = './models/'


def load_prophet_models(models_path=MODELS_PATH):
    return {
        ProductName.TShirtPackage30x54.value: model_from_json(
            open(models_path + '/t_shirt_package_30x54.json', 'r').read()
        ),
        ProductName.Russian_Bread.value: model_from_json(
            open(models_path + '/russian_bread_400.json', 'r').read()
        )
    }
