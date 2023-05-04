# Prerequisite

- [selenium](https://pypi.org/project/selenium/)
- [virtualenv](https://pypi.org/project/virtualenv/)

# Virtual Environment

```
virtualenv name

source name/bin/activate
```

# Install Requirements

```python
pip install -r requirement.txt
```

# Run Project

```python
python3 get_basic_data
```

# Description

Here I am searching jobs for Python Developer at Ahmedabad, Gujarat, India location on LinkedIn.
The url is "https://in.linkedin.com/jobs/search?keywords=Python%20Developer&location=Ahmedabad%2C%20Gujarat%2C%20India&geoId=104990346&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
"

LinkedIn has a feature of Infinite scrolling which means when user visits the page, he sees some data. And the other data is loaded if user scrolls down on runtime.
Once the scrolling is done, a button appears which loads other data. Once the whole data is loaded, the page finally ends.

The job details like Position, Company Name, Location and Benefits are being scraped and stored in Database.
