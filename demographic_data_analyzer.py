import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv")
    if len(df.isnull()): df = df[~df.isnull()]
    #print(df.head())
    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    df_races = df['race']
    df_races.index = df_races[:,]
    race_count =pd.Series( [df_races[race].count() for race in df_races.unique()], index=df_races.unique() ) # df_races.value_counts()

    # What is the average age of men?
    average_age_men = round(df.loc[(df['sex'] == 'Male')]['age'].mean(),1)

    # What is the percentage of people who have a Bachelor's degree?
    above_education_count, bachelors_education_count = df['education'].count(),df.loc[(df['education'] == 'Bachelors')]['education'].count()

    percentage_bachelors = round(bachelors_education_count/(above_education_count/100.),1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?
    with_advanced = df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    without_advanced_df = df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    countWithAdvanced = len(with_advanced)
    countWithoutAdvanced = len(without_advanced_df)
    countAbove = len(df)
    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = round(countWithAdvanced/(countAbove/100.),1)
    lower_education = round(countWithoutAdvanced/(countAbove/100.),1)
    countWithMoreThan50 = len(with_advanced[with_advanced['salary'].isin(['>50K', '>=50K'])])
    countWithoutMoreThan50 = len(without_advanced_df[without_advanced_df['salary'].isin(['>50K', '>=50K'])])
    # percentage with salary >50K
    higher_education_rich = round((countWithMoreThan50 / countWithAdvanced) * 100, 1)
    lower_education_rich = round((countWithoutMoreThan50 / countWithoutAdvanced) * 100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = (num_min_workers['salary'] == '>50K').mean() * 100
    # What country has the highest percentage of people that earn >50K?
    total_by_country = df['native-country'].value_counts()
    rich_by_country = df.loc[df['salary'] == '>50K']['native-country'].value_counts()
    country_stats = pd.DataFrame({
        'total': total_by_country,
        'rich': rich_by_country
    }).fillna(0)
    #print(country_stats)
    country_stats['percentage'] = (country_stats['rich'] / country_stats['total']) * 100
    highest_earning_country = country_stats['percentage'].idxmax()
    highest_earning_country_percentage = round(country_stats['percentage'].max(),1)
    #highest_earning_country = df.loc[df['salary'] == '>50K']['native-country'].value_counts().index[0]
    #total_high_earners = df['salary'].value_counts()['>50K']
    #highest_earning_country_count = df.loc[df['salary'] == '>50K']['native-country'].value_counts()[highest_earning_country]
    #highest_earning_country_percentage = (highest_earning_country_count / total_high_earners) * 100

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df.loc[(df['salary'] == '>50K') & (df['native-country'] == 'India')]['occupation'].value_counts().index[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
