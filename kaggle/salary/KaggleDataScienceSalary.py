import pandas as pd
import matplotlib.pyplot as plt

# https://www.kaggle.com/datasets/harishkumardatalab/data-science-salary-2021-to-2023
class KaggleDataScienceSalary:
  def __init__(self, file_path):
    self.file_path = file_path
    self.df = pd.read_csv(file_path)
    self.EU = ['BE', 'BG', 'CZ', 'DK', 'DE', 'EE', 'IE', 'EL', 'ES', 'FR', 'HR', 'IT', 'CY', 'LV', 'LT', 'LU', 'HU', 'MT', 'NL', 'AT', 'PL', 'PT', 'RO', 'SI', 'SK', 'FI', 'SE']

  def getDf(self):
    return self.df

  def meanSalaryPerEntryLevel(self, level, eu = False):
    df_by_location = self.df[self.df.company_location.isin(self.EU)] if eu else self.df
    level = df_by_location[df_by_location.experience_level == level]
    return level.groupby('work_year', as_index=False)['salary_in_usd'].mean()
  
  def meanSalaryPerEmploymentType(self, employment_type, eu = False):
    df_by_location = self.df[self.df.company_location.isin(self.EU)] if eu else self.df
    type = df_by_location[df_by_location.employment_type == employment_type]
    return type.groupby('work_year', as_index=False)['salary_in_usd'].mean()
  
  def plotByExperienceLevel(self, eu = False):
    entry = self.meanSalaryPerEntryLevel('EN', eu)
    exp = self.meanSalaryPerEntryLevel('EX', eu)
    middle = self.meanSalaryPerEntryLevel('MI', eu)
    senior = self.meanSalaryPerEntryLevel('SE', eu)
    plt.plot(entry['work_year'], entry['salary_in_usd']/1000, label='Entry-Level')
    plt.plot(exp['work_year'], exp['salary_in_usd']/1000, label='Experienced')
    plt.plot(middle['work_year'], middle['salary_in_usd']/1000, label='Mid-Level')
    plt.plot(senior['work_year'], senior['salary_in_usd']/1000, label='Senior')
    plt.legend()
    plt.xticks(range(2020, 2024, 1))
    plt.xlabel('Year')
    plt.ylabel('Salary, USD (thousands)')
    location = 'Europe' if eu else 'World'
    plt.title(f'Salary trends by exprerience level, {location}')
    plt.show()

  def plotByEmploymentType(self, eu = False):
    full = self.meanSalaryPerEmploymentType('FT', eu)
    part = self.meanSalaryPerEmploymentType('PT', eu)
    contractor = self.meanSalaryPerEmploymentType('CT', eu)
    freelancer = self.meanSalaryPerEmploymentType('FL', eu)
    plt.plot(full['work_year'], full['salary_in_usd']/1000, label='Full-Time')
    plt.plot(part['work_year'], part['salary_in_usd']/1000, label='Part-Time')
    plt.plot(contractor['work_year'], contractor['salary_in_usd']/1000, label='Contractor')
    plt.plot(freelancer['work_year'], freelancer['salary_in_usd']/1000, label='Freelancer')
    plt.legend()
    plt.xticks(range(2020, 2024, 1))
    plt.xlabel('Year')
    plt.ylabel('Salary, USD (thousands)')
    location = 'Europe' if eu else 'World'
    plt.title(f'Salary trends by employment type, {location}')
    plt.show()