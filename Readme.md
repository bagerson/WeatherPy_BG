
## WeatherPy Readme
### Benjamin Gerson 

* #### Design Features Attempted

Because the API call takes some time and it is not always clear from Jupyter Notebook whether the code is still running, I tried several design features to indicate the progress of the API calls.

I installed [Progress](https://pypi.org/project/progress/) which proved effective if the raw .py file was run in terminal: ![Progress Bar](https://github.com/bagerson/WeatherPy_BG/blob/master/Resources/Screen%20Shot%202019-06-03%20at%202.45.50%20PM.png "Screenshot from Terminal")

However, because the program is currently designed to run in Jupyer Notebook I removed the progress bar and used a counter whih indicated each 100 iterations:

```
if:
    counter % 100 == 0
    print(counter)
```

Which returned
```
100
200
400
....
```
This reduced the output for debugging purposes and proved easy to adapt to the log output required.

* #### Exception Handling

The initial exception where citipy returns a city that is not tracked by the OpenWeather API is immediately obvious:
![City Exception](https://github.com/bagerson/WeatherPy_BG/blob/master/Resources/WeatherPy_Exception.png "Exception Screenshot")

However it is also worth noting that the actual data may have errors.  In one iteration, the OpenWeather API returned a humidity value in excess of 100% which is not possible:

![Humidity Error](https://github.com/bagerson/WeatherPy_BG/blob/master/Resources/Screen%20Shot%202019-06-03%20at%204.55.50%20PM.png "Humidity Error")

It stands to reason that weather stations all over the world may occaisionally have technical problems, or that data is lost in transmission.  There may be future improvements whereby the data is checked for such irregularities before plotting.





```python

```
