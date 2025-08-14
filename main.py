
if __name__ == "__main__":
    years = list(range(2014, 2016))

    #from K_stock
    capitalstock_proj = households_capital_stock_over_time(years)

    # from DISPOSABLE INCOME

    gross_labour_income_proj = households_gross_labour_income_over_time(years)
    social_security_payments_proj = households_social_security_payments(gross_labour_income_proj)
    net_labor_income_proj = households_net_labour_income_over_time(gross_labour_income_proj,
                                                                   social_security_payments_proj)
    net_wealth_proj = households_net_labour_income_over_time(gross_labour_income_proj, social_security_payments_proj)
    social_benefits_proj = households_social_benefits(years)
    net_operating_surplus_proj = households_net_operating_surplus(years)
    taxable_income_proj = taxable_income_over_time(net_labor_income_proj, social_security_payments_proj,
                                                   net_operating_surplus_proj, households_property_income_received_over_time(years, households_financial_assets_over_time(years, households_financial_liabilities_over_time(years)) ,capitalstock_proj),
                                                   social_benefits_proj)
    delayed_taxable_income_proj = delayed_households_taxable_income_over_time(taxable_income_proj)
    income_tax_proj = households_income_tax()
    disposable_income_proj = households_disposable_income(net_labor_income_proj, social_benefits_proj, income_tax_proj,
                                                          compute_households_property_income_paid(years, households_financial_liabilities_over_time(years)),
                                                          households_wealth_tax_over_time(net_wealth_proj))
    gross_savings_proj = households_gross_savings(disposable_income_proj)

    # from FINANCE

    liabilities_proj = households_financial_liabilities_over_time(years)

    assets_proj = households_financial_assets_over_time(years, liabilities_proj)
    property_income_paid = compute_households_property_income_paid(years, liabilities_proj)
    property_income_received = households_property_income_received_over_time(years, assets_proj, capitalstock_proj)
    net_wealth_proj = households_net_wealth_over_time(years, liabilities_proj, assets_proj, capitalstock_proj)
    wealth_tax_proj = households_wealth_tax_over_time(net_wealth_proj)
