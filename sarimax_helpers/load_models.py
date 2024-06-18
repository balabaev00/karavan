from enums.product_name_enum import ProductName
import pickle

MODELS_PATH = './models/'


def load_sarimax_models(models_path=MODELS_PATH):
    return {
        ProductName.TShirtPackage30x54.value: pickle.load(
            open(models_path + '/t_shirt_package_30x54.pkl', 'rb')
        ),
        ProductName.Russian_Bread.value: pickle.load(
            open(models_path + '/russian_bread_400.pkl', 'rb')
        ),
        # ProductName.SPWheatBreadWithFlaxSeeds.value: pickle.load(
        #     open(models_path + '/sp_wheat_bread_with_flax_seeds.pkl', 'rb')
        # )
    }
