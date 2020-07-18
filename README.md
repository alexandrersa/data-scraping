# Dockerizing feature to crawling website.

**What is this project?**

Application developed with the aim of dynamically detecting the path of the website's logo, in addition to dynamically searching phone numbers in a URL list.

## How use this project?

1. Clone this project.
2. Open them in your terminal.
3. Set execution permissions for the start.sh and stop.sh scripts.
    ```sh
   $ chmod +x start.sh stop.sh
   ```
4. Build the image and run the container

    ```sh
    $ ./start.sh
    ```

4. Or you can simply start your compose enviornment:

    ```
    $ docker-compose -f .docker/docker-compose.yml up -d --build
    ```

Now you can run 
    ```
    cat websites.txt | docker run -i crawler
    ```
and will return a list of paths.

5. Stop your environment

    ```sh
    $ ./stop.sh
    ```
   