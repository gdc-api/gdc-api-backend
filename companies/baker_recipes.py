from model_bakery.recipe import Recipe
from companies.models import Company

generic_valid_company = Recipe(
    Company,
    name='Generic Store',
    description='The perfect Generic Store',
    segment='Others'
)

valid_company = Recipe(
    Company,
    name='Kenzie Store',
    description='The ideal store for devs',
    segment='Information Technology'
)

invalid_company_description = Recipe(
    Company,
    name='Store over fifty characters that cannot be created!!!',
    description=None,
    segment='Information Technology'
)

invalid_company_name = Recipe(
    Company,
    name=None,
)

invalid_company_segment = Recipe(
    Company,
    segment=None,
)

duplicated_name_company = Recipe(
    Company,
    name='Kenzie Store',
    description='Duplicated Store',
    segment='Information Technology'
)
