# garden_net

This is a toy project I have been playing with to create a network of sensors running on [cheap wifi enabled microcontrollers](https://www.amazon.com/ESP8266-Internet-Development-Wireless-Micropython/dp/B07RNX3W9J/ref=sr_1_5?keywords=esp8266+nodemcu&qid=1691991787&sprefix=esp8%2Caps%2C508&sr=8-5). Using a raspberry pi to serve as a data store and control center for monitoring and eventually controlling the power to several outlets using [power relays](https://www.amazon.com/SunFounder-Channel-Shield-Raspberry-Arduino/dp/B00DR9SE4A/?_encoding=UTF8&pd_rd_w=8xnGa&content-id=amzn1.sym.5f7e0a27-49c0-47d3-80b2-fd9271d863ca%3Aamzn1.symc.e5c80209-769f-4ade-a325-2eaec14b8e0e&pf_rd_p=5f7e0a27-49c0-47d3-80b2-fd9271d863ca&pf_rd_r=XMEZSB9V5AEZHAHAHF6X&pd_rd_wg=PeAz1&pd_rd_r=5ebf2999-5c92-4ab2-baae-1a1c6eec105a&ref_=pd_gw_ci_mcx_mr_hp_atf_m&th=1) based upon customizable rules about the data gathered from the sensors.

This is acheived by each microcontroller hosting a simple http server that responds with the latest data from the sensor or sensors connected. Which are gathered by sentry.py as service based upon configuration set up in the control center. Which will then evaluate the rules and either directly or through a publish subscribe system take any action that is required.

If you are interested in the project for whatever reason there is docker-compose.yml under control_center that will stand up the back end as I use it for development from there you can shell into the container and run the `init_db()` and `populate_dev_data()` methods from `app/db.py`. And the UI has been made under node 18 `npm -install` `npm start dev` should get things running from the ui folder.

Also please put away any pitchforks regarding the server being evoked with the call to python because again this container is only for developments purposes.
