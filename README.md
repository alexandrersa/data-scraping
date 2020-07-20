# Dockerizing feature to crawling website.

**What is this project?**

Application developed with the aim of dynamically detecting the path of the website's logo, in addition to dynamically searching phone numbers in a URL list.

## How use this project?

1. Clone this project.
2. Open them in your terminal.
3. Set execution permissions for the build.sh and stop.sh scripts.
    ```sh
   $ chmod +x build.sh stop.sh
   ```
4. Build the image and run the container

    ```sh
    $ ./build.sh
    ```

4. Or you can simply execute on data-scraping folder. 
    After executing this command, your environment will be reflected in the container you created now.:
    Then replace the existing list of sites with other sites of your choice.
    
    ```
    $ docker run -v crawler:/usr/src/app -it data-scraping_crawler /bin/bash
    ```

5. In this step will appear a console into docker container, then run.

    ```
    $ cd crawler
    $ cat crawler/spiders/websites.txt | scrapy crawl Crawler
    ```
    
There, now you can consult your file with the logo of the company you want, in addition to the contacts.

 If you want to stop the environment, just type in the ```exit()``` terminal.

7. To disable the docker instance, just execute the command below.

    ```sh
    $ ./stop.sh
    ```
   