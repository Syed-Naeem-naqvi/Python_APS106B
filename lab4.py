##############################
# APS106 Winter 2022 - Lab 4 #
##############################

import math


def heat_control_hysteresis_thresh(temp_measured, current_state, temp_desired, alpha):
    """
    (float, bool, float, float) -> bool

    Implement a hysteresis threshold to determine and return the
    next state of the heater using the current state, latest measurement,
    desired temperature, and hyteresis buffer range (+/- alpha).

    >>> heat_control_hysteresis_thresh(33.2, True, 40.0, 5.0)
    True

    >>> heat_control_hysteresis_thresh(28.4, True, 27.5, 1.0)
    True

    >>> heat_control_hysteresis_thresh(50.6, True, 40.0, 10.0)
    False

    >>> heat_control_hysteresis_thresh(30.8, False, 40.0, 2.9)
    True

    >>> heat_control_hysteresis_thresh(50, True, 70, 10)
    True
    >>> heat_control_hysteresis_thresh(50, False, 70, 10)
    True

    >>> heat_control_hysteresis_thresh(50, True, 60, 10)
    True
    >>> heat_control_hysteresis_thresh(50, False, 60, 10)
    False

    >>> heat_control_hysteresis_thresh(70, True, 50, 10)
    False
    >>> heat_control_hysteresis_thresh(70, False, 50, 10)
    False

    >>> heat_control_hysteresis_thresh(60, True, 50, 10)
    True
    >>> heat_control_hysteresis_thresh(60, False, 50, 10)
    False

    >>> heat_control_hysteresis_thresh(55, False, 50, 10)
    False
    >>> heat_control_hysteresis_thresh(55, True, 50, 10)
    True

    >>> heat_control_hysteresis_thresh(50, True, 55, 10)
    True
    >>> heat_control_hysteresis_thresh(50, False, 55, 10)
    False

    """

    # TODO Write your code here
    # Change the state of the heater, depending on if the temperature is higher or lower than the desired value
    if temp_measured < (temp_desired - alpha):
        current_state = True
    elif temp_measured > (temp_desired + alpha):
        current_state = False
    elif abs(temp_measured - temp_desired) <= alpha:  # If the temperature difference is within tolerance, keep the state as is.
        current_state = current_state

    # Output the new state of the heater
    return current_state


def newton_raphson_sqrt(n, epsilon):
    """
    (float,float) -> float

    Calcualtes the square root of a number, n, using the Newton-Raphson method.
    Returned value is the square root of n within tolerance amount
    specified by epsilon.

    >>> newton_raphson_sqrt(4.0,0.001)
    2.0

    >>> newton_raphson_sqrt(2.0, 0.1)
    1.417

    >>> newton_raphson_sqrt(9.0, 0.01)
    3.0
    >>> newton_raphson_sqrt(9.0, 0.2)
    3.024
    >>> newton_raphson_sqrt(9.0, 2.6)
    3.4
    """

    # TODO Write your code here
    # start with the initial condition x_n = 4
    x_n = n

    # While the |x^2 - n| >= epsilon, keep generating a new x_n term
    # Using newtons method.
    while abs(x_n ** 2 - n) >= epsilon:
        x_n = 1 / 2 * (x_n + n / x_n)
    # Once the value of sqrt(n) is accurate enough, round it off to three decimals and return.
    x_n = round(x_n, 3)
    return x_n


def get_sensor_measurement(t, c0, c1, c2, c3, c4):
    """
    (float,float,float,float,float,float) -> float

    Simulates a sensor value reading. The value returned by the
    function is generated by from the following equation:

        s(t) = c0*t + c1*sqrt(t) + c2*sin(t) + c3*cos(8t) + c4

    where t, c0, c1, c2, c3, and c4 are parameters passed into the function.
    The returned value is rounded to 3 decimal points.

    DO NOT EDIT THIS FUNCTION
    """
    measurement = c0 * t + c1 * newton_raphson_sqrt(abs(t), 0.0005) + c2 * math.sin(t) + c3 * math.cos(8 * t) + c4
    return round(measurement, 3)


def thresh_crossing_counter(temp_desired, hyst_alpha,
                            t_start, t_stop,
                            c0, c1, c2, c3, c4):
    """
    (float, float, float, float, float, float, float, float, float) -> int

    Counts the number of times a simulated sensor measurement crosses a
    hysteresis threshold.

    >>> thresh_crossing_counter(0.0, 0.2, 0.0, 10.01, -0.1, 2.0, 10.0, -5.0, -1.0)
    10
    >>> thresh_crossing_counter(0.0, 0.2, 0.0, 1, -0.1, 2.0, 10.0, -5.0, -1.0)
    1
    >>> thresh_crossing_counter(0.0, 0.2, 0.0, 4, -0.1, 2.0, 10.0, -5.0, -1.0)
    4
    >>> thresh_crossing_counter(0.0, 3, 0.0, 4, -0.1, 2.0, 10.0, -5.0, -1.0)
    2
    >>> thresh_crossing_counter(5.0, 0.2, 0.0, 10.01, -0.1, 2.0, 10.0, -5.0, -1.0)
    11

    """
    t_step = 0.05  # amount to increment the time after each sensor reading

    # Initialize the state
    # simply compare to the desired temperature because we don't yet know
    # the current state to use the hysteresis threshold
    state = get_sensor_measurement(t_start, c0, c1, c2, c3, c4) <= temp_desired

    # TODO Write your code to complete the function here
    number_of_state_changes = 0  # Initialize a counter to count the number of heater state changes.
    operation_state = temp_desired < state # The initial operation state of the heater (a boolean) is simply found by comparing the current temperature to the desired one.

    while t_stop >= t_start: # Start at the start time and count up to the end time by a step of t_step.
        state = get_sensor_measurement(t_start, c0, c1, c2, c3, c4)  # Obtain the temperature using the mock heater simulation
        new_state = heat_control_hysteresis_thresh(state, operation_state, temp_desired, hyst_alpha) # Now, the new state is found by using the first function.
        if new_state != operation_state:  # A state change is counted if the new state is different than the previous one.
            number_of_state_changes += 1
            operation_state = new_state  # Make the new state the current one
        t_start += t_step  # Add the time step

    # Return the number of steps counted to the outer scope.
    return number_of_state_changes


if __name__ == '__main__':
    import doctest
    doctest.testmod()