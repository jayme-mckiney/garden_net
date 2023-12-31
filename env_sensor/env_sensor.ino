/*********
  Rui Santos
  Complete project details at https://randomnerdtutorials.com  
*********/

// Including the ESP8266 WiFi library
#include <ESP8266WiFi.h>

#include "DHTesp.h"
DHTesp dht;
#ifdef ESP32
#pragma message(THIS EXAMPLE IS FOR ESP8266 ONLY!)
#error Select ESP8266 board.
#endif

// Replace with your network details
const char* ssid = "ssid";
const char* password = "";

// Web Server on port 80
WiFiServer server(80);

// DHT Sensor
const int DHTPin = 10;

// Temporary variables
static char celsiusTemp[7];
static char fahrenheitTemp[7];
static char humidityTemp[7];

// only runs once on boot
void setup() {
  // Initializing serial port for debugging purposes
  Serial.begin(115200);
  delay(dht.getMinimumSamplingPeriod());
  // Initialize DHT sensor.
  dht.setup(DHTPin, DHTesp::DHT22); 
  
  // Connecting to WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
  // Starting the web server
  server.begin();
  Serial.println("Web server running. Waiting for the ESP IP...");
  delay(10000);
  
  // Printing the ESP IP address
  Serial.println(WiFi.localIP());
}

// runs over and over again
void loop() {
  // Listenning for new clients
  WiFiClient client = server.available();
  
  if (client) {
    Serial.println("New client");
    // bolean to locate when the http request ends
    boolean blank_line = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();\
        
        if (c == '\n' && blank_line) {
            // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
            // read second time
            TempAndHumidity th_struct = dht.getTempAndHumidity();

            // check data and send error when appropriate

            float temp_f = dht.toFahrenheit(th_struct.temperature);

            client.println("HTTP/1.1 200 OK");
            client.println("Content-Type: application/json");
            client.println("Connection: close");
            client.println();
            client.print(", {\"temperatureF\": ");
            client.print(temp_f);
            client.print(", \"humidity\": ");
            client.print(th_struct.humidity);
            client.print("}");

            break;
        }
        if (c == '\n') {
          // when starts reading a new line
          blank_line = true;
        }
        else if (c != '\r') {
          // when finds a character on the current line
          blank_line = false;
        }
      }
    }  
    // closing the client connection
    delay(1);
    client.stop();
    Serial.println("Client disconnected.");
  }
}   
