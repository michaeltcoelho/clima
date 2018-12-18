### A client for scraping weather data from Climatempo

### Requirements

* Python 3.7.1.
* An activated python virtualenv.

#### Considering you have already installed the requirements:

### Installing clima

Clone the repository and install it:

```bash
git clone https://github.com/michaeltcoelho/clima.git
```

Go to `/clima` directory:

Run the following command:

```bash
make install
```

### Testing

Running tests:

```bash
make test
```

### Displaying brazilian cities in alphabetical order

See help:

```bash
clima show --help
```

You gonna see the following output:

```bash
Usage: clima show [OPTIONS]

  Display a given number of brazilian cities weather data ordered.

Options:
  --concurrency INTEGER
  --limit INTEGER
  --help                 Show this message and exit.
```

You can pass as options the number of concurrent scrapers running and the number of cities
you want to scrape.

```bash
clima show --concurrency 2 --limit 2
```

Result:
```bash
+---------------+-------+----------+---------------+---------------+-----------+
|     City      | State |  Month   | Min. Temp. (˚ | Max. Temp. (˚ | Rain (mm) |
|               |       |          |      C)       |      C)       |           |
+---------------+-------+----------+---------------+---------------+-----------+
| Abadia de Goi |  GO   | Dezembro |      21       |      29       |    264    |
|      ás       |       |          |               |               |           |
+---------------+-------+----------+---------------+---------------+-----------+
```
