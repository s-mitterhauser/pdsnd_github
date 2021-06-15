import time
import calendar
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city would you like to explore? Please enter Chicago, New York City or Washington: ').lower()
        if city in CITY_DATA:
            print('\nOkay, let\'s explore {}!\n'.format(city.title()))
            break
        else:
            print('\nThe entered city is not available, please try again!\n')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month_number = int(input('Would you like to filter by month? If yes, please choose from 1 to 6 or enter 0 for no filter: '))
            month = calendar.month_name[month_number].lower()
        except ValueError:
            print('\nNo valid date was entered. Please try again and make sure you enter a number between 1 and 6 or 0 for all.\n')
            continue
        if month_number >0 and month_number <7:
            print('\nThe data will now be filtered by {}!\n'.format(month.title()))
            break
        if month_number == 0:
            print('\nYou chose all and no month filter is set.\n')
            break
        if month_number >6 and month_number <13:
            print('\nSorry, but there is no data available for {}! The only available months are January till June.\n'.format(month.title()))
            continue
        else:
            print('\nNo valid date was entered. Please try again and make sure you enter the correct month number (1 - January; 6 - June) or 0 for all.\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = input('Would you like to filter by weekday? If yes, please enter the day (Monday-Sunday) or enter all for no filter: ')
            days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            if day.title() in days:
                print('\nThe data will now be filtered by {}!\n'.format(day).title())
                break
            if day.lower() == 'all':
                print('\nYou chose all and no weekday filter is set.\n')
                break
            else:
                print('\nNo valid day was entered. Please make sure you entered the full day name or "all".\n')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != "":
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Frequent Month:', calendar.month_name[popular_month].title())

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Frequent Day of Week:', popular_day)

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_comb_stations = df.value_counts(['Start Station', 'End Station'])[:1]
    print('\nMost Frequent Combination of Start and End Station:\n',popular_comb_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum() / 60)
    print('Total Travel Time:', total_travel_time,'Hours')

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    print('Average Travel Time:', mean_travel_time, 'Minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()[:]
    print('Count User Types:\n', user_types)

    if {'Gender', 'Birth Year'}.issubset(df.columns):
    # Display counts of gender
        gender = df['Gender'].value_counts()[:]
        print('\nCount Gender:\n', gender)

    # Display earliest, most recent, and most common year of birth
        earliest_birth = int(df['Birth Year'].min())
        print('\nEarliest Year of Birth:', earliest_birth)
        recent_birth = int(df['Birth Year'].max())
        print('Most Recent Year of Birth:', recent_birth)
        most_com_birth = int(df['Birth Year'].mode()[0])
        print('Most Common Year of Birth:', most_com_birth)

    else:
        print('\nNo gender and birth data available for Washington.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    rows = 0
    while True:
        details = input('Would you like to see more details and access the raw data? Enter yes or no.\n')
        if details.lower() == 'yes':
            print(df.iloc[rows:rows+5])
            rows += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
