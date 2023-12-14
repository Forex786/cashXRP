import ast
from icecream import ic
import random
import matplotlib.pyplot as plt

from class_mySQL import MySQLConnector

def display_dynamic_bar_graph():

    mydb = MySQLConnector()

    myData = ast.literal_eval(mydb.get_DashboardData())

    categories = []
    values = []
    for i in myData:
        categories.append(i[0])
        values.append(i[1])

    ic(categories)
    ic("original", values)

    # Create a bar graph
    fig, ax = plt.subplots()
    fig.set_facecolor('#2E2E2E')  # Set light grey window background color

    ax.set_facecolor('#2E2E2E')  # Set dark grey plot background color

    bars = ax.bar(categories, values, color=['lightgreen', 'orange', 'red', 'purple', 'darkblue', 'green'])
    plt.ylim(0, 100)

    # Adding labels and title with white text color
    ax.set_xlabel('Tx Status', color='white')
    ax.set_ylabel('Tx count', color='white')
    ax.set_title('cashXRP Tx running counts', color='white')

    # Set tick labels color to white
    ax.tick_params(axis='both', colors='white')

    plt.ion()  # Enable interactive mode

    text_objects = []  # To store the text objects for removal

    while True:

        nvalues = [v for v in values]

        # Remove previous text objects
        for text in text_objects:
            text.remove()
        text_objects = []  # Clear the list

        # Update the bar heights and add data values as text
        for bar, new_value in zip(bars, nvalues):
            bar.set_height(new_value)
            text = ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(new_value),
                           ha='center', va='bottom', color='white')  # Set text color to white
            text_objects.append(text)

        # Pause for a moment to visualize the update
        plt.pause(2)
        mydb = MySQLConnector()
        myData = ast.literal_eval(mydb.get_DashboardData())

        values = []
        for i in myData:
            values.append(i[1])

        # ic(values)
        mydb.close_connection()

    plt.ioff()  # Disable interactive mode
    plt.show()

if __name__ == "__main__":
    display_dynamic_bar_graph()
