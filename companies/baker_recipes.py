from model_bakery.recipe import Recipe
from companies.models import Comapany

generic_valid_company = Recipe(
    Comapany,
    name='Generic Store',
    description='The perfect Generic Store',
    segment='Others'
)

valid_company = Recipe(
    Comapany,
    name='Kenzie Store',
    description='The ideal store for devs',
    segment='Information Technology'
)

invalid_company_description = Recipe(
    Comapany,
    name='Store over fifty characters that cannot be created!!!',
    description=None,
    segment='Information Technology'
)

invalid_company_name = Recipe(
    Comapany,
    name=None,
)

invalid_company_segment = Recipe(
    Comapany,
    segment=None,
)

duplicated_name_company = Recipe(
    Comapany,
    name='Kenzie Store',
    description='Duplicated Store',
    segment='Information Technology'
)
