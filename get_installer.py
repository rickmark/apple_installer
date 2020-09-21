import gzip
import plistlib
import re

import requests

SEED_DIRECTORY = "/System/Library/PrivateFrameworks/Seeding.framework/Resources/SeedCatalogs.plist"
PRODUCT_ID_REGEX = re.compile('^\\d{3}-\\d+$')


def seed_catalog_url(seed_name: str) -> str:
    with open(SEED_DIRECTORY, "rb") as seed_file:
        return plistlib.load(seed_file)[seed_name]


def get_products(url: str) -> dict:
    catalog_response = requests.get(url)

    if catalog_response.headers['Content-Encoding'] == 'x-gzip':
        decompressed = gzip.decompress(catalog_response.content)

        return plistlib.loads(decompressed)['Products']
    else:
        return plistlib.loads(catalog_response.content)['Products']


def download_package(package: dict):
    pass


products = get_products(seed_catalog_url('DeveloperSeed'))

for product_id in products.keys():
    match = PRODUCT_ID_REGEX.match(product_id)
    product = products[product_id]
    if match and 'ExtendedMetaInfo' in product.keys() and \
            'InstallAssistantPackageIdentifiers' in product['ExtendedMetaInfo']:

        print(f"{product_id} - {product['ExtendedMetaInfo']}")
        for component in product['Packages']:
            print(f"\tComponent - {component}")
