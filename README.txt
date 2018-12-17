In order to run this flask application you have to add the following export:

	(Mac, Linux) export OAUTHLIB_INSECURE_TRANSPORT=1

	(Windows) $env:OAUTHLIB_INSECURE_TRANSPORT = "1"

In order for the application to work properly you will also have to make sure you fill out every portion of the form or else, the Spotify GET request and a few other functions will fail.