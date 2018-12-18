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

### Displaying the first 100 brazilian cities in alphabetical order

```bash
clima show --concurrency=<the number of concurrent workers: default is 5>
```
