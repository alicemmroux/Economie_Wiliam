import projection
import matplotlib.pyplot as plt

if __name__ == "__main__":
    years = list(range(2016, 2050))

    #from K_stock
    capitalstock_proj = projection.households_capital_stock_over_time(years)

    # from DISPOSABLE INCOME

    gross_labour_income_proj = projection.households_gross_labour_income_over_time(years)
    # print(gross_labour_income_proj)
    social_security_payments_proj = projection.households_social_security_payments(gross_labour_income_proj)
    net_labor_income_proj = projection.households_net_labour_income_over_time(gross_labour_income_proj,
                                                                   social_security_payments_proj)
    net_wealth_proj = projection.households_net_labour_income_over_time(gross_labour_income_proj, social_security_payments_proj)
    social_benefits_proj = projection.households_social_benefits(years)
    net_operating_surplus_proj = projection.households_net_operating_surplus(years)

    # net_lending_proj = projection.households_net_lending(gross_savings_proj)
    liabilities_proj = projection.households_financial_liabilities_over_time(years)
    dl_by_year = liabilities_proj.diff("Year", label="upper").reindex(Year=years, fill_value=0)

    variation_financial_assets_proj = projection.variation_households_financial_assets(dl_by_year)

    property_income_paid = projection.households_property_income_paid_over_time(years, liabilities_proj)
    assets_proj = projection.households_financial_assets_over_time(years, liabilities_proj)
    property_income_received = projection.households_property_income_received_over_time(years, assets_proj,
                                                                                        capitalstock_proj)
    taxable_income_proj = projection.taxable_income_over_time(net_labor_income_proj, social_security_payments_proj,
                                                   net_operating_surplus_proj, property_income_received,
                                                   social_benefits_proj)
    delayed_taxable_income_proj = projection.delayed_households_taxable_income_over_time(taxable_income_proj)
    income_tax_proj = projection.households_income_tax(delayed_taxable_income_proj)
    wealth_tax_proj = projection.households_wealth_tax_over_time(net_wealth_proj)
    disposable_income_proj = projection.households_disposable_income(net_labor_income_proj, social_benefits_proj, income_tax_proj, property_income_received, property_income_paid, wealth_tax_proj)
    gross_savings_proj = projection.households_gross_savings(disposable_income_proj)

    delayed_disposable_income_proj = projection.delayed_households_disposable_income_over_time(net_labor_income_proj, social_benefits_proj, income_tax_proj,
                                                   property_income_received, property_income_paid, wealth_tax_proj,
                                                   delay=1)

    net_wealth_proj = projection.households_net_wealth_over_time(years, liabilities_proj, assets_proj, capitalstock_proj)

    fuel_transport_consumption_proj = projection.consumption_households_fuel_transport(disposable_income_proj)
    air_transport_consumption_proj= projection.consumption_households_air_transport(disposable_income_proj)

    gov_revenue_transport_proj = projection.tax_revenue_transport_consumption_hh(fuel_transport_consumption_proj, air_transport_consumption_proj)

    gov_revenue_proj = projection.government_revenue_over_time(social_benefits_proj, income_tax_proj, wealth_tax_proj, gov_revenue_transport_proj)
    gov_revenue_total_by_country = gov_revenue_proj.sum(dim="HOUSEHOLDS_I")

    gov_investment_proj = projection.government_investment_per_household_type(capitalstock_proj)
    gov_primary_expenditure = projection.government_primary_expenditure_over_time(social_benefits_proj, gov_investment_proj)
    gov_budget = projection.government_budget_over_time(years, gov_primary_expenditure, gov_revenue_proj)

    gov_debt_total_by_country = gov_budget["debt"].sum(dim="HOUSEHOLDS_I")
    gov_interest_total_by_country = gov_budget["interest"].sum(dim="HOUSEHOLDS_I")
    gov_deficit_total_by_country = gov_budget["deficit"].sum(dim="HOUSEHOLDS_I")
    gov_expenditure_total_by_country = gov_budget["expenditure"].sum(dim="HOUSEHOLDS_I")

    # print (gov_budget["debt"].sel(Year=2025))
    # print(gov_budget["interest"].sel(Year=2025))
    # print(gov_budget["expenditure"].sel(Year=2025))
    # print(gov_budget["deficit"].sel(Year=2025))
    # print("Gov Revenue 2025")
    # print(gov_revenue_proj.sel(Year=2025))
    # print(gov_budget["debt"].sel(Year=2024))
    # print(gov_primary_expenditure.sel(Year=2025))
    # print(gov_revenue_total_by_country.sel(Year=2050))

    # print(gov_revenue_proj.sel(Year=2016))
    # print(gov_primary_expenditure.sel(Year=2016))
    # print(gov_budget["deficit"].sel(Year=2016))
    # print(gov_budget["interest"].sel(Year=2016))

    # for country in gov_interest_total_by_country.coords["REGIONS_I"].values:
    #     gov_interest_total_by_country.sel(REGIONS_I=country).plot(label=str(country))
    #
    # plt.legend(title="Country")
    # plt.title("Interest over time — total by country")
    # plt.xlabel("Year")
    # plt.show()


    # print(fuel_transport_consumption_proj.sel(Year=2050))
    # print(air_transport_consumption_proj.sel(Year=2050))
    # print(disposable_income_proj.sel(Year=2050))
    # print(taxable_income_proj.sel(Year=2030))
    # print("Net labor Income:")
    # print(net_labor_income_proj.sel(Year=2030))
    # print("Social benefits:")
    # print(social_benefits_proj.sel(Year=2030))
    # print("Income Tax:")
    # print(income_tax_proj.sel(Year=2030))
    # print("Property Income received:")
    # print(property_income_received.sel(Year=2030))
    # print("Property income paid")
    # print(property_income_paid.sel(Year=2030))
    # print("Wealth Tax:")
    # print(wealth_tax_proj.sel(Year=2040))
    # print("Disposable Income:")
    # print(disposable_income_proj.sel(Year=2040))
    # print("Financial Liabilities")
    # print(liabilities_proj.sel(Year=2040))


# for hh in air_transport_consumption_proj["HOUSEHOLDS_I"].values:
#     air_transport_consumption_proj.sel(REGIONS_I="IT", HOUSEHOLDS_I=hh) \
#         .plot(x="Year", label=str(hh))
#
# plt.legend()
# plt.title("Air transport consumption — IT by household")
# plt.show()

# for hh in air_transport_consumption_proj["HOUSEHOLDS_I"].values:
#     air_transport_consumption_proj.sel(REGIONS_I="FR", HOUSEHOLDS_I=hh) \
#         .plot(x="Year", label=str(hh))
#
# plt.legend()
# plt.title("Air transport consumption — FR by household")
# plt.show()

# for hh in fuel_transport_consumption_proj["HOUSEHOLDS_I"].values:
#     fuel_transport_consumption_proj.sel(REGIONS_I="FR", HOUSEHOLDS_I=hh) \
#         .plot(x="Year", label=str(hh))
#
# plt.legend()
# plt.title("Fuel-based transport consumption — FR by household")
# plt.show()

for country in air_transport_consumption_proj.sum(dim="HOUSEHOLDS_I").coords["REGIONS_I"].values:
    air_transport_consumption_proj.sum(dim="HOUSEHOLDS_I").sel(REGIONS_I=country).plot(x="Year", label=str(country))

plt.legend(title="Country")
plt.title("Air transport consumption — by country (total)")
plt.xlabel("Year")
plt.show()

