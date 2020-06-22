import requests
import re
import psycopg2

from bs4 import BeautifulSoup
from word2number import w2n
from configparser import ConfigParser

def scraping_data(soup):
    td = soup.findAll('td')
    for row in reversed(td):
        for link in row.findAll('a'):
            covid_bulletin_news = link.string
            bulletin_number = covid_bulletin_news[19:22]
            if("COVID-19 Bulletin" in covid_bulletin_news):
                if(int(bulletin_number) > 114):
                    covid_news = link.get('href')
                    covid_news_link = requests.get(covid_news)
                    soup_link = BeautifulSoup(
                    covid_news_link.text, 'html.parser')
                    for paragraph in soup_link.select('.content-section'):
                        announcement = paragraph.div.text
                        dates = paragraph.findAll(
                            'span', attrs={'class': 'article_date'})
                        match = re.search(
                            r'Public health officials advise (\S+)', announcement)
                        that_case = re.search(
                            r'Public health officials advise that(\S+)', announcement)
                        rematch = re.search(r'(\S+) new', announcement)
                        additional_case = re.search(
                            r'(\S+) additional case', announcement)

                        if(that_case):
                            cases = w2n.word_to_num(that_case.group(1))
                            for date in dates:
                                date_text = date.text
                        else:
                            if match:
                                if(match.group(1) != "there"):
                                    if(match.group(1) != "no"):
                                        if(match.group(1) == "an"):
                                            cases = 1
                                        elif(match.group(1) == "as"):
                                            cases = 0
                                        else:
                                            cases = (match.group(1))
                                    else:
                                        cases = 0
                                    for date in dates:
                                        date_text = date.text
                                else:
                                    if additional_case:
                                        cases = w2n.word_to_num(additional_case.group(1))
                                    else:
                                        if(rematch.group(1) != "no"):
                                            cases = w2n.word_to_num(rematch.group(1))
                                        else:
                                        	cases = 0
                                    for date in dates:
                                        date_text = date.text
    return date_text, cases

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))
    return db

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def insert_new_case(case_data, num_case):
    sql = """INSERT INTO covid19_scraping_data_table (date, cases)
             VALUES(%s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (case_data, num_case))
        # get the generated id back
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def main():
    response = requests.get('https://www.gov.mb.ca/health/newsreleases/index.html')
    soup = BeautifulSoup(response.text, 'html.parser')

    connect()
    date, cases = scraping_data(soup)
    insert_new_case(date,cases)

main()