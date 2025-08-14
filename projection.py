import xarray as xr

import init
init.initial_households_capital_stock()
init.base_number_of_households()
init.increase_in_households_capital_stock_due_to_investments()
init.variation_in_households_capital_stock_due_to_revalorizations()
init.decrease_in_households_capital_stock_due_to_depreciation()
init.ratio_liabilities_to_disposable_income()
init.increase_in_households_capital_stock_due_to_investments()
init.initial_households_financial_liabilities()
init.base_number_of_households()
init.initial_households_financial_assets()
init.interest_rate_for_households_liabilities()
init.interest_rate_for_households_assets()
init.wealth_tax_rate()
init.initial_households_gross_labor_income()
init.adjustment_factor_labour_compensation()
init.initial_households_net_operating_surplus()
init.initial_households_social_benefits()
init.adjustment_factor_net_operating_surplus()
init.adjustment_factor_social_benefits()


_subscript_dict = {
    "HOUSEHOLDS_I": ["LowINC", "HighINC"],
    "REGIONS_I": ["FR", "IT"],
}

def households_capital_stock_over_time(years):
    # Initial value per household
    stock = init.initial_households_capital_stock() / init.base_number_of_households()
    results = []

    for yr in years:
        if yr < 2015:
            rate = xr.zeros_like(stock)
        else:
            growth_rate = (
                init.increase_in_households_capital_stock_due_to_investments()
                + init.variation_in_households_capital_stock_due_to_revalorizations()
                - init.decrease_in_households_capital_stock_due_to_depreciation()
            )
            rate = stock * growth_rate  # multiply initial by rate

        stock = stock + rate
        results.append(stock)

    return xr.concat(results, dim="Year").assign_coords({"Year": years})

def households_gross_savings():
    return households_disposable_income(households_net_labour_income_over_time(gross_labour_income_proj,
                                                                   social_security_payments_proj), households_social_benefits(years), households_income_tax(), households_property_income_paid_over_time(years, liabilities_proj), households_wealth_tax_over_time()) - total_households_consumption_coicop()
def households_net_lending():
    return households_gross_savings() - init.increase_in_households_capital_stock_due_to_investments()

def households_financial_liabilities_over_time(years):
    stock = init.initial_households_financial_liabilities() / init.base_number_of_households()
    results = []

    for yr in years:
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = variation_in_households_financial_liabilities()

        stock = stock + growth
        results.append(stock.copy())

    return xr.concat(results, dim="Year").assign_coords({"Year": years})

def households_financial_assets_over_time(years, liabilities_by_year):
    stock = init.initial_households_financial_assets() / init.base_number_of_households()
    results = []

    for i, yr in enumerate(years):
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            liabilities = liabilities_by_year.sel(Year=yr)
            growth = variation_households_financial_assets()

        stock = stock + growth
        results.append(stock.copy().expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year").assign_coords({"Year": years})

def households_property_income_paid_over_time(years, liabilities_by_year):
    rate = init.interest_rate_for_households_liabilities()
    results = []

    for yr in years:
        liabilities = liabilities_by_year.sel(Year=yr)
        payment = liabilities * rate
        payment = payment.expand_dims(Year=[yr])  # Add year coordinate for concat
        results.append(payment)

    return xr.concat(results, dim="Year").assign_coords({"Year": years})

def compute_households_property_income_paid(years, liabilities_proj):
    return households_property_income_paid_over_time(years, liabilities_proj)

def households_property_income_received_over_time(years, assets_by_year, capitalstock_proj):
    rate = init.interest_rate_for_households_assets()
    results = []

    for yr in years:
        assets_t = assets_by_year.sel(Year=yr)
        capital_t = capitalstock_proj.sel(Year=yr)
        payment = (assets_t + capital_t) * rate
        results.append(payment.expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year")

def households_net_wealth_over_time(years, liabilities_by_year, assets_by_year, capitalstock_proj):
    results = []

    for yr in years:
        assets_t = assets_by_year.sel(Year=yr)
        capital_t = capitalstock_proj.sel(Year=yr)
        liabilities_t = liabilities_by_year.sel(Year=yr)
        payment = assets_t + capital_t - liabilities_t
        results.append(payment.expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year")


def households_wealth_tax_over_time(net_wealth_proj):
    return net_wealth_proj * init.wealth_tax_rate()

def households_gross_labour_income_over_time(years):
    stock = init.initial_households_gross_labor_income()
    results = []

    for i, yr in enumerate(years):
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = init.adjustment_factor_labour_compensation()

        stock = stock * (1 + growth)
        results.append(stock.copy().expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year").assign_coords({"Year": years})

def households_net_operating_surplus(years):
    stock = init.initial_households_net_operating_surplus()
    results = []

    for i, yr in enumerate(years):
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = init.adjustment_factor_net_operating_surplus()

        stock = stock * (1 + growth)
        results.append(stock.copy().expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year").assign_coords({"Year": years})


def households_social_benefits(years):
    stock = init.initial_households_social_benefits()
    results = []

    for i, yr in enumerate(years):
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = init.adjustment_factor_social_benefits()

        stock = stock * (1 + growth)
        results.append(stock.copy().expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year").assign_coords({"Year": years})


def households_social_security_payments(gross_labour_income_proj):
    return gross_labour_income_proj * households_social_security_rate()

def households_net_labour_income_over_time(gross_labour_income_proj, social_security_payments_proj):
    return gross_labour_income_proj - social_security_payments_proj

def taxable_income_over_time(net_labor_income_proj, social_security_payments_proj, net_operating_surplus_proj, property_income_received, social_benefits_proj):
    return net_labor_income_proj + social_security_payments_proj + net_operating_surplus_proj + property_income_received + social_benefits_proj + households_other_transfers_received()

def delayed_households_taxable_income_over_time(taxable_income_proj, delay=1):
    return taxable_income_proj.shift(Year=delay)

def households_disposable_income(net_labor_income_proj, social_benefits_proj, income_tax_proj, property_income_paid, wealth_tax_proj):
    return (net_labor_income_proj + social_benefits_proj + households_other_transfers_received() + property_income_received + households_basic_income())- (income_tax_proj + households_other_transfers_paid() + property_income_paid + wealth_tax_proj)

def delayed_households_disposable_income_over_time(taxable_income_proj, delay=1):
    return households_disposable_income(net_labor_income_proj, social_benefits_proj, income_tax_proj, property_income_paid, wealth_tax_proj).shift(Year=delay)