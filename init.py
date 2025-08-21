import xarray as xr


_subscript_dict = {
    "HOUSEHOLDS_I": ["LowINC", "HighINC"],
    "REGIONS_I": ["FR", "IT"],
}

#taux de variation EXO

depreciation_rate_real_estate_sp = xr.DataArray([[0.05, 0.05],[0.08,0.08]],
    dims=_subscript_dict.keys(),
    coords=_subscript_dict,
    )

increase_in_households_capital_stock_due_to_investments = xr.DataArray(
        [[0.05, 0.03], [0.04, 0.02]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

variation_in_households_capital_stock_due_to_revalorizations = xr.DataArray(
        [[0.02, 0.02], [0.035, 0.03]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

decrease_in_households_capital_stock_due_to_depreciation=xr.DataArray(
        [[0.01, 0.01], [0.02, 0.03]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

#increase_in_households_capital_stock_due_to_investments=xr.DataArray(
    #     [[50, 100], [40, 75]],
    #     dims=_subscript_dict.keys(),
    #     coords=_subscript_dict,
    # )

# ratio_liabilities_to_disposable_income=xr.DataArray(
#         [[0.02, 0.025], [0.015, 0.025]],
#         dims=_subscript_dict.keys(),
#         coords=_subscript_dict,
#     )

variation_rate_liabilities = xr.DataArray(
        [[0.03, 0.03], [0.035, 0.02]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

adjustment_factor_labour_compensation=xr.DataArray(
        [[0.03, 0.025], [0.035, 0.03]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

adjustment_factor_social_benefits=xr.DataArray(
        [[0.035, 0.02], [0.04, 0.025]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

adjustment_factor_net_operating_surplus=xr.DataArray(
        [[0.04, 0.035], [0.08, 0.07]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )
yearly_net_lending=xr.DataArray(
        [[0, 0], [500, 350]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

basic_income_increase = xr.DataArray([[0.015, 0.005],[0.015,0.005]],
    dims=_subscript_dict.keys(),
    coords=_subscript_dict,
    )

#
# #variables d'initialisation

initial_households_capital_stock=xr.DataArray(
        [[1000, 1000], [3500, 3000]],
        dims = _subscript_dict.keys(),
        coords=_subscript_dict,
    )

base_number_of_households_in_millions=xr.DataArray(
        [[4, 4], [4, 3]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

initial_households_financial_assets=xr.DataArray(
        [[5000, 4000], [6000, 5500]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

total_households_consumption_coicop=xr.DataArray(
        [[5000, 4000], [9000, 7500]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

initial_households_financial_liabilities=xr.DataArray(
        [[300, 200], [500, 400]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

initial_households_gross_labor_income = xr.DataArray([[25000, 20000], [35000, 30000]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

households_basic_income=xr.DataArray(
        [[200, 175], [200, 175]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

initial_households_social_benefits=xr.DataArray(
        [[150, 125], [150, 125]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

initial_households_net_operating_surplus=xr.DataArray(
        [[600, 800], [1200, 1100]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

households_other_transfers_paid=xr.DataArray(
        [[50, 30], [40, 25]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

households_other_transfers_received=xr.DataArray(
        [[55, 35], [45, 25]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

government_property_income = xr.DataArray([[0.75, 1], [0.5, 0.75]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

initial_government_debt = xr.DataArray(
        [[3000000, 3000000], [3000000, 3000000]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

government_consumption = xr.DataArray([[300, 200], [300, 200]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

# #taux d'imposition et taux d'interet
household_tax_rate_on_assets_to_finance_basic_income=xr.DataArray(
        [[0.05, 0.06], [0.06, 0.07]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

interest_rate_for_households_liabilities=xr.DataArray(
        [[0.02, 0.02], [0.03, 0.03]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

interest_rate_for_households_assets=xr.DataArray(
        [[0.02, 0.02], [0.03, 0.03]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

wealth_tax_rate=xr.DataArray(
        [[0, 0.00], [0.001, 0.008]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

households_social_security_rate=xr.DataArray(
        [[0.02, 0.025], [0.03, 0.035]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

income_tax_rate=xr.DataArray(
        [[0.20, 0.22], [0.30, 0.35]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

interest_rate_government_debt = xr.DataArray(
        [[0.034, 0.036], [0.034, 0.036]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

base_number_of_households_in_millions = xr.DataArray(
        [[30, 30], [25, 20]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

climate_change_damage_rate_on_capital_stock = xr.DataArray(
        [[0.15, 0.12], [0.10, 0.14]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

tax_rev_on_production = xr.DataArray(
         [[1000, 1000], [3000, 2000]],
         dims=_subscript_dict.keys(),
         coords=_subscript_dict,
     )

tax_rate_on_household_transport_consumption = xr.DataArray(
        [[0.05, 0.06], [0.05, 0.06]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

#WILIAM econometric estimations

income_elasticity_households_fuel_transport=xr.DataArray(
        [[0.7, 0.7], [0.7, 0.7]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

income_elasticity_households_air_transport=xr.DataArray(
        [[1.1, 1.1], [1.1, 1.1]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

price_elasticity_households_fuel_transport=xr.DataArray(
        [[0.4, 0.4], [0.4, 0.4]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

price_elasticity_households_air_transport=xr.DataArray(
        [[0.8, 0.8], [0.8, 0.8]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

price_households_air_transport=xr.DataArray(
        [[215, 150], [230, 175]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

price_households_fuel_transport=xr.DataArray(
        [[1100, 1500], [1200, 1600]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )

#CARBON TAX SWITCH
carbon_tax=xr.DataArray(
        [[0.05, 0.05], [0.05, 0.05]],
        dims=_subscript_dict.keys(),
        coords=_subscript_dict,
    )