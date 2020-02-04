import sys
import csv
import math

def round_half_up(n):
    '''
    input: float
    output: int
    ------------
    Alternative to the default python3 round() function - which uses a 'Bankers Rounding' (i.e round(2.5) = 2)
    This function will instead round half values up (i.e round_half_up(2.5) = 3)
    '''
    return int(math.floor(n + 0.5))

def get_prev_month(date_string):
    """
    input: string
    output: string
    ------------
    """
    date_split = date_string.split('/')
    month = int(date_split[0])
    year = int(date_split[2][0:4])

    prev_date = ''
    if month == 1:
        year -= 1
        prev_date =  '12/01/' + str(year) + date_split[2][4:]
    else:
        month -= 1
        prev_date =  '{:02}/01/'.format(month) + date_split[2]

    return prev_date

def date_order(date_string):
    """
    input: string
    output: float
    ------------
    Converts date string into float that can be used to order output by date
    """
    date_split = date_string.split('/')
    month = int(date_split[0])
    year = int(date_split[2][0:4])
    return year+(month*0.01)

def get_group_sum(reader, group_by_list):
    '''
    input: sting, list
    output: dict
    ------------
    Constructs a dictionary with a key determined by the provided groups
    and gets the sum of 'Value' per group
    '''
    col_names = next(reader)
    iter_dict = (dict(zip(col_names, row)) for row in reader)

    agg_dict = {}
    for item in iter_dict:
        item_key = tuple(item[group] for group in group_by_list) #TODO: Add exception handling
        item_value = int(item['Value']) #TODO: Add exception handling

        if item_key not in agg_dict.keys():
            agg_dict[item_key] = item_value
        else:
            agg_dict[item_key] += item_value
    return agg_dict

def get_rolling_avg(agg_dict):
    '''
    input: dict (tuple:int)
    ouput: list
    ------------
    Returns a list of lists with the calculated rolling average per group.
    Rolling average defined as: sum(total_past_values) / count(total_past_months)
    ------------
    Note: This function assumes that in order for an average to be rolling prior
    months must consecutive. Non-consecutive months will result in that rolling
    average resetting.
    '''
    avg_list = []
    for current in agg_dict.items():
        num_months = 0
        total_value = 0

        border = current[0][0]
        cross_time = get_prev_month(current[0][1])
        measure = current[0][2]

        past_key = (border,cross_time,measure)
        while past_key in agg_dict:
            num_months += 1
            total_value += agg_dict[tuple(past_key)]

            past_key = (border,get_prev_month(past_key[1]),measure)

        average = 0 if num_months < 1 else round_half_up(total_value / num_months)

        current_list = list(current[0])
        current_list.extend([current[1],average])
        avg_list.append(current_list)
    return(avg_list)

def main():
    with open(sys.argv[1], 'r') as input_file:
        file_reader = csv.reader(input_file, delimiter=',')
        crossing_sum = get_group_sum(file_reader, ['Border','Date','Measure'])

    #Sort list by desc order: Date, Value, Measure, Border
    crossing_avg = get_rolling_avg(crossing_sum)
    crossing_avg = sorted(crossing_avg, key = lambda x: (date_order(x[1]),x[3],x[2],x[0]), reverse = True)

    with open(sys.argv[2], 'w') as output_file:
        file_writer = csv.writer(output_file)
        file_writer.writerow(['Border','Date','Measure','Value','Average'])
        for line in crossing_avg:
            file_writer.writerow(line)

if __name__ == "__main__":
    main()
