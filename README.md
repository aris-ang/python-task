# Python Coding Task

## Project Description

This is my python implementation of the "citybike Wien Importer" coding task.

The application performs both steps of the task as described
- Retrieves the list of the bike stations from the designated endpoint, transforms and sorts it according to the specified criteria (step 1).
- Updates each bike station in the list with its address field, retrieved from the designated endpoint using the station's location (step 2).

For step one, i have separated the list transformation and sorting steps into two separate functions.
The reason for this (aside from single-responsibility) is to make it possible to use different sorting algorithms, if so desired.
I have used python's `sorted` function which according to python's documentation implements the `timsort` algorithm under the hood.
It took **`sorted` a maximum 0.001 seconds** to sort the list, which looks pretty good so i decided to keep it.

To implement step two, we have to perform a request for the location of each bike station in the list.
Naturally, if these requests are performed sequentially, the process will become quiet time-consuming.

To prevent bottleneck at this point, i have taken advantage of the asyncio package's `gather` function. **I have made use of `gather`
to send the HTTP requests** for all the stations at the same time, then used the list of addresses (responses) to populate the bike station
dictionaries with them.

As a result of the above, the whole process of the citybike Wien Importer completes in sub-second speed average time.

### IMPORTANT
During development, i observed that the `nearby address` endpoint returned status 429 due to the multiple concurrent requests.
I have created a separate branch named `rate_limit` in which i have modified the request mechanism to prevent 429 responses,
but the results take substantially longer to retrieve.
## Installation and Usage

To install the project, first use `git clone` to get it from the git repo.
All python requirements are installed by running `pip install -r requirements.txt` at the project's root directory.
After the requirements' installation, simply run `python main.py`.

### Configuration
All endpoints used for retrieving information about the citybike stations are kept as environment variables in a `.env` file. For security reasons, this file
is not included in version control, however you can use `.env.example` as a reference to create it before starting the application.
## Documentation

To automatically generate the project's documentation using Sphinx, run `.\make.bat html` from the project's `docs` directory.