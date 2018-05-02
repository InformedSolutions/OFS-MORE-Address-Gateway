# Addressing Gateway API

A RESTful web service, enabling integration with the OS Places API using HTTP protocols alone.

## Running the solution
To run the Addressing Gateway API you must first pull all python dependencies by running `pip install -r requirements.txt`.

Once these dependencies have been gathered, you can run the service itself by issuing the command `python manage.py runserver`. After running this command, the Addressing Gateway API will be made available (using the default Django port) on http://localhost:8000.

## Supported methods

For detail of the methods support by this API and how to use them, please see Swagger documentation provided on the path http://localhost:8000/addressing-gateway/static/swagger/index.html. Alternatively, you can generate offline documentation for ease of sharing by following the steps outlined below.

## Generating offline documentation

For easily generating offline documentation (a representation of the swagger interface content), the following steps should be taken:

1. Open the online Swagger.io editor available at http://editor.swagger.io/
2. Import the /application/static/swagger/swagger.json contained in this repository
3. Select 'Generate Client' - 'Html' in the Swagger.io editor to download a print friendly HTML representation of the spec
4. Open the packaged HTML page in a web browser
5. Use your browser's print to PDF function to automatically generate documentation that can be easily shared