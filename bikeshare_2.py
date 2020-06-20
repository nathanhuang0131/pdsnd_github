import pandas as pd
import time
import numpy as np

from datetime import datetime, timedelta
CITY_DATA= { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input('Which city\'s data you would like to see: Chicago, New York or Washington?')

    # TO DO: get user input for month (all, january, february, ... , june)
    q=input('Do you like to see month, day  or Both or none (no day and month filter)?')
    if q.lower() == 'none':
        month="none"
        day="none"
        print(q)
    elif q.lower()=='month':
        month=input("Which month would you like to see eg. Jan, Feb, Mar, Apr, May, Jun")
        day='none'
        print(q)
    elif q.lower()=='day':
        day=input('which date you would like to select: Monday, Tusesday, Wednesday, Thursday, Friday, Saturday, Sunday')
        month='none'
    else:
        month=input("Which month would you like to see eg. Jan, Feb, Mar, Apr, May, Jun")
        day=input('which date you would like to select: Monday, Tusesday, Wednesday, Thursday, Friday, Saturday, Sunday')
        print(q)
    print('-'*40)
    return city, month, day
def print_filters(city, month,day):
    if month == "none":
        month='All months'
    if day == 'none':
        day='All days in a week'
    print('filter is------- city: {}    month:{}    day: {}'.format(city,month,day))

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "both" to apply no month filter
        (str) day - name of the day of week to filter by, or "both" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if  month !='none':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if  day !='none':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel.
       If select "both" no month or day will be calculated as they have been
       selected"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'none':
        populer_month=df['month'].value_counts()
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
    #    month='All months'
        print("the most popular month is --------"+ months[populer_month.index[0]-1])
        print("the number of records in {} is {}".format(months[populer_month.index[0]-1],populer_month.values[0]))
    else:
        print('\nAs you selected month, {} is the month you filtered'.format(month))
    # TO DO: display the most common day of week
    if day == 'none':
        populer_day = df['day_of_week'].value_counts()
        print("the most popular day in selected months is --------"+ populer_day.index[0])
    else:
        print('\nAs you selected day of week, {} is the day of week you filtered'.format(day))
    #    day='All days in a week'

    # TO DO: display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts()
    print('the most common start hour is ------' + str(popular_hour.index[0]))
    #print('filter is------- city: {}    month:{}    day: {}'.format(city,month,day))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    #if month == "none":
    #    month='All months'
    #if day == 'none':
    #    day='All days in a week'
    # TO DO: display most commonly used start station
    popular_station=df['Start Station'].value_counts()
    print("Most popular start station is ------" +  popular_station.index[0])
    print('count number is {} times'.format(popular_station[0]))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].value_counts()
    print("most popular end station is ------" + popular_end_station.index[0])
    print('count number is {} times'.format(popular_end_station[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df['Start_End_Station'] = 'From ' + df['Start Station'].values+  ' to ' + df['End Station'].values
    print('The most popular combination station from start to end is ------' +  df['Start_End_Station'].value_counts().index[0])
    print('count number is {} times'.format(df['Start_End_Station'].value_counts()[0]))
    #print('filter is------- city: {}    month:{}    day: {}'.format(city,month,day))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    #if month == "none":
    #    month='All months'
    #if day == 'none':
    #    day='All days in a week'
    # display total travel time
    travel_duration=df['End Time'].subtract(df['Start Time'],fill_value=0)

    print("The total travel time is -------" + str(travel_duration.sum().total_seconds()) + ' seconds')

    # display mean travel time
    print("average travel time is ------" + str(travel_duration.mean().total_seconds())+' seconds')

    #print('filter is------- city: {}    month:{}    day: {}'.format(city,month,day))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types= df['User Type'].value_counts()
    print('user types are: \n')
    print(user_types)

    # Display counts of gender
    if city.lower() !='washington':
        gender_counts = df['Gender'].value_counts()
        print("\ngender distributions are \n")
        print(gender_counts)
    else:
        print('Washington does not have gender information')


    # Display earliest, most recent, and most common year of birth
    if city.lower()!='washington':
        year_birth = df['Birth Year'].value_counts()
        earliest_year_birth = df['Birth Year'].min()
        print('\n The earliest year of birth is ' + str(int(earliest_year_birth)))
        print('The most rescent year of birth is {}'.format(int(df['Birth Year'].max())))
        print('the most common year of birth is {} '.format(str(int(year_birth.index[0]))))
        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print('washington does not have birth information.')
    print('-'*40)
def view_line_detail(df):
    """Display detail lines to user"""
    """ five lines each time until stop. """
    user_input=input('Do you want to see detial lines? Tyep "Yes" to see five lines or type "No" to stop')
    i=0
    while True:
        print(df.iloc[i:i+5,:])
        i+=5
        user_input=input('Do you want to see detial lines? Tyep "Yes" to see five lines or type "No" to stop')
        if user_input.lower() != 'yes':
            break


def main():
    while True:
        #try and test error
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            time_stats(df,month,day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)
            print_filters(city,month,day)
            view_line_detail(df)
        except ValueError:
            print("Your entry is not eligible: Only cities indicated \" chicago, new york, washington is eligible")
            print("only months abbreviation or both/none are eligible; only full weekday such as Sunday is eligible.")
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
