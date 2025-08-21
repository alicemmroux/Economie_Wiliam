import xarray as xr
import numpy as np
import init

_subscript_dict = {
    "HOUSEHOLDS_I": ["LowINC", "HighINC"],
    "REGIONS_I": ["FR", "IT"],
}

def households_capital_stock_over_time(years):
    # Initial value per household
    stock = init.initial_households_capital_stock
    results = []

    for yr in years:
        if yr < 2015:
            rate = xr.zeros_like(stock)
        else:
            growth_rate = (
                init.increase_in_households_capital_stock_due_to_investments
                + init.variation_in_households_capital_stock_due_to_revalorizations
                - init.decrease_in_households_capital_stock_due_to_depreciation
            )
            rate = stock * growth_rate

        stock = stock + rate
        results.append(stock)

    return xr.concat(results, dim="Year").assign_coords({"Year": years})



def households_financial_liabilities_over_time(years):
    stock = init.initial_households_financial_liabilities
    results = []

    for yr in years:
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = init.variation_rate_liabilities

        stock = stock * (1 + growth)
        results.append(stock.copy())

    return xr.concat(results, dim="Year").assign_coords({"Year": years})


def variation_households_financial_assets(dl_by_year):
    return init.yearly_net_lending + dl_by_year

def households_financial_assets_over_time(years, variation_financial_assets_proj):
    stock = init.initial_households_financial_assets
    results = []

    for i, yr in enumerate(years):
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = variation_financial_assets_proj.sel(Year=yr)

        stock = stock + growth
        results.append(stock.copy().expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year").assign_coords({"Year": years})

def households_property_income_paid_over_time(years, liabilities_by_year):
    rate = init.interest_rate_for_households_liabilities
    results = []

    for yr in years:
        liabilities = liabilities_by_year.sel(Year=yr)
        payment = liabilities * rate
        payment = payment.expand_dims(Year=[yr])
        results.append(payment)

    return xr.concat(results, dim="Year").assign_coords({"Year": years})



def households_property_income_received_over_time(years, assets_by_year, capitalstock_proj):
    rate = init.interest_rate_for_households_assets
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
    return net_wealth_proj * (init.wealth_tax_rate + init.carbon_tax)

def households_gross_labour_income_over_time(years):
    stock = init.initial_households_gross_labor_income
    results = []

    for yr in years:
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = init.adjustment_factor_labour_compensation

        stock = stock * (1 + growth)
        results.append(stock.copy().expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year").assign_coords({"Year": years})

def households_net_operating_surplus(years):
    stock = init.initial_households_net_operating_surplus
    results = []

    for yr in years:
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = init.adjustment_factor_net_operating_surplus - init.carbon_tax

        stock = stock * (1 + growth)
        results.append(stock.copy().expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year").assign_coords({"Year": years})


def households_social_benefits(years):
    stock = init.initial_households_social_benefits
    results = []

    for yr in years:
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = init.adjustment_factor_social_benefits

        stock = stock * (1 + growth)
        results.append(stock.copy().expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year").assign_coords({"Year": years})


def households_social_security_payments(gross_labour_income_proj):
    return gross_labour_income_proj * init.households_social_security_rate

def households_net_labour_income_over_time(gross_labour_income_proj, social_security_payments_proj):
    return gross_labour_income_proj - social_security_payments_proj

def taxable_income_over_time(net_labor_income_proj, social_security_payments_proj, net_operating_surplus_proj, property_income_received, social_benefits_proj):
    return net_labor_income_proj + social_security_payments_proj + net_operating_surplus_proj + property_income_received + social_benefits_proj + init.households_other_transfers_received

def delayed_households_taxable_income_over_time(taxable_income_proj, delay=1):
    return taxable_income_proj.shift(Year=delay)

def households_income_tax(delayed_taxable_income_proj):
    return delayed_taxable_income_proj * init.income_tax_rate

def households_disposable_income(net_labor_income_proj, social_benefits_proj, income_tax_proj, property_income_received, property_income_paid, wealth_tax_proj):
    return (net_labor_income_proj + social_benefits_proj + init.households_other_transfers_received + property_income_received + init.households_basic_income)- (income_tax_proj + init.households_other_transfers_paid + property_income_paid + wealth_tax_proj)

def delayed_households_disposable_income_over_time(net_labor_income_proj, social_benefits_proj, income_tax_proj, property_income_received, property_income_paid, wealth_tax_proj, delay=1):
    return households_disposable_income(net_labor_income_proj, social_benefits_proj, income_tax_proj, property_income_received, property_income_paid, wealth_tax_proj).shift(Year=delay)

#ENERGY

def consumption_households_air_transport(disposable_income_proj):
    return np.exp(np.log(disposable_income_proj)*init.income_elasticity_households_air_transport - np.log(init.price_households_air_transport*(1+init.carbon_tax) )* init.price_elasticity_households_air_transport)

def consumption_households_fuel_transport(disposable_income_proj):
    return np.exp(np.log(disposable_income_proj)*init.income_elasticity_households_fuel_transport - \
                  np.log(init.price_households_fuel_transport * (1+init.carbon_tax) )* init.price_elasticity_households_fuel_transport )

#GOVERNMENT - Work in Progress

def households_gross_savings(disposable_income_proj):
    return disposable_income_proj - init.total_households_consumption_coicop


def government_spending_basic_income(years):
    stock = init.households_basic_income * init.base_number_of_households_in_millions
    results = []

    for yr in years:
        if yr < 2015:
            growth = xr.zeros_like(stock)
        else:
            growth = init.basic_income_increase

        stock = stock * (1 + growth)
        results.append(stock.copy().expand_dims(Year=[yr]))

    return xr.concat(results, dim="Year").assign_coords({"Year": years})

def tax_revenue_transport_consumption_hh(fuel_transport_consumption_proj, air_transport_consumption_proj):
    return ((fuel_transport_consumption_proj + air_transport_consumption_proj) * init.base_number_of_households_in_millions) * init.tax_rate_on_household_transport_consumption

def government_revenue_over_time(social_benefits_proj, income_tax_proj, wealth_tax_proj, gov_revenue_transport_proj):
    return (social_benefits_proj + income_tax_proj + wealth_tax_proj) * init.base_number_of_households_in_millions + init.government_property_income + gov_revenue_transport_proj + init.tax_rev_on_production

# still need to add INVESTMENT and CONSUMPTION
def government_primary_expenditure_over_time(social_benefits_proj, gov_investment_proj):
    return (social_benefits_proj + init.households_other_transfers_received + init.households_basic_income + gov_investment_proj ) * init.base_number_of_households_in_millions + init.government_consumption


def government_investment_per_household_type(capitalstock_proj):
    return capitalstock_proj * init.climate_change_damage_rate_on_capital_stock

#next up: government EXPENDITURE

def gov_interest_paid_t(debt_t, rate_t):
    return debt_t * rate_t

def gov_total_expenditure_t(primary_t, interest_t):
    return primary_t + interest_t

def gov_deficit_t(revenue_t, total_expenditure_t):
    return total_expenditure_t - revenue_t

def gov_debt_update(debt_t, deficit_t):
    return debt_t + deficit_t

def government_budget_over_time(years, gov_primary_expenditure, gov_revenue_proj):
    debt = init.initial_government_debt  # start-of-year debt at first year
    debt_out, interest_out, expend_out, deficit_out = [], [], [], []

    for yr in years:
        # pull this year's parameters
        r_t = init.interest_rate_government_debt
        Gp_t = gov_primary_expenditure.sel(Year=yr)
        T_t  = gov_revenue_proj.sel(Year=yr)

        if yr < 2015:
            interest_t = xr.zeros_like(debt)
            G_t = Gp_t  # total spend (no interest)
            deficit_t = xr.zeros_like(debt)  # freeze: no debt change
            # debt unchanged
        else:
            interest_t = gov_interest_paid_t(debt, r_t)
            G_t = gov_total_expenditure_t(Gp_t, interest_t)
            deficit_t = gov_deficit_t(T_t, G_t)
            debt = gov_debt_update(debt, deficit_t)

        # collect
        debt_out.append(debt.expand_dims(Year=[yr]))
        interest_out.append(interest_t.expand_dims(Year=[yr]))
        expend_out.append(G_t.expand_dims(Year=[yr]))
        deficit_out.append(deficit_t.expand_dims(Year=[yr]))

    debt_by_year     = xr.concat(debt_out,     dim="Year").assign_coords(Year=years)
    interest_by_year = xr.concat(interest_out, dim="Year").assign_coords(Year=years)
    expend_by_year   = xr.concat(expend_out,   dim="Year").assign_coords(Year=years)
    deficit_by_year  = xr.concat(deficit_out,  dim="Year").assign_coords(Year=years)
    return xr.Dataset({
        "debt": debt_by_year,
        "interest": interest_by_year,
        "expenditure": expend_by_year,
        "deficit": deficit_by_year,
    })
